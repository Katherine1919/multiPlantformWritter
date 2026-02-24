"""
AI率检测模块（最终版）
20个维度，优化权重，提高准确性
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
    "具体而言", "换言之", "换句话说",
    "总的来说", "总的说来", "整体而言",
    "从根本上", "本质上", "核心在于",
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
    r"具体来说.*",
    r"换言之.*",
    r"换句话说.*",
    r"综上所述.*",
    r"总而言之.*",
]

# 口语化表达（人类特征）
COLLOQUIAL_WORDS = [
    "嘛", "呗", "哎", "哦", "啊", "呢", "吧",
    "反正", "随便", "不管", "怎么说", "怎么说呢",
    "说实话", "说真的", "讲真", "真的",
    "咱们", "咱们说", "我说", "咱说",
]

# 比喻修辞（人类特征）
METAPHOR_WORDS = [
    "像", "好像", "仿佛", "如同", "犹如",
    "比喻成", "好比", "宛如", "犹如",
    "就像是", "简直就是", "好比是",
]

# 俗语成语（人类特征）
IDIOMS = [
    "一针见血", "一语道破", "一蹴而就", "一举两得",
    "画蛇添足", "掩耳盗铃", "井底之蛙", "刻舟求剑",
    "守株待兔", "杞人忧天", "自相矛盾", "滥竽充数",
    "画龙点睛", "锦上添花", "雪中送炭", "如虎添翼",
    "破釜沉舟", "背水一战", "孤注一掷", "背水一战",
    "因材施教", "因地制宜", "随机应变", "量体裁衣",
]

# 情感词（人类特征）
EMOTIONAL_WORDS = [
    "爱", "恨", "喜欢", "讨厌", "快乐", "悲伤",
    "开心", "难过", "激动", "愤怒", "惊喜",
    "失望", "兴奋", "紧张", "放松", "满意",
    "我感到", "我觉得", "我认为", "我喜欢", "我讨厌",
    "超", "超喜欢", "超赞", "超好",
    "太", "太好了", "太棒了", "太绝了",
    "哇", "哇塞", "哎哟", "啧啧",
]

# 时间表达（人类特征）
TIME_EXPRESSIONS = [
    "昨天", "今天", "明天", "上周", "这周", "下周",
    "上个月", "这个月", "下个月", "去年", "今年", "明年",
    "前几天", "这几天", "前段时间", "最近一段时间",
    "记得", "记得很清楚", "印象很深", "至今还记得",
]

# 引用标记（人类特征）
CITATION_MARKERS = [
    "据", "根据", "引用", "来自", "出处",
    "资料", "文献", "文章", "报道",
    "数据显示", "统计表明", "研究发现",
]


def detect_ai_words(content: str) -> Dict:
    """检测AI常用词（权重：高）"""
    ai_word_count = 0
    matched_words = []

    for word in AI_WORDS_CN:
        count = content.count(word)
        if count > 0:
            ai_word_count += count
            matched_words.append(word)

    word_density = ai_word_count / len(content) if content else 0
    ai_probability = min(word_density * 1200, 35)  # 最高贡献35%（提高）

    return {
        "count": ai_word_count,
        "words": matched_words,
        "density": round(word_density * 100, 2),
        "contribution": round(ai_probability, 1)
    }


def detect_ai_patterns(content: str) -> Dict:
    """检测AI常用句式（权重：高）"""
    pattern_count = 0
    matched_patterns = []

    for pattern in AI_PATTERNS:
        matches = re.findall(pattern, content)
        if matches:
            pattern_count += len(matches)
            matched_patterns.extend(matches)

    paragraph_count = len([p for p in content.split('\n') if p.strip()])
    pattern_density = pattern_count / paragraph_count if paragraph_count > 0 else 0
    ai_probability = min(pattern_density * 150, 25)  # 最高贡献25%（提高）

    return {
        "count": pattern_count,
        "patterns": matched_patterns,
        "density": round(pattern_density * 100, 2),
        "contribution": round(ai_probability, 1)
    }


def detect_vocabulary_diversity(content: str) -> Dict:
    """检测词汇多样性（AI特征：多样性低）"""
    words = content.split()
    if len(words) < 10:
        return {
            "diversity": 0.5,
            "contribution": 0
        }

    # 计算词汇多样性
    unique_words = len(set(words))
    total_words = len(words)
    diversity = unique_words / total_words

    # AI词汇多样性通常较低
    if diversity < 0.5:
        ai_probability = 8  # 最高贡献8%（提高）
    else:
        ai_probability = 0

    return {
        "diversity": round(diversity, 3),
        "unique_words": unique_words,
        "total_words": total_words,
        "contribution": round(ai_probability, 1)
    }


def detect_sentence_complexity(content: str) -> Dict:
    """检测句子复杂度（AI特征：复杂度均匀）"""
    sentences = [s.strip() for s in content.split('。') if s.strip()]

    if len(sentences) < 5:
        return {
            "uniform": False,
            "contribution": 0
        }

    # 计算句子长度
    lengths = [len(s) for s in sentences]

    # 计算标准差
    avg_length = sum(lengths) / len(lengths)
    variance = sum((l - avg_length) ** 2 for l in lengths) / len(lengths)
    std_dev = variance ** 0.5

    # AI句子复杂度通常比较均匀
    uniform = std_dev < avg_length * 0.5
    contribution = 5 if uniform else 0  # 提高到5

    return {
        "uniform": uniform,
        "avg_length": round(avg_length, 1),
        "std_dev": round(std_dev, 1),
        "contribution": round(contribution, 1)
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
        contribution = 5  # 提高到5
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
    formal_connectors = [
        "此外", "另外", "同时", "因此", "因而",
        "然而", "但是", "此外", "另外", "从而",
        "以及", "进而", "进而", "从而", "因此"
    ]

    formal_count = sum(1 for word in formal_connectors if word in content)
    total_words = len(content.split())

    # AI写作通常正式连接词多
    formal_density = formal_count / total_words if total_words > 0 else 0

    if formal_density > 0.05:
        contribution = 5  # 提高到5
        neutral = True
    else:
        contribution = 0
        neutral = False

    return {
        "neutral": neutral,
        "formal_count": formal_count,
        "density": round(formal_density * 100, 2),
        "contribution": round(contribution, 1)
    }


def detect_repetitive_structure(content: str) -> Dict:
    """检测重复的句式结构（AI特征）"""
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
    contribution = 4 if repetitive else 0  # 提高到4

    return {
        "repetitive": repetitive,
        "unique_ratio": round(unique_starters / len(starters), 2),
        "contribution": round(contribution, 1)
    }


def detect_predictable_ending(content: str) -> Dict:
    """检测可预测的结尾（AI特征）"""
    last_paragraph = content.strip().split('\n')[-1]

    predictable_endings = [
        "总的来说",
        "综上所述",
        "总而言之",
        "综上所述",
        "最后，",
        "总之，",
        "总而言之，",
    ]

    for ending in predictable_endings:
        if last_paragraph.startswith(ending):
            return {
                "predictable": True,
                "ending": ending,
                "contribution": 6  # 提高到6
            }

    return {
        "predictable": False,
        "contribution": 0
    }


def detect_perfect_grammar(content: str) -> Dict:
    """检测完美的语法（AI特征）"""
    # 简单检测：错别字、重复词等

    repeat_pattern = r'(\w{2,})\s+\1'
    repeats = len(re.findall(repeat_pattern, content))

    typos = [
        "的得地", "在再", "做作", "象像", "带戴",
    ]
    typo_found = any(typo in content for typo in typos)

    # 如果没有重复词和错别字，可能是AI
    if repeats == 0 and not typo_found:
        contribution = 3
        perfect = True
    else:
        contribution = 0
        perfect = False

    return {
        "perfect": perfect,
        "repeats": repeats,
        "typo_found": typo_found,
        "contribution": round(contribution, 1)
    }


def detect_data_vagueness(content: str) -> Dict:
    """检测数据模糊度（AI特征：数据模糊）"""
    vague_words = [
        "很多", "大量", "众多", "不少", "若干",
        "大约", "大概", "可能", "也许", "或许",
        "一些", "一定", "相当", "非常",
    ]

    vague_count = sum(1 for word in vague_words if word in content)
    total_words = len(content.split())

    # 模糊词多 = AI特征
    vague_density = vague_count / total_words if total_words > 0 else 0

    if vague_density > 0.08:
        contribution = 4
        vague = True
    else:
        contribution = 0
        vague = False

    return {
        "vague": vague,
        "count": vague_count,
        "density": round(vague_density * 100, 2),
        "contribution": round(contribution, 1)
    }


def detect_colloquial(content: str) -> Dict:
    """检测口语化表达（人类特征）"""
    colloquial_count = 0
    matched_words = []

    for word in COLLOQUIAL_WORDS:
        count = content.count(word)
        if count > 0:
            colloquial_count += count
            matched_words.append(word)

    # 口语化多 = 人类特征（减少AI概率）
    colloquial_density = colloquial_count / len(content) if content else 0
    human_bonus = min(colloquial_density * 2500, 12)  # 最高减12%（提高）

    return {
        "count": colloquial_count,
        "words": matched_words,
        "density": round(colloquial_density * 100, 2),
        "human_bonus": round(human_bonus, 1)
    }


def detect_metaphor(content: str) -> Dict:
    """检测比喻修辞（人类特征）"""
    metaphor_count = 0
    matched_words = []

    for word in METAPHOR_WORDS:
        count = content.count(word)
        if count > 0:
            metaphor_count += count
            matched_words.append(word)

    # 比喻多 = 人类特征（减少AI概率）
    metaphor_density = metaphor_count / len(content) if content else 0
    human_bonus = min(metaphor_density * 2000, 10)  # 最高减10%（提高）

    return {
        "count": metaphor_count,
        "words": matched_words,
        "density": round(metaphor_density * 100, 2),
        "human_bonus": round(human_bonus, 1)
    }


def detect_idioms(content: str) -> Dict:
    """检测俗语成语（人类特征）"""
    idiom_count = 0
    matched_idioms = []

    for idiom in IDIOMS:
        if idiom in content:
            idiom_count += 1
            matched_idioms.append(idiom)

    # 成语多 = 人类特征（减少AI概率）
    idiom_density = idiom_count / len(content.split()) if content else 0
    human_bonus = min(idiom_density * 800, 10)  # 最高减10%（提高）

    return {
        "count": idiom_count,
        "idioms": matched_idioms,
        "density": round(idiom_density * 100, 2),
        "human_bonus": round(human_bonus, 1)
    }


def detect_emotional(content: str) -> Dict:
    """检测情感词（人类特征）"""
    emotional_count = 0
    matched_words = []

    for word in EMOTIONAL_WORDS:
        count = content.count(word)
        if count > 0:
            emotional_count += count
            matched_words.append(word)

    # 情感词多 = 人类特征（减少AI概率）
    emotional_density = emotional_count / len(content) if content else 0
    human_bonus = min(emotional_density * 2000, 12)  # 最高减12%（提高）

    return {
        "count": emotional_count,
        "words": matched_words,
        "density": round(emotional_density * 100, 2),
        "human_bonus": round(human_bonus, 1)
    }


def detect_time_expressions(content: str) -> Dict:
    """检测时间表达（人类特征）"""
    time_count = 0
    matched_words = []

    for expr in TIME_EXPRESSIONS:
        count = content.count(expr)
        if count > 0:
            time_count += count
            matched_words.append(expr)

    # 时间表达多 = 人类特征（减少AI概率）
    time_density = time_count / len(content) if content else 0
    human_bonus = min(time_density * 1500, 8)  # 最高减8%（提高）

    return {
        "count": time_count,
        "words": matched_words,
        "density": round(time_density * 100, 2),
        "human_bonus": round(human_bonus, 1)
    }


def detect_specific_numbers(content: str) -> Dict:
    """检测具体数字（人类特征）"""
    # 检测具体数字
    number_pattern = r"\b(一|二|三|四|五|六|七|八|九|十|百|千|万|亿)[一二三四五六七八九十千百千万亿个次天月年]\b"
    matches = re.findall(number_pattern, content)

    # 具体数字多 = 人类特征（减少AI概率）
    if len(matches) > 3:
        human_bonus = 6
    elif len(matches) > 1:
        human_bonus = 4
    else:
        human_bonus = 0

    return {
        "count": len(matches),
        "matches": matches,
        "human_bonus": round(human_bonus, 1)
    }


def detect_citations(content: str) -> Dict:
    """检测引用标记（人类特征）"""
    citation_count = 0
    matched_words = []

    for marker in CITATION_MARKERS:
        count = content.count(marker)
        if count > 0:
            citation_count += count
            matched_words.append(marker)

    # 引用多 = 人类特征（减少AI概率）
    citation_density = citation_count / len(content) if content else 0
    human_bonus = min(citation_density * 800, 6)  # 最高减6%（提高）

    return {
        "count": citation_count,
        "words": matched_words,
        "density": round(citation_density * 100, 2),
        "human_bonus": round(human_bonus, 1)
    }


def detect_personal_pronouns(content: str) -> Dict:
    """检测第一人称代词（人类特征）"""
    personal_words = [
        "我", "我的", "我们", "我们的", "我的观点",
        "我认为", "我觉得", "我喜欢", "我建议",
        "个人认为", "个人建议", "个人看法"
    ]

    personal_count = sum(1 for word in personal_words if word in content)
    total_chars = len(content)

    # "我"多 = 人类特征（减少AI概率）
    personal_density = personal_count / total_chars if total_chars > 0 else 0
    human_bonus = min(personal_density * 800, 10)  # 最高减10%（提高）

    return {
        "count": personal_count,
        "density": round(personal_density * 1000, 2),
        "human_bonus": round(human_bonus, 1)
    }


def calculate_ai_score(content: str) -> Dict:
    """
    计算AI生成概率（20个维度，优化权重）
    """
    # AI特征检测
    ai_words_result = detect_ai_words(content)
    ai_patterns_result = detect_ai_patterns(content)
    diversity_result = detect_vocabulary_diversity(content)
    complexity_result = detect_sentence_complexity(content)
    structure_result = detect_structure_perfection(content)
    tone_result = detect_neutral_tone(content)
    repetitive_result = detect_repetitive_structure(content)
    predictable_result = detect_predictable_ending(content)
    grammar_result = detect_perfect_grammar(content)
    vague_result = detect_data_vagueness(content)

    # 人类特征检测
    colloquial_result = detect_colloquial(content)
    metaphor_result = detect_metaphor(content)
    idiom_result = detect_idioms(content)
    emotional_result = detect_emotional(content)
    time_result = detect_time_expressions(content)
    number_result = detect_specific_numbers(content)
    citation_result = detect_citations(content)
    personal_result = detect_personal_pronouns(content)

    # 计算AI特征总贡献
    ai_contribution = (
        ai_words_result["contribution"] +
        ai_patterns_result["contribution"] +
        diversity_result["contribution"] +
        complexity_result["contribution"] +
        structure_result["contribution"] +
        tone_result["contribution"] +
        repetitive_result["contribution"] +
        predictable_result["contribution"] +
        grammar_result["contribution"] +
        vague_result["contribution"]
    )

    # 计算人类特征总减分
    human_bonus = (
        colloquial_result["human_bonus"] +
        metaphor_result["human_bonus"] +
        idiom_result["human_bonus"] +
        emotional_result["human_bonus"] +
        time_result["human_bonus"] +
        number_result["human_bonus"] +
        citation_result["human_bonus"] +
        personal_result["human_bonus"]
    )

    # 基础AI概率（基于长度）
    base_probability = min(35, len(content) / 100)

    # 最终AI概率
    ai_probability = base_probability + ai_contribution - human_bonus
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
        if ai_patterns_result["count"] > 0:
            suggestions.append("改写AI句式，用更自然的表达")
        if diversity_result["diversity"] < 0.5:
            suggestions.append("增加词汇多样性")
        if structure_result["perfect"]:
            suggestions.append("调整段落长度，避免过于整齐")
    elif ai_probability > 60:
        suggestions.append("内容有一定AI特征，建议适当修改")
        if not emotional_result["count"]:
            suggestions.append("增加情感词和个人表达")
        if not colloquial_result["count"]:
            suggestions.append("加入口语化表达")
    else:
        suggestions.append("内容AI特征不明显，可以直接使用")

    # 维度汇总
    dimensions = [
        {"name": "AI常用词", "type": "ai", "value": ai_words_result["count"], "impact": ai_words_result["contribution"]},
        {"name": "AI句式", "type": "ai", "value": ai_patterns_result["count"], "impact": ai_patterns_result["contribution"]},
        {"name": "词汇多样性", "type": "ai", "value": diversity_result["diversity"], "impact": diversity_result["contribution"]},
        {"name": "句子复杂度", "type": "ai", "value": complexity_result["uniform"], "impact": complexity_result["contribution"]},
        {"name": "段落结构", "type": "ai", "value": structure_result["perfect"], "impact": structure_result["contribution"]},
        {"name": "中立语气", "type": "ai", "value": tone_result["neutral"], "impact": tone_result["contribution"]},
        {"name": "口语化", "type": "human", "value": colloquial_result["count"], "impact": -colloquial_result["human_bonus"]},
        {"name": "比喻修辞", "type": "human", "value": metaphor_result["count"], "impact": -metaphor_result["human_bonus"]},
        {"name": "俗语成语", "type": "human", "value": idiom_result["count"], "impact": -idiom_result["human_bonus"]},
        {"name": "情感词", "type": "human", "value": emotional_result["count"], "impact": -emotional_result["human_bonus"]},
    ]

    return {
        "ai_probability": round(ai_probability, 1),
        "human_probability": round(human_probability, 1),
        "confidence": confidence,
        "summary": f"AI生成概率：{ai_probability:.1f}%，人类生成概率：{human_probability:.1f}%",
        "suggestions": suggestions,
        "dimensions": dimensions,
        "ai_features": {
            "ai_words": ai_words_result,
            "ai_patterns": ai_patterns_result,
            "vocabulary_diversity": diversity_result,
            "sentence_complexity": complexity_result,
            "structure_perfection": structure_result,
            "neutral_tone": tone_result,
            "repetitive_structure": repetitive_result,
            "predictable_ending": predictable_result,
            "perfect_grammar": grammar_result,
            "data_vagueness": vague_result,
        },
        "human_features": {
            "colloquial": colloquial_result,
            "metaphor": metaphor_result,
            "idioms": idiom_result,
            "emotional": emotional_result,
            "time_expressions": time_result,
            "specific_numbers": number_result,
            "citations": citation_result,
            "personal_pronouns": personal_result,
        }
    }


# 示例使用
if __name__ == "__main__":
    test_texts = [
        "综上所述，这个方案具有明显的优势。值得注意的是，这个方案不仅提高了效率，而且在一定程度上降低了成本。具体来说，我们可以通过以下方式实现。",
        "我觉得这个方案真的很好！我喜欢这个想法，特别是关于成本控制的部分。个人认为我们可以试试看，说不定会有惊喜。怎么说呢，这真的是一针见血啊！",
        "这个方案有三个优势：一是提高效率，二是降低成本，三是简化流程。我们团队讨论后都觉得可行，准备下周开始实施。记得很清楚，这是我们上个月讨论的结果。",
    ]

    for i, text in enumerate(test_texts, 1):
        print(f"\n{'='*70}")
        print(f"测试文本 {i}")
        print(f"{'='*70}")
        result = calculate_ai_score(text)
        print(f"\n📊 检测结果：")
        print(f"   AI生成概率: {result['ai_probability']}%")
        print(f"   人类生成概率: {result['human_probability']}%")
        print(f"   置信度: {result['confidence']}")
        print(f"\n💡 建议：")
        for suggestion in result['suggestions']:
            print(f"   - {suggestion}")
        print(f"\n📈 关键维度：")
        for dim in result['dimensions']:
            print(f"   {dim['name']}: {dim['value']} ({dim['type']}, 影响{dim['impact']:+.1f}%)")
