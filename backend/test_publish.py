"""
一键发布API测试
"""

import asyncio
import httpx
from publish import app
from pydantic import BaseModel


class TestPublishTarget(BaseModel):
    platform: str
    account_id: str
    title: str
    content: str
    images: list = []
    tags: list = []


async def test_publish_api():
    """测试发布API"""

    print("="*60)
    print("一键发布API测试")
    print("="*60)

    base_url = "http://localhost:8000"

    # 测试1: 获取平台列表
    print("\n测试1: 获取平台列表")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{base_url}/api/v1/platforms")
            data = response.json()
            print(f"✅ 成功: {len(data['data'])} 个平台")
            for platform in data['data']:
                print(f"   - {platform['name']}: {platform['supports']}")
    except Exception as e:
        print(f"❌ 失败: {e}")

    # 测试2: 获取账号列表
    print("\n测试2: 获取账号列表")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{base_url}/api/v1/accounts")
            data = response.json()
            print(f"✅ 成功")
            for platform, accounts in data['data'].items():
                print(f"   - {platform}: {len(accounts)} 个账号")
    except Exception as e:
        print(f"❌ 失败: {e}")

    # 测试3: 发布到公众号（模拟）
    print("\n测试3: 发布到公众号")
    try:
        target = TestPublishTarget(
            platform="wechat",
            account_id="account_1",
            title="测试文章标题",
            content="这是一篇测试文章的内容。",
            images=[],
            tags=["测试"]
        )

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{base_url}/api/v1/publish/wechat",
                json=target.dict(),
                timeout=30
            )
            data = response.json()
            if data.get('success'):
                print(f"✅ 成功")
                print(f"   平台: {data['data']['platform']}")
                print(f"   状态: {data['data']['status']}")
                print(f"   消息: {data['data']['message']}")
                if data['data'].get('url'):
                    print(f"   URL: {data['data']['url']}")
            else:
                print(f"❌ 失败: {data}")
    except Exception as e:
        print(f"❌ 失败: {e}")

    # 测试4: 批量发布（模拟）
    print("\n测试4: 批量发布到多个平台")
    try:
        targets = [
            TestPublishTarget(
                platform="wechat",
                account_id="account_1",
                title="测试文章",
                content="测试内容...",
                images=[],
                tags=[]
            ),
            TestPublishTarget(
                platform="weibo",
                account_id="account_1",
                title="测试微博",
                content="测试微博内容...",
                images=[],
                tags=[]
            ),
            TestPublishTarget(
                platform="toutiao",
                account_id="account_1",
                title="测试头条",
                content="测试头条内容...",
                images=[],
                tags=[]
            )
        ]

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{base_url}/api/v1/publish",
                json=[t.dict() for t in targets],
                timeout=60
            )
            data = response.json()
            if data.get('success'):
                print(f"✅ 成功")
                print(f"   总数: {data['summary']['total']}")
                print(f"   成功: {data['summary']['success']}")
                print(f"   失败: {data['summary']['failed']}")
                for result in data['data']:
                    print(f"   - {result['platform']}: {result['status']}")
            else:
                print(f"❌ 失败: {data}")
    except Exception as e:
        print(f"❌ 失败: {e}")

    print("\n" + "="*60)
    print("测试完成")
    print("="*60)


if __name__ == "__main__":
    print("\n提示：请先启动 publish.py 服务")
    print("命令: uvicorn publish:app --reload\n")

    input("按回车继续...")

    asyncio.run(test_publish_api())
