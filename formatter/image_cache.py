"""
本地图片缓存管理器
下载并本地存储生成的图片，避免重复下载
"""
import os
import requests
import hashlib
from typing import Optional, Dict
from pathlib import Path


class ImageCacheManager:
    """图片缓存管理器"""

    def __init__(self, cache_dir: str = "cache/images/downloads"):
        """
        初始化缓存管理器

        Args:
            cache_dir: 缓存目录
        """
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

        # 创建索引文件
        self.index_file = self.cache_dir / "index.json"

    def _get_cache_key(self, url: str) -> str:
        """生成缓存key"""
        return hashlib.md5(url.encode()).hexdigest()

    def _load_index(self) -> Dict:
        """加载索引"""
        if self.index_file.exists():
            import json
            with open(self.index_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}

    def _save_index(self, index: Dict):
        """保存索引"""
        import json
        with open(self.index_file, 'w', encoding='utf-8') as f:
            json.dump(index, f, ensure_ascii=False, indent=2)

    def download_image(
        self,
        url: str,
        filename: Optional[str] = None,
        force_redownload: bool = False
    ) -> Dict:
        """
        下载图片

        Args:
            url: 图片URL
            filename: 文件名（可选）
            force_redownload: 是否强制重新下载

        Returns:
            {
                "success": bool,
                "local_path": str,
                "url": str,
                "size": int,
                "cached": bool
            }
        """
        try:
            cache_key = self._get_cache_key(url)
            index = self._load_index()

            # 检查是否已缓存
            if not force_redownload and cache_key in index:
                local_path = self.cache_dir / index[cache_key]["filename"]
                if local_path.exists():
                    return {
                        "success": True,
                        "local_path": str(local_path),
                        "url": url,
                        "size": local_path.stat().st_size,
                        "cached": True
                    }

            # 下载图片
            response = requests.get(url, timeout=30)
            response.raise_for_status()

            # 确定文件名
            if filename:
                # 保留扩展名
                ext = Path(filename).suffix
                if not ext:
                    # 从Content-Type推断
                    content_type = response.headers.get('Content-Type', '')
                    if 'jpeg' in content_type or 'jpg' in content_type:
                        ext = '.jpg'
                    elif 'png' in content_type:
                        ext = '.png'
                    elif 'webp' in content_type:
                        ext = '.webp'
                    else:
                        ext = '.jpg'
            else:
                # 默认使用jpg
                ext = '.jpg'

            filename = f"{cache_key}{ext}"
            local_path = self.cache_dir / filename

            # 保存图片
            with open(local_path, 'wb') as f:
                f.write(response.content)

            # 更新索引
            index[cache_key] = {
                "filename": filename,
                "url": url,
                "size": local_path.stat().st_size,
                "downloaded_at": int(local_path.stat().st_mtime)
            }
            self._save_index(index)

            return {
                "success": True,
                "local_path": str(local_path),
                "url": url,
                "size": local_path.stat().st_size,
                "cached": False
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "url": url
            }

    def download_images(
        self,
        urls: list,
        force_redownload: bool = False
    ) -> Dict:
        """
        批量下载图片

        Args:
            urls: 图片URL列表
            force_redownload: 是否强制重新下载

        Returns:
            {
                "success": int,
                "failed": int,
                "results": [...]
            }
        """
        results = []
        success = 0
        failed = 0

        for url in urls:
            result = self.download_image(url, force_redownload=force_redownload)
            results.append(result)

            if result["success"]:
                success += 1
            else:
                failed += 1

        return {
            "success": success,
            "failed": failed,
            "results": results
        }

    def get_local_path(self, url: str) -> Optional[str]:
        """
        获取本地路径

        Args:
            url: 图片URL

        Returns:
            本地路径（如果已缓存）
        """
        cache_key = self._get_cache_key(url)
        index = self._load_index()

        if cache_key in index:
            filename = index[cache_key]["filename"]
            local_path = self.cache_dir / filename

            if local_path.exists():
                return str(local_path)

        return None

    def clear_cache(self):
        """清空缓存"""
        import shutil

        # 删除所有图片文件（保留index.json）
        for file in self.cache_dir.glob("*"):
            if file.is_file() and file.name != "index.json":
                file.unlink()

        # 清空索引
        self._save_index({})

    def get_cache_stats(self) -> Dict:
        """获取缓存统计"""
        index = self._load_index()

        total_files = len(index)
        total_size = sum(item["size"] for item in index.values())

        # 统计文件类型
        file_types = {}
        for item in index.values():
            ext = Path(item["filename"]).suffix
            file_types[ext] = file_types.get(ext, 0) + 1

        return {
            "total_files": total_files,
            "total_size": total_size,
            "total_size_mb": round(total_size / 1024 / 1024, 2),
            "file_types": file_types,
            "cache_dir": str(self.cache_dir)
        }


def download_image(url: str, cache_dir: str = "cache/images/downloads") -> Dict:
    """
    快捷函数：下载图片

    Args:
        url: 图片URL
        cache_dir: 缓存目录

    Returns:
        下载结果
    """
    manager = ImageCacheManager(cache_dir)
    return manager.download_image(url)


def download_images(urls: list, cache_dir: str = "cache/images/downloads") -> Dict:
    """
    快捷函数：批量下载图片

    Args:
        urls: 图片URL列表
        cache_dir: 缓存目录

    Returns:
        下载结果
    """
    manager = ImageCacheManager(cache_dir)
    return manager.download_images(urls)
