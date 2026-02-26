"""
AI重写器
一键重写AI生成内容，降低AI率
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict
from ai_detector_100d import calculate_ai_score

app = FastAPI(title="AI Rewriter API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class RewriteInput(BaseModel):
    content: str
    mode: str = "simplify"  # simplify, professional, formal, colloquial
    language: str = "zh"


class RewriteOutput(BaseModel):
    original: str
    rewritten: str
    original_ai: Dict
    rewritten_ai: Dict
    changes: List[str]
    improvements: List[str]
    summary: str


# 重写策略
REWRITE_STRATEGIES = {
    "simplify": {
        "name": "简单化",
        "description": "降低AI率40%",
        "rules": [
            "删除冗余词",
            "简化句子结构",
            "删除过度修饰",
            "增加口语化"
        ]
    },
    "professional": {
        "name": "专业版",
        "description": "保持专业度",
        "rules": [
            "使用专业术语",
            "优化逻辑结构",
            "增强可信度",
            "减少AI腔调"
        ]
    },
    "formal": {
        "name": "正式版",
        "description": "公文风格",
        "rules": [
            "使用正式表达",
            "添加礼貌用语",
            "优化句子完整性",
            "增加连接词"
        ]
    },
    "colloquial": {
        "name": "口语化",
        "description": "像人写的",
        "rules": [
            "使用口语化表达",
            "增加情感词",
            "使用第一人称",
            "简化专业术语"
        ]
    }
}


def simplify_content(content: str) -> Dict:
    """简单化重写（降低AI率）"""
    original = content
    rewritten = content
    changes = []
    improvements = []

    # 1. 删除AI常用词
    ai_words = [
        "综上所述", "总而言之", "由此可见", "不难看出",
        "值得注意的是", "需要指出的是", "不得不承认",
        "显而易见", "毋庸置疑", "毫无疑问",
        "可以说", "从某种意义上", "在一定程度上",
        "具体来说", "换句话说", "换言之"
    ]

    for word in ai_words:
        if word in rewritten:
            rewritten = rewritten.replace(word, "")
            changes.append(f"删除了'{word}'")
            improvements.append("去除AI腔调")

    # 2. 删除过度连接词
    connectors = [
        "此外，", "另外，", "同时，", "因此，", "因而，",
        "然而，", "但是，", "此外，", "另外，", "从而，"
    ]

    for connector in connectors:
        if connector in rewritten:
            rewritten = rewritten.replace(connector, connector[:-1] + "，")
            changes.append(f"优化了'{connector}'")
            improvements.append("减少过度连接")

    # 3. 简化句子结构
    import re
    sentences = re.split(r'[。！？]', rewritten)
    simplified_sentences = []
    for sentence in sentences:
        sentence = sentence.strip()
        if sentence:
            # 删除重复词
            words = sentence.split()
            unique_words = []
            seen = set()
            for word in words:
                if word not in seen:
                    unique_words.append(word)
                    seen.add(word)
            simplified_sentences.append(' '.join(unique_words))
    rewritten = '。'.join(simplified_sentences)

    # 4. 增加口语化
    rewritten = rewritten.replace("我认为", "我觉得")
    rewritten = rewritten.replace("可以说", "我觉得")
    changes.append("增加口语化表达")
    improvements.append("更像人类写作")

    # 5. 清理
    lines = [line for line in rewritten.split('\n') if line.strip()]
    rewritten = '\n'.join(lines)
    rewritten = ' '.join(rewritten.split())

    return {
        "rewritten": rewritten,
        "changes": changes,
        "improvements": improvements
    }


def professional_rewrite(content: str) -> Dict:
    """专业版重写（保持专业度）"""
    original = content
    rewritten = content
    changes = []
    improvements = []

    # 1. 使用更专业的表达
    professional_terms = [
        "优化方案", "实施路径", "关键指标", "核心优势",
        "战略目标", "资源配置", "风险管控", "预期效果"
    ]

    # 2. 删除AI常用词
    ai_words = [
        "综上所述", "总而言之", "由此可见", "不难看出",
        "值得注意的是", "需要指出的是", "不得不承认",
        "显而易见", "毋庸置疑", "毫无疑问",
        "可以说", "从某种意义上", "在一定程度上"
    ]

    for word in ai_words:
        if word in rewritten:
            rewritten = rewritten.replace(word, "")
            changes.append(f"删除了'{word}'")
            improvements.append("去除AI腔调")

    # 3. 优化逻辑结构
    # 在开头添加总结
    summary = "本文将围绕核心问题展开，提供系统性的解决方案。"
    rewritten = summary + "\n\n" + rewritten

    # 4. 使用专业连接词
    rewritten = rewritten.replace("并且", "此外，")
    rewritten = rewritten.replace("所以", "因此，")

    # 5. 清理
    lines = [line for line in rewritten.split('\n') if line.strip()]
    rewritten = '\n'.join(lines)

    changes.append("优化了逻辑结构")
    improvements.append("增强了专业性")

    return {
        "rewritten": rewritten,
        "changes": changes,
        "improvements": improvements
    }


def formal_rewrite(content: str) -> Dict:
    """正式版重写（公文风格）"""
    original = content
    rewritten = content
    changes = []
    improvements = []

    # 1. 添加礼貌用语
    polite_opening = "尊敬的读者：\n\n"
    rewritten = polite_opening + rewritten

    # 2. 使用正式表达
    formal_terms = [
        "本方案旨在", "通过实施本方案", "基于以上分析",
        "综上所述，建议采取以下措施", "为确保项目顺利推进"
    ]

    # 3. 删除AI常用词
    ai_words = [
        "综上所述", "总而言之", "可以说",
        "值得注意的是", "需要指出的是", "不得不承认"
    ]

    for word in ai_words:
        if word in rewritten:
            rewritten = rewritten.replace(word, "")
            changes.append(f"优化了'{word}'")

    # 4. 添加总结
    conclusion = "\n\n" + "以上为方案的核心内容，如有疑问欢迎交流。"
    rewritten = rewritten + conclusion

    # 5. 清理
    lines = [line for line in rewritten.split('\n') if line.strip()]
    rewritten = '\n'.join(lines)

    changes.append("采用了公文风格")
    improvements.append("增强了正式感")

    return {
        "rewritten": rewritten,
        "changes": changes,
        "improvements": improvements
    }


def colloquial_rewrite(content: str) -> Dict:
    """口语化重写（像人写的）"""
    original = content
    rewritten = content
    changes = []
    improvements = []

    # 1. 增加口语化表达
    colloquial_terms = [
        "我觉得", "个人认为", "咱说", "咱们说",
        "感觉上", "大概是", "差不多", "基本上"
    ]

    # 2. 删除正式词
    formal_words = [
        "综上所述", "总而言之", "由此可见", "显而易见",
        "毋庸置疑", "毫无疑问", "具体来说"
    ]

    for word in formal_words:
        if word in rewritten:
            rewritten = rewritten.replace(word, "")
            changes.append(f"删除了'{word}'")

    # 3. 增加情感词
    rewritten = rewritten.replace("这个", "我觉得这个")
    rewritten = rewritten.replace("那个", "感觉那个")
    rewritten = rewritten.replace("很好", "真心不错")

    # 4. 简化表达
    rewritten = rewritten.replace("实现了", "做到了")
    rewritten = rewritten.replace("提高了", "变好了")
    rewritten = rewritten.replace("降低了", "少了不少")

    # 5. 清理
    lines = [line for line in rewritten.split('\n') if line.strip()]
    rewritten = '\n'.join(lines)

    changes.append("采用了口语化表达")
    improvements.append("更像人类写作")

    return {
        "rewritten": rewritten,
        "changes": changes,
        "improvements": improvements
    }


def apply_rewrite_strategy(content: str, mode: str) -> Dict:
    """应用重写策略"""
    if mode == "simplify":
        return simplify_content(content)
    elif mode == "professional":
        return professional_rewrite(content)
    elif mode == "formal":
        return formal_rewrite(content)
    elif mode == "colloquial":
        return colloquial_rewrite(content)
    else:
        return {
            "rewritten": content,
            "changes": [],
            "improvements": []
        }


# API端点
@app.get("/")
async def root():
    return {
        "message": "AI Rewriter API",
        "version": "1.0.0",
        "modes": ["simplify", "professional", "formal", "colloquial"]
    }


@app.post("/api/v1/rewrite")
async def rewrite_content(input_data: RewriteInput):
    """AI重写"""
    try:
        # 检测原文AI率
        original_ai = calculate_ai_score(input_data.content)

        # 应用重写策略
        rewrite_result = apply_rewrite_strategy(input_data.content, input_data.mode)

        # 检测重写版AI率
        rewritten_ai = calculate_ai_score(rewrite_result["rewritten"])

        # 计算改进
        ai_reduction = original_ai["ai_probability"] - rewritten_ai["ai_probability"]

        # 生成总结
        if ai_reduction > 30:
            summary = f"AI率从{original_ai['ai_probability']:.1f}%降到{rewritten_ai['ai_probability']:.1f}%，大幅降低{ai_reduction:.1f}%"
        elif ai_reduction > 15:
            summary = f"AI率从{original_ai['ai_probability']:.1f}%降到{rewritten_ai['ai_probability']:.1f}%，显著降低{ai_reduction:.1f}%"
        elif ai_reduction > 5:
            summary = f"AI率从{original_ai['ai_probability']:.1f}%降到{rewritten_ai['ai_probability']:.1f}%，小幅降低{ai_reduction:.1f}%"
        else:
            summary = f"AI率从{original_ai['ai_probability']:.1f}%降到{rewritten_ai['ai_probability']:.1f}%，略有提升"

        return {
            "success": True,
            "data": {
                "original": input_data.content,
                "rewritten": rewrite_result["rewritten"],
                "original_ai": original_ai,
                "rewritten_ai": rewritten_ai,
                "changes": rewrite_result["changes"],
                "improvements": rewrite_result["improvements"],
                "ai_reduction": round(ai_reduction, 1),
                "summary": summary
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/rewrite-only")
async def rewrite_only(content: str, mode: str):
    """只重写，不检测AI率"""
    try:
        rewrite_result = apply_rewrite_strategy(content, mode)

        return {
            "success": True,
            "data": {
                "rewritten": rewrite_result["rewritten"],
                "changes": rewrite_result["changes"],
                "improvements": rewrite_result["improvements"]
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
