"""
AI标题生成器
根据内容自动生成爆款标题
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import re

app = FastAPI(title="AI Title Generator API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ContentInput(BaseModel):
    content: str
    count: int = 5
    style: str = "clickbait"  # clickbait, professional, emotional, question


class TitleOutput(BaseModel):
    original: str
    titles: List[dict]
    summary: str


# 标题模板
TITLE_TEMPLATES = {
    "clickbait": [
        "震惊！{}，99%的人都没注意",
        "{}背后的真相，看完沉默了",
        "{}被低估了！这可能是...",
        "{}！专家终于说出了真相",
        "别再{}了，试试这个方法",
        "{}，原来这么简单？",
        "{}：你做对了，但不知道为什么",
        "99%的人都不知道{}的秘密",
        "{}！这个发现颠覆认知",
    ],
    "professional": [
        "深度解析：{}",
        "{}：完整指南与最佳实践",
        "如何{}：专家视角",
        "2026年{}：趋势与策略",
        "打破{}：创新方法与案例分析",
        "{}：从入门到精通",
        "高效{}：实用技巧与工具",
    ],
    "emotional": [
        "太心酸了！{}，看完想哭",
        "暖哭了！{}，这就是我想要的",
        "泪目！{}，终于有人懂我了",
        "{}！这种感觉太真实了",
        "{}！让我想起了那些年",
        "{}！终于找到同频的人了",
    ],
    "question": [
        "{}？看完你就懂了",
        "{}？真相令人意外",
        "{}？专家是这样解释的",
        "{}？可能和你想的不一样",
        "{}？这可能改变你的想法",
    ]
}


# 关键词提取
def extract_keywords(content: str) -> List[str]:
    """提取关键词"""
    # 简单提取：名词和形容词
    words = re.findall(r'[\u4e00-\u9fa5]{2,4}', content)

    # 过滤停用词
    stopwords = ['这是', '那个', '这个', '然后', '因为', '所以', '但是']
    keywords = [w for w in words if w not in stopwords and len(w) >= 2]

    return list(set(keywords))[:10]


# 生成标题
def generate_titles(content: str, count: int, style: str) -> List[dict]:
    """生成标题"""
    keywords = extract_keywords(content)

    # 获取内容摘要（前100字）
    summary = content[:100]

    # 根据风格生成
    if style == "clickbait":
        templates = TITLE_TEMPLATES["clickbait"]
        titles = []
        for i in range(count):
            template = templates[i % len(templates)]
            if keywords:
                keyword = keywords[i % len(keywords)]
                title = template.replace("{}", keyword)
            else:
                title = template.replace("{}", summary)
            titles.append({
                "title": title,
                "style": "clickbait",
                "score": 90
            })

    elif style == "professional":
        templates = TITLE_TEMPLATES["professional"]
        titles = []
        for i in range(count):
            template = templates[i % len(templates)]
            if keywords:
                keyword = keywords[i % len(keywords)]
                title = template.format(keyword)
            else:
                title = template.format(summary[:20])
            titles.append({
                "title": title,
                "style": "professional",
                "score": 85
            })

    elif style == "emotional":
        templates = TITLE_TEMPLATES["emotional"]
        titles = []
        for i in range(count):
            template = templates[i % len(templates)]
            if keywords:
                keyword = keywords[i % len(keywords)]
                title = template.replace("{}", keyword)
            else:
                title = template.replace("{}", summary[:10])
            titles.append({
                "title": title,
                "style": "emotional",
                "score": 80
            })

    elif style == "question":
        templates = TITLE_TEMPLATES["question"]
        titles = []
        for i in range(count):
            template = templates[i % len(templates)]
            if keywords:
                keyword = keywords[i % len(keywords)]
                title = template.replace("{}", keyword)
            else:
                title = template.replace("{}", summary[:15])
            titles.append({
                "title": title,
                "style": "question",
                "score": 75
            })

    return titles


# API端点
@app.get("/")
async def root():
    return {
        "message": "AI Title Generator API",
        "version": "1.0.0",
        "styles": ["clickbait", "professional", "emotional", "question"]
    }


@app.post("/api/v1/generate-titles")
async def generate_titles_api(input_data: ContentInput):
    """生成标题"""
    try:
        # 生成标题
        titles = generate_titles(input_data.content, input_data.count, input_data.style)

        # 排序
        titles.sort(key=lambda x: x['score'], reverse=True)

        return {
            "success": True,
            "data": {
                "original": input_data.content[:100] + "..." if len(input_data.content) > 100 else input_data.content,
                "titles": titles,
                "summary": f"生成了{len(titles)}个标题，风格：{input_data.style}"
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/trending-topics")
async def trending_topics(content: str):
    """生成热门话题标签"""
    try:
        keywords = extract_keywords(content)

        topics = []
        for keyword in keywords:
            topics.append({
                "topic": keyword,
                "volume": f"{(len(keyword) * 1000)}+",
                "growth": f"+{len(keyword) * 5}%",
                "trend": "rising"
            })

        return {
            "success": True,
            "data": {
                "topics": topics[:10],
                "summary": f"提取了{len(topics)}个热门话题"
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
