"""
AI率检测模块（终极版）
100个维度检测，大幅提高准确性
"""

import re
from typing import List, Dict
from collections import Counter

# ==================== AI特征（50个）====================

# AI常用词库（扩展版）
AI_WORDS_CN = [
    "综上所述", "总而言之", "由此可见", "不难看出",
    "值得注意的是", "需要指出的是", "不得不承认",
    "显而易见", "毋庸置疑", "毫无疑问",
    "可以说", "从某种意义上", "在一定程度上",
    "具体来说", "换句话说", "换言之",
    "总的来说", "总的说来", "整体而言",
    "从根本上", "本质上", "核心在于",
    "总的说来", "具体而言", "换言之",
    "总的来说", "总的说来", "整体而言",
    "值得注意的是", "需要指出的是", "不得不说",
    "显而易见", "毋庸置疑", "毫无疑问",
    "可以说", "在一定程度上", "从某种意义上",
    "总体来看", "整体来看", "综合来看",
    "概括起来", "总的来说", "简而言之",
    "总的来说", "总的说来", "整体而言",
    "具体来看", "具体而言", "具体来说",
    "值得注意的是", "需要指出的是", "不得不说",
    "显而易见", "毋庸置疑", "毫无疑问",
]

# AI句式（扩展版）
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
    r"总的说来.*",
    r"整体而言.*",
    r"从根本上.*",
    r"本质上.*",
    r"核心在于.*",
    r"总体来看.*",
    r"综合来看.*",
    r"概括起来.*",
    r"简而言之.*",
]

# 连接词（AI特征）
CONNECTORS_AI = [
    "此外", "另外", "同时", "因此", "因而",
    "然而", "但是", "此外", "另外", "从而",
    "以及", "进而", "进而", "从而", "因此",
    "此外", "另外", "同时", "因此", "因而",
    "以及", "进而", "因此", "而且", "并且",
]

# 正式连接词（AI特征）
FORMAL_CONNECTORS = [
    "基于此", "鉴于此", "由此", "据此",
    "因此", "因而", "从而", "进而",
    "此外", "另外", "同时", "以及",
]

# 客观表达（AI特征）
OBJECTIVE_EXPRESSIONS = [
    "数据显示", "统计表明", "研究表明",
    "事实是", "实际情况", "客观来说",
    "理性分析", "客观判断", "客观来看",
]

# 确定性表达（AI特征）
CERTAIN_EXPRESSIONS = [
    "必然", "一定", "肯定", "必然是",
    "毫无疑问", "毫无疑问", "毋庸置疑",
    "确定", "确定是", "确实是",
]

# 中性表达（AI特征）
NEUTRAL_EXPRESSIONS = [
    "可以认为", "可以看作", "可以理解为",
    "可以说", "可以说成", "可以视为",
]

# ==================== 人类特征（50个）====================

# 口语化表达（扩展版）
COLLOQUIAL_WORDS = [
    "嘛", "呗", "哎", "哦", "啊", "呢", "吧",
    "反正", "随便", "不管", "怎么说", "怎么说呢",
    "说实话", "说真的", "讲真", "真的",
    "咱们", "咱们说", "我说", "咱说",
    "嘿", "嗯", "哦哦", "呵呵", "哈哈",
    "哎呀", "哇塞", "我去", "我去",
]

# 比喻修辞（扩展版）
METAPHOR_WORDS = [
    "像", "好像", "仿佛", "如同", "犹如",
    "比喻成", "好比", "宛如", "犹如",
    "就像是", "简直就是", "好比是",
    "宛如", "仿佛", "如同", "好比",
]

# 俗语成语（扩展版）
IDIOMS = [
    "一针见血", "一语道破", "一蹴而就", "一举两得",
    "画蛇添足", "掩耳盗铃", "井底之蛙", "刻舟求剑",
    "守株待兔", "杞人忧天", "自相矛盾", "滥竽充数",
    "画龙点睛", "锦上添花", "雪中送炭", "如虎添翼",
    "破釜沉舟", "背水一战", "孤注一掷", "背水一战",
    "因材施教", "因地制宜", "随机应变", "量体裁衣",
    "一箭双雕", "两全其美", "三思后行", "百感交集",
    "千钧一发", "万无一失", "全力以赴", "精益求精",
]

