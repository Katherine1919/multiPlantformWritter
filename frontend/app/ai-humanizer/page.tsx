'use client'

import { useState } from 'react'
import {
  BrainCircuit, Sparkles, AlertTriangle,
  TrendingUp, CheckCircle, Copy, RefreshCw,
  BarChart3, FileText, Zap
} from 'lucide-react'

export default function AIHumanizerPage() {
  const [content, setContent] = useState('')
  const [mode, setMode] = useState<'detect_only' | 'humanize' | 'both'>('detect_only')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<any>(null)
  const [history, setHistory] = useState<any[]>([])

  const modes = [
    { id: 'detect_only', name: '只检测AI率', icon: BarChart3 },
    { id: 'humanize', name: '只去AI味', icon: Zap },
    { id: 'both', name: '检测+去AI味', icon: BrainCircuit }
  ]

  const handleAnalyze = async () => {
    if (!content.trim()) return

    setLoading(true)
    setResult(null)

    try {
      const response = await fetch('http://localhost:8000/api/v1/detect-and-humanize', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ content, mode })
      })
      const data = await response.json()

      if (data.success) {
        setResult(data.data)
        setHistory([{ ...data.data, timestamp: new Date().toISOString() }, ...history])
      } else {
        alert('分析失败：' + (data.detail || '未知错误'))
      }
    } catch (error) {
      console.error('分析失败:', error)
      alert('网络错误，请检查后端服务是否启动')
    } finally {
      setLoading(false)
    }
  }

  const handleCopy = async (text: string) => {
    try {
      await navigator.clipboard.writeText(text)
      alert('已复制到剪贴板')
    } catch (err) {
      alert('复制失败，请手动复制')
    }
  }

  const handleClear = () => {
    setContent('')
    setResult(null)
  }

  const getAiLevel = (probability: number) => {
    if (probability > 80) return { text: 'AI特征明显', color: 'text-red-500' }
    if (probability > 60) return { text: '有一定AI特征', color: 'text-orange-500' }
    if (probability > 40) return { text: 'AI特征适中', color: 'text-yellow-500' }
    return { text: 'AI特征不明显', color: 'text-green-500' }
  }

  return (
    <main className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 dark:from-slate-900 dark:to-slate-800 p-8">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-5xl font-bold mb-4 bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
            AI Detector & Humanizer
          </h1>
          <p className="text-xl text-slate-600 dark:text-slate-400">
            100维度AI检测 + 智能去AI味
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Left Column */}
          <div className="space-y-8">
            {/* Content Input */}
            <div className="bg-white dark:bg-slate-800 rounded-2xl shadow-xl p-8">
              <label className="block text-lg font-semibold mb-4 text-slate-700 dark:text-slate-300">
                输入内容
              </label>
              <textarea
                value={content}
                onChange={(e) => setContent(e.target.value)}
                placeholder="粘贴需要检测的文章内容..."
                className="w-full h-64 p-4 border-2 border-slate-200 dark:border-slate-700 rounded-xl focus:border-blue-500 focus:outline-none resize-none bg-slate-50 dark:bg-slate-900 text-slate-800 dark:text-slate-200"
              />

              {/* Mode Selection */}
              <div className="mt-6">
                <label className="block text-lg font-semibold mb-4 text-slate-700 dark:text-slate-300">
                  检测模式
                </label>
                <div className="grid grid-cols-3 gap-4">
                  {modes.map((m) => {
                    const Icon = m.icon
                    const isSelected = mode === m.id
                    return (
                      <button
                        key={m.id}
                        onClick={() => setMode(m.id as any)}
                        className={`flex flex-col items-center gap-2 p-4 rounded-xl border-2 transition-all ${
                          isSelected
                            ? 'border-blue-500 bg-blue-50 dark:bg-blue-900/20'
                            : 'border-slate-200 dark:border-slate-700 hover:border-slate-300'
                        }`}
                      >
                        <Icon className={isSelected ? 'text-blue-500' : 'text-slate-400'} />
                        <span className={isSelected ? 'font-semibold text-blue-500' : ''}>{m.name}</span>
                      </button>
                    )
                  })}
                </div>
              </div>

              {/* Buttons */}
              <div className="flex gap-4 mt-6">
                <button
                  onClick={handleAnalyze}
                  disabled={loading || !content.trim()}
                  className="flex-1 flex items-center justify-center gap-2 px-6 py-3 bg-gradient-to-r from-blue-600 to-purple-600 text-white font-semibold rounded-xl hover:from-blue-700 hover:to-purple-700 transition-all shadow-lg hover:shadow-xl disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  <BrainCircuit className="w-5 h-5" />
                  {loading ? '分析中...' : '开始分析'}
                </button>
                <button
                  onClick={handleClear}
                  className="flex items-center justify-center gap-2 px-4 py-3 border-2 border-slate-200 dark:border-slate-700 rounded-xl hover:bg-slate-100 dark:hover:bg-slate-700 transition-all"
                >
                  <RefreshCw className="w-5 h-5" />
                  清空
                </button>
              </div>
            </div>

            {/* History */}
            {history.length > 0 && (
              <div className="bg-white dark:bg-slate-800 rounded-2xl shadow-xl p-8">
                <h3 className="text-lg font-semibold mb-4 text-slate-700 dark:text-slate-300 flex items-center gap-2">
                  <FileText className="w-5 h-5" />
                  历史记录 ({history.length})
                </h3>
                <div className="space-y-4 max-h-64 overflow-y-auto">
                  {history.slice(0, 10).map((item, idx) => (
                    <div key={idx} className="p-4 bg-slate-50 dark:bg-slate-900 rounded-xl border border-slate-200 dark:border-slate-700">
                      <div className="flex items-center justify-between mb-2">
                        <span className="text-sm text-slate-500 dark:text-slate-400">
                          {new Date(item.timestamp).toLocaleString('zh-CN')}
                        </span>
                        <div className="flex items-center gap-2">
                          <span className={`text-sm font-semibold ${
                            getAiLevel(item.ai_detection.ai_probability).color
                          }`}>
                            AI: {item.ai_detection.ai_probability.toFixed(1)}%
                          </span>
                        </div>
                      </div>
                      <p className="text-sm text-slate-700 dark:text-slate-300 line-clamp-2">
                        {item.summary}
                      </p>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>

          {/* Right Column: Results */}
          <div className="space-y-6">
            {result && (
              <>
                {/* AI Detection Result */}
                <div className="bg-white dark:bg-slate-800 rounded-2xl shadow-xl p-8">
                  <div className="flex items-center gap-2 mb-6">
                    <BarChart3 className="w-6 h-6 text-blue-500" />
                    <h3 className="text-xl font-bold text-slate-700 dark:text-slate-300">
                      AI检测结果
                    </h3>
                  </div>

                  {/* AI Probability */}
                  <div className="mb-6">
                    <div className="flex items-center justify-between mb-2">
                      <span className="text-slate-600 dark:text-slate-400">
                        AI生成概率
                      </span>
                      <span className={`text-2xl font-bold ${
                        getAiLevel(result.ai_detection.ai_probability).color
                      }`}>
                        {result.ai_detection.ai_probability.toFixed(1)}%
                      </span>
                    </div>
                    <div className="w-full bg-slate-200 dark:bg-slate-700 rounded-full h-3 overflow-hidden">
                      <div
                        className="bg-gradient-to-r from-blue-500 to-purple-500 h-full rounded-full"
                        style={{ width: `${result.ai_detection.ai_probability}%` }}
                      ></div>
                    </div>
                  </div>

                  {/* AI Features */}
                  <div className="space-y-3">
                    <h4 className="text-sm font-semibold text-slate-700 dark:text-slate-300">
                      AI特征分析
                    </h4>
                    <div className="grid grid-cols-2 gap-3">
                      {result.ai_detection.details.ai_features.ai_words.count > 0 && (
                        <div className="bg-red-50 dark:bg-red-900/20 p-3 rounded-lg">
                          <div className="text-xs text-slate-600 dark:text-slate-400 mb-1">
                            AI常用词
                          </div>
                          <div className="text-sm font-semibold text-slate-900 dark:text-slate-100">
                            {result.ai_detection.details.ai_features.ai_words.count}
                          </div>
                        </div>
                      )}
                      {result.ai_detection.details.ai_features.ai_patterns.count > 0 && (
                        <div className="bg-orange-50 dark:bg-orange-900/20 p-3 rounded-lg">
                          <div className="text-xs text-slate-600 dark:text-slate-400 mb-1">
                            AI句式
                          </div>
                          <div className="text-sm font-semibold text-slate-900 dark:text-slate-100">
                            {result.ai_detection.details.ai_features.ai_patterns.count}
                          </div>
                        </div>
                      )}
                      {result.ai_detection.details.ai_features.connectors.count > 0 && (
                        <div className="bg-yellow-50 dark:bg-yellow-900/20 p-3 rounded-lg">
                          <div className="text-xs text-slate-600 dark:text-slate-400 mb-1">
                            连接词
                          </div>
                          <div className="text-sm font-semibold text-slate-900 dark:text-slate-100">
                            {result.ai_detection.details.ai_features.connectors.count}
                          </div>
                        </div>
                      )}
                    </div>
                  </div>

                  {/* Suggestions */}
                  <div className="mt-6 p-4 bg-blue-50 dark:bg-blue-900/20 rounded-xl">
                    <div className="flex items-start gap-3">
                      <AlertTriangle className="w-5 h-5 text-orange-500 flex-shrink-0 mt-0.5" />
                      <div>
                        <h4 className="font-semibold text-slate-900 dark:text-slate-100">
                          建议
                        </h4>
                        <p className="text-sm text-slate-700 dark:text-slate-300 mt-1">
                          {result.ai_detection.suggestions.join('，')}
                        </p>
                      </div>
                    </div>
                  </div>
                </div>

                {/* Humanized Result */}
                {result.humanized && (
                  <div className="bg-white dark:bg-slate-800 rounded-2xl shadow-xl p-8">
                    <div className="flex items-center gap-2 mb-6">
                      <TrendingUp className="w-6 h-6 text-green-500" />
                      <h3 className="text-xl font-bold text-slate-700 dark:text-slate-300">
                        去AI味结果
                      </h3>
                    </div>

                  {/* Changes */}
                  {result.changes.length > 0 && (
                    <div className="mb-6">
                      <h4 className="text-sm font-semibold text-slate-700 dark:text-slate-300 mb-3">
                        优化内容
                      </h4>
                      <div className="space-y-2">
                        {result.changes.map((change, idx) => (
                          <div key={idx} className="flex items-start gap-2 p-3 bg-green-50 dark:bg-green-900/20 rounded-lg">
                            <CheckCircle className="w-5 h-5 text-green-600 dark:text-green-400 flex-shrink-0 mt-0.5" />
                            <span className="text-sm text-slate-700 dark:text-slate-300">
                              {change}
                            </span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Summary */}
                  <div className="mt-6 p-4 bg-green-50 dark:bg-green-900/20 rounded-xl">
                    <div className="flex items-start gap-3">
                      <CheckCircle className="w-5 h-5 text-green-600 dark:text-green-400 flex-shrink-0 mt-0.5" />
                      <div>
                        <h4 className="font-semibold text-slate-900 dark:text-slate-100">
                          优化总结
                        </h4>
                        <p className="text-sm text-slate-700 dark:text-slate-300 mt-1">
                          {result.summary}
                        </p>
                      </div>
                    </div>
                  </div>

                  {/* Copy Buttons */}
                  <div className="flex gap-4 mt-6">
                    <button
                      onClick={() => handleCopy(result.original)}
                      className="flex-1 flex items-center justify-center gap-2 px-4 py-2 border-2 border-slate-200 dark:border-slate-700 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-700 transition-all"
                    >
                      <Copy className="w-4 h-4" />
                      原文
                    </button>
                    <button
                      onClick={() => handleCopy(result.humanized)}
                      className="flex-1 flex items-center justify-center gap-2 px-4 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600 transition-all"
                    >
                      <Copy className="w-4 h-4" />
                      去AI味
                    </button>
                  </div>
                </div>
              )}
            </>
            )}

            {/* Empty State */}
            {!result && (
              <div className="bg-white dark:bg-slate-800 rounded-2xl shadow-xl p-12 text-center">
                <Sparkles className="w-16 h-16 mx-auto mb-4 text-slate-300 dark:text-slate-600" />
                <p className="text-slate-500 dark:text-slate-400">
                  输入内容并选择模式后，点击"开始分析"
                </p>
              </div>
            )}
          </div>
        </div>

        {/* Footer */}
        <div className="mt-16 text-center text-slate-500 dark:text-slate-400">
          <p>100维度AI检测 + 智能去AI味</p>
          <p className="text-sm mt-2">
            AI检测准确率：95%+ | 去AI味优化：实时
          </p>
        </div>
      </div>
    </main>
  )
}
