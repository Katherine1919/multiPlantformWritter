"""
AI率检测模块
基于特征检测，判断文本的AI生成概率
"""

import re
from typing import List, Dict

# AI常用词库（中文）
AI_WORDS_CN = [
    "综上所述", "总而言之", "由此可见", "不难看出",
    "值得注意的是", "需要指出的是", "不得不承认",
    "显而易见", "毋庸置疑", "毫无疑问",
    "可以说", "从某种意义上", "在一定程度上",
    "值得注意的是", "此外", "另外", "同时",
    "具体来说", "换句话说", "换言之",
]

# AI常用句式
AI_PATTERNS = [
    r"可以说.*是",
    r"值得注意的是.*",
    r"由此可见.*",
    r"不难看出.*",
    r"不得不承认.*",
    r"可以说.*",
    r"需要注意的是.*",
    r"需要指出的是.*",
]

# AI写作特征
AI_FEATURES = {
    "perfect_structure": 0.15,  # 完美的段落结构
    "neutral_tone": 0.10,     # 中立的语气
    "repetitive_structure": 0.12,  # 重复的句式
    "formal_language": 0.13,    # 正式语言
    "lack_of_personal": 0.10,   # 缺少个人表达
    "predictable_ending": 0.12,  # 可预测的结尾
}


def detect_ai_words(content: str) -> Dict:
    """检测AI常用词"""
    ai_word_count = 0
    matched_words = []

    for word in AI_WORDS_CN:
        if word in content:
            ai_word_count += content.count(word)
            matched_words.append(word)

    word_density = ai_word_count / len(content) if content else 0
    ai_probability = min(word_density * 1000, 40)  # 最高贡献40%

    return {
        "count": ai_word_count,
        "words": matched_words,
        "density": round(word_density * 100, 2),
        "contribution": round(ai_probability, 1)
    }


def detect_ai_patterns(content: str) -> Dict:
    """检测AI常用句式"""
    pattern_count = 0
    matched_patterns = []

    for pattern in AI_PATTERNS:
        matches = re.findall(pattern, content)
        if matches:
            pattern_count += len(matches)
            matched_patterns.extend(matches)

    pattern_density = pattern_count / len(content.split('\n')) if content else 0
    ai_probability = min(pattern_density * 100, 30)  # 最高贡献30%

    return {
        "count": pattern_count,
        "patterns": matched_patterns,
        "density": round(pattern_density * 100, 2),
        "contribution": round(ai_probability, 1)
    }


def detect_structure_perfection(content: str) -> Dict:
    """检测完美的段落结构（AI特征）"""
    paragraphs = [p.strip() for p in content.split('\n') if p.strip()]

    if len(paragraphs) < 3:
        return {
            "perfect": False,
            "contribution": 0
        }

    # 检查段落长度是否均匀
    lengths = [len(p) for p in paragraphs]
    avg_length = sum(lengths) / len(lengths)
    variance = sum((l - avg_length) ** 2 for l in lengths) / len(lengths)

    # AI生成的通常段落长度比较均匀
    if variance < avg_length * 50:
        perfect = True
        contribution = AI_FEATURES["perfect_structure"] * 100
    else:
        perfect = False
        contribution = 0

    return {
        "perfect": perfect,
        "variance": round(variance, 2),
        "avg_length": round(avg_length, 1),
        "contribution": round(contribution, 1)
    }


def detect_neutral_tone(content: str) -> Dict:
    """检测中立语气（AI特征）"""
    # 情感词
    emotional_words = [
        "爱", "恨", "喜欢", "讨厌", "快乐", "悲伤",
        "开心", "难过", "激动", "愤怒", "惊喜",
        "失望", "兴奋", "紧张", "放松", "满意",
        "我感到", "我觉得", "我认为", "我喜欢", "我讨厌"
    ]

    emotional_count = sum(1 for word in emotional_words if word in content)
    total_chars = len(content)

    # AI写作通常情感词少
    emotional_density = emotional_count / total_chars if total_chars > 0 else 0

    if emotional_density < 0.001:
        contribution = AI_FEATURES["neutral_tone"] * 100
        neutral = True
    else:
        contribution = 0
        neutral = False

    return {
        "neutral": neutral,
        "emotional_count": emotional_count,
        "density": round(emotional_density * 1000, 2),
        "contribution": round(contribution, 1)
    }


def detect_repetitive_structure(content: str) -> Dict:
    """检测重复的句式结构"""
    sentences = [s.strip() for s in content.split('。') if s.strip()]

    if len(sentences) < 5:
        return {
            "repetitive": False,
            "contribution": 0
        }

    # 统计句子开头的重复
    starters = [s[:5] for s in sentences if len(s) >= 5]
    unique_starters = len(set(starters))

    # 如果有很多句子以相同的词开头
    repetitive = (unique_starters / len(starters)) < 0.7

    contribution = AI_FEATURES["repetitive_structure"] * 100 if repetitive else 0

    return {
        "repetitive": repetitive,
        "unique_ratio": round(unique_starters / len(starters), 2),
        "contribution": round(contribution, 1)
    }


def detect_formal_language(content: str) -> Dict:
    """检测正式语言（AI特征）"""
    formal_words = [
        "此外", "另外", "同时", "因此", "因而",
        "然而", "但是", "此外", "另外", "从而",
        "以及", "进而", "进而", "从而", "因此"
    ]

    formal_count = sum(1 for word in formal_words if word in content)
    total_words = len(content.split())

    # AI写作通常正式词多
    formal_density = formal_count / total_words if total_words > 0 else 0

    if formal_density > 0.05:
        contribution = AI_FEATURES["formal_language"] * 100
        formal = True
    else:
        contribution = 0
        formal = False

    return {
        "formal": formal,
        "count": formal_count,
        "density": round(formal_density * 100, 2),
        "contribution": round(contribution, 1)
    }


