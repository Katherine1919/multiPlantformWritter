#!/usr/bin/env python3
"""
本地图片缓存 - 快速示例
"""
import sys
sys.path.insert(0, '/home/admin/.openclaw/workspace/humanwriter')

from formatter import ImageCacheManager, download_image, download_images


def example_1_single_download():
    """示例1：单个图片下载"""
    print("=" * 60)
    print("示例1：单个图片下载")
    print("=" * 60)

    # 使用一个简单的测试图片URL
    test_url = "https://httpbin.org/image/png"

    result = download_image(test_url)

    if result["success"]:
        print(f"✅ 下载成功！")
        print(f"  URL: {result['url']}")
        print(f"  本地路径: {result['local_path']}")
        print(f"  大小: {result['size']} bytes")
        print(f"  来自缓存: {'是' if result['cached'] else '否'}")
    else:
        print(f"❌ 下载失败：{result.get('error')}")

    print()


def example_2_batch_download():
    """示例2：批量下载"""
    print("=" * 60)
    print("示例2：批量下载")
    print("=" * 60)

    # 使用多个测试图片URL
    urls = [
        "https://httpbin.org/image/png",
        "https://httpbin.org/image/jpeg",
        "https://httpbin.org/image/webp",
    ]

    result = download_images(urls)

    print(f"✅ 批量下载完成！")
    print(f"  成功: {result['success']}")
    print(f"  失败: {result['failed']}")

    for i, item in enumerate(result["results"]):
        if item["success"]:
            print(f"  [{i+1}] ✅ {item['local_path']}")
        else:
            print(f"  [{i+1}] ❌ {item.get('error')}")

    print()


def example_3_cache_stats():
    """示例3：查看缓存统计"""
    print("=" * 60)
    print("示例3：查看缓存统计")
    print("=" * 60)

    manager = ImageCacheManager()
    stats = manager.get_cache_stats()

    print(f"✅ 缓存统计：")
    print(f"  总文件数: {stats['total_files']}")
    print(f"  总大小: {stats['total_size_mb']} MB")
    print(f"  文件类型: {stats['file_types']}")
    print(f"  缓存目录: {stats['cache_dir']}")

    print()


def example_4_find_local_path():
    """示例4：查找本地路径"""
    print("=" * 60)
    print("示例4：查找本地路径")
    print("=" * 60)

    manager = ImageCacheManager()
    test_url = "https://httpbin.org/image/png"

    # 查找本地路径
    local_path = manager.get_local_path(test_url)

    if local_path:
        print(f"✅ 找到本地路径: {local_path}")
    else:
        print(f"❌ 未找到本地路径")

    print()


def example_5_clear_cache():
    """示例5：清空缓存"""
    print("=" * 60)
    print("示例5：清空缓存")
    print("=" * 60)

    manager = ImageCacheManager()

    # 获取清空前统计
    stats_before = manager.get_cache_stats()
    print(f"清空前: {stats_before['total_files']} 个文件")

    # 清空缓存
    manager.clear_cache()
    print("✅ 缓存已清空")

    # 获取清空后统计
    stats_after = manager.get_cache_stats()
    print(f"清空后: {stats_after['total_files']} 个文件")

    print()


def example_6_with_image_generation():
    """示例6：与图片生成集成"""
    print("=" * 60)
    print("示例6：与图片生成集成")
    print("=" * 60)

    from formatter import enhance_with_images

    markdown = """# 测试文章

这是一个测试文章，用于演示图片生成和缓存功能。"""

    # 生成图片（需要API Key）
    enhanced = enhance_with_images(
        markdown_content=markdown,
        style="photography",
        insert_cover=True,
        insert_section_images=False,
        max_images=1
    )

    if enhanced["success"]:
        print(f"✅ 生成了 {enhanced['count']} 张图片")

        # 下载到本地缓存
        cache_manager = ImageCacheManager()

        for img_info in enhanced["images"]:
            print(f"\n正在下载: {img_info['url']}")
            result = cache_manager.download_image(img_info["url"])

            if result["success"]:
                print(f"✅ 下载成功: {result['local_path']}")
                print(f"  大小: {result['size']} bytes")
                print(f"  来自缓存: {'是' if result['cached'] else '否'}")
            else:
                print(f"❌ 下载失败：{result.get('error')}")
    else:
        print(f"❌ 图片生成失败：{enhanced.get('error')}")
        print("  （可能需要配置 DASHSCOPE_API_KEY）")

    print()


if __name__ == "__main__":
    print("🚀 本地图片缓存 - 快速示例\n")

    # 运行示例
    example_1_single_download()
    example_2_batch_download()
    example_3_cache_stats()
    example_4_find_local_path()
    # example_5_clear_cache()  # 取消注释以测试清空缓存
    example_6_with_image_generation()

    print("🎉 所有示例运行完成！")