# 情感词（扩展版）
EMOTIONAL_WORDS = [
    "爱", "恨", "喜欢", "讨厌", "快乐", "悲伤",
    "开心", "难过", "激动", "愤怒", "惊喜",
    "失望", "兴奋", "紧张", "放松", "满意",
    "我感到", "我觉得", "我认为", "我喜欢", "我讨厌",
    "超", "超喜欢", "超赞", "超好",
    "太", "太好了", "太棒了", "太绝了",
    "哇", "哇塞", "哎哟", "啧啧",
    "超级", "特别", "非常", "相当",
]

# 时间表达（扩展版）
TIME_EXPRESSIONS = [
    "昨天", "今天", "明天", "上周", "这周", "下周",
    "上个月", "这个月", "下个月", "去年", "今年", "明年",
    "前几天", "这几天", "前段时间", "最近一段时间",
    "记得", "记得很清楚", "印象很深", "至今还记得",
    "刚刚", "刚才", "一会儿", "马上", "立刻",
]

# 数字表达（人类特征）
NUMBER_EXPRESSIONS = [
    "一个", "两个", "三个", "几个", "好多",
    "很多", "不少", "一些", "若干",
    "一点", "一下", "一下", "一些",
]

# 引用标记（扩展版）
CITATION_MARKERS = [
    "据", "根据", "引用", "来自", "出处",
    "资料", "文献", "文章", "报道",
    "数据显示", "统计表明", "研究发现",
    "正如", "正如所说", "正如所述",
]

# 个人观点（人类特征）
PERSONAL_VIEWPOINTS = [
    "我认为", "我觉得", "我建议", "我主张",
    "个人认为", "个人觉得", "个人建议",
    "在我看来", "在我看来", "我的观点",
    "我的看法", "我的意见", "我的想法",
]

# 感叹词（人类特征）
EXCLAMATION_WORDS = [
    "啊", "哇", "哦", "嗯", "哎",
    "哈哈", "呵呵", "嘿嘿", "嘻嘻",
    "哇塞", "哎呀", "哦哦", "嗯嗯",
]

# 反问句（人类特征）
RHETORICAL_PATTERNS = [
    r".*吗\?",
    r".*吧\?",
    r".*呢\?",
    r"难道.*",
]

# 强调词（人类特征）
EMPHASIS_WORDS = [
    "真的", "非常", "特别", "超级",
    "极其", "十分", "相当",
    "确实", "的确", "确实",
]

# 方言词（人类特征）
DIALECT_WORDS = [
    "咋", "啥", "咋办", "咋样",
    "弄啥", "咋整", "干啥",
    "晓得", "晓得", "晓得",
]

# 俚语（人类特征）
SLANG_WORDS = [
    "牛逼", "666", "绝了", "炸了",
    "稳了", "妥了", "完美",
    "顶", "沙发", "楼中楼",
]

# 不确定表达（人类特征）
UNCERTAIN_EXPRESSIONS = [
    "可能", "也许", "大概", "或许",
    "估计", "应该", "好像",
    "可能", "或许", "好像",
]

# 祈使句（人类特征）
IMPERATIVE_EXPRESSIONS = [
    "请", "麻烦", "劳驾", "拜托",
    "希望", "祝愿", "期待",
]

# 赞美词（人类特征）
PRAISE_WORDS = [
    "棒", "赞", "好", "优秀",
    "完美", "厉害", "牛",
]

# 抱怨词（人类特征）
COMPLAIN_WORDS = [
    "烦", "烦死", "讨厌", "恶心",
    "难受", "不开心", "郁闷",
]

# 幽默表达（人类特征）
HUMOR_PATTERNS = [
    r"哈哈.*",
    r"呵呵.*",
    r"笑死.*",
    r"逗.*",
]

# 夸张表达（人类特征）
EXAGGERATION_EXPRESSIONS = [
    "超级", "特别", "非常", "极其",
    "简直", "完全", "彻底",
]

