# lan-music-upload

各项目的局域网音乐上传页面集合。每个项目独立维护页面和静态资源，供对应应用的上传服务集成使用。

页面使用原生 HTML、CSS 和 JavaScript 实现，样式与交互均包含在 `index.html` 中，可直接作为静态资源部署。

## 项目目录

```text
lan-music-upload/
├── Fungo/
│   └── active/
│       ├── index.html                 # FungoChat 上传页面
│       └── static/
│           ├── common_app_logo.png    # 项目 Logo
│           ├── select.png             # 选择文件图标
│           └── upload.png             # 上传图标
├── GameParty/
│   └── active/
│       ├── index.html                 # GameParty 上传页面
│       └── static/                    # 同上，各项目独立维护
├── AGENTS.md                         # Agent 项目上下文与维护约定
└── README.md
```

| 项目 | 页面入口 | 静态资源 |
| --- | --- | --- |
| Fungo | `Fungo/active/index.html` | `Fungo/active/static/` |
| GameParty | `GameParty/active/index.html` | `GameParty/active/static/` |

## 页面功能

- 多选音乐文件，支持 MP3、AAC、M4A、FLAC、WAV 扩展名，忽略大小写。
- 展示文件名、大小、单文件上传进度及成功、失败状态。
- 每次点击上传后，按顺序逐个提交本次待上传文件。
- 支持移除待上传文件、取消正在上传的请求，以及清除已成功条目的页面记录。
- 展示格式、大小、重复文件、音频无效及网络异常等错误提示。

页面提示单曲最大 10MB，实际大小和音频有效性校验由上传服务负责。上传失败后，可移除失败条目并重新选择文件上传。

## 本地预览

无需安装前端依赖或执行构建。安装 Python 3 后，在仓库根目录按需选择一个项目启动静态服务。

预览 Fungo 页面

```bash
python3 -m http.server 8080 --directory Fungo/active
```

预览 GameParty 页面

```bash
python3 -m http.server 8080 --directory GameParty/active
```

启动后，在浏览器打开 `http://localhost:8080/`。使用 `Ctrl+C` 停止服务，再切换项目。

静态服务用于预览页面和文件选择交互。完整上传依赖对应应用提供的 `/upload` 服务，本仓库仅包含页面及静态资源。

## 集成与上传接口

将目标项目的 `active/` 目录作为 Web 服务根目录，保留 `index.html` 和 `static/` 的相对位置，并在同一服务下提供 `POST /upload`。

Fungo 页面正文图片使用 `/static/...` 绝对路径，GameParty 页面图片使用 `./static/...` 相对路径。两个页面均向站点根路径 `/upload` 发起请求，部署时需确保这些路径能够正确访问。

### 请求

| 项目 | 约定 |
| --- | --- |
| 方法与路径 | `POST /upload` |
| 请求体 | `multipart/form-data`，由浏览器通过 `FormData` 生成 |
| 文件字段 | `file`，每次请求提交一个文件，并携带原始文件名 |

### 响应

页面解析 JSON 响应，并根据 `success` 字段判断上传结果。

上传成功

```json
{"success": true}
```

上传失败

```json
{"success": false, "error": "file_too_large"}
```

页面已适配的服务端错误码

| 错误码 | 含义 |
| --- | --- |
| `unsupported_format` | 文件格式不支持 |
| `file_too_large` | 文件超过单曲 10MB 限制 |
| `upload_in_progress` | 服务端已有上传任务进行中 |
| `no_file` | 请求中缺少文件 |
| `duplicate_file` | 音乐已存在 |
| `invalid_audio` | 音频损坏或无法识别 |

网络异常时展示连接失败提示，未知错误码或 JSON 解析失败时展示通用失败提示。

## 维护与新增项目

1. 在项目对应的 `active/index.html` 中调整页面内容、样式和交互，在 `active/static/` 中维护图片资源。
2. 新增项目时，可参考已有目录创建 `<项目名>/active/index.html` 和 `<项目名>/active/static/`，更新页面标题、Logo 和资源路径。
3. 上传服务需与页面的请求字段、JSON 响应和错误码保持一致。
4. 更新本 README 的项目目录与入口表，便于定位各项目页面。

### 手动验收

- 确认页面标题、Logo、按钮图标和文件列表显示正常。
- 选择多个支持格式的文件，检查文件名、大小和移除操作。
- 接入对应上传服务后，检查上传进度、成功状态、取消操作和失败提示。
- 检查超大文件、重复文件及无效音频的服务端校验结果是否正确展示。
