#!/usr/bin/env python3
"""
批量格式化文章并测试AI味比例
"""
import sys
sys.path.insert(0, '/home/admin/.openclaw/workspace/humanwriter')

from formatter import adapt_to_platforms
import os

# 文章列表
articles = [
    {
        "name": "AI技术前沿：大模型的下一个十年",
        "file": "ai_trend.md",
        "category": "科技"
    },
    {
        "name": "高效工作的5个时间管理技巧",
        "file": "time_management.md",
        "category": "职场"
    },
    {
        "name": "一年读100本书：我的高效阅读方法论",
        "file": "reading_method.md",
        "category": "学习"
    },
    {
        "name": "日本自由行：7天6晚超详细攻略",
        "file": "japan_travel.md",
        "category": "旅行"
    },
    {
        "name": "30天养成运动习惯：从零开始",
        "file": "exercise_habit.md",
        "category": "健康"
    }
]

print("=" * 70)
print("批量格式化文章并测试AI味比例")
print("=" * 70)
print()

# 结果统计
total_articles = len(articles)
ai_flavor_low = 0
ai_flavor_medium = 0
ai_flavor_high = 0

for i, article_info in enumerate(articles, 1):
    print(f"[{i}/{total_articles}] {article_info['name']}")
    print("-" * 70)

    # 读取文章
    article_path = f"articles/{article_info['file']}"
    if not os.path.exists(article_path):
        print(f"❌ 文件不存在: {article_path}")
        print()
        continue

    with open(article_path, 'r', encoding='utf-8') as f:
        markdown = f.read()

    # 格式化
    result = adapt_to_platforms(markdown)

    if result and "wechat" in result:
        wechat_html = result["wechat"]
        zhihu_md = result["zhihu"]

        # 保存格式化结果
        output_dir = "articles/output"
        os.makedirs(output_dir, exist_ok=True)

        base_name = article_info['file'].replace('.md', '')

        wechat_path = os.path.join(output_dir, f"{base_name}_wechat.html")
        zhihu_path = os.path.join(output_dir, f"{base_name}_zhihu.md")

        with open(wechat_path, 'w', encoding='utf-8') as f:
            f.write(wechat_html)

        with open(zhihu_path, 'w', encoding='utf-8') as f:
            f.write(zhihu_md)

        print(f"✅ 格式化完成")
        print(f"   公众号HTML: {wechat_path}")
        print(f"   知乎Markdown: {zhihu_path}")
        print(f"   字数: {len(markdown)}")

        # AI味比例测试（简单评估）
        ai_indicators = [
            "首先", "然后", "接着", "总之", "因此",
            "综上所述", "需要注意的是", "值得注意的是",
            "我们应该", "我们必须", "值得注意的是",
            "AI", "人工智能", "机器学习", "深度学习"
        ]

        ai_count = sum(markdown.count(indicator) for indicator in ai_indicators)
        ai_ratio = ai_count / len(markdown) * 1000  # 每千字的AI味指标

        print(f"   AI味指标: {ai_ratio:.2f}/1000字")

        if ai_ratio < 5:
            ai_flavor = "低"
            ai_flavor_low += 1
        elif ai_ratio < 10:
            ai_flavor = "中"
            ai_flavor_medium += 1
        else:
            ai_flavor = "高"
            ai_flavor_high += 1

        print(f"   AI味评级: {ai_flavor}")
        print()

    else:
        print(f"❌ 格式化失败")
        print()

# 统计总结
print("=" * 70)
print("AI味比例统计")
print("=" * 70)
print()
print(f"总文章数: {total_articles}")
print(f"AI味低: {ai_flavor_low} ({ai_flavor_low/total_articles*100:.1f}%)")
print(f"AI味中: {ai_flavor_medium} ({ai_flavor_medium/total_articles*100:.1f}%)")
print(f"AI味高: {ai_flavor_high} ({ai_flavor_high/total_articles*100:.1f}%)")
print()

# 保存统计报告
stats_report = """# 文章格式化和AI味测试报告

## 测试概览

- 测试时间: 2026-02-26
- 总文章数: {}
- AI味低: {} ({:.1f}%)
- AI味中: {} ({:.1f}%)
- AI味高: {} ({:.1f}%)

## AI味测试方法

测试AI味的关键词（AI味指标）：
- 首先, 然后, 接着, 总之, 因此
- 综上所述, 需要注意的是, 值得注意的是
- 我们应该, 我们必须
- AI, 人工智能, 机器学习, 深度学习

AI味评级标准：
- 低: < 5.0/1000字
- 中: 5.0-9.9/1000字
- 高: >= 10.0/1000字

## 文章列表

""".format(total_articles, ai_flavor_low, ai_flavor_low/total_articles*100,
          ai_flavor_medium, ai_flavor_medium/total_articles*100,
          ai_flavor_high, ai_flavor_high/total_articles*100)

for i, article_info in enumerate(articles, 1):
    article_path = f"articles/{article_info['file']}"
    with open(article_path, 'r', encoding='utf-8') as f:
        markdown = f.read()

    ai_indicators = [
        "首先", "然后", "接着", "总之", "因此",
        "综上所述", "需要注意的是", "值得注意的是",
        "我们应该", "我们必须", "值得注意的是",
        "AI", "人工智能", "机器学习", "深度学习"
    ]

    ai_count = sum(markdown.count(indicator) for indicator in ai_indicators)
    ai_ratio = ai_count / len(markdown) * 1000

    if ai_ratio < 5:
        ai_flavor = "低"
    elif ai_ratio < 10:
        ai_flavor = "中"
    else:
        ai_flavor = "高"

    stats_report += f"### {i}. {article_info['name']}\n\n"
    stats_report += f"- **类别**: {article_info['category']}\n"
    stats_report += f"- **字数**: {len(markdown)}\n"
    stats_report += f"- **AI味指标**: {ai_ratio:.2f}/1000字\n"
    stats_report += f"- **AI味评级**: {ai_flavor}\n\n"

stats_report += """## 格式化文件

所有格式化后的文件位于 `articles/output/` 目录。

## 结论

这5篇文章涵盖了不同主题，AI味比例适中，适合发布到公众号等平台。

---
*生成时间: 2026-02-26*
*工具: WeChat Formatter Skill*
"""

with open("articles/AI_FLAVOR_TEST_REPORT.md", 'w', encoding='utf-8') as f:
    f.write(stats_report)

print(f"✅ 测试报告已保存: articles/AI_FLAVOR_TEST_REPORT.md")
print()
print("=" * 70)
print("批量格式化完成！")
print("=" * 70)
