"""
Markdown解析器
解析Markdown内容，提取结构化数据
"""
import re
from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class MarkdownSection:
    """Markdown段落"""
    type: str  # heading, paragraph, list, code, quote, image
    level: int = 0  # 标题级别(1-6)
    content: str = ""
    raw: str = ""
    metadata: Optional[Dict] = None


class MarkdownParser:
    """Markdown解析器"""

    def __init__(self, content: str):
        self.content = content
        self.sections: List[MarkdownSection] = []
        self.title = ""
        self.summary = ""

    def parse(self) -> List[MarkdownSection]:
        """解析Markdown内容"""
        lines = self.content.split('\n')
        current_section = None
        code_block = False
        code_lang = ""
        code_lines = []

        for line in lines:
            # 代码块处理
            if line.strip().startswith('```'):
                if not code_block:
                    code_block = True
                    code_lang = line.strip()[3:] or "text"
                else:
                    # 结束代码块
                    if code_lines:
                        self.sections.append(MarkdownSection(
                            type="code",
                            content='\n'.join(code_lines),
                            raw=f"```{code_lang}\n{''.join(code_lines)}\n```",
                            metadata={"language": code_lang}
                        ))
                    code_block = False
                    code_lang = ""
                    code_lines = []
                continue

            if code_block:
                code_lines.append(line)
                continue

            # 标题处理
            heading_match = re.match(r'^(#{1,6})\s+(.+)$', line)
            if heading_match:
                level = len(heading_match.group(1))
                content = heading_match.group(2).strip()

                # 提取主标题
                if level == 1 and not self.title:
                    self.title = content

                self.sections.append(MarkdownSection(
                    type="heading",
                    level=level,
                    content=content,
                    raw=line
                ))
                continue

            # 图片处理
            image_match = re.match(r'!\[([^\]]*)\]\(([^)]+)\)', line)
            if image_match:
                alt_text = image_match.group(1)
                url = image_match.group(2)
                self.sections.append(MarkdownSection(
                    type="image",
                    content=alt_text,
                    raw=line,
                    metadata={"url": url, "alt": alt_text}
                ))
                continue

            # 引用处理
            if line.strip().startswith('>'):
                content = line.strip()[1:].strip()
                self.sections.append(MarkdownSection(
                    type="quote",
                    content=content,
                    raw=line
                ))
                continue

            # 列表处理
            list_match = re.match(r'^\s*[-*+]\s+(.+)$', line)
            if list_match:
                content = list_match.group(1)
                self.sections.append(MarkdownSection(
                    type="list",
                    content=content,
                    raw=line
                ))
                continue

            # 空行处理
            if not line.strip():
                continue

            # 普通段落
            if current_section and current_section.type == "paragraph":
                current_section.content += "\n" + line
                current_section.raw += "\n" + line
            else:
                current_section = MarkdownSection(
                    type="paragraph",
                    content=line,
                    raw=line
                )
                self.sections.append(current_section)

        # 提取摘要（第一个段落，非标题）
        for section in self.sections:
            if section.type == "paragraph" and not self.summary:
                self.summary = section.content[:100] + "..."
                break

        return self.sections

    def get_metadata(self) -> Dict:
        """获取元数据"""
        return {
            "title": self.title,
            "summary": self.summary,
            "sections_count": len(self.sections),
            "headings_count": sum(1 for s in self.sections if s.type == "heading"),
            "images_count": sum(1 for s in self.sections if s.type == "image"),
            "word_count": len(self.content)
        }

    def to_plain_text(self) -> str:
        """转换为纯文本（用于微博/头条）"""
        text_parts = []
        for section in self.sections:
            if section.type == "heading":
                text_parts.append(f"\n【{section.content}】\n")
            elif section.type == "paragraph":
                text_parts.append(section.content)
            elif section.type == "list":
                text_parts.append(f"• {section.content}")
            elif section.type == "quote":
                text_parts.append(f"💬 {section.content}")
        return "\n".join(text_parts)
