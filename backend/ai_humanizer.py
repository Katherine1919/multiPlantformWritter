"""
AI检测 + 去AI味一体工具
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict
from ai_detector_100d import calculate_ai_score

app = FastAPI(title="AI Detector & Humanizer API")

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
    mode: str = "detect_only"  # detect_only, humanize, both


class ContentOutput(BaseModel):
    original: str
    humanized: str
    ai_detection: Dict
    changes: List[str]
    summary: str


# 去AI味逻辑
def humanize_content(content: str) -> Dict:
    """
    去除AI写作痕迹，使内容更像人类

    返回：
    {
        "humanized": str,
        "changes": List[str]
    }
    """
    original = content
    humanized = content
    changes = []

    # 1. 删除AI常用词
    ai_words = [
        "综上所述", "总而言之", "由此可见", "不难看出",
        "值得注意的是", "需要指出的是", "不得不承认",
        "显而易见", "毋庸置疑", "毫无疑问",
        "可以说", "从某种意义上", "在一定程度上",
        "具体来说", "换句话说", "换言之",
        "总的来说", "总的说来", "整体而言",
        "从根本上", "本质上", "核心在于"
    ]

    for word in ai_words:
        if word in humanized:
            humanized = humanized.replace(word, "")
            changes.append(f"删除了 '{word}'")

    # 2. 删除AI句式
    ai_patterns = [
        r"可以说.*是",
        r"值得注意的是.*",
        r"由此可见.*",
        r"不难看出.*",
        r"不得不承认.*"
        r"总的来说.*",
        r"总而言之.*"
    ]

    for pattern in ai_patterns:
        import re
        matches = re.findall(pattern, humanized)
        for match in matches:
            # 尝试删除整个句子
            humanized = humanized.replace(match, "")
            changes.append(f"删除了AI句式: '{match}'")

    # 3. 删除过度连接词
    connectors = [
        "此外，", "另外，", "同时，", "因此，", "因而，",
        "然而，", "但是，", "此外，", "另外，", "从而，"
    ]

    for connector in connectors:
        if connector in humanized:
            humanized = humanized.replace(connector, connector[:-1] + "，")
            changes.append(f"优化了连接词: '{connector}'")

    # 4. 增加口语化表达
    humanized = humanized.replace("我认为", "我觉得")
    humanized = humanized.replace("可以说", "我觉得")

    # 5. 删除空行
    lines = [line for line in humanized.split('\n') if line.strip()]
    humanized = '\n'.join(lines)

    # 6. 清理多余空格
    humanized = ' '.join(humanized.split())

    return {
        "humanized": humanized,
        "changes": changes
    }


# API端点
@app.get("/")
async def root():
    return {
        "message": "AI Detector & Humanizer API",
        "version": "1.0.0",
        "features": [
            "AI率检测（100维度）",
            "自动去AI味",
            "对比显示",
            "优化建议"
        ]
    }


@app.post("/api/v1/detect-and-humanize")
async def detect_and_humanize(input_data: ContentInput):
    """
    AI检测 + 去AI味一体工具

    mode:
    - detect_only: 只检测AI率
    - humanize: 只去AI味
    - both: 检测 + 去AI味（推荐）
    """
    try:
        # 检测AI率
        ai_detection = calculate_ai_score(input_data.content)

        result = {
            "original": input_data.content,
            "humanized": "",
            "ai_detection": ai_detection,
            "changes": [],
            "summary": ""
        }

        # 去AI味
        if input_data.mode in ["humanize", "both"]:
            humanize_result = humanize_content(input_data.content)
            result["humanized"] = humanize_result["humanized"]
            result["changes"] = humanize_result["changes"]

            # 重新检测AI率
            new_detection = calculate_ai_score(result["humanized"])
            ai_reduction = ai_detection["ai_probability"] - new_detection["ai_probability"]

            result["summary"] = f"AI率从 {ai_detection['ai_probability']:.1f}% 降到 {new_detection['ai_probability']:.1f}%，降低了 {ai_reduction:.1f}%"
        else:
            result["humanized"] = input_data.content
            result["summary"] = ai_detection["summary"]

        return {
            "success": True,
            "data": result
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/detect-only")
async def detect_only(content: str):
    """只检测AI率"""
    ai_detection = calculate_ai_score(content)

    return {
        "success": True,
        "data": {
            "ai_detection": ai_detection
        }
    }


@app.post("/api/v1/humanize-only")
async def humanize_only(content: str):
    """只去AI味"""
    result = humanize_content(content)

    return {
        "success": True,
        "data": {
            "humanized": result["humanized"],
            "changes": result["changes"]
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
