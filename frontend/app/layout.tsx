import './globals.css'
import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import { Providers } from './providers'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'AI Video Generator - Create Stunning Videos with AI',
  description: 'Professional AI-powered video creation platform. Create educational content, marketing videos, presentations, and more with our advanced Canvas Editor and Video Stitching Pipeline.',
  keywords: 'AI video generator, video creation, Canvas editor, automated video stitching, educational videos, marketing videos',
  authors: [{ name: 'AI Video Generator Team' }],
  openGraph: {
    title: 'AI Video Generator - Create Stunning Videos with AI',
    description: 'Professional AI-powered video creation platform',
    url: 'https://ai-video-generator.com',
    siteName: 'AI Video Generator',
    images: [
      {
        url: '/og-image.jpg',
        width: 1200,
        height: 630,
      },
    ],
    locale: 'en_US',
    type: 'website',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'AI Video Generator - Create Stunning Videos with AI',
    description: 'Professional AI-powered video creation platform',
    images: ['/og-image.jpg'],
  },
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" className="scroll-smooth">
      <body className={`${inter.className} antialiased`}>
        <Providers>
          {children}
        </Providers>
      </body>
    </html>
  )
}
