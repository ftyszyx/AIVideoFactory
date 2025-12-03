# AIVideoFactory
AIVideoFactory


## 项目流程
使用python,自动化生成视频
1.用户输入提示词，让大模型(deepseek)根据提示词生成视频分镜文本和视频介绍（用于生成背景音乐）
2.根据分镜文本，生成对应分镜的图片提示词(deepseek)
3.根据图片提示词，让图片大模型(nano-banana-pro)生成分镜的图片
4.根据视频介绍，让ai通过线上音乐库找到最合适的背景音乐
5.生成剪映草稿(参考https://github.com/GuanYixuan/pyJianYingDraft)

## 开发环境
语言：python
包管理：uv

