"""
完整演示：Markdown → 生成图片 → 格式化 → 多平台适配
"""
import os
from formatter import (
    enhance_with_images,
    adapt_to_platforms
)


def demo_complete_workflow():
    """完整工作流演示"""
    print("=" * 60)
    print("HumanWriter 完整工作流演示")
    print("=" * 60)
    print()

    # 步骤0：检查API Key
    api_key = os.getenv("DASHSCOPE_API_KEY")
    if api_key:
        print(f"✅ 已配置阿里云API Key: {api_key[:10]}...")
        print()
    else:
        print("⚠️ 未配置API Key，仅演示格式化和平台适配功能")
        print("   设置方法：export DASHSCOPE_API_KEY=sk-your-api-key")
        print()

    # 步骤1：原始Markdown
    markdown = """# 2026年AI工具趋势

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

## 总结
内容创作的未来已来，抓住趋势，成为领先者。"""

    print("📝 步骤1：原始Markdown")
    print("-" * 60)
    print(markdown[:200] + "...")
    print()

    # 步骤2：生成图片（如果有API Key）
    enhanced_markdown = markdown
    image_count = 0

    if api_key:
        print("🎨 步骤2：生成图片")
        print("-" * 60)

        enhance_result = enhance_with_images(
            markdown_content=markdown,
            style="photography",
            insert_cover=True,
            insert_section_images=True,
            max_images=2
        )

        if enhance_result["success"]:
            enhanced_markdown = enhance_result["markdown"]
            image_count = enhance_result["count"]

            print(f"✅ 成功生成 {image_count} 张图片")
            for i, img in enumerate(enhance_result["images"]):
                print(f"  [{i+1}] {img['position']}: {img['url']}")
        else:
            print(f"❌ 图片生成失败：{enhance_result.get('error')}")

        print()
    else:
        print("⏭️ 步骤2：跳过图片生成（无API Key）")
        print()

    # 步骤3：格式化和平台适配
    print("📊 步骤3：格式化和平台适配")
    print("-" * 60)

    adapted = adapt_to_platforms(enhanced_markdown)

    print(f"✅ 适配成功！")
    print(f"  - 标题: {adapted['metadata']['title']}")
    print(f"  - 字数: {adapted['metadata']['word_count']}")
    print(f"  - 段落数: {adapted['metadata']['sections_count']}")
    print(f"  - 图片数: {adapted['metadata']['images_count']}")
    print()

    # 步骤4：输出各平台内容
    print("📱 步骤4：各平台内容")
    print("=" * 60)

    # 公众号
    print("\n📌 公众号（HTML）")
    print("-" * 60)
    wechat_html = adapted["wechat"]
    print(wechat_html[:300] + "...")

    # 知乎
    print("\n📌 知乎（Markdown）")
    print("-" * 60)
    zhihu_md = adapted["zhihu"]
    print(zhihu_md[:200] + "...")

    # 小红书
    print("\n📌 小红书（emoji）")
    print("-" * 60)
    xhs_content = adapted["xiaohongshu"]
    print(xhs_content[:200] + "...")

    # 微博
    print("\n📌 微博（140字摘要）")
    print("-" * 60)
    weibo_data = adapted["weibo"]
    print(f"内容: {weibo_data['content']}")
    print(f"长度: {weibo_data['length']} 字符")
    print(f"符合限制: {'✅' if weibo_data['within_limit'] else '❌'}")

    # 头条
    print("\n📌 头条（标题 + 正文）")
    print("-" * 60)
    toutiao_data = adapted["toutiao"]
    print(f"标题: {toutiao_data['title']}")
    print(f"摘要: {toutiao_data['summary']}")
    print(f"字数: {toutiao_data['word_count']}")

    print()
    print("=" * 60)
    print("✅ 完整工作流演示完成！")
    print("=" * 60)


def demo_quick_start():
    """快速开始演示"""
    print("\n" + "=" * 60)
    print("HumanWriter 快速开始")
    print("=" * 60)
    print()

    # 方式1：仅格式化
    print("方式1：仅格式化（无图片生成）")
    print("-" * 60)

    from formatter import adapt_to_platforms

    markdown = """# 测试文章

这是一个测试文章。

## 核心功能

AI检测器、多平台适配。"""

    result = adapt_to_platforms(markdown)

    print(f"✅ 适配成功！")
    print(f"  - 公众号: {len(result['wechat'])} 字符")
    print(f"  - 知乎: {len(result['zhihu'])} 字符")
    print()

    # 方式2：生成图片 + 格式化
    print("方式2：生成图片 + 格式化（需要API Key）")
    print("-" * 60)

    api_key = os.getenv("DASHSCOPE_API_KEY")
    if api_key:
        from formatter import enhance_with_images, adapt_to_platforms

        enhanced = enhance_with_images(
            markdown_content=markdown,
            style="photography",
            insert_cover=True,
            insert_section_images=False,
            max_images=1
        )

        if enhanced["success"]:
            print(f"✅ 生成 {enhanced['count']} 张图片")

            adapted = adapt_to_platforms(enhanced["markdown"])
            print(f"✅ 适配成功！")
            print(f"  - 公众号: {len(adapted['wechat'])} 字符（含图片）")
    else:
        print("⚠️ 需要配置 DASHSCOPE_API_KEY")

    print()


if __name__ == "__main__":
    # 快速开始
    demo_quick_start()

    # 完整工作流
    demo_complete_workflow()
