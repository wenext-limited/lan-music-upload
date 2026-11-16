# 项目约定

- 本仓库维护 Fungo、GameParty 的静态音乐上传页面，入口为 `<项目名>/active/index.html`，图片位于同级 `static/`。
- HTML、CSS、JavaScript 集中在各自页面中，上传服务由对应 App 提供，接口为 `POST /upload`，文件字段为 `file`。
- Fungo 正文图片使用 `/static/...`，GameParty 使用 `./static/...`，调整路径时核对 App 服务方式。
- 打包统一使用 `scripts/package.py`，读取当前 HEAD 的资源并生成可复现 ZIP，保留顶层 `active/`。客户端校验整个 ZIP 的 SHA-256，安装后的网页根为 `package/active`。
- 中文沟通，按用户授权范围做最小改动，复用现有实现，保留用户已有修改。
- README 保持简洁，保留项目说明、使用命令和必要接口约定。实现放独立脚本，具体 SHA 值由打包产物提供。
- 修改后核对路径并执行 `git diff --check`。打包脚本变更需验证重复打包的 SHA 一致、解压结构正确。UI 交由用户验收。
