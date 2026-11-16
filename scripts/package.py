#!/usr/bin/env python3
"""从当前 HEAD 生成元数据固定的音乐上传页面 ZIP。"""

import argparse
import hashlib
import io
import re
import subprocess
import sys
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


def git(*arguments):
    return subprocess.check_output(["git", *arguments], cwd=ROOT)


def resource_entries(project, commit):
    prefix = (project + "/").encode("utf-8")
    records = git("ls-tree", "-r", "-z", "--full-tree", commit, "--", project + "/active/")
    entries = []
    for record in filter(None, records.split(b"\0")):
        metadata, path = record.split(b"\t", 1)
        mode, kind, object_id = metadata.split()
        name = path[len(prefix):].decode("utf-8")
        if any(part.startswith(".") or part == "__MACOSX" for part in name.split("/")):
            continue
        if kind != b"blob" or mode not in (b"100644", b"100755"):
            raise ValueError("资源应为普通文件 " + name)
        entries.append((name, object_id.decode("ascii")))
    if "active/index.html" not in dict(entries):
        raise ValueError("当前 HEAD 缺少 " + project + "/active/index.html")
    return sorted(entries, key=lambda entry: entry[0].encode("utf-8"))


def build_archive(entries):
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", compression=zipfile.ZIP_STORED, allowZip64=False) as archive:
        for name, object_id in entries:
            # 固定 ZIP 元数据，存储模式消除压缩库版本对产物字节的影响。
            info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_STORED
            info.create_system = 3
            info.create_version = 20
            info.extract_version = 20
            info.flag_bits = 0
            info.volume = 0
            info.internal_attr = 0
            info.external_attr = 0o100644 << 16
            info.extra = b""
            info.comment = b""
            archive.writestr(info, git("cat-file", "blob", object_id))
    data = buffer.getvalue()
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        if archive.testzip() is not None:
            raise ValueError("ZIP 完整性校验失败")
    return data


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    projects = sorted(path.name for path in ROOT.iterdir() if (path / "active").is_dir())
    parser.add_argument("project", choices=projects, help="目标项目")
    arguments = parser.parse_args()
    commit = git("rev-parse", "--verify", "HEAD^{commit}").decode().strip()
    data = build_archive(resource_entries(arguments.project, commit))
    output = ROOT / "dist" / arguments.project / "lan-upload-assets.zip"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(data)
    digest = hashlib.sha256(data).hexdigest()
    checksum = digest + "  " + output.name + "\n"
    checksum_path = output.with_name(digest + ".sha256")
    checksum_path.write_bytes(checksum.encode("ascii"))
    for previous in output.parent.glob("*.sha256"):
        if previous != checksum_path and (
            previous.name == output.name + ".sha256"
            or re.fullmatch(r"[0-9a-f]{64}", previous.stem)
        ):
            previous.unlink()
    print("commit=" + commit)
    print("zip=" + str(output))
    print("sha256=" + digest)


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, subprocess.CalledProcessError, zipfile.BadZipFile, zipfile.LargeZipFile) as error:
        print("打包失败 " + str(error), file=sys.stderr)
        sys.exit(1)
