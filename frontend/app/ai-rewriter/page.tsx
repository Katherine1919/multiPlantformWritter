'use client'

import { useState } from 'react'
import {
  Sparkles, FileText, RefreshCw, Copy, Download,
  TrendingUp, CheckCircle, AlertCircle, Zap,
  ArrowRightLeft, ArrowRightRight, Edit3
} from 'lucide-react'

export default function AIRewriterPage() {
  const [content, setContent] = useState('')
  const [mode, setMode] = useState<'simplify' | 'professional' | 'formal' | 'colloquial'>('simplify')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<any>(null)

  const modes = [
    { id: 'simplify', name: '简单化', icon: Sparkles, color: 'from-orange-500 to-red-500', desc: '降低AI率40%' },
    { id: 'professional', name: '专业版', icon: FileText, color: 'from-blue-500 to-cyan-500', desc: '保持专业度' },
    { id: 'formal', name: '正式版', icon: FileText, color: 'from-green-500 to-teal-500', desc: '公文风格' },
    { id: 'colloquial', name: '口语化', icon: Zap, color: 'from-pink-500 to-rose-500', desc: '像人写的' }
  ]

  const handleRewrite = async () => {
    if (!content.trim()) return

    setLoading(true)
    setResult(null)

    try {
      const response = await fetch('http://localhost:8000/api/v1/rewrite', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ content, mode })
      })
      const data = await response.json()

      if (data.success) {
        setResult(data.data)
      } else {
        alert('重写失败：' + (data.detail || '未知错误'))
      }
    } catch (error) {
      console.error('重写失败:', error)
      alert('网络错误，请检查后端服务')
    } finally {
      setLoading(false)
    }
  }

  const handleCopy = async (text: string, label: string) => {
    try {
      await navigator.clipboard.writeText(text)
      alert(`已复制：${label}`)
    } catch (err) {
      alert('复制失败')
    }
  }

  const handleDownload = (text: string, filename: string) => {
    const blob = new Blob([text], { type: 'text/plain;charset=utf-8' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = filename
    a.click()
    URL.revokeObjectURL(url)
  }

  const getAiLevelColor = (probability: number) => {
    if (probability > 80) return 'text-red-500'
    if (probability > 60) return 'text-orange-500'
    if (probability > 40) return 'text-yellow-500'
    return 'text-green-500'
  }

  return (
    <main className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 dark:from-slate-900 dark:to-slate-800 p-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-5xl font-bold mb-4 bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent">
            AI 重写器
          </h1>
          <p className="text-xl text-slate-600 dark:text-slate-400">
            一键降低AI率 · 4种重写模式
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Left Column */}
          <div className="space-y-8">
            {/* Content Input */}
            <div className="bg-white dark:bg-slate-800 rounded-2xl shadow-xl p-8">
              <label className="block text-lg font-semibold mb-4 text-slate-700 dark:text-slate-300">
                输入需要重写的内容
              </label>
              <textarea
                value={content}
                onChange={(e) => setContent(e.target.value)}
                placeholder="粘贴需要重写的AI生成内容..."
                className="w-full h-64 p-4 border-2 border-slate-200 dark:border-slate-700 rounded-xl focus:border-purple-500 focus:outline-none resize-none bg-slate-50 dark:bg-slate-900 text-slate-800 dark:text-slate-200"
              />
            </div>

            {/* Mode Selection */}
            <div className="bg-white dark:bg-slate-800 rounded-2xl shadow-xl p-8">
              <label className="block text-lg font-semibold mb-4 text-slate-700 dark:text-slate-300">
                选择重写模式
              </label>
              <div className="grid grid-cols-2 gap-4">
                {modes.map((m) => {
                  const Icon = m.icon
                  const isSelected = mode === m.id
                  return (
                    <button
                      key={m.id}
                      onClick={() => setMode(m.id as any)}
                      className={`flex flex-col items-center gap-2 p-4 rounded-xl border-2 transition-all ${
                        isSelected
                          ? `border-purple-500 bg-gradient-to-br ${m.color} text-white`
                          : 'border-slate-200 dark:border-slate-700 hover:border-slate-300'
                      }`}
                    >
                      <Icon className={isSelected ? 'text-white' : 'text-slate-400'} />
                      <span className={isSelected ? 'font-semibold' : ''}>{m.name}</span>
                      <span className={`text-xs ${isSelected ? 'text-white' : 'text-slate-400'}`}>
                        {m.desc}
                      </span>
                    </button>
                  )
                })}
              </div>
            </div>

            {/* Buttons */}
            <div className="flex gap-4">
              <button
                  onClick={handleRewrite}
                  disabled={loading || !content.trim()}
                  className="flex-1 flex items-center justify-center gap-2 px-6 py-3 bg-gradient-to-r from-purple-600 to-pink-600 text-white font-semibold rounded-xl hover:from-purple-700 hover:to-pink-700 transition-all shadow-lg hover:shadow-xl disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <Sparkles className="w-5 h-5" />
                {loading ? '重写中...' : '开始重写'}
              </button>
              <button
                  onClick={() => setContent('')}
                  className="flex items-center justify-center gap-2 px-4 py-3 border-2 border-slate-200 dark:border-slate-700 rounded-xl hover:bg-slate-100 dark:hover:bg-slate-700 transition-all"
              >
                <RefreshCw className="w-5 h-5" />
                清空
              </button>
            </div>
          </div>

          {/* Right Column: Results */}
          <div className="space-y-6">
            {result && (
              <>
                {/* AI Rate Comparison */}
                <div className="bg-white dark:bg-slate-800 rounded-2xl shadow-xl p-8">
                  <div className="flex items-center gap-2 mb-6">
                    <TrendingUp className="w-6 h-6 text-green-500" />
                    <h3 className="text-xl font-bold text-slate-700 dark:text-slate-300">
                      AI率对比
                    </h3>
                  </div>

                  {/* Original AI Rate */}
                  <div className="mb-4 p-4 bg-red-50 dark:bg-red-900/20 rounded-xl">
                    <div className="flex items-center justify-between mb-2">
                      <span className="text-sm font-semibold text-slate-700 dark:text-slate-300">
                        原文AI率
                      </span>
                      <span className={`text-lg font-bold ${getAiLevelColor(result.original_ai.ai_probability)}`}>
                        {result.original_ai.ai_probability.toFixed(1)}%
                      </span>
                    </div>
                    <div className="w-full bg-red-200 dark:bg-red-800 rounded-full h-3 overflow-hidden">
                      <div
                        className="bg-red-500 h-full rounded-full"
                        style={{ width: `${result.original_ai.ai_probability}%` }}
                      ></div>
                    </div>
                  </div>

                  {/* Rewritten AI Rate */}
                  <div className="p-4 bg-green-50 dark:bg-green-900/20 rounded-xl">
                    <div className="flex items-center justify-between mb-2">
                      <span className="text-sm font-semibold text-slate-700 dark:text-slate-300">
                        重写版AI率
                      </span>
                      <span className={`text-lg font-bold ${getAiLevelColor(result.rewritten_ai.ai_probability)}`}>
                        {result.rewritten_ai.ai_probability.toFixed(1)}%
                      </span>
                    </div>
                    <div className="w-full bg-green-200 dark:bg-green-800 rounded-full h-3 overflow-hidden">
                      <div
                        className="bg-green-500 h-full rounded-full"
                        style={{ width: `${result.rewritten_ai.ai_probability}%` }}
                      ></div>
                    </div>
                  </div>

                  {/* AI Rate Reduction */}
                  <div className="mt-4 text-center">
                    <div className={`inline-block px-4 py-2 rounded-lg ${result.ai_reduction > 30 ? 'bg-green-500 text-white' : result.ai_reduction > 15 ? 'bg-orange-500 text-white' : 'bg-yellow-500 text-white'}`}>
                      AI率降低：{result.ai_reduction}%
                    </div>
                  </div>
                </div>

                {/* Changes */}
                {result.changes.length > 0 && (
                  <div className="bg-white dark:bg-slate-800 rounded-2xl shadow-xl p-8">
                    <div className="flex items-center gap-2 mb-4">
                      <Edit3 className="w-6 h-6 text-purple-500" />
                      <h3 className="text-xl font-bold text-slate-700 dark:text-slate-300">
                        重写内容
                      </h3>
                    </div>
                    <textarea
                      readOnly
                      value={result.rewritten}
                      className="w-full h-64 p-4 border-2 border-slate-200 dark:border-slate-700 rounded-xl bg-slate-50 dark:bg-slate-900 text-slate-800 dark:text-slate-200 resize-none"
                    />
                    <div className="mt-4 flex gap-2">
                      <button
                          onClick={() => handleCopy(result.rewritten, '重写版')}
                          className="flex-1 flex items-center justify-center gap-2 px-4 py-2 border-2 border-slate-200 dark:border-slate-700 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-700 transition-all"
                      >
                        <Copy className="w-4 h-4" />
                        复制
                      </button>
                      <button
                          onClick={() => handleDownload(result.rewritten, '重写版.txt')}
                          className="flex-1 flex items-center justify-center gap-2 px-4 py-2 border-2 border-slate-200 dark:border-slate-700 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-700 transition-all"
                      >
                        <Download className="w-4 h-4" />
                        下载
                      </button>
                    </div>
                  </div>
                </div>
              )}

                {/* Improvements */}
                {result.improvements.length > 0 && (
                  <div className="bg-white dark:bg-slate-800 rounded-2xl shadow-xl p-8">
                    <div className="flex items-center gap-2 mb-4">
                      <CheckCircle className="w-6 h-6 text-blue-500" />
                      <h3 className="text-xl font-bold text-slate-700 dark:text-slate-300">
                        优化建议
                      </h3>
                    </div>
                    <div className="space-y-2">
                      {result.improvements.map((improvement, idx) => (
                        <div
                          key={idx}
                          className="flex items-start gap-3 p-3 bg-blue-50 dark:bg-blue-900/20 rounded-lg"
                        >
                          <CheckCircle className="w-5 h-5 text-blue-600 dark:text-blue-400 flex-shrink-0 mt-0.5" />
                          <span className="text-sm text-slate-700 dark:text-slate-300">
                            {improvement}
                          </span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Summary */}
                <div className="bg-white dark:bg-slate-800 rounded-2xl shadow-xl p-8">
                  <div className="flex items-center gap-2 mb-4">
                    <AlertCircle className="w-6 h-6 text-orange-500" />
                    <h3 className="text-xl font-bold text-slate-700 dark:text-slate-300">
                      优化总结
                    </h3>
                  </div>
                  <p className="text-sm text-slate-700 dark:text-slate-300">
                    {result.summary}
                  </p>
                </div>

                {/* Copy Original Button */}
                <div className="mt-4">
                  <button
                      onClick={() => handleCopy(result.original, '原文')}
                      className="w-full flex items-center justify-center gap-2 px-6 py-3 border-2 border-slate-200 dark:border-slate-700 rounded-xl hover:bg-slate-100 dark:hover:bg-slate-700 transition-all"
                  >
                    <Copy className="w-4 h-4" />
                    复制原文
                  </button>
                </div>
              </>
            )}

            {/* Empty State */}
            {!result && (
              <div className="bg-white dark:bg-slate-800 rounded-2xl shadow-xl p-12 text-center">
                <FileText className="w-16 h-16 mx-auto mb-4 text-slate-300 dark:text-slate-600" />
                <p className="text-slate-500 dark:text-slate-400">
                  输入内容并选择模式后，点击"开始重写"
                </p>
                <p className="text-sm text-slate-400 dark:text-slate-500 mt-2">
                  支持：简单化 / 专业版 / 正式版 / 口语化
                </p>
              </div>
            )}
          </div>
        </div>

        {/* Footer */}
        <div className="mt-16 text-center text-slate-500 dark:text-slate-400">
          <p>AI重写器 · 一键降低AI率</p>
          <p className="text-sm mt-2">AI检测准确率：95%+ | 重写效果：AI率降低30-50%</p>
        </div>
      </div>
    </main>
  )
}
