# 本地图片缓存功能 - 使用指南

## 概述

本地图片缓存功能可以将生成的图片下载到本地存储，避免重复下载，提升访问速度并降低API调用成本。

---

## 🎯 核心功能

### 1. 自动下载
- 自动下载生成的图片到本地
- 支持单个下载和批量下载
- 自动识别图片格式（JPG/PNG/WEBP）

### 2. 智能缓存
- 基于URL的MD5哈希生成缓存key
- 避免重复下载相同图片
- 支持强制重新下载

### 3. 索引管理
- 维护图片索引文件（index.json）
- 记录下载时间、文件大小、原始URL
- 支持快速查询本地路径

### 4. 缓存统计
- 统计总文件数
- 统计总大小（MB）
- 按文件类型分类统计

---

## 🚀 快速开始

### 方式1：使用快捷函数

```python
from formatter import download_image, download_images

# 单个下载
result = download_image("https://example.com/image.jpg")

if result["success"]:
    print(f"✅ 下载成功: {result['local_path']}")
    print(f"大小: {result['size']} bytes")
    print(f"来自缓存: {'是' if result['cached'] else '否'}")

# 批量下载
urls = [
    "https://example.com/image1.jpg",
    "https://example.com/image2.jpg"
]

result = download_images(urls)

print(f"✅ 成功: {result['success']}")
print(f"❌ 失败: {result['failed']}")
```

### 方式2：使用缓存管理器

```python
from formatter import ImageCacheManager

# 初始化
manager = ImageCacheManager("cache/images/downloads")

# 下载图片
result = manager.download_image("https://example.com/image.jpg")

if result["success"]:
    print(f"✅ 下载成功: {result['local_path']}")

# 获取本地路径
local_path = manager.get_local_path("https://example.com/image.jpg")
print(f"本地路径: {local_path}")

# 获取缓存统计
stats = manager.get_cache_stats()
print(f"缓存统计: {stats}")

# 清空缓存
manager.clear_cache()
```

### 方式3：与图片生成集成

```python
from formatter import enhance_with_images, ImageCacheManager

# 生成图片
enhanced = enhance_with_images(markdown, style="photography")

if enhanced["success"]:
    # 初始化缓存管理器
    cache_manager = ImageCacheManager()

    # 下载所有生成的图片
    for img_info in enhanced["images"]:
        result = cache_manager.download_image(img_info["url"])

        if result["success"]:
            print(f"✅ 已下载: {result['local_path']}")

            # 更新图片信息为本地路径
            img_info["local_path"] = result["local_path"]
```

---

## 📊 API参考

### ImageCacheManager

#### `__init__(cache_dir: str = "cache/images/downloads")`

初始化缓存管理器。

**参数**：
- `cache_dir`: 缓存目录路径

#### `download_image(url: str, filename: Optional[str] = None, force_redownload: bool = False)`

下载单个图片。

**参数**：
- `url`: 图片URL
- `filename`: 文件名（可选）
- `force_redownload`: 是否强制重新下载

**返回**：
```python
{
    "success": True,
    "local_path": "cache/images/downloads/abc123.jpg",
    "url": "https://example.com/image.jpg",
    "size": 102400,
    "cached": False
}
```

#### `download_images(urls: list, force_redownload: bool = False)`

批量下载图片。

**参数**：
- `urls`: 图片URL列表
- `force_redownload`: 是否强制重新下载

**返回**：
```python
{
    "success": 3,
    "failed": 0,
    "results": [...]
}
```

#### `get_local_path(url: str)`

获取图片的本地路径。

**参数**：
- `url`: 图片URL

**返回**：本地路径字符串（如果已缓存），否则返回None

#### `clear_cache()`

清空所有缓存图片。

#### `get_cache_stats()`

获取缓存统计信息。

**返回**：
```python
{
    "total_files": 10,
    "total_size": 5120000,
    "total_size_mb": 4.88,
    "file_types": {".jpg": 8, ".png": 2},
    "cache_dir": "cache/images/downloads"
}
```

### 快捷函数

#### `download_image(url: str, cache_dir: str = "cache/images/downloads")`

下载单个图片的快捷函数。

#### `download_images(urls: list, cache_dir: str = "cache/images/downloads")`

批量下载图片的快捷函数。

---

## 💡 使用场景

### 场景1：批量处理文章

```python
from formatter import enhance_with_images, ImageCacheManager
import os

cache_manager = ImageCacheManager()
article_dir = "articles/"

for filename in os.listdir(article_dir):
    if filename.endswith('.md'):
        # 生成图片
        with open(os.path.join(article_dir, filename), 'r') as f:
            markdown = f.read()

        enhanced = enhance_with_images(markdown, style="photography")

        # 下载图片
        if enhanced["success"]:
            for img_info in enhanced["images"]:
                result = cache_manager.download_image(img_info["url"])
                if result["success"]:
                    print(f"✅ {filename}: {result['local_path']}")
```

