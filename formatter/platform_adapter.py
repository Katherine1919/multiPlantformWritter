"""
平台适配器
将Markdown内容适配到不同平台
"""
from typing import Dict, List
from .markdown_parser import MarkdownParser


class PlatformAdapter:
    """平台适配器"""

    def __init__(self, markdown_content: str):
        self.parser = MarkdownParser(markdown_content)
        self.parser.parse()
        self.metadata = self.parser.get_metadata()

    def adapt_to_wechat(self) -> str:
        """适配公众号（HTML格式）"""
        from .wechat_formatter import WeChatFormatter
        formatter = WeChatFormatter(self.parser)
        return formatter.format()

    def adapt_to_zhihu(self) -> str:
        """适配知乎（Markdown格式）"""
        # 知乎支持标准Markdown，稍微优化一下
        content = self.parser.content

        # 添加标题
        if self.metadata["title"]:
            content = f"# {self.metadata['title']}\n\n" + content

        return content

    def adapt_to_xiaohongshu(self) -> str:
        """适配小红书（emoji + 分段）"""
        sections = []
        for section in self.parser.sections:
            if section.type == "heading":
                emoji = "🔸" * section.level
                sections.append(f"\n{emoji} {section.content}\n")
            elif section.type == "paragraph":
                # 每段加emoji
                sections.append(f"✨ {section.content}")
            elif section.type == "list":
                sections.append(f"📌 {section.content}")
            elif section.type == "quote":
                sections.append(f"💬 {section.content}")
            elif section.type == "image":
                sections.append(f"🖼️ [{section.metadata.get('alt', '图片')}]")

        # 添加hashtags
        hashtags = " #AI写作 #内容创作 #HumanWriter"
        return "\n".join(sections) + hashtags

    def adapt_to_weibo(self) -> Dict:
        """适配微博（140字摘要 + 链接）"""
        plain_text = self.parser.to_plain_text()

        # 提取前140字
        summary = plain_text[:137] + "..."

        # 构建微博内容
        content = f"【{self.metadata.get('title', '新文章')}】\n{summary}\n\n#AI写作 #内容创作"

        return {
            "content": content,
            "length": len(content),
            "within_limit": len(content) <= 140
        }

    def adapt_to_toutiao(self) -> Dict:
        """适配头条（标题 + 正文）"""
        plain_text = self.parser.to_plain_text()

        return {
            "title": self.metadata.get("title", "未命名文章"),
            "content": plain_text,
            "summary": self.metadata.get("summary", ""),
            "word_count": self.metadata.get("word_count", 0)
        }

    def adapt_all(self) -> Dict[str, any]:
        """适配所有平台"""
        return {
            "wechat": self.adapt_to_wechat(),
            "zhihu": self.adapt_to_zhihu(),
            "xiaohongshu": self.adapt_to_xiaohongshu(),
            "weibo": self.adapt_to_weibo(),
            "toutiao": self.adapt_to_toutiao(),
            "metadata": self.metadata
        }


def adapt_to_platforms(markdown_content: str, platforms: List[str] = None) -> Dict:
    """快捷函数：适配指定平台"""
    if platforms is None:
        platforms = ["wechat", "zhihu", "xiaohongshu", "weibo", "toutiao"]

    adapter = PlatformAdapter(markdown_content)
    all_adapted = adapter.adapt_all()

    # 返回指定平台 + metadata
    result = {k: v for k, v in all_adapted.items() if k in platforms}
    result["metadata"] = all_adapted["metadata"]

    return result
