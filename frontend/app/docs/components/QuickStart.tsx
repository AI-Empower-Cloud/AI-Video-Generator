'use client'

import { motion } from 'framer-motion'
import { useInView } from 'framer-motion'
import { useRef } from 'react'
import { Clock, Play, CheckCircle, ArrowRight } from 'lucide-react'

const steps = [
  {
    step: 1,
    title: 'Get Your API Key',
    description: 'Sign up and get your free API key from the dashboard',
    time: '2 min',
    code: `// Get your API key from the dashboard
const API_KEY = 'your-api-key-here'`
  },
  {
    step: 2,
    title: 'Install SDK',
    description: 'Install our SDK for your preferred programming language',
    time: '1 min',
    code: `# Install via npm
npm install ai-video-generator

# Or via pip
pip install ai-video-generator`
  },
  {
    step: 3,
    title: 'Generate Your First Video',
    description: 'Create a video with just a few lines of code',
    time: '3 min',
    code: `import { VideoGenerator } from 'ai-video-generator'

const generator = new VideoGenerator(API_KEY)

const video = await generator.create({
  prompt: "A peaceful sunset over mountains",
  duration: 30,
  style: "cinematic"
})

console.log(video.url)`
  },
  {
    step: 4,
    title: 'Customize & Deploy',
    description: 'Fine-tune your video settings and integrate into your app',
    time: '5 min',
    code: `// Advanced configuration
const video = await generator.create({
  prompt: "Product demo video",
  duration: 60,
  style: "professional",
  resolution: "1080p",
  aspectRatio: "16:9",
  voiceover: {
    text: "Welcome to our product",
    voice: "professional-female"
  }
})`
  }
]

export default function QuickStart() {
  const ref = useRef(null)
  const isInView = useInView(ref, { once: true, amount: 0.2 })

  return (
    <section ref={ref} className="py-20 bg-white">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 50 }}
          animate={isInView ? { opacity: 1, y: 0 } : { opacity: 0, y: 50 }}
          transition={{ duration: 0.8 }}
          className="text-center mb-16"
        >
          <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">
            Quick Start Guide
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Get up and running with AI video generation in less than 10 minutes. 
            Follow these simple steps to create your first video.
          </p>
        </motion.div>

        <div className="space-y-12">
          {steps.map((step, index) => (
            <motion.div
              key={step.step}
              initial={{ opacity: 0, x: index % 2 === 0 ? -50 : 50 }}
              animate={isInView ? { opacity: 1, x: 0 } : { opacity: 0, x: index % 2 === 0 ? -50 : 50 }}
              transition={{ duration: 0.8, delay: index * 0.2 }}
              className={`grid grid-cols-1 lg:grid-cols-2 gap-12 items-center ${
                index % 2 === 1 ? 'lg:flex-row-reverse' : ''
              }`}
            >
              <div className={index % 2 === 1 ? 'lg:order-2' : ''}>
                <div className="flex items-center mb-4">
                  <div className="w-12 h-12 bg-gradient-to-r from-purple-600 to-blue-600 rounded-full flex items-center justify-center text-white font-bold text-xl mr-4">
                    {step.step}
                  </div>
                  <div className="flex items-center text-gray-500 text-sm">
                    <Clock className="w-4 h-4 mr-1" />
                    {step.time}
                  </div>
                </div>
                
                <h3 className="text-3xl font-bold text-gray-900 mb-4">
                  {step.title}
                </h3>
                
                <p className="text-lg text-gray-600 mb-6 leading-relaxed">
                  {step.description}
                </p>
                
                <div className="flex items-center space-x-4">
                  <button className="bg-gradient-to-r from-purple-600 to-blue-600 text-white px-6 py-3 rounded-lg font-semibold hover:from-purple-700 hover:to-blue-700 transition-all duration-200 flex items-center space-x-2">
                    <Play className="w-5 h-5" />
                    <span>Try This Step</span>
                  </button>
                  <button className="text-purple-600 hover:text-purple-700 font-semibold flex items-center space-x-1">
                    <span>Learn More</span>
                    <ArrowRight className="w-4 h-4" />
                  </button>
                </div>
              </div>

              <div className={index % 2 === 1 ? 'lg:order-1' : ''}>
                <div className="bg-gray-900 rounded-xl p-6 relative overflow-hidden">
                  <div className="flex items-center justify-between mb-4">
                    <div className="flex space-x-2">
                      <div className="w-3 h-3 bg-red-500 rounded-full" />
                      <div className="w-3 h-3 bg-yellow-500 rounded-full" />
                      <div className="w-3 h-3 bg-green-500 rounded-full" />
                    </div>
                    <span className="text-gray-400 text-sm">Step {step.step}</span>
                  </div>
                  
                  <pre className="text-green-400 text-sm leading-relaxed overflow-x-auto">
                    <code>{step.code}</code>
                  </pre>
                  
                  <div className="absolute top-4 right-4">
                    <CheckCircle className="w-5 h-5 text-green-400" />
                  </div>
                </div>
              </div>
            </motion.div>
          ))}
        </div>

        <motion.div
          initial={{ opacity: 0, y: 50 }}
          animate={isInView ? { opacity: 1, y: 0 } : { opacity: 0, y: 50 }}
          transition={{ duration: 0.8, delay: 0.8 }}
          className="mt-16 text-center"
        >
          <div className="bg-gradient-to-br from-purple-50 to-blue-50 rounded-2xl p-8 border border-purple-100">
            <h3 className="text-2xl font-bold text-gray-900 mb-4">
              🎉 Congratulations!
            </h3>
            <p className="text-lg text-gray-600 mb-6">
              You've successfully created your first AI-generated video. Ready to explore advanced features?
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <button className="bg-purple-600 text-white px-8 py-3 rounded-lg font-semibold hover:bg-purple-700 transition-colors duration-200">
                Explore Advanced Features
              </button>
              <button className="border-2 border-purple-600 text-purple-600 px-8 py-3 rounded-lg font-semibold hover:bg-purple-600 hover:text-white transition-colors duration-200">
                View More Examples
              </button>
            </div>
          </div>
        </motion.div>
      </div>
    </section>
  )
}
