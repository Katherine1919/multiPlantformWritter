# HumanWriter - 多平台内容适配工具

让一篇文章一键适配Twitter/知乎/公众号/小红书。

## 🎯 产品功能

### 1. 多平台文字适配
- ✅ Twitter（280字短文 + #tag）
- ✅ 知乎（Markdown格式）
- ✅ 公众号（HTML富文本）
- ✅ 小红书（emoji + 多图）

### 2. 图片处理
- ✅ 上传图片
- ✅ 比例调整（16:9 / 1:1 / 3:4）
- ✅ 预览 + 下载
- ⏳ AI生成配图（开发中）

### 3. 内容质量检测
- ✅ AI痕迹检测
- ✅ 可读性评分
- ✅ 互动性分析
- ✅ 优化建议

### 4. 一键发布
- ⏳ 公众号API
- ⏳ Twitter API
- ⏳ 今日头条API
- ❌ 知乎（无公开API）
- ❌ 小红书（无公开API）

---

## 🏗️ 技术架构

```
前端：Next.js 14 + React + TypeScript + Tailwind CSS
后端：Python + FastAPI
图片：DALL-E API / Canvas
部署：Vercel
```

---

## 📦 项目结构

```
humanwriter/
├── frontend/
│   ├── app/
│   │   ├── page.tsx              # 主页面
│   │   ├── layout.tsx            # 布局
│   │   └── globals.css           # 样式
│   ├── components/
│   │   └── ImageUpload.tsx       # 图片上传
│   ├── package.json
│   └── README.md
├── backend/
│   ├── main.py                   # 主API
│   ├── quality.py                # 质量检测
│   ├── publish.py                # 发布API
│   └── requirements.txt
├── articles/                    # 公众号文章
│   ├── content-trends-2026.md    # 趋势分析
│   ├── humanwriter-intro.md      # 产品介绍
│   └── humanwriter-tutorial.md   # 技术教程
└── README.md
```

---

## 🚀 快速开始

### 前端

```bash
cd frontend
npm install
npm run dev
```

访问：http://localhost:3000

### 后端

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

访问：http://localhost:8000

---

## 💰 定价

### 免费试用7天
- ✅ 全功能免费
- ✅ 每天5篇文章
- ✅ 无需支付

### 付费订阅
- **基础版（¥9/月）**：无限使用
- **Pro版（¥29/月）**：+图片生成 + 排版模板
- **企业版（¥299/月）**：+团队协作 + API

---

## 📋 API文档

### 1. 内容质量检测

```bash
POST /api/v1/quality-check

Request:
{
  "content": "文章内容",
  "platform": "wechat"
}

Response:
{
  "score": {
    "overall": 85.5,
    "readability": 90.0,
    "engagement": 75.0,
    "ai_detection": 80.0
  },
  "issues": [...],
  "summary": "内容质量优秀"
}
```

### 2. 一键发布

```bash
POST /api/v1/publish

Request:
{
  "targets": [
    {
      "platform": "wechat",
      "title": "标题",
      "content": "内容"
    }
  ]
}

Response:
{
  "total": 1,
  "success": 1,
  "failed": 0,
  "results": [...]
}
```

---

## 📈 已完成功能

- [x] 多平台文字适配
- [x] 图片上传
- [x] 图片比例调整
- [x] 内容质量检测
- [x] 公众号文章（3篇）
- [x] 发布API（框架）

---

## 🚧 开发中功能

- [ ] AI生成配图（DALL-E）
- [ ] 去AI味功能
- [ ] 排版模板库
- [ ] 一键发布（各平台认证）

---

## 📝 待办

1. **图片生成**
   - 集成DALL-E API
   - 风格统一
   - 批量生成

2. **去AI味**
   - 识别AI常用词
   - 自动替换
   - 语气调整

3. **发布功能**
   - 公众号API认证
   - Twitter API认证
   - 其他平台集成

4. **用户系统**
   - 注册/登录
   - 订阅管理
   - 试用到期检测

---

## 📄 许可证

MIT
