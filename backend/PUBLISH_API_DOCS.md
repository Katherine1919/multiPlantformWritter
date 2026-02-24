# 一键发布API使用文档

## 🎯 功能说明

支持一键发布到5个平台：
- ✅ 公众号（官方API）
- ✅ 知乎（爬虫方式）
- ✅ 小红书（爬虫方式）
- ✅ 微博（官方API）
- ✅ 头条（官方API）

---

## 📦 技术栈

```
后端：Python + FastAPI
发布方式：API + 爬虫（Selenium）
部署：Railway / Vercel
```

---

## 🚀 快速开始

### 1. 安装依赖

```bash
cd backend
pip install -r requirements.txt
```

### 2. 配置环境变量

创建 `.env` 文件：

```bash
# 公众号
WECHAT_APP_ID=your_app_id
WECHAT_APP_SECRET=your_app_secret
WECHAT_ACCESS_TOKEN=your_access_token

# 微博
WEIBO_APP_KEY=your_app_key
WEIBO_APP_SECRET=your_app_secret
WEIBO_ACCESS_TOKEN=your_access_token

# 头条
TOUTIAO_APP_ID=your_app_id
TOUTIAO_APP_SECRET=your_app_secret
TOUTIAO_ACCESS_TOKEN=your_access_token

# 知乎（爬虫）
ZHIHU_ACCOUNT=your_zhihu_account
ZHIHU_PASSWORD=your_zhihu_password

# 小红书（爬虫）
XIAOHONGSHU_ACCOUNT=your_account
XIAOHONGSHU_PASSWORD=your_password
```

### 3. 启动服务

```bash
uvicorn publish:app --reload
```

---

## 📋 API端点

### 1. 获取平台列表

```
GET /api/v1/platforms
```

**响应**：
```json
{
  "success": true,
  "data": [
    {
      "id": "wechat",
      "name": "公众号",
      "supports": ["article", "scheduled", "images"],
      "api_available": true
    },
    ...
  ]
}
```

---

### 2. 获取账号列表

```
GET /api/v1/accounts
GET /api/v1/accounts?platform=wechat
```

**响应**：
```json
{
  "success": true,
  "data": {
    "wechat": [
      {"id": "account_1", "name": "公众号1", "type": "service_account"}
    ]
  }
}
```

---

### 3. 发布到多个平台

```
POST /api/v1/publish
```

**请求体**：
```json
[
  {
    "platform": "wechat",
    "account_id": "account_1",
    "title": "文章标题",
    "content": "文章内容",
    "images": ["https://example.com/image.jpg"],
    "tags": ["AI", "工具"],
    "scheduled_time": "2026-02-25T10:00:00"
  },
  {
    "platform": "weibo",
    "account_id": "account_1",
    "title": "微博标题",
    "content": "微博内容...",
    "images": []
  }
]
```

**响应**：
```json
{
  "success": true,
  "data": [
    {
      "platform": "wechat",
      "status": "success",
      "message": "发布成功",
      "url": "https://mp.weixin.qq.com/s/xxx",
      "published_at": "2026-02-24T10:00:00"
    },
    ...
  ],
  "summary": {
    "total": 2,
    "success": 2,
    "failed": 0
  }
}
```

---

### 4. 发布到单个平台

```
POST /api/v1/publish/{platform}
```

**示例**：
```
POST /api/v1/publish/wechat
Content-Type: application/json

{
  "platform": "wechat",
  "account_id": "account_1",
  "title": "文章标题",
  "content": "文章内容",
  "images": [],
  "tags": []
}
```

---

## 🔧 平台配置说明

### 公众号

