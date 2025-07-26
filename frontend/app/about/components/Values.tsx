'use client'

import { motion } from 'framer-motion'
import { useInView } from 'framer-motion'
import { useRef } from 'react'
import { Shield, Heart, Rocket, Zap, Eye, Users } from 'lucide-react'

const values = [
  {
    icon: Shield,
    title: 'Privacy First',
    description: 'Your data and creations are protected with enterprise-grade security.',
    color: 'text-green-600'
  },
  {
    icon: Heart,
    title: 'Human-Centered',
    description: 'AI should enhance human creativity, not replace it.',
    color: 'text-red-600'
  },
  {
    icon: Rocket,
    title: 'Innovation',
    description: 'We push boundaries to deliver cutting-edge video generation technology.',
    color: 'text-purple-600'
  },
  {
    icon: Zap,
    title: 'Efficiency',
    description: 'Create professional videos in minutes, not hours.',
    color: 'text-yellow-600'
  },
  {
    icon: Eye,
    title: 'Transparency',
    description: 'Clear pricing, open communication, and honest about our capabilities.',
    color: 'text-blue-600'
  },
  {
    icon: Users,
    title: 'Collaboration',
    description: 'Building together with our community and partners.',
    color: 'text-indigo-600'
  }
]

export default function Values() {
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
            Our Values
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            The principles that guide everything we do and every decision we make.
          </p>
        </motion.div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {values.map((value, index) => {
            const Icon = value.icon
            return (
              <motion.div
                key={value.title}
                initial={{ opacity: 0, y: 30 }}
                animate={isInView ? { opacity: 1, y: 0 } : { opacity: 0, y: 30 }}
                transition={{ duration: 0.6, delay: index * 0.1 }}
                className="group relative bg-gradient-to-br from-gray-50 to-gray-100 rounded-xl p-8 hover:shadow-xl transition-all duration-300 border border-gray-200 hover:border-gray-300"
              >
                <div className="absolute inset-0 bg-gradient-to-br from-purple-500/5 to-blue-500/5 rounded-xl opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
                
                <div className="relative z-10">
                  <div className="flex items-center justify-center w-16 h-16 bg-white rounded-xl shadow-lg mb-6 group-hover:scale-110 transition-transform duration-300">
                    <Icon className={`w-8 h-8 ${value.color}`} />
                  </div>
                  
                  <h3 className="text-2xl font-bold text-gray-900 mb-4 group-hover:text-purple-700 transition-colors duration-300">
                    {value.title}
                  </h3>
                  
                  <p className="text-gray-600 leading-relaxed">
                    {value.description}
                  </p>
                </div>
              </motion.div>
            )
          })}
        </div>

        <motion.div
          initial={{ opacity: 0, y: 50 }}
          animate={isInView ? { opacity: 1, y: 0 } : { opacity: 0, y: 50 }}
          transition={{ duration: 0.8, delay: 0.6 }}
          className="mt-16 text-center"
        >
          <div className="bg-gradient-to-br from-purple-600 to-blue-600 rounded-2xl p-8 text-white">
            <h3 className="text-3xl font-bold mb-4">
              Join Our Mission
            </h3>
            <p className="text-xl text-purple-100 mb-8 max-w-2xl mx-auto">
              We're always looking for passionate people who share our values and want to shape the future of video creation.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <button className="bg-white text-purple-600 px-8 py-3 rounded-lg font-semibold hover:bg-gray-100 transition-colors duration-200">
                View Open Positions
              </button>
              <button className="border-2 border-white text-white px-8 py-3 rounded-lg font-semibold hover:bg-white hover:text-purple-600 transition-colors duration-200">
                Partner With Us
              </button>
            </div>
          </div>
        </motion.div>
      </div>
    </section>
  )
}
