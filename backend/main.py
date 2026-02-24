"""
HumanWriter Backend - 增强版
添加AI率检测功能
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import httpx
import os
from dotenv import load_dotenv

# 导入AI检测模块
from ai_detector import calculate_ai_score

load_dotenv()

app = FastAPI(
    title="HumanWriter API",
    description="多平台内容适配 + AI率检测",
    version="1.1.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 数据模型
class ArticleInput(BaseModel):
    title: str
    content: str
    style: Optional[str] = "professional"
    tone: Optional[str] = "neutral"


class AIDetectInput(BaseModel):
    content: str
    platform: Optional[str] = "general"


class HumanizedArticle(BaseModel):
    title: str
    content: str
    changes: List[str]


class PublishTarget(BaseModel):
    platform: str
    account_id: str
    scheduled_time: Optional[str] = None


class PublishRequest(BaseModel):
    article_id: str
    targets: List[PublishTarget]


@app.get("/")
async def root():
    return {
        "message": "HumanWriter API",
        "version": "1.1.0",
        "features": ["多平台适配", "AI率检测"]
    }


@app.post("/api/v1/ai-detect")
async def ai_detect(input_data: AIDetectInput):
    """
    AI率检测
    """
    try:
        result = calculate_ai_score(input_data.content)
        return {
            "success": True,
            "data": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/humanize")
async def humanize(article: ArticleInput):
    """
    去AI味
    """
    try:
        # 简化版去AI味
        changes = []
        content = article.content

        # 去除AI常用词
        ai_patterns = [
            "综上所述", "总而言之", "值得注意的是",
            "显而易见", "毋庸置疑", "可以说"
        ]

        for pattern in ai_patterns:
            if pattern in content:
                content = content.replace(pattern, "")
                changes.append(f"删除了 '{pattern}'")

        # 调整语气
        if article.tone == "warm":
            content = content.replace("因此", "所以")
            content = content.replace("然而", "但是")
            changes.append("调整为更温暖的语气")

        return {
            "success": True,
            "data": {
                "title": article.title,
                "content": content,
                "changes": changes
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/publish")
async def publish(request: PublishRequest):
    """
    发布到全平台
    """
    results = []

    for target in request.targets:
        results.append({
            "platform": target.platform,
            "status": "published",
            "url": f"https://example.com/{target.platform}/article/{request.article_id}"
        })

    return {
        "success": True,
        "data": results
    }


@app.get("/api/v1/platforms")
async def get_platforms():
    """
    获取支持的平台列表
    """
    return {
        "success": True,
        "data": [
            {"id": "twitter", "name": "Twitter", "available": True, "features": ["article", "scheduled"]},
            {"id": "zhihu", "name": "知乎", "available": False, "note": "暂无公开API"},
            {"id": "xiaohongshu", "name": "小红书", "available": False, "note": "暂无公开API"},
            {"id": "toutiao", "name": "头条", "available": True, "features": ["article", "scheduled"]},
            {"id": "baijiahao", "name": "百家号", "available": True, "features": ["article", "scheduled"]}
        ]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
