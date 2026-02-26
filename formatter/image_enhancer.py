"""
图片增强器
为Markdown文章自动生成并插入配图
"""
from typing import Optional, Dict
from .markdown_parser import MarkdownParser
from .image_generator import AliWanxiangGenerator


class ImageEnhancer:
    """图片增强器"""

    def __init__(
        self,
        api_key: Optional[str] = None,
        auto_generate: bool = True,
        style: str = "photography"
    ):
        """
        初始化图片增强器

        Args:
            api_key: 阿里云API Key
            auto_generate: 是否自动生成图片
            style: 图片风格
        """
        self.api_key = api_key
        self.auto_generate = auto_generate
        self.style = style
        self.generator = AliWanxiangGenerator(api_key)

    def enhance(
        self,
        markdown_content: str,
        insert_cover: bool = True,
        insert_section_images: bool = True,
        max_images: int = 3
    ) -> Dict:
        """
        增强Markdown（添加图片）

        Args:
            markdown_content: Markdown内容
            insert_cover: 是否插入封面图
            insert_section_images: 是否插入段落配图
            max_images: 最大图片数量

        Returns:
            {
                "success": bool,
                "markdown": str,  # 增强后的Markdown
                "images": list,    # 图片URL列表
                "error": str       # 错误信息
            }
        """
        try:
            # 解析Markdown
            parser = MarkdownParser(markdown_content)
            parser.parse()
            metadata = parser.get_metadata()

            images = []
            enhanced_lines = []
            lines = markdown_content.split('\n')

            # 插入封面图
            if insert_cover and metadata.get("title"):
                cover_result = self.generator.generate_for_article(
                    title=metadata["title"],
                    content=parser.to_plain_text()[:500],
                    style=self.style
                )

                if cover_result.get("success"):
                    cover_url = cover_result["images"][0]
                    images.append({
                        "position": "cover",
                        "url": cover_url,
                        "prompt": cover_result["prompt"]
                    })

                    # 在标题后插入封面图
                    enhanced_lines.append(f"![封面]({cover_url})")
                    enhanced_lines.append("")

            # 统计图片数量
            image_count = 0

            # 遍历段落，插入配图
            if insert_section_images and len(images) < max_images:
                i = 0
                while i < len(lines) and image_count < max_images:
                    line = lines[i]

                    # 在H2标题后插入图片
                    if line.strip().startswith("## ") and image_count < max_images:
                        # 生成配图
                        section_title = line.strip()[3:].strip()

                        # 提取段落内容
                        section_content = ""
                        j = i + 1
                        while j < len(lines) and not lines[j].startswith("#"):
                            if lines[j].strip() and not lines[j].startswith("!"):
                                section_content += lines[j] + "\n"
                                if len(section_content) > 200:
                                    break
                            j += 1

                        # 生成图片
                        image_result = self.generator.generate_for_article(
                            title=section_title,
                            content=section_content,
                            style=self.style
                        )

                        if image_result.get("success"):
                            image_url = image_result["images"][0]
                            images.append({
                                "position": f"section_{image_count}",
                                "url": image_url,
                                "title": section_title,
                                "prompt": image_result["prompt"]
                            })

                            # 在标题后插入图片
                            enhanced_lines.append(line)
                            enhanced_lines.append(f"![{section_title}]({image_url})")
                            enhanced_lines.append("")
                            image_count += 1
                        else:
                            enhanced_lines.append(line)
                    else:
                        enhanced_lines.append(line)

                    i += 1
            else:
                # 不插入段落配图，直接复制所有行
                if not insert_cover:
                    enhanced_lines = lines

            # 组合增强后的Markdown
            enhanced_markdown = '\n'.join(enhanced_lines)

            return {
                "success": True,
                "markdown": enhanced_markdown,
                "images": images,
                "count": len(images)
            }

        except Exception as e:
            return {
                "success": False,
                "markdown": markdown_content,
                "images": [],
                "error": str(e)
            }

    def generate_cover_only(
        self,
        title: str,
        content: str
    ) -> Dict:
        """
        仅生成封面图

        Args:
            title: 文章标题
            content: 文章内容

        Returns:
            生成结果
        """
        return self.generator.generate_for_article(title, content, self.style)


def enhance_with_images(
    markdown_content: str,
    style: str = "photography",
    api_key: Optional[str] = None,
    insert_cover: bool = True,
    insert_section_images: bool = True,
    max_images: int = 3
) -> Dict:
    """
    快捷函数：为Markdown添加配图

    Args:
        markdown_content: Markdown内容
        style: 图片风格
        api_key: 阿里云API Key
        insert_cover: 是否插入封面图
        insert_section_images: 是否插入段落配图
        max_images: 最大图片数量

    Returns:
        增强结果

    Example:
        result = enhance_with_images(
            markdown_content="# 文章标题\n\n这是内容...",
            style="photography",
            insert_cover=True,
            max_images=3
        )

        if result["success"]:
            print(f"✅ 成功生成 {result['count']} 张图片")
            print(result["markdown"])
        else:
            print(f"❌ 失败：{result['error']}")
    """
    enhancer = ImageEnhancer(api_key, style=style)
    return enhancer.enhance(
        markdown_content,
        insert_cover,
        insert_section_images,
        max_images
    )


def generate_cover_image(
    title: str,
    content: str,
    style: str = "photography",
    api_key: Optional[str] = None
) -> Dict:
    """
    快捷函数：仅生成封面图

    Args:
        title: 文章标题
        content: 文章内容
        style: 图片风格
        api_key: 阿里云API Key

    Returns:
        生成结果

    Example:
        result = generate_cover_image(
            title="2026年AI工具趋势",
            content="随着AI技术的快速发展..."
        )

        if result["success"]:
            print(f"✅ 封面图：{result['images'][0]}")
    """
    enhancer = ImageEnhancer(api_key, style=style)
    return enhancer.generate_cover_only(title, content)
