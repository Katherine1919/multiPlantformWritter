import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'HumanWriter - 多平台内容适配工具',
  description: '一键适配Twitter/知乎/公众号/小红书，支持图片处理',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="zh-CN">
      <body>{children}</body>
    </html>
  )
}
