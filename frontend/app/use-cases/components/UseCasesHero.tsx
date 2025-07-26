'use client'

import { motion } from 'framer-motion'
import { Play, Sparkles, Zap } from 'lucide-react'

export default function UseCasesHero() {
  return (
    <section className="relative min-h-screen flex items-center justify-center bg-gradient-to-br from-purple-900 via-blue-900 to-indigo-900 overflow-hidden">
      {/* Background Effects */}
      <div className="absolute inset-0">
        <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-purple-500/20 rounded-full blur-3xl animate-pulse" />
        <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-blue-500/20 rounded-full blur-3xl animate-pulse delay-1000" />
        <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-indigo-500/20 rounded-full blur-3xl animate-pulse delay-500" />
      </div>

      <div className="relative z-10 max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
          <motion.div
            initial={{ opacity: 0, x: -50 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.8 }}
          >
            <h1 className="text-5xl md:text-6xl font-bold text-white mb-6">
              Endless
              <span className="bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent">
                {' '}Possibilities
              </span>
            </h1>
            <p className="text-xl md:text-2xl text-gray-300 mb-8 leading-relaxed">
              From marketing campaigns to educational content, social media to enterprise training—
              discover how AI video generation transforms every industry.
            </p>
            
            <div className="flex flex-col sm:flex-row gap-4 mb-12">
              <button className="bg-gradient-to-r from-purple-600 to-pink-600 text-white px-8 py-4 rounded-lg font-semibold hover:from-purple-700 hover:to-pink-700 transition-all duration-200 flex items-center justify-center space-x-2">
                <Play className="w-5 h-5" />
                <span>Watch Demo</span>
              </button>
              <button className="border-2 border-white text-white px-8 py-4 rounded-lg font-semibold hover:bg-white hover:text-purple-900 transition-all duration-200">
                Explore Use Cases
              </button>
            </div>

            <div className="grid grid-cols-3 gap-6">
              <div className="text-center">
                <div className="text-3xl font-bold text-white mb-2">500+</div>
                <div className="text-purple-200">Use Cases</div>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold text-white mb-2">50+</div>
                <div className="text-purple-200">Industries</div>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold text-white mb-2">99%</div>
                <div className="text-purple-200">Success Rate</div>
              </div>
            </div>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, x: 50 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.8, delay: 0.2 }}
            className="relative"
          >
            <div className="relative z-10 bg-white/10 backdrop-blur-lg rounded-2xl p-8 border border-white/20">
              <div className="grid grid-cols-2 gap-4">
                <div className="bg-gradient-to-br from-purple-500 to-pink-500 rounded-xl p-6 text-white">
                  <Sparkles className="w-8 h-8 mb-4" />
                  <h3 className="font-semibold mb-2">Marketing</h3>
                  <p className="text-sm opacity-90">Product demos, ads, social content</p>
                </div>
                <div className="bg-gradient-to-br from-blue-500 to-indigo-500 rounded-xl p-6 text-white">
                  <Zap className="w-8 h-8 mb-4" />
                  <h3 className="font-semibold mb-2">Education</h3>
                  <p className="text-sm opacity-90">Training videos, courses, tutorials</p>
                </div>
                <div className="bg-gradient-to-br from-green-500 to-teal-500 rounded-xl p-6 text-white">
                  <Sparkles className="w-8 h-8 mb-4" />
                  <h3 className="font-semibold mb-2">Entertainment</h3>
                  <p className="text-sm opacity-90">Stories, animations, content</p>
                </div>
                <div className="bg-gradient-to-br from-orange-500 to-red-500 rounded-xl p-6 text-white">
                  <Zap className="w-8 h-8 mb-4" />
                  <h3 className="font-semibold mb-2">Enterprise</h3>
                  <p className="text-sm opacity-90">Training, presentations, comms</p>
                </div>
              </div>
            </div>
            
            {/* Decorative elements */}
            <div className="absolute -top-4 -right-4 w-24 h-24 bg-gradient-to-br from-purple-400 to-pink-400 rounded-full blur-xl opacity-60" />
            <div className="absolute -bottom-4 -left-4 w-32 h-32 bg-gradient-to-br from-blue-400 to-indigo-400 rounded-full blur-xl opacity-60" />
          </motion.div>
        </div>
      </div>
    </section>
  )
}