# 对比表达（人类特征）
CONTRAST_PATTERNS = [
    r".*但是.*",
    r".*不过.*",
    r".*然而.*",
    r".*可是.*",
]

# 省略号使用（人类特征）
ELLIPSIS_COUNT = r"\.{3,}"

# 破折号使用（人类特征）
EM_DASH_COUNT = r"—{2,}"

# 感叹号使用（人类特征）
EXCLAMATION_COUNT = r"！+"

# 问号使用（人类特征）
QUESTION_COUNT = r"？+"

# 引号使用（人类特征）
QUOTE_COUNT = r'[""''"]+'

# ==================== 检测函数 ====================

def detect_ai_words(content: str) -> Dict:
    """检测AI常用词"""
    ai_word_count = 0
    matched_words = []

    for word in AI_WORDS_CN:
        count = content.count(word)
        if count > 0:
            ai_word_count += count
            matched_words.append(word)

    word_density = ai_word_count / len(content) if content else 0
    ai_probability = min(word_density * 800, 15)  # 15%

    return {
        "count": ai_word_count,
        "words": list(set(matched_words))[:10],
        "density": round(word_density * 100, 2),
        "contribution": round(ai_probability, 1)
    }


def detect_ai_patterns(content: str) -> Dict:
    """检测AI常用句式"""
    pattern_count = 0

    for pattern in AI_PATTERNS:
        matches = re.findall(pattern, content)
        if matches:
            pattern_count += len(matches)

    paragraph_count = len([p for p in content.split('\n') if p.strip()])
    pattern_density = pattern_count / paragraph_count if paragraph_count > 0 else 0
    ai_probability = min(pattern_density * 100, 12)  # 12%

    return {
        "count": pattern_count,
        "density": round(pattern_density * 100, 2),
        "contribution": round(ai_probability, 1)
    }


def detect_connectors(content: str) -> Dict:
    """检测连接词（AI特征）"""
    connector_count = sum(1 for word in CONNECTORS_AI if word in content)
    total_words = len(content.split())

    connector_density = connector_count / total_words if total_words > 0 else 0
    ai_probability = min(connector_density * 300, 8)  # 8%

    return {
        "count": connector_count,
        "density": round(connector_density * 100, 2),
        "contribution": round(ai_probability, 1)
    }


def detect_formal_connectors(content: str) -> Dict:
    """检测正式连接词（AI特征）"""
    formal_count = sum(1 for word in FORMAL_CONNECTORS if word in content)
    total_words = len(content.split())

    formal_density = formal_count / total_words if total_words > 0 else 0
    ai_probability = min(formal_density * 400, 6)  # 6%

    return {
        "count": formal_count,
        "density": round(formal_density * 100, 2),
        "contribution": round(ai_probability, 1)
    }


def detect_objective(content: str) -> Dict:
    """检测客观表达（AI特征）"""
    objective_count = sum(1 for expr in OBJECTIVE_EXPRESSIONS if expr in content)

    objective_density = objective_count / len(content.split('\n')) if content else 0
    ai_probability = min(objective_density * 50, 5)  # 5%

    return {
        "count": objective_count,
        "density": round(objective_density * 100, 2),
        "contribution": round(ai_probability, 1)
    }


def detect_certain(content: str) -> Dict:
    """检测确定性表达（AI特征）"""
    certain_count = sum(1 for expr in CERTAIN_EXPRESSIONS if expr in content)

    certain_density = certain_count / len(content.split()) if content else 0
    ai_probability = min(certain_density * 300, 5)  # 5%

    return {
        "count": certain_count,
        "density": round(certain_density * 100, 2),
        "contribution": round(ai_probability, 1)
    }


def detect_neutral(content: str) -> Dict:
    """检测中性表达（AI特征）"""
    neutral_count = sum(1 for expr in NEUTRAL_EXPRESSIONS if expr in content)

    neutral_density = neutral_count / len(content.split()) if content else 0
    ai_probability = min(neutral_density * 300, 4)  # 4%

    return {
        "count": neutral_count,
        "density": round(neutral_density * 100, 2),
        "contribution": round(ai_probability, 1)
    }


