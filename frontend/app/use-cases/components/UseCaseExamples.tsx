'use client'

import { motion } from 'framer-motion'
import { useInView } from 'framer-motion'
import { useRef } from 'react'
import { Play, Clock, Users, ArrowRight } from 'lucide-react'

const examples = [
  {
    category: 'Marketing',
    title: 'Product Launch Campaign',
    description: 'Created a series of product demo videos for a tech startup\'s new app launch.',
    metrics: {
      timeaved: '85% faster',
      engagement: '340% increase',
      conversions: '150% boost'
    },
    video: '/api/placeholder/600/400',
    duration: '2:30'
  },
  {
    category: 'Education',
    title: 'Online Course Content',
    description: 'Generated 50+ educational videos for a professional certification program.',
    metrics: {
      timeSaved: '90% faster',
      completion: '75% rate',
      satisfaction: '4.8/5 rating'
    },
    video: '/api/placeholder/600/400',
    duration: '15:45'
  },
  {
    category: 'Social Media',
    title: 'Viral Content Series',
    description: 'Created engaging short-form content that gained millions of views across platforms.',
    metrics: {
      reach: '2.5M views',
      shares: '50K shares',
      followers: '25K new'
    },
    video: '/api/placeholder/600/400',
    duration: '0:30'
  },
  {
    category: 'Corporate',
    title: 'Training Videos',
    description: 'Developed comprehensive onboarding content for a global company\'s new employees.',
    metrics: {
      efficiency: '60% faster',
      retention: '85% improvement',
      satisfaction: '95% positive'
    },
    video: '/api/placeholder/600/400',
    duration: '8:20'
  }
]

export default function UseCaseExamples() {
  const ref = useRef(null)
  const isInView = useInView(ref, { once: true, amount: 0.2 })

  return (
    <section ref={ref} className="py-20 bg-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 50 }}
          animate={isInView ? { opacity: 1, y: 0 } : { opacity: 0, y: 50 }}
          transition={{ duration: 0.8 }}
          className="text-center mb-16"
        >
          <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">
            Real Results
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            See how our clients have transformed their content creation process and achieved 
            measurable results with AI-generated videos.
          </p>
        </motion.div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
          {examples.map((example, index) => (
            <motion.div
              key={example.title}
              initial={{ opacity: 0, y: 50 }}
              animate={isInView ? { opacity: 1, y: 0 } : { opacity: 0, y: 50 }}
              transition={{ duration: 0.6, delay: index * 0.2 }}
              className="group bg-gradient-to-br from-gray-50 to-blue-50 rounded-2xl overflow-hidden shadow-lg hover:shadow-2xl transition-all duration-300"
            >
              {/* Video Thumbnail */}
              <div className="relative aspect-video bg-gradient-to-br from-purple-400 to-blue-500 flex items-center justify-center">
                <Play className="w-16 h-16 text-white group-hover:scale-110 transition-transform duration-300" />
                <div className="absolute bottom-4 right-4 bg-black/50 text-white px-3 py-1 rounded-lg text-sm flex items-center space-x-1">
                  <Clock className="w-4 h-4" />
                  <span>{example.duration}</span>
                </div>
                <div className="absolute top-4 left-4 bg-white/20 backdrop-blur-lg text-white px-3 py-1 rounded-lg text-sm font-semibold">
                  {example.category}
                </div>
              </div>

              <div className="p-8">
                <h3 className="text-2xl font-bold text-gray-900 mb-3 group-hover:text-purple-700 transition-colors duration-300">
                  {example.title}
                </h3>
                
                <p className="text-gray-600 mb-6 leading-relaxed">
                  {example.description}
                </p>

                {/* Metrics */}
                <div className="grid grid-cols-3 gap-4 mb-6">
                  {Object.entries(example.metrics).map(([key, value]) => (
                    <div key={key} className="text-center">
                      <div className="text-2xl font-bold text-purple-600">{value}</div>
                      <div className="text-sm text-gray-500 capitalize">{key.replace(/([A-Z])/g, ' $1')}</div>
                    </div>
                  ))}
                </div>

                <button className="w-full bg-gradient-to-r from-purple-600 to-blue-600 text-white py-3 px-6 rounded-lg font-semibold hover:from-purple-700 hover:to-blue-700 transition-all duration-200 flex items-center justify-center space-x-2 group">
                  <span>View Case Study</span>
                  <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform duration-200" />
                </button>
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
          <div className="bg-gradient-to-br from-gray-900 to-purple-900 rounded-2xl p-8 text-white">
            <h3 className="text-3xl font-bold mb-4">
              Ready to See Your Results?
            </h3>
            <p className="text-xl text-gray-300 mb-8 max-w-2xl mx-auto">
              Join thousands of creators and businesses who are already transforming their content with AI video generation.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <button className="bg-white text-purple-600 px-8 py-3 rounded-lg font-semibold hover:bg-gray-100 transition-colors duration-200">
                Start Free Trial
              </button>
              <button className="border-2 border-white text-white px-8 py-3 rounded-lg font-semibold hover:bg-white hover:text-purple-600 transition-colors duration-200">
                Book a Demo
              </button>
            </div>
          </div>
        </motion.div>
      </div>
    </section>
  )
}
