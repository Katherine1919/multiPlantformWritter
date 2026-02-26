"""
阿里通义万相API图片生成器
根据文章内容自动生成配图
"""
import requests
import os
import base64
from typing import Optional, Dict
import hashlib


class AliWanxiangGenerator:
    """阿里通义万相图片生成器"""

    def __init__(self, api_key: Optional[str] = None):
        """
        初始化图片生成器

        Args:
            api_key: 阿里云API Key，默认从环境变量读取
        """
        self.api_key = api_key or os.getenv("DASHSCOPE_API_KEY")
        self.base_url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text2image/image-synthesis"
        self.cache_dir = "cache/images"

        # 创建缓存目录
        os.makedirs(self.cache_dir, exist_ok=True)

    def generate(
        self,
        prompt: str,
        style: str = "photography",
        size: str = "1024*1024",
        n: int = 1,
        use_cache: bool = True
    ) -> Dict:
        """
        生成图片

        Args:
            prompt: 图片描述
            style: 图片风格
            size: 图片尺寸
            n: 生成数量
            use_cache: 是否使用缓存

        Returns:
            {
                "success": bool,
                "images": ["url1", "url2", ...],
                "prompt": str,
                "style": str
            }
        """
        # 检查缓存
        if use_cache:
            cache_key = self._get_cache_key(prompt, style, size)
            cached_result = self._load_from_cache(cache_key)
            if cached_result:
                return cached_result

        # 调用API
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }

            payload = {
                "model": "wanx-v1",
                "input": {
                    "prompt": prompt,
                    "style": style,
                    "size": size,
                    "n": n
                },
                "parameters": {
                    "watermark": False  # 去除水印
                }
            }

            response = requests.post(
                self.base_url,
                headers=headers,
                json=payload,
                timeout=30
            )

            response.raise_for_status()
            result = response.json()

            # 解析结果
            if "output" in result and "results" in result["output"]:
                images = [item["url"] for item in result["output"]["results"]]

                result_dict = {
                    "success": True,
                    "images": images,
                    "prompt": prompt,
                    "style": style
                }

                # 保存到缓存
                if use_cache:
                    self._save_to_cache(cache_key, result_dict)

                return result_dict
            else:
                return {
                    "success": False,
                    "error": "生成失败",
                    "raw": result
                }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def generate_for_article(
        self,
        title: str,
        content: str,
        style: str = "photography",
        use_cache: bool = True
    ) -> Dict:
        """
        为文章生成封面图

        Args:
            title: 文章标题
            content: 文章内容
            style: 图片风格
            use_cache: 是否使用缓存

        Returns:
            生成结果
        """
        # 提取关键词
        keywords = self._extract_keywords(title, content)

        # 生成prompt
        prompt = self._build_prompt(title, keywords, style)

        # 生成图片
        return self.generate(prompt, style=style, use_cache=use_cache)

    def _extract_keywords(self, title: str, content: str) -> list:
        """提取关键词"""
        # 简单实现：从标题和前100字中提取
        text = title + " " + content[:100]

        # 关键词列表（可以根据需要扩展）
        keywords = []

        # 技术类关键词
        tech_keywords = [
            "AI", "人工智能", "机器学习", "深度学习",
            "Python", "JavaScript", "编程", "代码",
            "算法", "数据", "云计算", "大数据",
            "自动化", "工作流", "API", "SDK"
        ]

        # 商业类关键词
        business_keywords = [
            "营销", "推广", "品牌", "增长",
            "用户", "产品", "服务", "体验",
            "效率", "成本", "收益", "ROI"
        ]

        # 创作类关键词
        creative_keywords = [
            "创作", "写作", "内容", "文章",
            "设计", "排版", "美工", "插画"
        ]

        # 提取匹配的关键词
        for keyword in tech_keywords + business_keywords + creative_keywords:
            if keyword in text:
                keywords.append(keyword)

        # 如果没有关键词，使用默认
        if not keywords:
            keywords = ["科技", "创新", "未来"]

        return keywords[:3]  # 最多3个关键词

    def _build_prompt(self, title: str, keywords: list, style: str) -> str:
        """构建prompt"""
        # 根据风格选择prompt模板
        if style == "photography":
            prompt = f"Professional photography, {title}, "
            prompt += ", ".join(keywords)
            prompt += ", high quality, 8K, detailed, sharp focus"
        elif style == "illustration":
            prompt = f"Modern illustration, {title}, "
            prompt += ", ".join(keywords)
            prompt += ", flat design, vector art, clean lines, vibrant colors"
        elif style == "3d":
            prompt = f"3D render, {title}, "
            prompt += ", ".join(keywords)
            prompt += ", isometric, octane render, soft lighting, high detail"
        else:
            prompt = f"{title}, "
            prompt += ", ".join(keywords)
            prompt += ", high quality, professional"

        return prompt

    def _get_cache_key(self, prompt: str, style: str, size: str) -> str:
        """生成缓存key"""
        content = f"{prompt}_{style}_{size}"
        return hashlib.md5(content.encode()).hexdigest()

    def _load_from_cache(self, cache_key: str) -> Optional[Dict]:
        """从缓存加载"""
        cache_file = os.path.join(self.cache_dir, f"{cache_key}.json")

        if os.path.exists(cache_file):
            import json
            with open(cache_file, 'r', encoding='utf-8') as f:
                return json.load(f)

        return None

    def _save_to_cache(self, cache_key: str, result: Dict):
        """保存到缓存"""
        cache_file = os.path.join(self.cache_dir, f"{cache_key}.json")

        import json
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)


def generate_article_cover(
    title: str,
    content: str,
    style: str = "photography",
    api_key: Optional[str] = None,
    use_cache: bool = True
) -> Dict:
    """
    快捷函数：为文章生成封面图

    Args:
        title: 文章标题
        content: 文章内容
        style: 图片风格
        api_key: 阿里云API Key
        use_cache: 是否使用缓存

    Returns:
        生成结果

    Example:
        result = generate_article_cover(
            title="2026年AI工具趋势",
            content="随着AI技术的快速发展...",
            style="photography"
        )

        if result["success"]:
            print(f"✅ 生成成功！图片URL: {result['images'][0]}")
        else:
            print(f"❌ 生成失败：{result['error']}")
    """
    generator = AliWanxiangGenerator(api_key)
    return generator.generate_for_article(title, content, style, use_cache)


def generate_custom_image(
    prompt: str,
    style: str = "photography",
    api_key: Optional[str] = None,
    use_cache: bool = True
) -> Dict:
    """
    快捷函数：自定义生成图片

    Args:
        prompt: 图片描述
        style: 图片风格
        api_key: 阿里云API Key
        use_cache: 是否使用缓存

    Returns:
        生成结果

    Example:
        result = generate_custom_image(
            prompt="Professional workspace with laptop and coffee",
            style="photography"
        )
    """
    generator = AliWanxiangGenerator(api_key)
    return generator.generate(prompt, style=style, use_cache=use_cache)