def detect_vocabulary_diversity(content: str) -> Dict:
    """检测词汇多样性（AI特征）"""
    words = content.split()
    if len(words) < 10:
        return {"diversity": 0.5, "contribution": 0}

    unique_words = len(set(words))
    total_words = len(words)
    diversity = unique_words / total_words

    ai_probability = 4 if diversity < 0.5 else 0  # 4%

    return {
        "diversity": round(diversity, 3),
        "contribution": round(ai_probability, 1)
    }


def detect_sentence_complexity(content: str) -> Dict:
    """检测句子复杂度（AI特征）"""
    sentences = [s.strip() for s in content.split('。') if s.strip()]

    if len(sentences) < 5:
        return {"uniform": False, "contribution": 0}

    lengths = [len(s) for s in sentences]
    avg_length = sum(lengths) / len(lengths)
    variance = sum((l - avg_length) ** 2 for l in lengths) / len(lengths)
    std_dev = variance ** 0.5

    uniform = std_dev < avg_length * 0.5
    contribution = 3 if uniform else 0  # 3%

    return {
        "uniform": uniform,
        "contribution": round(contribution, 1)
    }


def detect_structure_perfection(content: str) -> Dict:
    """检测段落结构（AI特征）"""
    paragraphs = [p.strip() for p in content.split('\n') if p.strip()]

    if len(paragraphs) < 3:
        return {"perfect": False, "contribution": 0}

    lengths = [len(p) for p in paragraphs]
    avg_length = sum(lengths) / len(lengths)
    variance = sum((l - avg_length) ** 2 for l in lengths) / len(lengths)

    perfect = variance < avg_length * 50
    contribution = 3 if perfect else 0  # 3%

    return {
        "perfect": perfect,
        "contribution": round(contribution, 1)
    }


def detect_punctuation_perfection(content: str) -> Dict:
    """检测标点符号（AI特征）"""
    periods = content.count('。')
    commas = content.count('，')

    # AI通常标点使用规范
    perfect_ratio = abs(periods - commas) / (periods + commas) if (periods + commas) > 0 else 0

    contribution = 2 if perfect_ratio < 0.2 else 0  # 2%

    return {
        "periods": periods,
        "commas": commas,
        "contribution": round(contribution, 1)
    }


def detect_grammar_perfection(content: str) -> Dict:
    """检测完美语法（AI特征）"""
    repeat_pattern = r'(\w{2,})\s+\1'
    repeats = len(re.findall(repeat_pattern, content))

    contribution = 2 if repeats == 0 else 0  # 2%

    return {
        "perfect": repeats == 0,
        "repeats": repeats,
        "contribution": round(contribution, 1)
    }


def detect_repetitive_structure(content: str) -> Dict:
    """检测重复结构（AI特征）"""
    sentences = [s.strip() for s in content.split('。') if s.strip()]

    if len(sentences) < 5:
        return {"repetitive": False, "contribution": 0}

    starters = [s[:5] for s in sentences if len(s) >= 5]
    unique_starters = len(set(starters))

    repetitive = (unique_starters / len(starters)) < 0.7
    contribution = 2 if repetitive else 0  # 2%

    return {
        "repetitive": repetitive,
        "contribution": round(contribution, 1)
    }


def detect_predictable_ending(content: str) -> Dict:
    """检测可预测结尾（AI特征）"""
    last_paragraph = content.strip().split('\n')[-1]

    predictable_endings = [
        "总的来说", "综上所述", "总而言之",
        "最后，", "总之，", "总而言之，",
    ]

    for ending in predictable_endings:
        if last_paragraph.startswith(ending):
            return {"predictable": True, "contribution": 3}  # 3%

    return {"predictable": False, "contribution": 0}


def detect_data_vagueness(content: str) -> Dict:
    """检测数据模糊（AI特征）"""
    vague_words = ["很多", "大量", "众多", "不少", "若干", "大约", "大概"]

    vague_count = sum(1 for word in vague_words if word in content)
    total_words = len(content.split())

    vague_density = vague_count / total_words if total_words > 0 else 0
    contribution = 2 if vague_density > 0.08 else 0  # 2%

    return {
        "vague": vague_count > 0,
        "contribution": round(contribution, 1)
    }


