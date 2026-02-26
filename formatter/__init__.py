"""
HumanWriter格式化器
Markdown解析、排版、图片生成、平台适配
"""

from .markdown_parser import MarkdownParser, MarkdownSection
from .wechat_formatter import WeChatFormatter, format_markdown_to_wechat
from .platform_adapter import (
    PlatformAdapter,
    adapt_to_platforms
)
from .image_generator import (
    AliWanxiangGenerator,
    generate_article_cover,
    generate_custom_image
)
from .image_enhancer import (
    ImageEnhancer,
    enhance_with_images,
    generate_cover_image
)
from .image_cache import (
    ImageCacheManager,
    download_image,
    download_images
)

__all__ = [
    # Markdown解析
    "MarkdownParser",
    "MarkdownSection",

    # 公众号排版
    "WeChatFormatter",
    "format_markdown_to_wechat",

    # 平台适配
    "PlatformAdapter",
    "adapt_to_platforms",

    # 图片生成
    "AliWanxiangGenerator",
    "generate_article_cover",
    "generate_custom_image",

    # 图片增强
    "ImageEnhancer",
    "enhance_with_images",
    "generate_cover_image",

    # 图片缓存
    "ImageCacheManager",
    "download_image",
    "download_images",
]

__version__ = "1.0.0"
