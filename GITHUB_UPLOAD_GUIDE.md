# HumanWriter - GitHub上传指南

## 🎯 上传方法

### 方法1：使用GitHub CLI（推荐）

#### 1. 登录GitHub CLI

```bash
# 运行登录命令
gh auth login --scopes repo

# 然后在浏览器中完成认证
```

#### 2. 创建仓库并推送

```bash
cd /home/admin/.openclaw/workspace/humanwriter

# 创建仓库
gh repo create Katherine1919/HumanWriter \
  --public \
  --description "HumanWriter - 多平台内容适配工具 | 让内容创作更简单" \
  --source=. \
  --remote=origin

# 推送代码
git push -u origin master
```

---

### 方法2：手动创建仓库

#### 1. 在GitHub上手动创建仓库

访问：https://github.com/new

填写：
- Repository name: `HumanWriter`
- Description: `HumanWriter - 多平台内容适配工具`
- Public: ✅

#### 2. 推送代码

```bash
cd /home/admin/.openclaw/workspace/humanwriter

# 添加remote（替换YOUR_USERNAME为你的用户名）
git remote add origin https://github.com/YOUR_USERNAME/HumanWriter.git

# 推送
git push -u origin master
```

---

### 方法3：使用HTTPS Token

#### 1. 生成Personal Access Token

1. 访问：https://github.com/settings/tokens
2. 点击：Generate new token (classic)
3. 勾选：repo
4. 生成并复制token

#### 2. 推送

```bash
cd /home/admin/.openclaw/workspace/humanwriter

# 添加remote（使用token）
git remote add origin https://YOUR_TOKEN@github.com/YOUR_USERNAME/HumanWriter.git

# 推送
git push -u origin master
```

---

## 📋 仓库设置建议

### 仓库信息
- **Name**: HumanWriter
- **Description**: 多平台内容适配工具 | 让内容创作更简单
- **Visibility**: Public
- **Topics**: ai, content-creation, multi-platform, automation, tools

### README
已在根目录创建，包含：
- 功能说明
- 快速开始
- 技术栈
- 定价

### License
建议使用：MIT License

---

## 🚀 上传后的工作

1. **添加Topics**
   - 访问仓库设置
   - 添加：ai, content-creation, multi-platform, automation, tools

2. **启用GitHub Pages**
   - 访问仓库设置 → Pages
   - 选择：frontend/ 目录
   - 部署前端演示

3. **创建Releases**
   - Tag: v1.0.0
   - Release notes: 首次发布

---

## 📊 上传内容

### 文件统计
- 总文件：38个
- 代码行数：约12,000行
- 文档：5篇

### 主要文件
- `frontend/` - Next.js前端
- `backend/` - Python后端
- `articles/` - 公众号文章（3篇）
- `*.md` - 完整文档

---

## ✅ 当前状态

- ✅ Git初始化完成
- ✅ 文件已commit
- ❌ 推送到GitHub（待完成）

---

## 💡 快速命令

### 登录 + 创建 + 推送（一键）

```bash
# 1. 登录（需要浏览器认证）
gh auth login --scopes repo

# 2. 创建仓库 + 推送
cd /home/admin/.openclaw/workspace/humanwriter
gh repo create Katherine1919/HumanWriter \
  --public \
  --description "多平台内容适配工具 | 让内容创作更简单" \
  --source=. \
  --remote=origin && \
git push -u origin master
```

### 只推送（如果仓库已创建）

```bash
cd /home/admin/.openclaw/workspace/humanwriter

# 添加remote
git remote add origin https://github.com/Katherine1919/HumanWriter.git

# 推送
git push -u origin master
```

---

*上传指南版本：1.0*
*更新时间：2026-02-24*