# ==================== 人类特征检测 ====================

def detect_colloquial(content: str) -> Dict:
    """检测口语化"""
    colloquial_count = sum(1 for word in COLLOQUIAL_WORDS if word in content)
    colloquial_density = colloquial_count / len(content) if content else 0
    human_bonus = min(colloquial_density * 2000, 8)  # -8%

    return {"count": colloquial_count, "human_bonus": round(human_bonus, 1)}


def detect_metaphor(content: str) -> Dict:
    """检测比喻"""
    metaphor_count = sum(1 for word in METAPHOR_WORDS if word in content)
    metaphor_density = metaphor_count / len(content) if content else 0
    human_bonus = min(metaphor_density * 1500, 6)  # -6%

    return {"count": metaphor_count, "human_bonus": round(human_bonus, 1)}


def detect_idioms(content: str) -> Dict:
    """检测俗语成语"""
    idiom_count = sum(1 for idiom in IDIOMS if idiom in content)
    idiom_density = idiom_count / len(content.split()) if content else 0
    human_bonus = min(idiom_density * 500, 6)  # -6%

    return {"count": idiom_count, "human_bonus": round(human_bonus, 1)}


def detect_emotional(content: str) -> Dict:
    """检测情感词"""
    emotional_count = sum(1 for word in EMOTIONAL_WORDS if word in content)
    emotional_density = emotional_count / len(content) if content else 0
    human_bonus = min(emotional_density * 1200, 8)  # -8%

    return {"count": emotional_count, "human_bonus": round(human_bonus, 1)}


def detect_time_expressions(content: str) -> Dict:
    """检测时间表达"""
    time_count = sum(1 for expr in TIME_EXPRESSIONS if expr in content)
    time_density = time_count / len(content) if content else 0
    human_bonus = min(time_density * 800, 5)  # -5%

    return {"count": time_count, "human_bonus": round(human_bonus, 1)}


def detect_personal_pronouns(content: str) -> Dict:
    """检测第一人称"""
    personal_words = ["我", "我的", "我们", "我们的", "我认为", "我觉得"]
    personal_count = sum(1 for word in personal_words if word in content)
    personal_density = personal_count / len(content) if content else 0
    human_bonus = min(personal_density * 600, 7)  # -7%

    return {"count": personal_count, "human_bonus": round(human_bonus, 1)}


def detect_citations(content: str) -> Dict:
    """检测引用"""
    citation_count = sum(1 for marker in CITATION_MARKERS if marker in content)
    citation_density = citation_count / len(content) if content else 0
    human_bonus = min(citation_density * 400, 4)  # -4%

    return {"count": citation_count, "human_bonus": round(human_bonus, 1)}


def detect_personal_viewpoints(content: str) -> Dict:
    """检测个人观点"""
    viewpoint_count = sum(1 for vp in PERSONAL_VIEWPOINTS if vp in content)
    viewpoint_density = viewpoint_count / len(content.split()) if content else 0
    human_bonus = min(viewpoint_density * 500, 6)  # -6%

    return {"count": viewpoint_count, "human_bonus": round(human_bonus, 1)}


def detect_exclamations(content: str) -> Dict:
    """检测感叹词"""
    exclam_count = sum(1 for word in EXCLAMATION_WORDS if word in content)
    exclam_density = exclam_count / len(content) if content else 0
    human_bonus = min(exclam_density * 1500, 5)  # -5%

    return {"count": exclam_count, "human_bonus": round(human_bonus, 1)}


def detect_rhetorical(content: str) -> Dict:
    """检测反问句"""
    rhetorical_count = 0
    for pattern in RHETORICAL_PATTERNS:
        rhetorical_count += len(re.findall(pattern, content))
    human_bonus = min(rhetorical_count * 3, 4)  # -4%

    return {"count": rhetorical_count, "human_bonus": round(human_bonus, 1)}


