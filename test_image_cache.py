"""
测试脚本：测试图片缓存功能
"""
from formatter import ImageCacheManager, download_image, download_images


def test_single_download():
    """测试单个图片下载"""
    print("=== 测试单个图片下载 ===")

    # 使用公共图片URL（无需API）
    test_url = "https://via.placeholder.com/800x600/1890ff/ffffff?text=Test+Image"

    result = download_image(test_url)

    if result["success"]:
        print(f"✅ 下载成功！")
        print(f"  - URL: {result['url']}")
        print(f"  - 本地路径: {result['local_path']}")
        print(f"  - 大小: {result['size']} bytes")
        print(f"  - 来自缓存: {'是' if result['cached'] else '否'}")
        print()
    else:
        print(f"❌ 下载失败：{result.get('error')}")
        print()


def test_cache_hit():
    """测试缓存命中"""
    print("=== 测试缓存命中 ===")

    test_url = "https://via.placeholder.com/800x600/1890ff/ffffff?text=Test+Image"

    # 第一次下载
    print("第一次下载...")
    result1 = download_image(test_url)

    if result1["success"]:
        print(f"✅ 下载成功，来自缓存: {'是' if result1['cached'] else '否'}")

    # 第二次下载（应该命中缓存）
    print("\n第二次下载（相同URL）...")
    result2 = download_image(test_url)

    if result2["success"]:
        print(f"✅ 下载成功，来自缓存: {'是' if result2['cached'] else '否'}")

        if result2["cached"]:
            print(f"✅ 缓存命中！本地路径: {result2['local_path']}")

    print()


def test_batch_download():
    """测试批量下载"""
    print("=== 测试批量下载 ===")

    urls = [
        "https://via.placeholder.com/800x600/1890ff/ffffff?text=Image+1",
        "https://via.placeholder.com/800x600/52c41a/ffffff?text=Image+2",
        "https://via.placeholder.com/800x600/faad14/ffffff?text=Image+3",
    ]

    result = download_images(urls)

    print(f"✅ 批量下载完成！")
    print(f"  - 成功: {result['success']}")
    print(f"  - 失败: {result['failed']}")

    for i, item in enumerate(result["results"]):
        if item["success"]:
            print(f"  [{i+1}] ✅ {item['local_path']}")
        else:
            print(f"  [{i+1}] ❌ {item.get('error')}")

    print()


def test_cache_manager():
    """测试缓存管理器"""
    print("=== 测试缓存管理器 ===")

    manager = ImageCacheManager("cache/images/downloads")

    # 获取缓存统计
    stats = manager.get_cache_stats()

    print(f"✅ 缓存统计：")
    print(f"  - 总文件数: {stats['total_files']}")
    print(f"  - 总大小: {stats['total_size_mb']} MB")
    print(f"  - 文件类型: {stats['file_types']}")
    print(f"  - 缓存目录: {stats['cache_dir']}")
    print()


def test_get_local_path():
    """测试获取本地路径"""
    print("=== 测试获取本地路径 ===")

    manager = ImageCacheManager("cache/images/downloads")

    test_url = "https://via.placeholder.com/800x600/1890ff/ffffff?text=Test+Image"

    # 先下载
    download_image(test_url)

    # 查找本地路径
    local_path = manager.get_local_path(test_url)

    if local_path:
        print(f"✅ 找到本地路径: {local_path}")
    else:
        print(f"❌ 未找到本地路径")

    print()


def test_clear_cache():
    """测试清空缓存"""
    print("=== 测试清空缓存 ===")

    manager = ImageCacheManager("cache/images/downloads")

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


def test_with_generated_images():
    """测试与图片生成集成"""
    print("=== 测试与图片生成集成 ===")

    # 这里需要实际的图片生成结果
    # 模拟一个生成结果
    mock_result = {
        "success": True,
        "images": [
            "https://via.placeholder.com/1024x1024/1890ff/ffffff?text=Cover"
        ],
        "prompt": "Test prompt",
        "style": "photography"
    }

    if mock_result["success"]:
        # 下载生成的图片
        for url in mock_result["images"]:
            result = download_image(url)
            if result["success"]:
                print(f"✅ 已下载生成的图片: {result['local_path']}")

    print()


if __name__ == "__main__":
    print("🚀 开始测试图片缓存功能\n")

    test_single_download()
    test_cache_hit()
    test_batch_download()
    test_cache_manager()
    test_get_local_path()
    # test_clear_cache()  # 取消注释以测试清空缓存
    test_with_generated_images()

    print("🎉 所有测试完成！")
