'use client'

import { motion } from 'framer-motion'
import { useInView } from 'framer-motion'
import { useRef } from 'react'
import { Calendar, Trophy, Rocket, Star, Users, Globe } from 'lucide-react'

const milestones = [
  {
    year: '2023',
    quarter: 'Q1',
    title: 'Company Founded',
    description: 'Started with a vision to democratize video creation using AI',
    icon: Rocket,
    color: 'bg-purple-600'
  },
  {
    year: '2023',
    quarter: 'Q2',
    title: 'First AI Model',
    description: 'Released our first video generation model with basic text-to-video capabilities',
    icon: Star,
    color: 'bg-blue-600'
  },
  {
    year: '2023',
    quarter: 'Q3',
    title: 'Beta Launch',
    description: 'Launched private beta with 1,000 selected creators and received overwhelming response',
    icon: Users,
    color: 'bg-green-600'
  },
  {
    year: '2023',
    quarter: 'Q4',
    title: 'Public Release',
    description: 'Opened platform to the public, reaching 100,000 videos created in first month',
    icon: Globe,
    color: 'bg-indigo-600'
  },
  {
    year: '2024',
    quarter: 'Q1',
    title: 'Advanced Features',
    description: 'Launched style transfer, voice synthesis, and multi-scene video generation',
    icon: Trophy,
    color: 'bg-pink-600'
  },
  {
    year: '2024',
    quarter: 'Q2',
    title: 'Enterprise Solutions',
    description: 'Introduced enterprise-grade features with custom model training capabilities',
    icon: Calendar,
    color: 'bg-orange-600'
  }
]

export default function Timeline() {
  const ref = useRef(null)
  const isInView = useInView(ref, { once: true, amount: 0.2 })

  return (
    <section ref={ref} className="py-20 bg-gradient-to-br from-gray-50 to-blue-50">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 50 }}
          animate={isInView ? { opacity: 1, y: 0 } : { opacity: 0, y: 50 }}
          transition={{ duration: 0.8 }}
          className="text-center mb-16"
        >
          <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">
            Our Journey
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            From a bold idea to a platform used by creators worldwide. Here's how we've grown.
          </p>
        </motion.div>

        <div className="relative">
          {/* Timeline Line */}
          <div className="absolute left-1/2 transform -translate-x-1/2 w-1 h-full bg-gradient-to-b from-purple-400 to-blue-400 rounded-full" />

          <div className="space-y-16">
            {milestones.map((milestone, index) => {
              const Icon = milestone.icon
              const isEven = index % 2 === 0

              return (
                <motion.div
                  key={`${milestone.year}-${milestone.quarter}`}
                  initial={{ opacity: 0, x: isEven ? -100 : 100 }}
                  animate={isInView ? { opacity: 1, x: 0 } : { opacity: 0, x: isEven ? -100 : 100 }}
                  transition={{ duration: 0.8, delay: index * 0.2 }}
                  className={`relative flex items-center ${isEven ? 'justify-start' : 'justify-end'}`}
                >
                  <div className={`w-full ${isEven ? 'pr-8 text-right' : 'pl-8 text-left'} md:w-5/12`}>
                    <div className="bg-white rounded-xl p-6 shadow-lg border border-gray-200 hover:shadow-xl transition-shadow duration-300">
                      <div className={`flex items-center mb-4 ${isEven ? 'justify-end' : 'justify-start'}`}>
                        <div className={`px-3 py-1 rounded-full text-sm font-semibold text-white ${milestone.color}`}>
                          {milestone.year} {milestone.quarter}
                        </div>
                      </div>
                      
                      <h3 className="text-2xl font-bold text-gray-900 mb-3">
                        {milestone.title}
                      </h3>
                      
                      <p className="text-gray-600 leading-relaxed">
                        {milestone.description}
                      </p>
                    </div>
                  </div>

                  {/* Timeline Node */}
                  <div className="absolute left-1/2 transform -translate-x-1/2 w-16 h-16 bg-white rounded-full border-4 border-purple-400 flex items-center justify-center shadow-lg">
                    <Icon className="w-8 h-8 text-purple-600" />
                  </div>
                </motion.div>
              )
            })}
          </div>
        </div>

        <motion.div
          initial={{ opacity: 0, y: 50 }}
          animate={isInView ? { opacity: 1, y: 0 } : { opacity: 0, y: 50 }}
          transition={{ duration: 0.8, delay: 1.2 }}
          className="mt-20 text-center"
        >
          <div className="bg-gradient-to-br from-purple-600 to-blue-600 rounded-2xl p-8 text-white">
            <h3 className="text-3xl font-bold mb-4">
              What's Next?
            </h3>
            <p className="text-xl text-purple-100 mb-8 max-w-2xl mx-auto">
              We're just getting started. Exciting new features and capabilities are coming soon.
            </p>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 text-center">
              <div>
                <div className="text-2xl font-bold mb-2">Real-time Video</div>
                <div className="text-purple-200">Live video generation</div>
              </div>
              <div>
                <div className="text-2xl font-bold mb-2">3D Animation</div>
                <div className="text-purple-200">Three-dimensional scenes</div>
              </div>
              <div>
                <div className="text-2xl font-bold mb-2">VR Integration</div>
                <div className="text-purple-200">Virtual reality experiences</div>
              </div>
            </div>
          </div>
        </motion.div>
      </div>
    </section>
  )
}