### 场景2：替换Markdown中的URL为本地路径

```python
from formatter import enhance_with_images, ImageCacheManager
import re

cache_manager = ImageCacheManager()

# 生成图片
enhanced = enhance_with_images(markdown, style="photography")

# 下载图片并替换URL
if enhanced["success"]:
    updated_markdown = enhanced["markdown"]

    for img_info in enhanced["images"]:
        # 下载图片
        result = cache_manager.download_image(img_info["url"])

        if result["success"]:
            # 替换Markdown中的URL为本地路径
            local_path = result['local_path']
            url = img_info['url']

            # 转换为相对路径
            rel_path = os.path.relpath(local_path)

            # 替换
            updated_markdown = updated_markdown.replace(url, rel_path)

    print(updated_markdown)
```

### 场景3：定期清理缓存

```python
from formatter import ImageCacheManager

cache_manager = ImageCacheManager()

# 获取缓存统计
stats = cache_manager.get_cache_stats()

# 如果缓存超过100MB，清空
if stats["total_size_mb"] > 100:
    print(f"缓存过大 ({stats['total_size_mb']} MB)，正在清理...")
    cache_manager.clear_cache()
    print("✅ 缓存已清空")
```

---

## 🔧 配置说明

### 缓存目录

默认缓存目录：`cache/images/downloads/`

**修改缓存目录**：
```python
from formatter import ImageCacheManager

manager = ImageCacheManager("custom/cache/path")
```

### 索引文件

索引文件：`cache/images/downloads/index.json`

**索引结构**：
```json
{
  "abc123def456": {
    "filename": "abc123def456.jpg",
    "url": "https://example.com/image.jpg",
    "size": 102400,
    "downloaded_at": 1708905600
  }
}
```

---

## ⚠️ 注意事项

1. **网络连接**：确保能够访问图片URL
2. **存储空间**：监控缓存大小，及时清理
3. **文件权限**：确保有写入缓存目录的权限
4. **URL有效性**：检查URL是否可访问
5. **并发下载**：大量图片下载可能触发限制

---

## 🧪 测试

运行测试脚本：

```bash
python test_image_cache.py
```

**测试内容**：
1. 单个图片下载
2. 缓存命中测试
3. 批量下载
4. 缓存管理器功能
5. 本地路径查询
6. 缓存清空
7. 与图片生成集成

---

## 📈 性能指标

| 操作 | 时间 | 说明 |
|------|------|------|
| 单个下载（新） | 取决于网络 | 通常1-5秒 |
| 单个下载（缓存） | <10ms | 本地文件读取 |
| 批量下载（10张） | 10-50秒 | 取决于网络 |
| 缓存统计 | <10ms | 读取索引文件 |
| 缓存清空 | <100ms | 删除文件 |

---

## 💰 成本节省

### API调用节省

- **无缓存**：每次都需要调用API
- **有缓存**：缓存命中后直接使用本地文件
- **节省比例**：取决于缓存命中率

假设缓存命中率为80%：
- 100次请求 = 20次API调用 + 80次本地读取
- 节省80%的API调用

### 网络带宽节省

- **图片大小**：平均500KB
- **下载次数**：100次
- **总流量**：50MB（无缓存）vs 10MB（80%缓存）
- **节省**：40MB

---

## 🚀 集成到n8n工作流

### 工作流设计

```
1. 生成图片 (AliWanxiangGenerator)
   ↓
2. 提取URL (Code节点)
   ↓
3. 下载图片 (Execute Command)
   ↓
4. 替换URL (Code节点)
   ↓
5. 格式化 (PlatformAdapter)
   ↓
6. 发布
```

### 代码示例

```bash
# n8n Execute Command节点
cd /home/admin/.openclaw/workspace/humanwriter && python -c "
from formatter import ImageCacheManager
import json

urls = {{ $json.urls }}
cache_manager = ImageCacheManager()

results = []
for url in urls:
    result = cache_manager.download_image(url)
    results.append(result)

print(json.dumps(results, ensure_ascii=False))
"
```

---

## 🎯 最佳实践

1. **定期清理**：设置定时任务清理旧缓存
2. **监控大小**：监控缓存目录大小
3. **使用相对路径**：替换URL为相对路径
4. **批量处理**：使用批量下载提升效率
5. **错误处理**：处理下载失败的情况

---

## 📚 相关文档

- **图片生成指南**：`IMAGE_GENERATOR_GUIDE.md`
- **格式化器文档**：`FORMATTER_README.md`
- **WeChat Formatter Skill**：`/home/admin/.openclaw/workspace/skills/wechat-formatter/`

---

*功能完成时间：2026-02-26*
