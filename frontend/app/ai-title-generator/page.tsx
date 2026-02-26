'use client'

import { useState } from 'react'
import {
  Sparkles, Lightbulb, Zap, Copy, RefreshCw,
  TrendingUp, Hash, ChevronRight
} from 'lucide-react'

export default function AITitleGeneratorPage() {
  const [content, setContent] = useState('')
  const [style, setStyle] = useState<'clickbait' | 'professional' | 'emotional' | 'question'>('clickbait')
  const [count, setCount] = useState(5)
  const [titles, setTitles] = useState<any[]>([])
  const [loading, setLoading] = useState(false)

  const styles = [
    { id: 'clickbait', name: '爆款标题', icon: Sparkles, color: 'from-orange-500 to-red-500' },
    { id: 'professional', name: '专业标题', icon: Lightbulb, color: 'from-blue-500 to-cyan-500' },
    { id: 'emotional', name: '情感标题', icon: Zap, color: 'from-pink-500 to-rose-500' },
    { id: 'question', name: '疑问标题', icon: TrendingUp, color: 'from-purple-500 to-indigo-500' }
  ]

  const handleGenerate = async () => {
    if (!content.trim()) return

    setLoading(true)
    setTitles([])

    try {
      const response = await fetch('http://localhost:8000/api/v1/generate-titles', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ content, count: parseInt(count.toString()), style })
      })
      const data = await response.json()

      if (data.success) {
        setTitles(data.data.titles)
      } else {
        alert('生成失败：' + (data.detail || '未知错误'))
      }
    } catch (error) {
      console.error('生成失败:', error)
      alert('网络错误，请检查后端服务')
    } finally {
      setLoading(false)
    }
  }

  const handleCopy = async (title: string) => {
    try {
      await navigator.clipboard.writeText(title)
      alert('已复制：' + title)
    } catch (err) {
      alert('复制失败')
    }
  }

  const handleClear = () => {
    setContent('')
    setTitles([])
  }

  const getStyleColor = (style: string) => {
    const colorMap: Record<string, string> = {
      'clickbait': 'text-orange-500',
      'professional': 'text-blue-500',
      'emotional': 'text-pink-500',
      'question': 'text-purple-500'
    }
    return colorMap[style] || 'text-slate-500'
  }

  return (
    <main className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 dark:from-slate-900 dark:to-slate-800 p-8">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-5xl font-bold mb-4 bg-gradient-to-r from-orange-500 to-red-500 bg-clip-text text-transparent">
            AI 标题生成器
          </h1>
          <p className="text-xl text-slate-600 dark:text-slate-400">
            一键生成爆款标题 · 4种风格
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Left Column: Input */}
          <div className="space-y-8">
            {/* Content Input */}
            <div className="bg-white dark:bg-slate-800 rounded-2xl shadow-xl p-8">
              <label className="block text-lg font-semibold mb-4 text-slate-700 dark:text-slate-300">
                输入文章内容
              </label>
              <textarea
                value={content}
                onChange={(e) => setContent(e.target.value)}
                placeholder="粘贴你的文章内容，AI会提取关键词并生成标题..."
                className="w-full h-48 p-4 border-2 border-slate-200 dark:border-slate-700 rounded-xl focus:border-orange-500 focus:outline-none resize-none bg-slate-50 dark:bg-slate-900 text-slate-800 dark:text-slate-200"
              />
            </div>

            {/* Style Selection */}
            <div className="bg-white dark:bg-slate-800 rounded-2xl shadow-xl p-8">
              <label className="block text-lg font-semibold mb-4 text-slate-700 dark:text-slate-300">
                选择标题风格
              </label>
              <div className="grid grid-cols-2 gap-4">
                {styles.map((s) => {
                  const Icon = s.icon
                  const isSelected = style === s.id
                  return (
                    <button
                      key={s.id}
                      onClick={() => setStyle(s.id as any)}
                      className={`flex flex-col items-center gap-2 p-4 rounded-xl border-2 transition-all ${
                        isSelected
                          ? `border-${isSelected ? 'orange' : 'blue'}-500 bg-gradient-to-br ${s.color} text-white`
                          : 'border-slate-200 dark:border-slate-700 hover:border-slate-300'
                      }`}
                    >
                      <Icon className={isSelected ? 'text-white' : 'text-slate-400'} />
                      <span className={isSelected ? 'font-semibold' : ''}>{s.name}</span>
                    </button>
                  )
                })}
              </div>
            </div>

            {/* Count Selection */}
            <div className="bg-white dark:bg-slate-800 rounded-2xl shadow-xl p-8">
              <label className="block text-lg font-semibold mb-4 text-slate-700 dark:text-slate-300">
                生成标题数量
              </label>
              <div className="flex items-center gap-4">
                <input
                  type="range"
                  min="1"
                  max="10"
                  value={count}
                  onChange={(e) => setCount(parseInt(e.target.value))}
                  className="flex-1"
                />
                <span className="text-2xl font-bold text-slate-700 dark:text-slate-300">
                  {count}
                </span>
              </div>
            </div>

            {/* Buttons */}
            <div className="flex gap-4">
              <button
                onClick={handleGenerate}
                disabled={loading || !content.trim()}
                className="flex-1 flex items-center justify-center gap-2 px-6 py-3 bg-gradient-to-r from-orange-500 to-red-500 text-white font-semibold rounded-xl hover:from-orange-600 hover:to-red-600 transition-all shadow-lg hover:shadow-xl disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <Lightbulb className="w-5 h-5" />
                {loading ? '生成中...' : '生成标题'}
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

          {/* Right Column: Results */}
          <div className="space-y-6">
            {titles.length > 0 && (
              <>
                {/* Results Summary */}
                <div className="bg-white dark:bg-slate-800 rounded-2xl shadow-xl p-8">
                  <div className="flex items-center justify-between mb-4">
                    <div className="flex items-center gap-2">
                      <Hash className="text-purple-500" />
                      <h3 className="text-lg font-bold text-slate-700 dark:text-slate-300">
                        生成结果
                      </h3>
                    </div>
                    <span className={`text-sm font-semibold ${getStyleColor(style)}`}>
                      {style}风格
                    </span>
                  </div>
                  <p className="text-sm text-slate-500 dark:text-slate-400">
                    生成了{titles.length}个标题
                  </p>
                </div>

                {/* Title Cards */}
                {titles.map((title, idx) => (
                  <div
                    key={idx}
                    className="bg-white dark:bg-slate-800 rounded-2xl shadow-xl p-6 hover:shadow-2xl transition-all"
                  >
                    <div className="flex items-start justify-between mb-3">
                      <span className={`text-2xl font-bold ${getStyleColor(title.style)}`}>
                        {title.title}
                      </span>
                      <div className="flex items-center gap-2">
                        <span className="text-sm text-slate-400 dark:text-slate-500">
                          {title.style}
                        </span>
                        <span className="text-sm font-semibold text-green-500">
                          {title.score}分
                        </span>
                      </div>
                    </div>
                    <div className="flex gap-2 mt-4">
                      <button
                        onClick={() => handleCopy(title.title)}
                        className="flex-1 flex items-center justify-center gap-2 px-4 py-2 border-2 border-slate-200 dark:border-slate-700 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-700 transition-all"
                      >
                        <Copy className="w-4 h-4" />
                        复制
                      </button>
                      <button
                        onClick={() => handleCopy(title.title)}
                        className="flex-1 flex items-center justify-center gap-2 px-4 py-2 bg-gradient-to-r from-orange-500 to-red-500 text-white rounded-lg hover:from-orange-600 hover:to-red-600 transition-all"
                      >
                        <ChevronRight className="w-4 h-4" />
                        使用
                      </button>
                    </div>
                  </div>
                ))}
              </>
            )}

            {/* Empty State */}
            {titles.length === 0 && (
              <div className="bg-white dark:bg-slate-800 rounded-2xl shadow-xl p-12 text-center">
                <Lightbulb className="w-16 h-16 mx-auto mb-4 text-slate-300 dark:text-slate-600" />
                <p className="text-slate-500 dark:text-slate-400">
                  输入文章内容并选择风格后，点击"生成标题"
                </p>
                <p className="text-sm text-slate-400 dark:text-slate-500 mt-2">
                  支持：爆款标题 / 专业标题 / 情感标题 / 疑问标题
                </p>
              </div>
            )}
          </div>
        </div>

        {/* Footer */}
        <div className="mt-16 text-center text-slate-500 dark:text-slate-400">
          <p>AI标题生成器 · 基于关键词智能生成</p>
          <p className="text-sm mt-2">支持4种风格 · 实时生成 · 一键复制</p>
        </div>
      </div>
    </main>
  )
}
