# AsterXu Lab Skills

用于 CC Switch 发现、安装和更新的公开 Skill 仓库。

## 当前 Skill

| Skill | 用途 | 必要环境 |
| --- | --- | --- |
| [hexo-blog-post](skills/hexo-blog-post/SKILL.md) | 将项目经验、技术分析与复盘整理成 AsterXu Lab 博客文章，支持草稿、构建预览和按授权发布 | 已有 Hexo 博客、站点 `AGENTS.md` 与项目构建环境 |

Skill 不包含本机博客路径。使用时提供实际博客目录，或在已有博客工作区调用；文章格式、分类、配图与部署目标由站点约定决定。写作请求不自动授权源码推送、图床上传或公网部署。

## CC Switch 安装与更新

1. 在 Skill 页面打开仓库管理，添加 `aster-xu-lab/skills`，分支填写 `main`。
2. 在发现页找到 `hexo-blog-post`，安装并启用需要的宿主。
3. 后续通过“检查更新”扫描源内容，再执行单项或批量更新。

仓库地址：[https://github.com/aster-xu-lab/skills](https://github.com/aster-xu-lab/skills)。

如果已有同名 Skill 仍关联旧源，通过 CC Switch 重新关联到本仓库并核对来源。添加仓库本身不改变既有安装的更新源。CC Switch 按内容 SHA-256 检测变化；更新会替换安装目录，先处理安装副本中的个人改动。具体入口以使用中的 CC Switch 版本为准，见 [官方 Skill 管理手册](https://github.com/farion1231/cc-switch/blob/main/docs/user-manual/en/3-extensions/3.3-skills.md)。

## 来源与维护

本仓库只发布经过审核的分发产物；`distribution-manifest.json` 记录源文件哈希、公开文件哈希和适配说明。维护时从资产正本单向同步，不在安装副本分别修改。分发历史独立，不包含资产源仓库的历史或本机配置。

`hexo-blog-post` 由 AsterXu Lab 维护；参考文件保留外部研究方法和视觉工具的来源链接，不包含第三方 Skill 正文。配图和研究能力按任务使用宿主已有工具，安装本 Skill 不自动安装其他工具或配置模型后端。

当前已完成公开内容适配和结构、引用检查；实际文章构建、部署与宿主自动路由尚未验证。仓库尚未指定开放源代码许可证。
