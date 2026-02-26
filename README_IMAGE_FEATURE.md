# HumanWriter - 图片生成功能

## ✨ 新功能：阿里通义万相图片生成

### 📖 概述

HumanWriter现已集成阿里通义万相API，可以为Markdown文章自动生成封面图和配图。

---

## 🚀 快速开始

### 1. 获取API Key

访问 [阿里云灵积平台](https://dashscope.aliyun.com/) 获取API Key。

### 2. 配置环境变量

```bash
export DASHSCOPE_API_KEY=sk-your-api-key
```

### 3. 使用

```python
from formatter import enhance_with_images, adapt_to_platforms

markdown = """# 文章标题
这是内容..."""

# 生成图片
enhanced = enhance_with_images(markdown, style="photography")

# 格式化
adapted = adapt_to_platforms(enhanced["markdown"])

# 输出
print("公众号:", adapted["wechat"])
```

---

## 🎨 支持的风格

| 风格 | 描述 | 适用场景 |
|------|------|---------|
| `photography` | 摄影风格 | 科技、商业、生活类文章 |
| `illustration` | 插画风格 | 教程、指南、轻松内容 |
| `3d` | 3D渲染 | 产品、技术、设计类文章 |

---

## 📦 核心功能

### 1. 文章封面生成

```python
from formatter import generate_article_cover

result = generate_article_cover(
    title="2026年AI工具趋势",
    content="随着AI技术的快速发展...",
    style="photography"
)

if result["success"]:
    print(f"✅ 封面图：{result['images'][0]}")
```

### 2. Markdown增强

```python
from formatter import enhance_with_images

result = enhance_with_images(
    markdown_content=markdown,
    style="photography",
    insert_cover=True,
    insert_section_images=True,
    max_images=3
)

if result["success"]:
    print(f"✅ 生成 {result['count']} 张图片")
    print(result["markdown"])
```

### 3. 完整工作流

```python
from formatter import enhance_with_images, adapt_to_platforms

# 输入
markdown = open("article.md").read()

# 生成图片 + 格式化
enhanced = enhance_with_images(markdown, style="photography")
adapted = adapt_to_platforms(enhanced["markdown"])

# 输出各平台格式
print("公众号:", adapted["wechat"])
print("知乎:", adapted["zhihu"])
print("小红书:", adapted["xiaohongshu"])
```

---

## 🧪 测试

运行演示脚本：

```bash
# 完整演示
python demo_complete.py

# 图片生成测试
python test_image_generator.py
```

---

## 📚 文档

- **使用指南**：`IMAGE_GENERATOR_GUIDE.md`
- **完成报告**：`IMAGE_GENERATOR_REPORT.md`
- **格式化器文档**：`FORMATTER_README.md`

---

## 💡 最佳实践

### 1. 风格选择

根据文章类型选择合适的风格：

| 文章类型 | 推荐风格 |
|---------|---------|
| 科技新闻 | `photography` |
| 产品介绍 | `3d` |
| 教程指南 | `illustration` |

### 2. 图片数量控制

| 文章字数 | 推荐图片数 |
|---------|-----------|
| < 500字 | 1张（仅封面） |
| 500-1000字 | 2-3张 |
| > 1000字 | 3-5张 |

### 3. 缓存使用

默认开启缓存，避免重复调用API。

**清除缓存**：
```bash
rm -rf cache/images/*
```

---

## ⚠️ 注意事项

1. **API Key安全**：不要将API Key提交到Git仓库
2. **成本控制**：缓存命中率越高，成本越低
3. **图片质量**：生成图片质量较高，但可能需要多次尝试
4. **响应时间**：通常5-15秒生成一张图片

---

## 📊 性能指标

- **API响应时间**：5-15秒/张
- **缓存读取时间**：<10ms
- **图片尺寸**：1024x1024（默认）
- **支持风格**：3种

---

## 🎉 示例

### 完整工作流演示

```bash
# 配置API Key
export DASHSCOPE_API_KEY=sk-your-api-key

# 运行演示
python demo_complete.py
```

### 输出示例

```
============================================================
HumanWriter 完整工作流演示
============================================================

🎨 步骤2：生成图片
------------------------------------------------------------
✅ 成功生成 2 张图片
  [1] cover: https://...
  [2] section_0: https://...

📊 步骤3：格式化和平台适配
------------------------------------------------------------
✅ 适配成功！
  - 标题: 2026年AI工具趋势
  - 字数: 262
  - 段落数: 11
  - 图片数: 2

📌 公众号（HTML）
------------------------------------------------------------
<section style="max-width: 677px...">
  <h1>2026年AI工具趋势</h1>
  <img src="https://..." alt="封面" />
  ...
```

---

## 🚀 立即开始

```bash
# 1. 配置API Key
export DASHSCOPE_API_KEY=sk-your-api-key

# 2. 运行演示
python demo_complete.py

# 3. 开始使用
from formatter import generate_article_cover, enhance_with_images, adapt_to_platforms
```

---

## 📞 支持

如有问题，请参考：

- [阿里云灵积文档](https://help.aliyun.com/zh/dashscope/)
- [通义万相API文档](https://help.aliyun.com/zh/dashscope/developer-reference/wanx-api-overview)

---

*功能完成时间：2026-02-26*
*代码量：~3500行*

## 水印说明

**默认设置**：生成的图片**不包含水印**

- 代码中已设置 `watermark: False`
- 所有生成的图片都是无水印版本
- 可以直接用于公众号、知乎等平台

**重要提示**：如需添加水印，请手动修改 `formatter/image_generator.py` 中的配置。
