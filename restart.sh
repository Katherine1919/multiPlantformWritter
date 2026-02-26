#!/bin/bash
# 重启所有服务

echo "🔄 重启HumanWriter服务..."

# 停止现有服务
pkill -f "npm run dev"
pkill -f "uvicorn"
pkill -f "python3 -m uvicorn"

sleep 3

# 启动后端API
cd /home/admin/.openclaw/workspace/humanwriter/backend

# 启动AI检测器
echo "启动AI检测器..."
python3 -m uvicorn ai_detector_100d:app --host 0.0.0.0 --port 8000 > detector.log 2>&1 &

# 启动AI重写器
echo "启动AI重写器..."
python3 -m uvicorn ai_rewriter:app --host 0.0.0.0 --port 8001 > rewriter.log 2>&1 &

# 启动前端
echo "启动前端..."
cd /home/admin/.openclaw/workspace/humanwriter/frontend
npm run dev > frontend.log 2>&1 &

sleep 5

echo "✅ 服务启动完成"
echo ""
echo "📊 服务地址："
echo "   主页：http://localhost:3000"
echo "   AI检测：http://localhost:3000/ai-humanizer"
echo "   标题生成：http://localhost:3000/ai-title-generator"
echo "   AI重写：http://localhost:3000/ai-rewriter"
echo ""
echo "   API端口："
echo "   AI检测：8000"
echo "   AI重写：8001"
echo "   发布：8002"
echo ""
echo "📋 日志文件："
echo "   backend/detector.log"
echo "   backend/rewriter.log"
echo "   frontend/frontend.log"
