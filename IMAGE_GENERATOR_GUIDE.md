# 阿里通义万相图片生成 - 使用指南

## 概述

本模块实现了**基于阿里通义万相API的图片生成功能**，可以为Markdown文章自动生成封面图和配图。

---

## 🎯 核心功能

### 1. 文章封面生成
根据文章标题和内容自动生成封面图

### 2. 段落配图生成
为每个主要章节自动生成配图

### 3. 自定义图片生成
根据自定义描述生成图片

### 4. 图片风格选择
支持多种风格：摄影、插画、3D

### 5. 缓存机制
自动缓存生成的图片，避免重复调用API

---

## 🚀 快速开始

### 步骤1：获取阿里云API Key

1. 访问 [阿里云灵积平台](https://dashscope.aliyun.com/)
2. 注册/登录账号
3. 进入 API-KEY管理
4. 创建新的API Key
5. 复制API Key

### 步骤2：配置环境变量

```bash
# 设置API Key
export DASHSCOPE_API_KEY=sk-your-api-key-here

# 或者添加到 ~/.bashrc
echo 'export DASHSCOPE_API_KEY=sk-your-api-key-here' >> ~/.bashrc
source ~/.bashrc
```

### 步骤3：安装依赖

```bash
pip install requests
```

---

## 📖 使用示例

### 示例1：生成文章封面

```python
from formatter.image_generator import generate_article_cover

title = "2026年AI工具趋势"
content = """随着AI技术的快速发展，内容创作工具正在经历前所未有的变革。"""

result = generate_article_cover(title, content, style="photography")

if result["success"]:
    print(f"✅ 封面图：{result['images'][0]}")
else:
    print(f"❌ 失败：{result['error']}")
```

### 示例2：自定义图片生成

```python
from formatter.image_generator import generate_custom_image

result = generate_custom_image(
    prompt="Professional workspace with laptop and coffee",
    style="photography"
)

if result["success"]:
    print(f"✅ 图片：{result['images'][0]}")
```

### 示例3：增强Markdown（自动插入图片）

```python
from formatter.image_enhancer import enhance_with_images

markdown = """# 2026年AI工具趋势

## 核心趋势

### AI写作助手
AI写作助手已经成为标配工具。

### 多平台适配
一键发布是核心需求。"""

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

### 示例4：完整工作流（生成图片 + 格式化 + 分发）

```python
from formatter.image_enhancer import enhance_with_images
from formatter.platform_adapter import adapt_to_platforms

# 原始Markdown
markdown = """# HumanWriter产品介绍

## 核心功能

### AI检测器
100维度检测，准确率95%+。

### 多平台适配
支持5个平台。"""

# 步骤1：生成图片
enhanced = enhance_with_images(markdown, style="photography")

if enhanced["success"]:
    print(f"✅ 生成 {enhanced['count']} 张图片")

    # 步骤2：格式化
    adapted = adapt_to_platforms(enhanced["markdown"])

    # 步骤3：输出
    print("公众号HTML:", adapted["wechat"][:200])
    print("知乎Markdown:", adapted["zhihu"][:200])
    print("小红书:", adapted["xiaohongshu"][:200])
```

---

## 🎨 图片风格

支持的风格：

| 风格 | 描述 | 适用场景 |
|------|------|---------|
| `photography` | 摄影风格，真实感强 | 科技、商业、生活类文章 |
| `illustration` | 插画风格，扁平化设计 | 教程、指南、轻松内容 |
| `3d` | 3D渲染，立体感强 | 产品、技术、设计类文章 |

**使用方法**：
```python
result = generate_article_cover(title, content, style="illustration")
```

---

## 📊 API参考

### generate_article_cover()

为文章生成封面图。

**参数**：
- `title` (str): 文章标题
- `content` (str): 文章内容
- `style` (str): 图片风格（默认：`photography`）
- `api_key` (str, optional): API Key（默认从环境变量读取）
- `use_cache` (bool): 是否使用缓存（默认：`True`）

**返回**：
```python
{
    "success": True,
    "images": ["https://..."],
    "prompt": "...",
    "style": "photography"
}
```

### generate_custom_image()

自定义生成图片。

**参数**：
- `prompt` (str): 图片描述
- `style` (str): 图片风格（默认：`photography`）
- `api_key` (str, optional): API Key
- `use_cache` (bool): 是否使用缓存（默认：`True`）

**返回**：
```python
{
    "success": True,
    "images": ["https://..."],
    "prompt": "...",
    "style": "photography"
}
```

### enhance_with_images()

为Markdown自动添加图片。

**参数**：
- `markdown_content` (str): Markdown内容
- `style` (str): 图片风格（默认：`photography`）
- `api_key` (str, optional): API Key
- `insert_cover` (bool): 是否插入封面图（默认：`True`）
- `insert_section_images` (bool): 是否插入段落配图（默认：`True`）
- `max_images` (int): 最大图片数量（默认：`3`）

**返回**：
```python
{
    "success": True,
    "markdown": "# 标题\n\n![封面](https://...)",
    "images": [
        {
            "position": "cover",
            "url": "https://...",
            "prompt": "..."
        },
        {
            "position": "section_0",
            "url": "https://...",
            "title": "章节标题",
            "prompt": "..."
        }
    ],
    "count": 2
}
```

---

## 🔧 配置说明

### 环境变量

| 变量名 | 说明 | 示例 |
|--------|------|------|
| `DASHSCOPE_API_KEY` | 阿里云API Key | `sk-xxxxxxxxxxxxxxxx` |

### 缓存目录

生成的图片信息会自动缓存到 `cache/images/` 目录。

缓存文件命名：`{cache_key}.json`

---

## 🧪 测试

运行测试脚本：

```bash
# 设置API Key
export DASHSCOPE_API_KEY=sk-your-api-key

# 运行测试
python test_image_generator.py
```

**测试内容**：
1. 自定义图片生成
2. 文章封面生成
3. Markdown增强（添加图片）
4. 不同风格测试
5. 与格式化器的集成

---

## 💡 最佳实践

### 1. 提示词优化

系统会自动从标题和内容中提取关键词，生成合适的提示词。

**示例**：
- 标题："2026年AI工具趋势"
- 提取关键词："AI", "工具", "趋势"
- 生成的Prompt："Professional photography, 2026年AI工具趋势, AI, 工具, 趋势, high quality, 8K, detailed"

### 2. 风格选择

根据文章类型选择合适的风格：

| 文章类型 | 推荐风格 |
|---------|---------|
| 科技新闻 | `photography` |
| 产品介绍 | `3d` |
| 教程指南 | `illustration` |
| 生活随笔 | `photography` |

### 3. 图片数量控制

根据文章长度设置合适的图片数量：

| 文章字数 | 推荐图片数 |
|---------|-----------|
| < 500字 | 1张（仅封面） |
| 500-1000字 | 2-3张 |
| > 1000字 | 3-5张 |

```python
result = enhance_with_images(
    markdown_content=markdown,
    max_images=3  # 最多3张
)
```

### 4. 缓存使用

默认开启缓存，避免重复调用API。

**手动清除缓存**：
```bash
rm -rf cache/images/*
```

---

## ⚠️ 常见问题

### Q1：API Key如何获取？

A：访问 [阿里云灵积平台](https://dashscope.aliyun.com/)，注册/登录后创建API Key。

### Q2：图片生成失败？

A：检查以下项目：
- API Key是否正确
- 账户余额是否充足
- 网络连接是否正常

### Q3：如何自定义提示词？

A：使用 `generate_custom_image()` 函数，传入自定义prompt。

### Q4：图片生成速度？

A：通常5-15秒生成一张图片。

### Q5：API调用费用？

A：参考 [阿里云价格页](https://help.aliyun.com/zh/dashscope/developer-reference/wanx-image-generation-price)

---

## 📈 性能优化

### 1. 使用缓存

默认开启，避免重复调用API。

### 2. 并发生成

可以同时生成多张图片：

```python
import concurrent.futures

titles = ["文章1", "文章2", "文章3"]

with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
    futures = [
        executor.submit(generate_article_cover, title, content)
        for title in titles
    ]

    for future in concurrent.futures.as_completed(futures):
        result = future.result()
        print(result)
```

### 3. 批量处理

处理多篇文章：

```python
import os
from formatter.image_enhancer import enhance_with_images

article_dir = "articles/"
results = []

for filename in os.listdir(article_dir):
    if filename.endswith('.md'):
        with open(os.path.join(article_dir, filename), 'r') as f:
            markdown = f.read()

        result = enhance_with_images(markdown, style="photography")
        results.append({
            "file": filename,
            "result": result
        })
```

---

## 🚀 集成到n8n

### 步骤1：配置环境变量

在n8n中配置 `DASHSCOPE_API_KEY` 环境变量。

### 步骤2：创建工作流

在现有工作流中添加"生成图片"节点：

```json
{
  "parameters": {
    "command": "cd /home/admin/.openclaw/workspace/humanwriter && python -c \"\nfrom formatter.image_enhancer import enhance_with_images\nimport json\n\nmarkdown = '''{{ $json.markdown }}'''\nresult = enhance_with_images(markdown, style='photography')\nprint(json.dumps(result, ensure_ascii=False))\n\""
  },
  "type": "n8n-nodes-base.executeCommand"
}
```

### 步骤3：连接节点

```
输入 → 生成图片 → 格式化 → 发布
```

---

## 📚 相关文档

- [阿里云灵积文档](https://help.aliyun.com/zh/dashscope/)
- [通义万相API文档](https://help.aliyun.com/zh/dashscope/developer-reference/wanx-api-overview)
- [HumanWriter使用文档](./FORMATTER_README.md)

---

## 🎉 总结

本模块提供了完整的图片生成解决方案：

- ✅ 文章封面自动生成
- ✅ 段落配图自动插入
- ✅ 多种风格选择
- ✅ 智能缓存机制
- ✅ 与格式化器无缝集成

只需设置API Key，即可为所有文章自动生成高质量配图！

---

## 水印说明

**默认设置**：生成的图片**不包含水印**

- 代码中已设置 `watermark: False`
- 所有生成的图片都是无水印版本
- 可以直接用于公众号、知乎等平台

**如需添加水印**：
- 修改 `formatter/image_generator.py` 中的 `watermark` 参数为 `True`
- 或在自定义 API 调用时添加水印参数

---

*最后更新：2026-02-26*