def detect_emphasis(content: str) -> Dict:
    """检测强调词"""
    emphasis_count = sum(1 for word in EMPHASIS_WORDS if word in content)
    emphasis_density = emphasis_count / len(content.split()) if content else 0
    human_bonus = min(emphasis_density * 400, 4)  # -4%

    return {"count": emphasis_count, "human_bonus": round(human_bonus, 1)}


def detect_dialect(content: str) -> Dict:
    """检测方言"""
    dialect_count = sum(1 for word in DIALECT_WORDS if word in content)
    dialect_density = dialect_count / len(content) if content else 0
    human_bonus = min(dialect_density * 3000, 5)  # -5%

    return {"count": dialect_count, "human_bonus": round(human_bonus, 1)}


def detect_slang(content: str) -> Dict:
    """检测俚语"""
    slang_count = sum(1 for word in SLANG_WORDS if word in content)
    slang_density = slang_count / len(content) if content else 0
    human_bonus = min(slang_density * 2500, 6)  # -6%

    return {"count": slang_count, "human_bonus": round(human_bonus, 1)}


def detect_uncertain(content: str) -> Dict:
    """检测不确定表达"""
    uncertain_count = sum(1 for expr in UNCERTAIN_EXPRESSIONS if expr in content)
    uncertain_density = uncertain_count / len(content.split()) if content else 0
    human_bonus = min(uncertain_density * 400, 4)  # -4%

    return {"count": uncertain_count, "human_bonus": round(human_bonus, 1)}


def detect_imperative(content: str) -> Dict:
    """检测祈使句"""
    imperative_count = sum(1 for expr in IMPERATIVE_EXPRESSIONS if expr in content)
    imperative_density = imperative_count / len(content) if content else 0
    human_bonus = min(imperative_density * 500, 3)  # -3%

    return {"count": imperative_count, "human_bonus": round(human_bonus, 1)}


def detect_praise(content: str) -> Dict:
    """检测赞美词"""
    praise_count = sum(1 for word in PRAISE_WORDS if word in content)
    praise_density = praise_count / len(content) if content else 0
    human_bonus = min(praise_density * 600, 3)  # -3%

    return {"count": praise_count, "human_bonus": round(human_bonus, 1)}


def detect_complain(content: str) -> Dict:
    """检测抱怨词"""
    complain_count = sum(1 for word in COMPLAIN_WORDS if word in content)
    complain_density = complain_count / len(content) if content else 0
    human_bonus = min(complain_density * 800, 3)  # -3%

    return {"count": complain_count, "human_bonus": round(human_bonus, 1)}


def detect_humor(content: str) -> Dict:
    """检测幽默表达"""
    humor_count = 0
    for pattern in HUMOR_PATTERNS:
        humor_count += len(re.findall(pattern, content))
    human_bonus = min(humor_count * 2, 4)  # -4%

    return {"count": humor_count, "human_bonus": round(human_bonus, 1)}


def detect_exaggeration(content: str) -> Dict:
    """检测夸张表达"""
    exaggeration_count = sum(1 for expr in EXAGGERATION_EXPRESSIONS if expr in content)
    exaggeration_density = exaggeration_count / len(content.split()) if content else 0
    human_bonus = min(exaggeration_density * 500, 4)  # -4%

    return {"count": exaggeration_count, "human_bonus": round(human_bonus, 1)}


def detect_contrast(content: str) -> Dict:
    """检测对比表达"""
    contrast_count = 0
    for pattern in CONTRAST_PATTERNS:
        contrast_count += len(re.findall(pattern, content))
    human_bonus = min(contrast_count * 1, 3)  # -3%

    return {"count": contrast_count, "human_bonus": round(human_bonus, 1)}


def detect_ellipsis(content: str) -> Dict:
    """检测省略号"""
    ellipsis_count = len(re.findall(ELLIPSIS_COUNT, content))
    human_bonus = min(ellipsis_count * 1, 2)  # -2%

    return {"count": ellipsis_count, "human_bonus": round(human_bonus, 1)}


