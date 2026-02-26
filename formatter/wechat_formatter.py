"""
公众号HTML排版器
将Markdown内容转换为符合公众号规范的HTML
"""
from typing import List
from .markdown_parser import MarkdownParser, MarkdownSection


class WeChatFormatter:
    """公众号排版器"""

    def __init__(self, parser: MarkdownParser):
        self.parser = parser
        self.sections = parser.sections

    def format(self) -> str:
        """格式化为HTML"""
        html_parts = []

        # HTML头部
        html_parts.append(self._get_header())

        # 遍历所有段落
        for section in self.sections:
            if section.type == "heading":
                html_parts.append(self._format_heading(section))
            elif section.type == "paragraph":
                html_parts.append(self._format_paragraph(section))
            elif section.type == "list":
                html_parts.append(self._format_list(section))
            elif section.type == "code":
                html_parts.append(self._format_code(section))
            elif section.type == "quote":
                html_parts.append(self._format_quote(section))
            elif section.type == "image":
                html_parts.append(self._format_image(section))

        # HTML尾部
        html_parts.append(self._get_footer())

        return "\n".join(html_parts)

    def _get_header(self) -> str:
        """HTML头部"""
        return '''<section style="max-width: 677px; margin: 0 auto; font-size: 16px; color: #333; line-height: 1.8;">'''

    def _get_footer(self) -> str:
        """HTML尾部"""
        return '''</section>'''

    def _format_heading(self, section: MarkdownSection) -> str:
        """格式化标题"""
        if section.level == 1:
            style = "font-size: 22px; font-weight: bold; color: #000; margin: 30px 0 20px; padding-bottom: 10px; border-bottom: 2px solid #1890ff;"
        elif section.level == 2:
            style = "font-size: 20px; font-weight: bold; color: #333; margin: 25px 0 15px; padding-left: 10px; border-left: 4px solid #1890ff;"
        elif section.level == 3:
            style = "font-size: 18px; font-weight: bold; color: #333; margin: 20px 0 12px;"
        else:
            style = "font-size: 17px; font-weight: bold; color: #666; margin: 15px 0 10px;"

        return f'''<h{section.level} style="{style}">{section.content}</h{section.level}>'''

    def _format_paragraph(self, section: MarkdownSection) -> str:
        """格式化段落"""
        # 处理加粗
        content = section.content.replace('**', '<b>').replace('</b>', '</b>')
        # 处理斜体
        content = content.replace('*', '<i>').replace('</i>', '</i>')

        style = "margin: 15px 0; text-align: justify; text-indent: 2em;"

        return f'''<p style="{style}">{content}</p>'''

    def _format_list(self, section: MarkdownSection) -> str:
        """格式化列表"""
        return f'''
        <p style="margin: 10px 0; padding-left: 20px;">
            <span style="display: inline-block; width: 6px; height: 6px; background: #1890ff; border-radius: 50%; margin-right: 10px;"></span>
            {section.content}
        </p>'''

    def _format_code(self, section: MarkdownSection) -> str:
        """格式化代码块"""
        lang = section.metadata.get("language", "text")
        style = "background: #f6f8fa; padding: 15px; margin: 20px 0; border-radius: 4px; font-family: 'Consolas', 'Monaco', monospace; font-size: 14px; overflow-x: auto;"

        return f'''
        <div style="{style}">
            <div style="font-size: 12px; color: #666; margin-bottom: 10px;">📌 {lang}</div>
            <pre style="white-space: pre-wrap; margin: 0;"><code>{section.content}</code></pre>
        </div>'''

    def _format_quote(self, section: MarkdownSection) -> str:
        """格式化引用"""
        style = "background: #f0f7ff; padding: 15px 20px; margin: 20px 0; border-left: 4px solid #1890ff; border-radius: 0 4px 4px 0; color: #666; font-style: italic;"

        return f'''<blockquote style="{style}">
            💬 {section.content}
        </blockquote>'''

    def _format_image(self, section: MarkdownSection) -> str:
        """格式化图片"""
        url = section.metadata.get("url", "")
        alt = section.metadata.get("alt", "")

        style = "display: block; width: 100%; max-width: 677px; margin: 20px auto; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);"

        return f'''
        <img src="{url}" alt="{alt}" style="{style}" />
        <p style="text-align: center; font-size: 12px; color: #999; margin-top: 5px;">{alt}</p>'''


def format_markdown_to_wechat(markdown_content: str) -> str:
    """快捷函数：Markdown → 公众号HTML"""
    parser = MarkdownParser(markdown_content)
    parser.parse()
    formatter = WeChatFormatter(parser)
    return formatter.format()
