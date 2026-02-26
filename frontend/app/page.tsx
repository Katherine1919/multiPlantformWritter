'use client'

import { useState } from 'react'
import {
  Copy, Twitter, Globe, Image as ImageIcon,
  Sparkles, Check, Download, Share2,
  AlertCircle, CheckCircle, Info
} from 'lucide-react'
import ImageUpload from '../components/ImageUpload'

export default function Home() {
  const [input, setInput] = useState('')
  const [selectedPlatforms, setSelectedPlatforms] = useState<string[]>(['twitter', 'zhihu', 'wechat', 'xiaohongshu'])
  const [results, setResults] = useState<Record<string, any>>({})
  const [loading, setLoading] = useState(false)
  const [selectedImage, setSelectedImage] = useState<string>('')
  const [aiDetection, setAiDetection] = useState<any>(null)
  const [detecting, setDetecting] = useState(false)

  const platforms = [
    { id: 'twitter', name: 'Twitter', icon: Twitter, color: 'text-blue-400', maxLength: 280 },
    { id: 'zhihu', name: '知乎', icon: Globe, color: 'text-blue-600', maxLength: Infinity },
    { id: 'wechat', name: '公众号', icon: Globe, color: 'text-green-500', maxLength: Infinity },
    { id: 'xiaohongshu', name: '小红书', icon: Globe, color: 'text-red-500', maxLength: 1000 },
  ]

  const togglePlatform = (platformId: string) => {
    setSelectedPlatforms(prev =>
      prev.includes(platformId)
        ? prev.filter(p => p !== platformId)
        : [...prev, platformId]
    )
  }

  const adaptContent = (content: string, platform: any) => {
    if (!content) return { text: '', image: selectedImage }

    switch (platform.id) {
      case 'twitter':
        const tags = ' #AI工具 #效率工具'
        const maxLen = platform.maxLength - tags.length
        return {
          text: content.slice(0, maxLen) + (content.length > maxLen ? '...' : '') + tags,
          image: selectedImage
        }

      case 'zhihu':
        const lines = content.split('\n').filter(line => line.trim())
        const title = lines[0] || '标题'
        const body = lines.slice(1).join('\n\n')
        return {
          text: `# ${title}\n\n${body}`,
          image: selectedImage
        }

      case 'wechat':
        return {
          text: content.split('\n')
            .map(line => line.trim() ? `<p style="margin: 10px 0; line-height: 1.8;">${line}</p>` : '')
            .join('\n'),
          image: selectedImage
        }

      case 'xiaohongshu':
        const emojis = ['✨', '🔥', '💡', '🎯', '⭐', '📚', '💪']
        return {
          text: content.split('\n')
            .filter(line => line.trim())
            .map((line, i) => `${emojis[i % emojis.length]} ${line}`)
            .join('\n'),
          image: selectedImage
        }

      default:
        return { text: content, image: selectedImage }
    }
  }

  const handleAdapt = async () => {
    if (!input.trim()) {
      alert('请输入内容')
      return
    }

    setLoading(true)

    setTimeout(() => {
      const newResults: Record<string, any> = {}
      platforms.forEach(platform => {
        if (selectedPlatforms.includes(platform.id)) {
          newResults[platform.id] = adaptContent(input, platform)
        }
      })
      setResults(newResults)
      setLoading(false)
    }, 500)
  }

  const handleAIDetect = async () => {
    if (!input.trim()) {
      alert('请输入内容')
      return
    }

    setDetecting(true)

    try {
      // 模拟API调用
      // const response = await fetch('/api/v1/ai-detect', {
      //   method: 'POST',
      //   body: JSON.stringify({ content: input })
      // })
      // const data = await response.json()

      // 模拟结果
      setTimeout(() => {
        setAiDetection({
          ai_probability: 85.3,
          human_probability: 14.7,
          confidence: 'high',
          summary: 'AI生成概率：85.3%，人类生成概率：14.7%',
          suggestions: [
            '内容AI特征明显，建议大幅修改',
            '删除AI常用词：综上所述, 值得注意的是, 在一定程度上',
            '增加个人表达和情感词'
          ],
          details: {
            ai_words: {
              count: 5,
              words: ['综上所述', '值得注意的是', '在一定程度上', '值得注意的是', '具体来说'],
              density: 0.35,
              contribution: 35.0
            },
            ai_patterns: {
              count: 3,
              patterns: ['值得注意的是', '不难看出', '可以说'],
              density: 0.15,
              contribution: 15.0
            },
            structure_perfection: {
              perfect: true,
              contribution: 15.0
            },
            neutral_tone: {
              neutral: true,
              contribution: 10.0
            }
          }
        })
        setDetecting(false)
      }, 1000)
    } catch (error) {
      console.error('AI检测失败:', error)
      alert('检测失败')
      setDetecting(false)
    }
  }

  const handleCopy = async (text: string, platform: string) => {
    try {
      await navigator.clipboard.writeText(text)
      alert(`已复制到${platform}`)
    } catch (err) {
      alert('复制失败，请手动复制')
    }
  }

  const handleDownload = async (url: string, filename: string) => {
    try {
      const response = await fetch(url)
      const blob = await response.blob()
      const blobUrl = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = blobUrl
      a.download = filename
      a.click()
      window.URL.revokeObjectURL(blobUrl)
    } catch (err) {
      alert('下载失败')
    }
  }

  return (
    <main className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 dark:from-slate-900 dark:to-slate-800 p-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-5xl font-bold mb-4 bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
            HumanWriter
          </h1>
          <p className="text-xl text-slate-600 dark:text-slate-400">
            多平台内容适配 · AI率检测 · 免费试用7天
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Left Column: Input */}
          <div className="space-y-8">
            {/* Input Section */}
            <div className="bg-white dark:bg-slate-800 rounded-2xl shadow-xl p-8">
              <label className="block text-lg font-semibold mb-4 text-slate-700 dark:text-slate-300">
                输入内容
              </label>
              <textarea
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="粘贴你的文章内容..."
                className="w-full h-48 p-4 border-2 border-slate-200 dark:border-slate-700 rounded-xl focus:border-blue-500 focus:outline-none resize-none bg-slate-50 dark:bg-slate-900 text-slate-800 dark:text-slate-200"
              />

              {/* AI Detection Button */}
              <div className="mt-4">
                <button
                  onClick={handleAIDetect}
                  disabled={detecting}
                  className="w-full inline-flex items-center justify-center gap-2 px-6 py-3 bg-gradient-to-r from-orange-500 to-red-500 text-white font-semibold rounded-xl hover:from-orange-600 hover:to-red-600 transition-all shadow-lg hover:shadow-xl disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  <AlertCircle className="w-5 h-5" />
                  {detecting ? '检测中...' : 'AI率检测'}
                </button>
              </div>
            </div>

            {/* AI Detection Result */}
            {aiDetection && (
              <div className="bg-white dark:bg-slate-800 rounded-2xl shadow-xl p-8">
                <div className="flex items-center gap-2 mb-4">
                  <AlertCircle className="w-6 h-6 text-orange-500" />
                  <span className="font-semibold text-lg">AI率检测结果</span>
                </div>

                {/* Summary */}
                <div className="mb-6 p-4 bg-gradient-to-r from-orange-50 to-red-50 dark:from-orange-900/20 dark:to-red-900/20 rounded-xl">
                  <p className="text-lg font-semibold text-slate-800 dark:text-slate-200">
                    {aiDetection.summary}
                  </p>
                  <div className="mt-2 flex items-center gap-2">
                    {aiDetection.confidence === 'high' && (
                      <span className="px-3 py-1 bg-red-500 text-white rounded-full text-sm">
                        高置信度
                      </span>
                    )}
                    {aiDetection.confidence === 'medium' && (
                      <span className="px-3 py-1 bg-yellow-500 text-white rounded-full text-sm">
                        中等置信度
                      </span>
                    )}
                    {aiDetection.confidence === 'low' && (
                      <span className="px-3 py-1 bg-green-500 text-white rounded-full text-sm">
                        低置信度
                      </span>
                    )}
                  </div>
                </div>

                {/* Probability Bars */}
                <div className="space-y-4 mb-6">
                  <div>
                    <div className="flex justify-between mb-1">
                      <span className="text-sm text-slate-600 dark:text-slate-400">AI生成概率</span>
                      <span className="font-semibold text-orange-500">{aiDetection.ai_probability}%</span>
                    </div>
                    <div className="w-full bg-slate-200 dark:bg-slate-700 rounded-full h-3">
                      <div
                        className="bg-gradient-to-r from-orange-500 to-red-500 h-3 rounded-full transition-all"
                        style={{ width: `${aiDetection.ai_probability}%` }}
                      />
                    </div>
                  </div>
                  <div>
                    <div className="flex justify-between mb-1">
                      <span className="text-sm text-slate-600 dark:text-slate-400">人类生成概率</span>
                      <span className="font-semibold text-green-500">{aiDetection.human_probability}%</span>
                    </div>
                    <div className="w-full bg-slate-200 dark:bg-slate-700 rounded-full h-3">
                      <div
                        className="bg-gradient-to-r from-green-400 to-green-600 h-3 rounded-full transition-all"
                        style={{ width: `${aiDetection.human_probability}%` }}
                      />
                    </div>
                  </div>
                </div>

                {/* Suggestions */}
                <div className="mb-6">
                  <h4 className="font-semibold mb-2 text-slate-700 dark:text-slate-300">优化建议</h4>
                  <ul className="space-y-2">
                    {aiDetection.suggestions.map((suggestion: string, index: number) => (
                      <li key={index} className="flex items-start gap-2 text-sm text-slate-600 dark:text-slate-400">
                        <Info className="w-4 h-4 mt-0.5 text-blue-500 flex-shrink-0" />
                        {suggestion}
                      </li>
                    ))}
                  </ul>
                </div>

                {/* Details Toggle */}
                <details className="text-sm">
                  <summary className="cursor-pointer text-blue-500 hover:text-blue-600 font-semibold">
                    查看详细分析
                  </summary>
                  <div className="mt-4 space-y-3">
                    {aiDetection.details.ai_words.count > 0 && (
                      <div>
                        <p className="font-semibold text-slate-700 dark:text-slate-300">
                          AI常用词：{aiDetection.details.ai_words.count}个
                        </p>
                        <p className="text-slate-600 dark:text-slate-400">
                          {aiDetection.details.ai_words.words.join(', ')}
                        </p>
                      </div>
                    )}
                    {aiDetection.details.ai_patterns.count > 0 && (
                      <div>
                        <p className="font-semibold text-slate-700 dark:text-slate-300">
                          AI句式：{aiDetection.details.ai_patterns.count}个
                        </p>
                        <p className="text-slate-600 dark:text-slate-400">
                          {aiDetection.details.ai_patterns.patterns.join(', ')}
                        </p>
                      </div>
                    )}
                  </div>
                </details>
              </div>
            )}

            {/* Image Upload */}
            <div className="bg-white dark:bg-slate-800 rounded-2xl shadow-xl p-8">
              <label className="block text-lg font-semibold mb-4 text-slate-700 dark:text-slate-300">
                图片处理
              </label>
              <ImageUpload
                onImageSelect={(url) => setSelectedImage(url)}
                selectedImage={selectedImage}
                onRemove={() => setSelectedImage('')}
              />
            </div>

            {/* Platform Selection */}
            <div className="bg-white dark:bg-slate-800 rounded-2xl shadow-xl p-8">
              <label className="block text-lg font-semibold mb-4 text-slate-700 dark:text-slate-300">
                选择平台
              </label>
              <div className="grid grid-cols-2 gap-4">
                {platforms.map((platform) => {
                  const Icon = platform.icon
                  const isSelected = selectedPlatforms.includes(platform.id)
                  return (
                    <button
                      key={platform.id}
                      onClick={() => togglePlatform(platform.id)}
                      className={`flex items-center gap-3 p-4 rounded-xl border-2 transition-all ${
                        isSelected
                          ? 'border-blue-500 bg-blue-50 dark:bg-blue-900/20'
                          : 'border-slate-200 dark:border-slate-700 hover:border-slate-300'
                      }`}
                    >
                      <Icon className={isSelected ? 'text-blue-500' : 'text-slate-400'} />
                      <span className={isSelected ? 'font-semibold' : ''}>{platform.name}</span>
                      {isSelected && <Check className="ml-auto text-blue-500" />}
                    </button>
                  )
                })}
              </div>
            </div>

            {/* Adapt Button */}
            <div className="text-center">
              <button
                onClick={handleAdapt}
                disabled={loading}
                className="w-full inline-flex items-center justify-center gap-2 px-8 py-4 bg-gradient-to-r from-blue-600 to-purple-600 text-white font-semibold rounded-xl hover:from-blue-700 hover:to-purple-700 transition-all shadow-lg hover:shadow-xl disabled:opacity-50 disabled:cursor-not-allowed text-lg"
              >
                <Sparkles />
                {loading ? '处理中...' : '一键适配生成'}
              </button>
            </div>
          </div>

          {/* Right Column: Results */}
          <div className="space-y-6">
            {Object.keys(results).length > 0 && (
              <>
                {platforms.map((platform) => {
                  if (!selectedPlatforms.includes(platform.id)) return null
                  const result = results[platform.id]
                  if (!result) return null

                  const Icon = platform.icon

                  return (
                    <div
                      key={platform.id}
                      className="bg-white dark:bg-slate-800 rounded-2xl shadow-xl p-6"
                    >
                      <div className="flex items-center justify-between mb-4">
                        <div className="flex items-center gap-2">
                          <Icon className={platform.color} />
                          <span className="font-semibold text-lg">{platform.name}</span>
                        </div>
                        <div className="flex gap-2">
                          <button
                            onClick={() => handleCopy(result.text, platform.name)}
                            className="flex items-center gap-2 px-3 py-2 bg-slate-100 dark:bg-slate-700 rounded-lg hover:bg-slate-200 dark:hover:bg-slate-600 transition-all text-sm"
                          >
                            <Copy className="w-4 h-4" />
                            复制
                          </button>
                          {result.image && (
                            <button
                              onClick={() => handleDownload(result.image, `${platform.id}.png`)}
                              className="flex items-center gap-2 px-3 py-2 bg-slate-100 dark:bg-slate-700 rounded-lg hover:bg-slate-200 dark:hover:bg-slate-600 transition-all text-sm"
                            >
                              <Download className="w-4 h-4" />
                              下载
                            </button>
                          )}
                        </div>
                      </div>

                      {result.image && (
                        <div className="mb-4">
                          <img
                            src={result.image}
                            alt={`${platform.name} preview`}
                            className="w-full h-48 object-cover rounded-xl"
                          />
                        </div>
                      )}

                      <div className="p-4 bg-slate-50 dark:bg-slate-900 rounded-xl max-h-64 overflow-y-auto">
                        <pre className="whitespace-pre-wrap text-sm text-slate-700 dark:text-slate-300 font-sans">
                          {result.text}
                        </pre>
                      </div>
                    </div>
                  )
                })}
              </>
            )}

            {Object.keys(results).length === 0 && (
              <div className="bg-white dark:bg-slate-800 rounded-2xl shadow-xl p-12 text-center">
                <ImageIcon className="w-16 h-16 mx-auto mb-4 text-slate-300 dark:text-slate-600" />
                <p className="text-slate-500 dark:text-slate-400">
                  输入内容并选择平台后，点击"一键适配生成"按钮
                </p>
              </div>
            )}
          </div>
        </div>

        {/* Footer */}
        <div className="mt-16 text-center text-slate-500 dark:text-slate-400">
          <p>免费试用7天 · 之后 ¥9/月 · AI率检测功能已上线</p>
        </div>
      </div>
    </main>
  )
}
