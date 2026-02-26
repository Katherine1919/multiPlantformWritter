#!/usr/bin/env python3
"""
使用WeChat Formatter Skill格式化文章
"""
import sys
sys.path.insert(0, '/home/admin/.openclaw/workspace/humanwriter')

from formatter import adapt_to_platforms, enhance_with_images, ImageCacheManager
import os

# 读取文章
article_path = "/home/admin/.openclaw/workspace/humanwriter/articles/wechat_formatter_story.md"
with open(article_path, 'r', encoding='utf-8') as f:
    markdown = f.read()

print("=" * 70)
print("WeChat Formatter Skill - 文章格式化")
print("=" * 70)
print()

# 检查是否有API Key
has_api_key = os.getenv("DASHSCOPE_API_KEY")

if has_api_key:
    print("✅ 检测到DASHSCOPE_API_KEY，启用图片生成功能")
    print()

    # 生成图片
    print("正在生成图片...")
    enhanced = enhance_with_images(
        markdown_content=markdown,
        style="photography",
        insert_cover=True,
        insert_section_images=True,
        max_images=5
    )

    if enhanced["success"]:
        print(f"✅ 图片生成成功：{enhanced['count']} 张")
        print()

        # 下载图片到本地缓存
        print("正在下载图片到本地缓存...")
        cache_manager = ImageCacheManager()

        for i, img_info in enumerate(enhanced["images"]):
            result = cache_manager.download_image(img_info["url"])
            if result["success"]:
                print(f"  [{i+1}] ✅ {result['local_path']}")
                img_info["local_path"] = result["local_path"]
            else:
                print(f"  [{i+1}] ❌ {result.get('error')}")
        print()

        # 使用带图片的Markdown
        markdown = enhanced["markdown"]
    else:
        print(f"⚠️ 图片生成失败：{enhanced.get('error')}")
        print("将使用无图片模式继续...")
        print()
else:
    print("⚠️ 未检测到DASHSCOPE_API_KEY，使用无图片模式")
    print("如需生成图片，请设置环境变量：")
    print("  export DASHSCOPE_API_KEY=sk-your-key")
    print()

# 格式化为多平台
print("正在格式化文章...")
adapted = adapt_to_platforms(markdown)

print("✅ 格式化完成！")
print()

# 输出结果
print("=" * 70)
print("格式化结果")
print("=" * 70)
print()

print("📱 公众号HTML（前500字符）：")
print("-" * 70)
print(adapted["wechat"][:500] + "...")
print()

print("📖 知乎Markdown（前300字符）：")
print("-" * 70)
print(adapted["zhihu"][:300] + "...")
print()

print("🔸 小红书（前300字符）：")
print("-" * 70)
print(adapted["xiaohongshu"][:300] + "...")
print()

print("🐦 微博摘要：")
print("-" * 70)
print(adapted["weibo"])
print()

print("📰 头条标题：")
print("-" * 70)
print(adapted["toutiao"]["title"])
print()

# 保存结果
output_dir = "/home/admin/.openclaw/workspace/humanwriter/articles/output"
os.makedirs(output_dir, exist_ok=True)

# 保存公众号HTML
wechat_html_path = os.path.join(output_dir, "wechat_formatter_story_wechat.html")
with open(wechat_html_path, 'w', encoding='utf-8') as f:
    f.write(adapted["wechat"])

# 保存知乎Markdown
zhihu_md_path = os.path.join(output_dir, "wechat_formatter_story_zhihu.md")
with open(zhihu_md_path, 'w', encoding='utf-8') as f:
    f.write(adapted["zhihu"])

# 保存小红书
xiaohongshu_path = os.path.join(output_dir, "wechat_formatter_story_xiaohongshu.txt")
with open(xiaohongshu_path, 'w', encoding='utf-8') as f:
    f.write(adapted["xiaohongshu"])

# 保存微博
weibo_path = os.path.join(output_dir, "wechat_formatter_story_weibo.txt")
with open(weibo_path, 'w', encoding='utf-8') as f:
    weibo_content = adapted["weibo"]["content"] if isinstance(adapted["weibo"], dict) else adapted["weibo"]
    f.write(weibo_content)

# 保存头条
toutiao_path = os.path.join(output_dir, "wechat_formatter_story_toutiao.md")
with open(toutiao_path, 'w', encoding='utf-8') as f:
    f.write(f"# {adapted['toutiao']['title']}\n\n{adapted['toutiao']['content']}")

print("=" * 70)
print("📁 文件已保存")
print("=" * 70)
print()
print(f"公众号HTML: {wechat_html_path}")
print(f"知乎Markdown: {zhihu_md_path}")
print(f"小红书: {xiaohongshu_path}")
print(f"微博: {weibo_path}")
print(f"头条: {toutiao_path}")
print()

print("🎉 格式化完成！")
print()
print("提示：")
print("  - 公众号HTML可直接复制到公众号编辑器")
print("  - 知乎Markdown可直接粘贴到知乎")
print("  - 小红书格式已优化，可直接发布")
print("  - 微博已自动截断到140字")
print("  - 头条格式为标题+正文结构")
print()
print("=" * 70)
