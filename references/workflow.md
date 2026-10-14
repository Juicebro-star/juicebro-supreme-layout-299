# 分享版执行流程

本包包含排版指令、全部当前主题组件、校验/预览源码、固定文末与双入口原图。所有路径相对本skill目录，不依赖另外安装排版引擎或原作者的Obsidian。

## 输入和输出

已有Markdown/纯文本并明确要求排版时直接处理；Word/PDF按 `../vendor/layout-engine/references/format-normalize.md` 转换。包内Word提取脚本用Python标准库；PDF读取由调用它的AI工具提供。用户只给素材要求写文章时，先写正文和80字摘要，再等排版指令。

优先按用户指定目录输出，未指定用当前工作区 `outputs/YYYYMMDD_短标题/`，保存Markdown、HTML、预览及assets。路径来自当前环境，不写死电脑用户名。

## 文末素材准备

以下命令中的SKILL为本skill实际路径，ARTICLE为本篇输出目录。

```bash
python3 "$SKILL/scripts/package_article.py" prepare "$ARTICLE"
```

Windows可将python3换成python或py -3，并使用实际路径。

复制原图和文末片段到本篇assets，写 `qr-source-urls.json`。将文末片段放在主题正文后，已有署名/CTA合并为一套。`--source`可指定更新后的同结构文末目录；同名内容不同会停止，不静默覆盖。

个人复用者要求自己的署名或二维码时，按其素材装配文末；不需要默认文末时跳过prepare。个人二维码可以使用普通本地文件名，按本地图嵌入；不要继续写果汁哥星球的价格或入口。

## 校验与预览

```bash
python3 "$SKILL/scripts/package_article.py" preview "$ARTICLE/短标题_排版_果汁哥至尊299.html"
```

使用包内引擎，不需第三方Python库；推荐Python3.9及以上。脚本拒绝ERROR和WARNING，生成 `_预览.html`，再补复制图片映射。原图仍留在本篇assets供预览，复制时普通本地图转data URI，默认双二维码转为已提供的微信原图URL。只处理预览，不上传、不登录、不发布。

本地图必须在文章目录内，避免引用其他工作区素材；不支持的文件类型需先正常转换，不把错误写成成功。

## 验收

打开预览页，检查桌面及390px手机版，图片均加载、章节与下划线正确、代码块不空洞、二维码左右对应；实际点击复制按钮，检查 `window.juiceLastCopy.success`。复制载荷不含本地图片路径、按钮或脚本。本地图片已嵌入不保证微信编辑器保留图片，实际粘贴后仍需检查。

二维码使用原图；可用本机解码工具核对payload，历史 `assets/footer/qr_validation.json` 仅是原件的历史验证记录。没有实际验证时明确“本次未解码”或“加入状态未验证”，不虚报。80字摘要实际计数并交付，更新正文后同步修改。

完成交付预览、摘要及校验结论，状态为“待发”。
