# 项目上下文

## 定位与入口

- `lan-music-upload` 汇集不同项目的局域网音乐上传页面，当前包括 Fungo 和 GameParty。
- 技术栈为原生 HTML、CSS、JavaScript，每个页面的样式和逻辑集中在各自的 `index.html`。
- 每个项目独立维护 `<项目名>/active/index.html` 与 `<项目名>/active/static/`。
- 当前仓库内容为页面、图片资源和文档，上传服务由对应应用提供。
- 详细使用方法和接口说明见 `README.md`。优先读取目标项目页面，跨项目修改时再核对其他项目。

| 项目 | 页面入口 | 浏览器标题 |
| --- | --- | --- |
| Fungo | `Fungo/active/index.html` | FungoChat Music Uploader |
| GameParty | `GameParty/active/index.html` | GameParty Music Uploader |

## 现有行为与集成约定

- 支持 `.mp3`、`.aac`、`.m4a`、`.flac`、`.wav`，前端按扩展名过滤，忽略大小写。
- 页面提示单曲最大 10MB，文件大小与音频有效性依赖服务端校验。
- 文件状态为 `pending → uploading → done / error`。每次点击上传会依次处理当次待上传条目。
- 上传中移除条目会调用 `XMLHttpRequest.abort()`。点击成功图标会清除对应页面条目。
- 失败条目需移除后重新选择，才能再次上传。
- 使用 `XMLHttpRequest` 向同源站点根路径 `POST /upload` 提交 `FormData`，文件字段为 `file`，保留原始文件名。
- 响应按 JSON 解析，以 `success` 字段判断结果。失败示例为 `{"success": false, "error": "file_too_large"}`。
- 服务端错误码包括 `unsupported_format`、`file_too_large`、`upload_in_progress`、`no_file`、`duplicate_file`、`invalid_audio`。
- Fungo 正文图片引用 `/static/...`，页面图标引用 `./static/...`。GameParty 图片均引用 `./static/...`。
- 静态资源包括 `common_app_logo.png`、`select.png`、`upload.png`。将目标项目的 `active/` 作为服务根目录即可匹配现有路径。

## 协作与修改范围

- 使用中文，沟通简明，先明确目标、影响范围、方案和验收方式。
- 按用户明确授权的范围执行。复杂需求或重构先确认需求与计划，相关文档默认放在 `docs/`。
- 维护目标项目自身的页面与资源，跨项目同步按用户要求执行。
- 优先复用页面现有实现，保持风格一致，修改聚焦当前需求。
- 接口、目录或资源路径发生变化时，同步维护 `README.md` 和本文件中的相关约定。
- 保留用户已有改动，Git 暂存与提交遵循用户明确授权。

## 预览与验证

在仓库根目录选择目标项目启动静态预览，需安装 Python 3。

```bash
python3 -m http.server 8080 --directory Fungo/active
```

或预览 GameParty

```bash
python3 -m http.server 8080 --directory GameParty/active
```

- 访问 `http://localhost:8080/`，使用 `Ctrl+C` 停止服务后切换项目。
- 当前使用静态文件直接运行，完整上传验收需接入对应应用的 `/upload` 服务。
- 文档修改核对实际文件、路径和交互逻辑，并执行 `git diff --check`。
- 页面修改优先由用户验收 UI，自动化 UI 测试需用户明确要求。
- 上传交互验收覆盖文件选择与移除、进度、成功、失败和取消，具体步骤见 `README.md`。
- 完成时说明修改范围、已验证项和待验证项。