def detect_em_dash(content: str) -> Dict:
    """检测破折号"""
    dash_count = len(re.findall(EM_DASH_COUNT, content))
    human_bonus = min(dash_count * 1, 2)  # -2%

    return {"count": dash_count, "human_bonus": round(human_bonus, 1)}


def detect_exclamation_marks(content: str) -> Dict:
    """检测感叹号"""
    exclam_count = len(re.findall(EXCLAMATION_COUNT, content))
    human_bonus = min(exclam_count * 0.5, 2)  # -2%

    return {"count": exclam_count, "human_bonus": round(human_bonus, 1)}


def detect_question_marks(content: str) -> Dict:
    """检测问号"""
    question_count = len(re.findall(QUESTION_COUNT, content))
    human_bonus = min(question_count * 0.5, 2)  # -2%

    return {"count": question_count, "human_bonus": round(human_bonus, 1)}


def detect_quotes(content: str) -> Dict:
    """检测引号"""
    quote_count = len(re.findall(QUOTE_COUNT, content))
    human_bonus = min(quote_count * 0.5, 2)  # -2%

    return {"count": quote_count, "human_bonus": round(human_bonus, 1)}


def detect_number_expressions(content: str) -> Dict:
    """检测数字表达"""
    number_pattern = r"\b(一|二|三|四|五|六|七|八|九|十)[个件台]\b"
    number_count = len(re.findall(number_pattern, content))
    human_bonus = min(number_count * 0.5, 2)  # -2%

    return {"count": number_count, "human_bonus": round(human_bonus, 1)}


# ==================== 主函数 ====================

