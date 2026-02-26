"""
测试脚本：测试图片生成功能
"""
import os
from formatter.image_generator import (
    generate_article_cover,
    generate_custom_image
)
from formatter.image_enhancer import (
    enhance_with_images,
    generate_cover_image
)


def test_custom_image():
    """测试自定义图片生成"""
    print("=== 测试自定义图片生成 ===")

    # 检查API Key
    api_key = os.getenv("DASHSCOPE_API_KEY")
    if not api_key:
        print("⚠️ 未设置 DASHSCOPE_API_KEY 环境变量，跳过API测试")
        print("   设置方法：export DASHSCOPE_API_KEY=your_api_key")
        return

    result = generate_custom_image(
        prompt="Professional workspace with laptop and coffee, modern office, clean desk, natural lighting",
        style="photography",
        use_cache=True
    )

    if result["success"]:
        print(f"✅ 生成成功！")
        print(f"  - 图片URL: {result['images'][0]}")
        print(f"  - Prompt: {result['prompt']}")
        print()
    else:
        print(f"❌ 生成失败：{result.get('error')}")
        print()


def test_article_cover():
    """测试文章封面生成"""
    print("=== 测试文章封面生成 ===")

    api_key = os.getenv("DASHSCOPE_API_KEY")
    if not api_key:
        print("⚠️ 未设置 DASHSCOPE_API_KEY 环境变量，跳过API测试")
        print()

    title = "2026年内容创作工具趋势"
    content = """随着AI技术的快速发展，内容创作工具正在经历前所未有的变革。

## 核心趋势

### 1. AI写作助手
AI写作助手已经成为内容创作者的标配工具。它们可以帮助我们快速生成初稿、优化文章结构、提升写作效率。

### 2. 多平台适配
一键发布到多个平台是现代内容创作者的核心需求。

> "未来，每个人都可以成为内容创作者。"

## 技术亮点

100维度AI检测：行业领先的AI检测技术，准确率95%+。

## 总结
内容创作的未来已来，抓住趋势，成为领先者。"""

    result = generate_article_cover(
        title=title,
        content=content,
        style="photography"
    )

    if result.get("success"):
        print(f"✅ 封面生成成功！")
        print(f"  - 图片URL: {result['images'][0]}")
        print(f"  - Prompt: {result['prompt']}")
        print(f"  - Style: {result['style']}")
        print()
    else:
        print(f"❌ 封面生成失败：{result.get('error')}")
        print()


def test_enhance_with_images():
    """测试Markdown增强（添加图片）"""
    print("=== 测试Markdown增强（添加图片） ===")

    api_key = os.getenv("DASHSCOPE_API_KEY")
    if not api_key:
        print("⚠️ 未设置 DASHSCOPE_API_KEY 环境变量，跳过API测试")
        print()

    markdown = """# 2026年AI工具趋势

## 引言
随着AI技术的快速发展，内容创作工具正在经历前所未有的变革。

## 核心趋势

### AI写作助手
AI写作助手已经成为内容创作者的标配工具。

### 多平台适配
一键发布到多个平台是现代内容创作者的核心需求。

## 总结
内容创作的未来已来，抓住趋势，成为领先者。"""

    result = enhance_with_images(
        markdown_content=markdown,
        style="photography",
        insert_cover=True,
        insert_section_images=True,
        max_images=2
    )

    if result["success"]:
        print(f"✅ 增强成功！")
        print(f"  - 生成图片数: {result['count']}")
        print(f"  - 图片列表:")
        for img in result["images"]:
            print(f"    * [{img['position']}] {img['url']}")
        print(f"\n增强后的Markdown（前500字）:")
        print(result["markdown"][:500] + "...")
        print()
    else:
        print(f"❌ 增强失败：{result.get('error')}")
        print()


def test_styles():
    """测试不同风格"""
    print("=== 测试不同风格 ===")

    api_key = os.getenv("DASHSCOPE_API_KEY")
    if not api_key:
        print("⚠️ 未设置 DASHSCOPE_API_KEY 环境变量，跳过API测试")
        print()

    styles = ["photography", "illustration", "3d"]
    prompt = "Technology innovation, AI tools, modern workspace"

    for style in styles:
        print(f"测试风格: {style}")

        result = generate_custom_image(
            prompt=prompt,
            style=style,
            use_cache=True
        )

        if result["success"]:
            print(f"  ✅ 成功: {result['images'][0]}")
        else:
            print(f"  ❌ 失败: {result.get('error')}")

        print()


def test_integration_with_formatter():
    """测试与格式化器的集成"""
    print("=== 测试与格式化器的集成 ===")

    from formatter.platform_adapter import adapt_to_platforms

    markdown = """# HumanWriter产品介绍

## 什么是HumanWriter？

HumanWriter是一款多平台内容适配工具。

## 核心功能

### AI检测器
100维度检测，准确率95%+。

### 多平台适配
支持公众号、知乎、小红书、微博、头条。

## 总结
HumanWriter，让内容创作更高效。"""

    # 先增强（添加图片）
    enhanced_result = enhance_with_images(
        markdown_content=markdown,
        style="photography",
        insert_cover=True,
        insert_section_images=False,
        max_images=1
    )

    if enhanced_result["success"]:
        print(f"✅ 增强成功，生成 {enhanced_result['count']} 张图片")

        # 再适配到各平台
        adapted = adapt_to_platforms(enhanced_result["markdown"])

        print(f"✅ 适配成功！")
        print(f"  - 公众号HTML: {len(adapted['wechat'])} 字符")
        print(f"  - 知乎Markdown: {len(adapted['zhihu'])} 字符")
        print(f"  - 小红书: {len(adapted['xiaohongshu'])} 字符")
        print(f"\n知乎Markdown预览（含图片）:")
        print(adapted["zhihu"][:400] + "...")
        print()
    else:
        print(f"❌ 增强失败：{enhanced_result.get('error')}")
        print()


if __name__ == "__main__":
    print("🚀 开始测试图片生成功能\n")

    # 检查API Key
    api_key = os.getenv("DASHSCOPE_API_KEY")
    if not api_key:
        print("⚠️ 提示：图片生成需要阿里云API Key")
        print("   设置方法：")
        print("   export DASHSCOPE_API_KEY=sk-your-api-key")
        print()
        print("   获取API Key：")
        print("   1. 访问 https://dashscope.aliyun.com/")
        print("   2. 注册/登录")
        print("   3. 创建API Key")
        print()

    test_custom_image()
    test_article_cover()
    test_enhance_with_images()
    test_styles()
    test_integration_with_formatter()

    print("🎉 所有测试完成！")
