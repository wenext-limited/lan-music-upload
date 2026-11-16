# lan-music-upload

各项目的局域网音乐上传页面，使用原生 HTML、CSS 和 JavaScript 实现。

## 目录

```text
Fungo/active/         # Fungo 页面及 static 图片资源
GameParty/active/     # GameParty 页面及 static 图片资源
scripts/package.py   # 可复现 ZIP 打包脚本
```

## 预览

直接用浏览器打开对应项目的 `active/index.html` 即可预览。

Fungo 正文图片使用 `/static/...`，可在仓库根目录启动 HTTP 服务预览，访问 `http://localhost:8080/`。

```bash
python3 -m http.server 8080 --directory Fungo/active
```

实际上传需要对应 App 提供 `/upload` 接口。

## 打包

需要 Git 和 Python 3.9+。在仓库根目录执行对应项目的命令。

```bash
python3 scripts/package.py GameParty
python3 scripts/package.py Fungo
```

打包当前 `HEAD` 已提交的内容。

产物位于 `dist/<项目名>/`，包括 `YYYYMMDDHHmmss_assets.zip` 和 `<SHA256>.sha256` 校验文件。文件名前缀使用新加坡时间（UTC+8），精确到秒。ZIP 内保留顶层 `active/`。

每次打包会清空对应的 `dist/<项目名>/`，只保留本次 ZIP 和校验文件。

脚本统一文件顺序、时间、权限和存储方式，同一项目、同一 Git 文件内容可生成相同 ZIP 和 SHA-256。发布新包时，同步更新客户端资源地址与 SHA-256 校验值。

## 上传接口

页面向同源 `POST /upload` 提交 `multipart/form-data`，文件字段为 `file`。支持 MP3、AAC、M4A、FLAC、WAV，页面提示单曲最大 10MB，大小及音频有效性由服务端校验。

接口返回 JSON，成功为 `{"success": true}`，失败为 `{"success": false, "error": "错误码"}`。

### 错误码

| 错误码 | 来源 | 含义 |
| --- | --- | --- |
| `unsupported_format` | 服务端 | 文件格式不支持 |
| `file_too_large` | 服务端 | 单曲超过 10MB |
| `upload_in_progress` | 服务端 | 已有上传任务进行中 |
| `no_file` | 服务端 | 请求缺少文件 |
| `duplicate_file` | 服务端 | 音乐已存在 |
| `invalid_audio` | 服务端 | 音频损坏或无法识别 |
| `network_error` | 页面 | 网络连接失败 |
| `parse_error` | 页面 | 响应 JSON 解析失败 |
| `upload_failed` | 页面 | 上传失败，服务端未提供错误码 |
| `aborted` | 页面 | 用户取消上传 |