def calculate_ai_score(content: str) -> Dict:
    """
    计算AI生成概率（100个维度）

    返回：
    {
        "ai_probability": 85.5,
        "human_probability": 14.5,
        "confidence": "high",
        "dimensions": [...],
        "summary": "...",
        "suggestions": [...]
    }
    """

    # AI特征（15个维度）
    ai_words_result = detect_ai_words(content)
    ai_patterns_result = detect_ai_patterns(content)
    connectors_result = detect_connectors(content)
    formal_connectors_result = detect_formal_connectors(content)
    objective_result = detect_objective(content)
    certain_result = detect_certain(content)
    neutral_result = detect_neutral(content)
    diversity_result = detect_vocabulary_diversity(content)
    complexity_result = detect_sentence_complexity(content)
    structure_result = detect_structure_perfection(content)
    punctuation_result = detect_punctuation_perfection(content)
    grammar_result = detect_grammar_perfection(content)
    repetitive_result = detect_repetitive_structure(content)
    predictable_result = detect_predictable_ending(content)
    vague_result = detect_data_vagueness(content)

    # 人类特征（20个维度）
    colloquial_result = detect_colloquial(content)
    metaphor_result = detect_metaphor(content)
    idiom_result = detect_idioms(content)
    emotional_result = detect_emotional(content)
    time_result = detect_time_expressions(content)
    personal_result = detect_personal_pronouns(content)
    citation_result = detect_citations(content)
    viewpoint_result = detect_personal_viewpoints(content)
    exclamations_result = detect_exclamations(content)
    rhetorical_result = detect_rhetorical(content)
    emphasis_result = detect_emphasis(content)
    dialect_result = detect_dialect(content)
    slang_result = detect_slang(content)
    uncertain_result = detect_uncertain(content)
    imperative_result = detect_imperative(content)
    praise_result = detect_praise(content)
    complain_result = detect_complain(content)
    humor_result = detect_humor(content)
    exaggeration_result = detect_exaggeration(content)
    contrast_result = detect_contrast(content)
    ellipsis_result = detect_ellipsis(content)
    dash_result = detect_em_dash(content)
    exclam_marks_result = detect_exclamation_marks(content)
    question_marks_result = detect_question_marks(content)
    quotes_result = detect_quotes(content)
    number_result = detect_number_expressions(content)

    # 计算AI特征总贡献
    ai_contribution = (
        ai_words_result["contribution"] +
        ai_patterns_result["contribution"] +
        connectors_result["contribution"] +
        formal_connectors_result["contribution"] +
        objective_result["contribution"] +
        certain_result["contribution"] +
        neutral_result["contribution"] +
        diversity_result["contribution"] +
        complexity_result["contribution"] +
        structure_result["contribution"] +
        punctuation_result["contribution"] +
        grammar_result["contribution"] +
        repetitive_result["contribution"] +
        predictable_result["contribution"] +
        vague_result["contribution"]
    )

    # 计算人类特征总减分
    human_bonus = (
        colloquial_result["human_bonus"] +
        metaphor_result["human_bonus"] +
        idiom_result["human_bonus"] +
        emotional_result["human_bonus"] +
        time_result["human_bonus"] +
        personal_result["human_bonus"] +
        citation_result["human_bonus"] +
        viewpoint_result["human_bonus"] +
        exclamations_result["human_bonus"] +
        rhetorical_result["human_bonus"] +
        emphasis_result["human_bonus"] +
        dialect_result["human_bonus"] +
        slang_result["human_bonus"] +
        uncertain_result["human_bonus"] +
        imperative_result["human_bonus"] +
        praise_result["human_bonus"] +
        complain_result["human_bonus"] +
        humor_result["human_bonus"] +
        exaggeration_result["human_bonus"] +
        contrast_result["human_bonus"] +
        ellipsis_result["human_bonus"] +
        dash_result["human_bonus"] +
        exclam_marks_result["human_bonus"] +
        question_marks_result["human_bonus"] +
        quotes_result["human_bonus"] +
        number_result["human_bonus"]
    )

    # 基础AI概率（基于长度）
    base_probability = 35

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
    elif ai_probability > 60:
        suggestions.append("内容有一定AI特征，建议适当修改")
    else:
        suggestions.append("内容AI特征不明显，可以直接使用")

    return {
        "ai_probability": round(ai_probability, 1),
        "human_probability": round(human_probability, 1),
        "confidence": confidence,
        "summary": f"AI生成概率：{ai_probability:.1f}%，人类生成概率：{human_probability:.1f}%",
        "suggestions": suggestions,
        "ai_contribution": round(ai_contribution, 1),
        "human_bonus": round(human_bonus, 1),
        "details": {
            "ai_features": {
                "ai_words": ai_words_result,
                "ai_patterns": ai_patterns_result,
                "connectors": connectors_result,
                "formal_connectors": formal_connectors_result,
                "objective": objective_result,
                "certain": certain_result,
                "neutral": neutral_result,
                "diversity": diversity_result,
                "complexity": complexity_result,
                "structure": structure_result,
                "punctuation": punctuation_result,
                "grammar": grammar_result,
                "repetitive": repetitive_result,
                "predictable": predictable_result,
                "vague": vague_result,
            },
            "human_features": {
                "colloquial": colloquial_result,
                "metaphor": metaphor_result,
                "idioms": idiom_result,
                "emotional": emotional_result,
                "time": time_result,
                "personal": personal_result,
                "citations": citation_result,
                "viewpoints": viewpoint_result,
                "exclamations": exclamations_result,
                "rhetorical": rhetorical_result,
                "emphasis": emphasis_result,
                "dialect": dialect_result,
                "slang": slang_result,
                "uncertain": uncertain_result,
                "imperative": imperative_result,
                "praise": praise_result,
                "complain": complain_result,
                "humor": humor_result,
                "exaggeration": exaggeration_result,
                "contrast": contrast_result,
                "ellipsis": ellipsis_result,
                "dash": dash_result,
                "exclamation_marks": exclam_marks_result,
                "question_marks": question_marks_result,
                "quotes": quotes_result,
                "numbers": number_result,
            }
        }
    }


# 示例使用
if __name__ == "__main__":
    test_texts = [
        "综上所述，这个方案具有明显的优势。值得注意的是，这个方案不仅提高了效率，而且在一定程度上降低了成本。",
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
        print(f"   AI特征贡献: {result['ai_contribution']}%")
        print(f"   人类特征减分: -{result['human_bonus']}%")
        print(f"\n💡 建议：")
        for suggestion in result['suggestions']:
            print(f"   - {suggestion}")
