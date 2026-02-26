'use client'

import { useState, useRef } from 'react'
import { Upload, Image as ImageIcon, Sparkles, Download, Trash2 } from 'lucide-react'

interface ImageUploadProps {
  onImageSelect: (url: string, file: File) => void
  selectedImage?: string
  onRemove?: () => void
}

export default function ImageUpload({ onImageSelect, selectedImage, onRemove }: ImageUploadProps) {
  const [loading, setLoading] = useState(false)
  const [generating, setGenerating] = useState(false)
  const fileInputRef = useRef<HTMLInputElement>(null)

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (!file) return

    const reader = new FileReader()
    reader.onloadend = () => {
      onImageSelect(reader.result as string, file)
    }
    reader.readAsDataURL(file)
  }

  const handleGenerateImage = async (prompt: string) => {
    setGenerating(true)

    try {
      // 调用DALL-E API
      // const response = await fetch('/api/generate-image', {
      //   method: 'POST',
      //   body: JSON.stringify({ prompt })
      // })
      // const data = await response.json()

      // 模拟生成
      await new Promise(resolve => setTimeout(resolve, 2000))

      // 这里应该返回生成的图片URL
      console.log('Generated image for:', prompt)
    } catch (error) {
      console.error('生成图片失败:', error)
      alert('生成图片失败')
    } finally {
      setGenerating(false)
    }
  }

  return (
    <div className="space-y-4">
      {/* 图片预览 */}
      {selectedImage && (
        <div className="relative group">
          <img
            src={selectedImage}
            alt="Preview"
            className="w-full h-64 object-cover rounded-xl border-2 border-slate-200 dark:border-slate-700"
          />
          {onRemove && (
            <button
              onClick={onRemove}
              className="absolute top-2 right-2 p-2 bg-red-500 text-white rounded-lg opacity-0 group-hover:opacity-100 transition-opacity"
            >
              <Trash2 className="w-4 h-4" />
            </button>
          )}
        </div>
      )}

      {/* 上传按钮 */}
      <div className="flex gap-4">
        <button
          onClick={() => fileInputRef.current?.click()}
          className="flex-1 flex items-center justify-center gap-2 p-4 border-2 border-dashed border-slate-300 dark:border-slate-600 rounded-xl hover:border-blue-500 transition-all"
        >
          <Upload className="w-5 h-5" />
          上传图片
        </button>

        <button
          onClick={() => {
            const promptText = window.prompt('输入图片描述：') || ''
            if (promptText) handleGenerateImage(promptText)
          }}
          disabled={generating}
          className="flex-1 flex items-center justify-center gap-2 p-4 bg-gradient-to-r from-purple-600 to-pink-600 text-white rounded-xl hover:from-purple-700 hover:to-pink-700 transition-all disabled:opacity-50"
        >
          <Sparkles className="w-5 h-5" />
          {generating ? '生成中...' : 'AI生成'}
        </button>
      </div>

      <input
        ref={fileInputRef}
        type="file"
        accept="image/*"
        onChange={handleFileSelect}
        className="hidden"
      />

      {/* 图片比例选择 */}
      <div className="flex gap-2">
        <button className="flex-1 py-2 px-4 border-2 border-slate-200 dark:border-slate-700 rounded-lg hover:border-blue-500 transition-all">
          16:9
        </button>
        <button className="flex-1 py-2 px-4 border-2 border-slate-200 dark:border-slate-700 rounded-lg hover:border-blue-500 transition-all">
          1:1
        </button>
        <button className="flex-1 py-2 px-4 border-2 border-slate-200 dark:border-slate-700 rounded-lg hover:border-blue-500 transition-all">
          3:4
        </button>
      </div>
    </div>
  )
}