**获取方式**：
1. 登录 [微信公众平台](https://mp.weixin.qq.com)
2. 开发 → 基本配置
3. 获取 AppID 和 AppSecret
4. 调用接口获取 access_token

**API文档**：https://developers.weixin.qq.com/doc/offiaccount/Basic_Information/Get_access_token

---

### 微博

**获取方式**：
1. 登录 [微博开放平台](https://open.weibo.com)
2. 微博开放平台 → 我的应用 → 应用信息
3. 获取 App Key 和 App Secret
4. 授权后获取 access_token

**API文档**：https://open.weibo.com/wiki/%E5%BE%AE%E5%8F%91%E8%80%85%E6%96%87%E6%A1%A3

---

### 头条

**获取方式**：
1. 登录 [头条号平台](https://mp.toutiao.com)
2. 开发者 → 应用管理
3. 获取 AppID 和 AppSecret
4. 授权后获取 access_token

**API文档**：https://open.toutiao.com/docs

---

### 知乎

**说明**：知乎没有公开API，需要使用Selenium爬虫

**实现方式**：
1. 模拟登录
2. 提交文章
3. 获取文章URL

**注意事项**：
- 可能违反知乎服务条款
- 建议使用官方客户端或网页版
- 爬虫方式可能不稳定

---

### 小红书

**说明**：小红书没有公开API，需要使用移动端或爬虫

**实现方式**：
1. 模拟移动端登录
2. 发布笔记
3. 获取笔记URL

**注意事项**：
- 可能违反小红书服务条款
- 建议使用官方App
- 爬虫方式可能不稳定

---

## 🎨 前端集成

### 示例：React组件

```typescript
import React, { useState } from 'react';

export default function PublishDialog({ adaptedContent }: { adaptedContent: any }) {
  const [selectedPlatforms, setSelectedPlatforms] = useState(['wechat', 'weibo']);
  const [publishing, setPublishing] = useState(false);
  const [results, setResults] = useState([]);

  const handlePublish = async () => {
    setPublishing(true);

    const targets = selectedPlatforms.map(platform => ({
      platform,
      account_id: "account_1",
      title: adaptedContent.title,
      content: adaptedContent.text,
      images: adaptedContent.image ? [adaptedContent.image] : [],
      tags: []
    }));

    try {
      const response = await fetch('/api/v1/publish', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(targets)
      });

      const data = await response.json();
      setResults(data.data);
    } catch (error) {
      alert('发布失败');
    } finally {
      setPublishing(false);
    }
  };

  return (
    <div>
      <h3>一键发布</h3>

      {/* 平台选择 */}
      <div>
        {['wechat', 'weibo', 'zhihu', 'xiaohongshu', 'toutiao'].map(platform => (
          <label key={platform}>
            <input
              type="checkbox"
              checked={selectedPlatforms.includes(platform)}
              onChange={(e) => {
                if (e.target.checked) {
                  setSelectedPlatforms([...selectedPlatforms, platform]);
                } else {
                  setSelectedPlatforms(selectedPlatforms.filter(p => p !== platform));
                }
              }}
            />
            {platform}
          </label>
        ))}
      </div>

      {/* 发布按钮 */}
      <button
        onClick={handlePublish}
        disabled={publishing}
      >
        {publishing ? '发布中...' : '一键发布'}
      </button>

      {/* 发布结果 */}
      {results.length > 0 && (
        <div>
          <h4>发布结果：</h4>
          {results.map((result, idx) => (
            <div key={idx}>
              {result.platform}: {result.status}
              {result.url && <a href={result.url} target="_blank">查看</a>}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
```

---

## 🔒 安全建议

### 1. 环境变量
- ✅ 不要在代码中硬编码API Token
- ✅ 使用 `.env` 文件
- ✅ 把 `.env` 加入 `.gitignore`

### 2. 加密存储
- ✅ 数据库存储Token时加密
- ✅ 使用HTTPS传输
- ✅ 定期轮换Token

### 3. 访问控制
- ✅ 添加用户认证
- ✅ 限制API调用频率
- ✅ 记录操作日志

---

## ⚠️ 注意事项

### 知乎/小红书
- 使用爬虫可能违反服务条款
- 建议使用官方客户端
- 爬虫方式可能不稳定

### API限流
- 各平台都有调用频率限制
- 建议实现队列机制
- 错误重试要控制次数

### 内容审核
- 发布后需要等待审核
- 审核通过后才能正常显示
- 注意各平台的审核规则

---

## 📊 使用流程

```
用户输入内容
  ↓
多平台适配
  ↓
选择发布平台
  ↓
一键发布
  ↓
返回发布结果
  ├─ 成功：返回URL
  ├─ 失败：返回错误信息
  └─ 审核：等待审核
```

---

## 🎯 下一步

- [ ] 实现知乎爬虫（Selenium）
- [ ] 实现小红书爬虫（移动端）
- [ ] 添加任务队列（Celery）
- [ ] 实现发布历史记录
- [ ] 添加定时发布功能

---

*文档版本：1.0*
*更新时间：2026-02-24*
