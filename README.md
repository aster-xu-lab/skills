# AsterXu Lab Skills

用于 CC Switch 发现、安装和更新的公开 Skill 仓库。

## 当前 Skill

| Skill | 用途 | 必要环境 |
| --- | --- | --- |
| [hexo-blog-post](skills/hexo-blog-post/SKILL.md) | 将项目经验、技术分析与复盘整理成 Hexo 博客文章，支持草稿、构建预览和按授权发布 | 已有 Hexo 博客、站点 `AGENTS.md` 与项目构建环境 |
| [codebase-quality](skills/codebase-quality/SKILL.md) | 全库或模块级的代码质量审查、重复逻辑判断、边界拆分与分步重构 | 目标项目可运行的检查命令；只读审查不需要额外环境 |
| [doc-governance](skills/doc-governance/SKILL.md) | 文档漂移修复、冗余精简与文档索引、权威边界检查 | 已有文档体系的目标项目；无额外运行环境 |
| [commit-history-review](skills/commit-history-review/SKILL.md) | 已提交 Git 历史的窗口、增量与单提交回顾；输出质量评估、启示与延伸动作 | 目标仓库的 Git 历史；只读审查不需要额外环境 |
| [skill-config-maintenance](skills/skill-config-maintenance/SKILL.md) | 审计并安全清理公开分发 Skill 的外置配置；显式调用、默认只读，删除需归档与确认 | 目标机器有 `aster-xu-lab` 配置目录；无额外运行环境 |

Skill 不包含本机路径。博客 Skill 使用时提供实际博客目录，或在已有博客工作区调用；站点定位可保存在本机用户级配置（`~/.config/aster-xu-lab/hexo-blog-post.json`，Windows 为 `%APPDATA%\aster-xu-lab\hexo-blog-post.json`），该配置不随 Skill 分发。文章格式、分类、配图与部署目标由站点约定决定。写作请求不自动授权源码推送、图床上传或公网部署。

审查与文档治理 Skill 默认只读：前者输出带证据的问题清单，后者区分「已确认漂移」与「待确认缺口」。提交历史回顾同样只读，输出审查快照、逐提交发现、启示与延伸动作，不自动修复或提交。配置维护 Skill 也默认只读，删除必须逐文件确认并先归档。四者在用户明确授权后才修改，且保留原验证基线与已有编辑。

## 配置管理

部分 Skill 会在 `${XDG_CONFIG_HOME:-$HOME/.config}/aster-xu-lab/`（Windows 为 `%APPDATA%\aster-xu-lab\`）保存本机配置：

- `hexo-blog-post.json`：Hexo 站点定位。
- `commit-history-review.json`：每个仓库上次审查的 commit 基线。

配置不随 Skill 安装目录更新，也不自动跨设备同步；卸载 Skill 不会删除配置。需要盘点或清理时，显式调用 `skill-config-maintenance`：

- 默认只读，按注册表与安装目录区分已安装、孤立候选、未登记、JSON 损坏、schema 不匹配与软链。
- 删除必须显式指定文件、先归档并确认；已安装 Skill 的配置需要再次确认，软链不自动删除。
- 不清理 CC Switch 数据库、应用缓存或其他目录。

## CC Switch 安装与更新

1. 在 Skill 页面打开仓库管理，添加 `aster-xu-lab/skills`，分支填写 `main`。
2. 在发现页找到需要的 Skill，安装并启用需要的宿主。
3. 后续通过“检查更新”扫描源内容，再执行单项或批量更新。

仓库地址：[https://github.com/aster-xu-lab/skills](https://github.com/aster-xu-lab/skills)。

如果已有同名 Skill 仍关联旧源，通过 CC Switch 重新关联到本仓库并核对来源。添加仓库本身不改变既有安装的更新源。CC Switch 按内容 SHA-256 检测变化；更新会替换安装目录，先处理安装副本中的个人改动。具体入口以使用中的 CC Switch 版本为准，见 [官方 Skill 管理手册](https://github.com/farion1231/cc-switch/blob/main/docs/user-manual/en/3-extensions/3.3-skills.md)。

## 来源与维护

本仓库只发布经过审核的分发产物；`distribution-manifest.json` 记录源文件哈希、公开文件哈希和适配说明。维护时从资产正本单向同步，不在安装副本分别修改。分发历史独立，不包含资产源仓库的历史或本机配置。

- `hexo-blog-post` 由 AsterXu Lab 维护；参考文件保留外部研究方法和视觉工具的来源链接，不包含第三方 Skill 正文。配图和研究能力按任务使用宿主已有工具，安装本 Skill 不自动安装其他工具或配置模型后端。Skill 内含主笔与独立审校的角色简报，需要时可委派通用子 Agent 执行；已安装同名 Agent 时优先使用。
- `codebase-quality` 提炼自个人项目实践，并参考 superpowers、addyosmani 与 mattpocock 的固定版本；只提炼判断方法，不继承其自动委派、文件写入或发布动作。上游均为 MIT 许可。只读审查可委派内置的 auditor 角色简报执行，重构仍需明确授权。
- `doc-governance` 提炼自个人文档治理实践，来源标注已通用化，不包含原项目名称与内部路径。
- `commit-history-review` 提炼自个人提交审查实践，并参考 Matt Pocock、Superpowers、Addy Osmani 与 ECC 的固定版本；只提炼回顾流程与判断方法，不继承自动修复、自动提交或多 Agent 编排。上游均为 MIT 许可。
- `skill-config-maintenance` 提炼自个人分发 Skill 的配置维护实践；只读取本机 `aster-xu-lab` 配置目录与注册表，不包含私有资产库路径或业务配置。

## 许可证

`codebase-quality`、`doc-governance`、`commit-history-review` 与 `skill-config-maintenance` 以 MIT 许可发布。`hexo-blog-post` 尚未指定开放源代码许可证，公开可读不代表授权第三方再分发。

## 验证边界

已完成公开内容适配和结构、引用检查；代码审查、文档治理、提交历史回顾、配置审计与删除流程在真实项目中的效果、宿主自动路由与跨宿主行为尚未验证。配置维护在真实用户配置目录、Windows、dotfiles 软链与 CC Switch 安装副本上尚未验证。
