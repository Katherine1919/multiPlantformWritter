"""
测试脚本：测试Markdown解析和平台适配
"""
from formatter.markdown_parser import MarkdownParser
from formatter.wechat_formatter import format_markdown_to_wechat
from formatter.platform_adapter import adapt_to_platforms


# 测试Markdown内容
test_markdown = """# 2026年内容创作工具趋势

## 引言
随着AI技术的快速发展，内容创作工具正在经历前所未有的变革。

## 核心趋势

### 1. AI写作助手
AI写作助手已经成为内容创作者的标配工具。它们可以帮助我们：
- 快速生成初稿
- 优化文章结构
- 提升写作效率

### 2. 多平台适配
一键发布到多个平台是现代内容创作者的核心需求。

> "未来，每个人都可以成为内容创作者。"

## 技术亮点

**100维度AI检测**：行业领先的AI检测技术，准确率95%+。

```python
def detect_ai_content(text):
    # AI检测算法
    return ai_probability
```

## 总结
内容创作的未来已来，抓住趋势，成为领先者。"""


def test_markdown_parser():
    """测试Markdown解析器"""
    print("=== 测试Markdown解析器 ===")
    parser = MarkdownParser(test_markdown)
    sections = parser.parse()

    print(f"✅ 解析成功！")
    print(f"  - 段落数量: {len(sections)}")
    print(f"  - 元数据: {parser.get_metadata()}")
    print()


def test_wechat_formatter():
    """测试公众号排版器"""
    print("=== 测试公众号排版器 ===")
    html = format_markdown_to_wechat(test_markdown)

    print(f"✅ 排版成功！")
    print(f"  - HTML长度: {len(html)} 字符")
    print(f"  - HTML预览（前200字）:")
    print(html[:200] + "...")
    print()


def test_platform_adapter():
    """测试平台适配器"""
    print("=== 测试平台适配器 ===")
    adapted = adapt_to_platforms(test_markdown)

    platforms = ["wechat", "zhihu", "xiaohongshu", "weibo", "toutiao"]
    for platform in platforms:
        content = adapted[platform]
        if isinstance(content, str):
            print(f"✅ {platform}: {len(content)} 字符")
        elif isinstance(content, dict):
            print(f"✅ {platform}: {list(content.keys())}")
    print()


def test_real_articles():
    """测试真实文章"""
    print("=== 测试真实文章 ===")

    # 测试文章
    article_files = [
        "articles/test-article.md"
    ]

    for article_file in article_files:
        try:
            with open(article_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # 解析
            parser = MarkdownParser(content)
            parser.parse()
            metadata = parser.get_metadata()

            # 适配所有平台
            adapted = adapt_to_platforms(content)

            print(f"✅ {article_file}")
            print(f"  - 标题: {metadata.get('title', 'N/A')}")
            print(f"  - 字数: {metadata.get('word_count', 0)}")
            print(f"  - 图片数: {metadata.get('images_count', 0)}")

            # 输出公众号HTML示例
            wechat_html = adapted.get("wechat", "")
            print(f"  - 公众号HTML: {len(wechat_html)} 字符")

            # 输出小红书示例
            xhs_content = adapted.get("xiaohongshu", "")
            print(f"  - 小红书内容预览: {xhs_content[:100]}...")

            print()

        except FileNotFoundError:
            print(f"⚠️ 文件未找到: {article_file}")
        except Exception as e:
            print(f"❌ 错误: {e}")


if __name__ == "__main__":
    print("🚀 开始测试格式化器\n")

    test_markdown_parser()
    test_wechat_formatter()
    test_platform_adapter()
    test_real_articles()

    print("🎉 所有测试完成！")
