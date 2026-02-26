# 公众号文章自动化排版与分发 - 执行计划

## 目标
输入一次Markdown → 自动排版HTML → 一键分发5个平台（公众号/知乎/小红书/微博/头条）

## 技术方案（方案B - 均衡）

### 架构
```
Markdown输入
    ↓
格式解析器（Python）
    ↓
排版引擎（多模板）
    ↓
平台适配器（5个平台）
    ↓
API发布
```

### 核心组件

#### 1. Markdown解析器
```python
# formatter/markdown_parser.py
- 解析标题、段落、列表、代码块
- 提取图片链接
- 识别特殊格式（引用/表格）
```

#### 2. 公众号HTML排版器
```python
# formatter/wechat_formatter.py
- 响应式布局（手机优先）
- 字体/颜色/间距优化
- 图片自适应
- 引用样式美化
```

#### 3. 平台适配器
```python
# formatter/platform_adapter.py
- 微信：HTML富文本
- 知乎：Markdown + 图片
- 小红书：emoji + 分段
- 微博：140字摘要 + 链接
- 头条：标题 + 正文
```

#### 4. n8n集成
```json
// n8n workflow
1. Manual Trigger
2. HTTP Request (OpenClaw Skill)
3. 调用后端发布API
4. 返回5个平台结果
```

## 执行步骤

### Step 1: Markdown解析器（30分钟）
- [x] 创建formatter目录
- [ ] 实现基础解析
- [ ] 测试3篇文章

### Step 2: 公众号排版器（60分钟）
- [ ] HTML模板设计
- [ ] 样式优化
- [ ] 图片处理
- [ ] 响应式测试

### Step 3: 平台适配器（30分钟）
- [ ] 5个平台适配规则
- [ ] 字数/格式限制
- [ ] 特殊符号处理

### Step 4: n8n工作流（30分钟）
- [ ] 工作流设计
- [ ] OpenClaw集成
- [ ] 端到端测试

### Step 5: 文档与测试（30分钟）
- [ ] 使用文档
- [ ] 3篇文章测试
- [ ] Bug修复

## 文件结构
```
humanwriter/
├── formatter/
│   ├── __init__.py
│   ├── markdown_parser.py      # Markdown解析
│   ├── wechat_formatter.py     # 公众号排版
│   ├── platform_adapter.py     # 平台适配
│   └── templates/
│       └── wechat.html         # HTML模板
├── n8n/
│   └── auto-publish.json       # n8n工作流
└── test_formatter.py           # 测试脚本
```

## 成功标准
- [ ] 3篇文章自动排版（符合公众号规范）
- [ ] 一键分发到5个平台（成功率100%）
- [ ] n8n工作流可复用
- [ ] 完整文档

## 时间规划
总计：3小时
- Step 1: 30分钟
- Step 2: 60分钟
- Step 3: 30分钟
- Step 4: 30分钟
- Step 5: 30分钟
