# 果汁哥至尊排版skill（299版）

这是给能读本地文件、运行Python的AI Agent使用的公众号排版skill。ZIP里已经带齐排版组件、Python脚本、文末原图与许可证，不需要作者的电脑、Obsidian或另装排版引擎。排版由AI根据组件库完成，辅助脚本负责素材准备、校验和可复制预览；单独运行Python并不会自动理解文章或完成排版。

## 下载

[下载完整分享包 ZIP](https://github.com/Juicebro-star/juicebro-supreme-layout-299/releases/latest/download/juicebro-supreme-layout-299.zip)，解压后保留整个文件夹。

已使用 Git 的 Codex 用户也可以安装到个人技能目录（先确认没有同名旧版）：

```bash
git clone https://github.com/Juicebro-star/juicebro-supreme-layout-299.git ~/.agents/skills/juicebro-supreme-layout-299
```

## 最快开始

1. 解压ZIP，保留整个 `juicebro-supreme-layout-299` 文件夹，别只取SKILL.md。
2. 把文件夹交给你的AI Agent，并说：“阅读这个文件夹的SKILL.md和README，按你的技能安装规则安装；先检查同名skill，不要覆盖我的旧版本。”
3. 给它文章，发：“用果汁哥至尊排版skill（299版）排这篇文章，输出HTML、可复制预览和80字摘要。”

也可以不安装，直接指定解压后SKILL.md的实际路径，让支持文件与命令的AI按它执行。具体Agent的技能导入方式可能不同，包内没有对Claude Code、Cursor等客户端逐一实测。

## Codex本地安装

按官方文档，个人skill可放在 `~/.agents/skills/`，项目skill可放在项目的 `.agents/skills/`。最终目录应是 `~/.agents/skills/juicebro-supreme-layout-299/SKILL.md`，不要多套一层目录。检查同名目录后再移动，保留所有scripts、references、assets、vendor和agents。

重新打开/刷新技能列表后，直接说上面的调用语，或者显式使用 `$juicebro-supreme-layout-299`。没有自动发现时，指定SKILL.md完整路径执行。官方路径说明：https://learn.chatgpt.com/docs/build-skills#where-codex-loads-local-skills

## 换成你的文末

本包默认保留果汁哥署名、星球与免费交流群二维码；星球说明仍为年费199。299版是skill名称。

想用自己的账号，给AI你的署名和两张二维码并说：“保留这套排版，文末换成我的署名和二维码，删除果汁哥星球价格和入口。”不想要文末则说：“只要排版，不加果汁哥文末。”无需自己修改Python源码。

## 环境和边界

辅助脚本推荐Python3.9及以上，只用标准库，无API密钥或联网上传要求。浏览器建议Chrome；脚本可跨目录移动，Windows可用python或py -3执行。

正文图片复制时嵌入，默认二维码使用微信原图URL；真实公众号粘贴后检查图片与样式。skill不自动登录、发布或群发。二维码是否可加入由对应入口当前状态决定。

简单示例文章见 `examples/试排文章.md`。完整执行说明见references/workflow.md。软件来源与AGPL许可见THIRD_PARTY_NOTICES.md和LICENSE。