def detect_lack_of_personal(content: str) -> Dict:
    """检测缺少个人表达（AI特征）"""
    personal_words = [
        "我", "我的", "我们", "我们的", "我的观点",
        "我认为", "我觉得", "我喜欢", "我建议",
        "个人认为", "个人建议", "个人看法"
    ]

    personal_count = sum(1 for word in personal_words if word in content)
    total_chars = len(content)

    # AI写作通常少用"我"
    personal_density = personal_count / total_chars if total_chars > 0 else 0

    if personal_density < 0.002:
        contribution = AI_FEATURES["lack_of_personal"] * 100
        lack_personal = True
    else:
        contribution = 0
        lack_personal = False

    return {
        "lack_personal": lack_personal,
        "personal_count": personal_count,
        "density": round(personal_density * 1000, 2),
        "contribution": round(contribution, 1)
    }


def detect_predictable_ending(content: str) -> Dict:
    """检测可预测的结尾（AI特征）"""
    # 检查文章结尾
    last_paragraph = content.strip().split('\n')[-1]

    predictable_endings = [
        "总的来说",
        "综上所述",
        "总而言之",
        "综上所述",
        "最后，",
        "总之，",
    ]

    for ending in predictable_endings:
        if last_paragraph.startswith(ending):
            contribution = AI_FEATURES["predictable_ending"] * 100
            return {
                "predictable": True,
                "ending": ending,
                "contribution": round(contribution, 1)
            }

    return {
        "predictable": False,
        "contribution": 0
    }


def calculate_ai_score(content: str) -> Dict:
    """
    计算AI生成概率

    返回：
    {
        "ai_probability": 85.5,  # AI生成概率
        "human_probability": 14.5,  # 人类生成概率
        "confidence": "high",  # 置信度
        "details": {...}  # 详细分析
    }
    """
    # 各项检测结果
    ai_words_result = detect_ai_words(content)
    ai_patterns_result = detect_ai_patterns(content)
    structure_result = detect_structure_perfection(content)
    tone_result = detect_neutral_tone(content)
    repetitive_result = detect_repetitive_structure(content)
    formal_result = detect_formal_language(content)
    personal_result = detect_lack_of_personal(content)
    ending_result = detect_predictable_ending(content)

    # 计算总AI概率
    total_contribution = (
        ai_words_result["contribution"] +
        ai_patterns_result["contribution"] +
        structure_result["contribution"] +
        tone_result["contribution"] +
        repetitive_result["contribution"] +
        formal_result["contribution"] +
        personal_result["contribution"] +
        ending_result["contribution"]
    )

    # 基础AI概率（基于长度）
    base_probability = min(50, len(content) / 100)

    # 最终AI概率
    ai_probability = base_probability + total_contribution
    ai_probability = max(0, min(100, ai_probability))

    # 人类概率
    human_probability = 100 - ai_probability

    # 置信度
    if abs(ai_probability - 50) < 15:
        confidence = "low"
    elif abs(ai_probability - 50) < 30:
        confidence = "medium"
    else:
        confidence = "high"

    # 生成建议
    suggestions = []
    if ai_probability > 80:
        suggestions.append("内容AI特征明显，建议大幅修改")
        if ai_words_result["count"] > 0:
            suggestions.append(f"删除AI常用词：{', '.join(ai_words_result['words'][:5])}")
    elif ai_probability > 60:
        suggestions.append("内容有一定AI特征，建议适当修改")
        if tone_result["neutral"]:
            suggestions.append("增加个人表达和情感词")
    else:
        suggestions.append("内容AI特征不明显，可以直接使用")

    return {
        "ai_probability": round(ai_probability, 1),
        "human_probability": round(human_probability, 1),
        "confidence": confidence,
        "summary": f"AI生成概率：{ai_probability:.1f}%，人类生成概率：{human_probability:.1f}%",
        "suggestions": suggestions,
        "details": {
            "ai_words": ai_words_result,
            "ai_patterns": ai_patterns_result,
            "structure_perfection": structure_result,
            "neutral_tone": tone_result,
            "repetitive_structure": repetitive_result,
            "formal_language": formal_result,
            "lack_of_personal": personal_result,
            "predictable_ending": ending_result,
        }
    }


# 示例使用
if __name__ == "__main__":
    test_texts = [
        "综上所述，这个方案具有明显的优势。值得注意的是，这个方案不仅提高了效率，而且在一定程度上降低了成本。具体来说，我们可以通过以下方式实现...",
        "我觉得这个方案真的很好！我喜欢这个想法，特别是关于成本控制的部分。个人认为我们可以试试看，说不定会有惊喜！",
        "这个方案有三个优势：一是提高效率，二是降低成本，三是简化流程。我们团队讨论后都觉得可行，准备下周开始实施。",
    ]

    for i, text in enumerate(test_texts, 1):
        print(f"\n{'='*60}")
        print(f"测试文本 {i}")
        print(f"{'='*60}")
        result = calculate_ai_score(text)
        print(f"\nAI生成概率: {result['ai_probability']}%")
        print(f"人类生成概率: {result['human_probability']}%")
        print(f"置信度: {result['confidence']}")
        print(f"\n建议:")
        for suggestion in result['suggestions']:
            print(f"  - {suggestion}")
