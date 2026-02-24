"""
HumanWriter Backend - 内容质量检测
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import re
from textblob import TextBlob

app = FastAPI(title="Content Quality API")

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
    platform: str = "general"  # wechat, zhihu, xiaohongshu, twitter


class QualityScore(BaseModel):
    overall: float  # 0-100
    readability: float
    engagement: float
    ai_detection: float


class QualityIssue(BaseModel):
    type: str  # grammar, style, engagement, ai_detection
    severity: str  # high, medium, low
    message: str
    suggestion: str


class QualityReport(BaseModel):
    score: QualityScore
    issues: List[QualityIssue]
    summary: str


def detect_ai_patterns(content: str) -> List[dict]:
    """检测AI写作痕迹"""
    ai_patterns = [
        "综上所述",
        "值得注意的是",
        "显而易见",
        "可以说",
        "总而言之",
        "由此可见",
        "不难看出",
    ]

    issues = []
    for pattern in ai_patterns:
        if pattern in content:
            issues.append({
                "type": "ai_detection",
                "severity": "medium",
                "message": f"发现AI常用词：'{pattern}'",
                "suggestion": f"建议删除'{pattern}'，用更自然的表达"
            })

    return issues


def check_readability(content: str) -> dict:
    """检查可读性"""
    blob = TextBlob(content)

    # 句子数量
    sentences = len(blob.sentences)
    if sentences == 0:
        sentences = 1

    # 平均句子长度
    words = len(blob.words)
    avg_sentence_length = words / sentences

    # 可读性评分
    readability_score = 100 - (avg_sentence_length - 15) * 2
    readability_score = max(0, min(100, readability_score))

    issues = []

    # 句子过长
    if avg_sentence_length > 30:
        issues.append({
            "type": "readability",
            "severity": "high",
            "message": f"句子过长（平均{avg_sentence_length:.1f}词）",
            "suggestion": "建议将长句子拆分成短句"
        })

    # 段落过长
    paragraphs = content.split('\n\n')
    if len(paragraphs) > 0 and len(max(paragraphs, key=len)) > 300:
        issues.append({
            "type": "readability",
            "severity": "medium",
            "message": "段落过长",
            "suggestion": "建议将长段落拆分成多个短段落"
        })

    return {"score": readability_score, "issues": issues}


def check_engagement(content: str, platform: str) -> dict:
    """检查互动性"""
    issues = []

    # 检查提问
    if '?' not in content:
        issues.append({
            "type": "engagement",
            "severity": "low",
            "message": "没有提问",
            "suggestion": "建议在结尾添加问题，引导读者互动"
        })

    # 检查emoji（小红书）
    if platform == "xiaohongshu":
        emojis = re.findall(r'[\U00010000-\U0010ffff]', content)
        if len(emojis) < 3:
            issues.append({
                "type": "engagement",
                "severity": "medium",
                "message": "emoji太少",
                "suggestion": "建议添加3-5个emoji，增加视觉吸引力"
            })

    # 检查数字/数据
    if not re.search(r'\d+', content):
        issues.append({
            "type": "engagement",
            "severity": "low",
            "message": "没有数字/数据",
            "suggestion": "建议添加具体数据，增加可信度"
        })

    # 互动性评分
    engagement_score = 100 - len(issues) * 15
    engagement_score = max(0, min(100, engagement_score))

    return {"score": engagement_score, "issues": issues}


def check_style(content: str, platform: str) -> dict:
    """检查风格"""
    issues = []

    # 检查重复词
    words = content.split()
    word_counts = {}
    for word in words:
        if len(word) > 3:
            word_counts[word] = word_counts.get(word, 0) + 1

    for word, count in word_counts.items():
        if count > 5:
            issues.append({
                "type": "style",
                "severity": "low",
                "message": f"词语重复：'{word}'出现{count}次",
                "suggestion": f"建议用同义词替换'{word}'"
            })

    # 公众号风格
    if platform == "wechat":
        # 检查段落间距
        if '\n\n' not in content:
            issues.append({
                "type": "style",
                "severity": "medium",
                "message": "缺少段落间距",
                "suggestion": "建议添加空行，提高阅读体验"
            })

    # 知乎风格
    if platform == "zhihu":
        # 检查是否有标题
        if not re.search(r'^#', content, re.MULTILINE):
            issues.append({
                "type": "style",
                "severity": "low",
                "message": "缺少标题",
                "suggestion": "建议添加#标题，符合知乎格式"
            })

    return {"issues": issues}


@app.post("/api/v1/quality-check")
async def quality_check(input_data: ContentInput):
    """内容质量检测"""

    try:
        # 检测AI痕迹
        ai_issues = detect_ai_patterns(input_data.content)

        # 检查可读性
        readability_result = check_readability(input_data.content)

        # 检查互动性
        engagement_result = check_engagement(input_data.content, input_data.platform)

        # 检查风格
        style_result = check_style(input_data.content, input_data.platform)

        # 汇总问题
        all_issues = (
            ai_issues +
            readability_result["issues"] +
            engagement_result["issues"] +
            style_result["issues"]
        )

        # 计算总分
        overall_score = (
            readability_result["score"] * 0.4 +
            engagement_result["score"] * 0.3 +
            (100 - len(ai_issues) * 10) * 0.3
        )
        overall_score = max(0, min(100, overall_score))

        # 生成总结
        if overall_score >= 80:
            summary = "内容质量优秀，可以直接发布"
        elif overall_score >= 60:
            summary = "内容质量良好，建议优化后发布"
        else:
            summary = "内容质量一般，建议大幅优化"

        return {
            "success": True,
            "data": {
                "score": {
                    "overall": round(overall_score, 1),
                    "readability": round(readability_result["score"], 1),
                    "engagement": round(engagement_result["score"], 1),
                    "ai_detection": max(0, 100 - len(ai_issues) * 10)
                },
                "issues": all_issues,
                "summary": summary
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
async def root():
    return {"message": "Content Quality API", "version": "1.0.0"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
