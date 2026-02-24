"""
一键发布API配置文件
存储各平台的API Token和账号信息
"""

import os
from typing import Dict, Optional
from pydantic import BaseSettings, Field


class PlatformConfig(BaseSettings):
    """平台配置"""

    # 公众号配置
    wechat_app_id: Optional[str] = Field(None, env="WECHAT_APP_ID")
    wechat_app_secret: Optional[str] = Field(None, env="WECHAT_APP_SECRET")
    wechat_access_token: Optional[str] = Field(None, env="WECHAT_ACCESS_TOKEN")

    # 微博配置
    weibo_app_key: Optional[str] = Field(None, env="WEIBO_APP_KEY")
    weibo_app_secret: Optional[str] = Field(None, env="WEIBO_APP_SECRET")
    weibo_access_token: Optional[str] = Field(None, env="WEIBO_ACCESS_TOKEN")

    # 头条配置
    toutiao_app_id: Optional[str] = Field(None, env="TOUTIAO_APP_ID")
    toutiao_app_secret: Optional[str] = Field(None, env="TOUTIAO_APP_SECRET")
    toutiao_access_token: Optional[str] = Field(None, env="TOUTIAO_ACCESS_TOKEN")

    # 知乎配置（爬虫方式）
    zhihu_account: Optional[str] = Field(None, env="ZHIHU_ACCOUNT")
    zhihu_password: Optional[str] = Field(None, env="ZHIHU_PASSWORD")
    zhihu_cookies: Optional[str] = Field(None, env="ZHIHU_COOKIES")

    # 小红书配置（爬虫方式）
    xiaohongshu_account: Optional[str] = Field(None, env="XIAOHONGSHU_ACCOUNT")
    xiaohongshu_password: Optional[str] = Field(None, env="XIAOHONGSHU_PASSWORD")
    xiaohongshu_cookies: Optional[str] = Field(None, env="XIAOHONGSHU_COOKIES")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


def get_platform_config() -> Dict[str, dict]:
    """获取所有平台配置"""
    config = PlatformConfig()

    return {
        "wechat": {
            "app_id": config.wechat_app_id,
            "app_secret": config.wechat_app_secret,
            "access_token": config.wechat_access_token,
            "configured": bool(config.wechat_app_id and config.wechat_app_secret)
        },
        "weibo": {
            "app_key": config.weibo_app_key,
            "app_secret": config.weibo_app_secret,
            "access_token": config.weibo_access_token,
            "configured": bool(config.weibo_app_key and config.weibo_app_secret)
        },
        "toutiao": {
            "app_id": config.toutiao_app_id,
            "app_secret": config.toutiao_app_secret,
            "access_token": config.toutiao_access_token,
            "configured": bool(config.toutiao_app_id and config.toutiao_app_secret)
        },
        "zhihu": {
            "account": config.zhihu_account,
            "password": config.zhihu_password,
            "cookies": config.zhihu_cookies,
            "configured": bool(config.zhihu_account and config.zhihu_password)
        },
        "xiaohongshu": {
            "account": config.xiaohongshu_account,
            "password": config.xiaohongshu_password,
            "cookies": config.xiaohongshu_cookies,
            "configured": bool(config.xiaohongshu_account and config.xiaohongshu_password)
        }
    }


# 示例环境变量文件
EXAMPLE_ENV = """
# 公众号配置
WECHAT_APP_ID=your_app_id
WECHAT_APP_SECRET=your_app_secret
WECHAT_ACCESS_TOKEN=your_access_token

# 微博配置
WEIBO_APP_KEY=your_app_key
WEIBO_APP_SECRET=your_app_secret
WEIBO_ACCESS_TOKEN=your_access_token

# 头条配置
TOUTIAO_APP_ID=your_app_id
TOUTIAO_APP_SECRET=your_app_secret
TOUTIAO_ACCESS_TOKEN=your_access_token

# 知乎配置（爬虫）
ZHIHU_ACCOUNT=your_zhihu_account
ZHIHU_PASSWORD=your_zhihu_password
ZHIHU_COOKIES=your_zhihu_cookies

# 小红书配置（爬虫）
XIAOHONGSHU_ACCOUNT=your_xiaohongshu_account
XIAOHONGSHU_PASSWORD=your_xiaohongshu_password
XIAOHONGSHU_COOKIES=your_xiaohongshu_cookies
"""


if __name__ == "__main__":
    print("="*60)
    print("一键发布API配置检查")
    print("="*60)

    configs = get_platform_config()

    for platform, config in configs.items():
        status = "✅ 已配置" if config["configured"] else "❌ 未配置"
        print(f"\n{platform.upper()}:")
        print(f"  状态: {status}")

        if config["configured"]:
            for key, value in config.items():
                if key != "configured" and value:
                    print(f"  {key}: {'*'*10}")

    print("\n" + "="*60)
    print("提示：")
    print("1. 复制示例环境变量到 .env 文件")
    print("2. 填写各平台的API Token或账号密码")
    print("3. 重启服务使配置生效")
    print("="*60)

    print("\n示例 .env 文件：")
    print(EXAMPLE_ENV)
