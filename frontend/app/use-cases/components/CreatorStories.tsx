'use client'

import { motion } from 'framer-motion'
import { useInView } from 'framer-motion'
import { useRef } from 'react'
import { Star, Quote, ArrowLeft, ArrowRight } from 'lucide-react'

const stories = [
  {
    name: 'Sarah Martinez',
    role: 'Marketing Director',
    company: 'TechFlow Solutions',
    industry: 'Software',
    avatar: '/api/placeholder/100/100',
    story: 'We went from spending weeks on video production to creating professional content in hours. Our engagement rates increased by 300% and our team can now focus on strategy instead of technical production.',
    results: {
      timeSaved: '85%',
      engagement: '+300%',
      costReduction: '70%'
    },
    rating: 5
  },
  {
    name: 'Dr. Michael Chen',
    role: 'Course Creator',
    company: 'EduMaster Academy',
    industry: 'Education',
    avatar: '/api/placeholder/100/100',
    story: 'Creating educational content used to be my biggest bottleneck. Now I can produce high-quality training videos for my online courses in minutes. My students love the consistent quality and engaging visuals.',
    results: {
      courseCompletion: '+45%',
      studentSatisfaction: '4.9/5',
      contentOutput: '500%'
    },
    rating: 5
  },
  {
    name: 'Emily Rodriguez',
    role: 'Content Creator',
    company: 'FitLife Channel',
    industry: 'Fitness & Wellness',
    avatar: '/api/placeholder/100/100',
    story: 'As a solo creator, I was struggling to keep up with content demand. This platform has been a game-changer. I can now create workout videos, nutrition guides, and motivational content at scale.',
    results: {
      subscribers: '+250K',
      videoOutput: '10x',
      revenue: '+180%'
    },
    rating: 5
  }
]

export default function CreatorStories() {
  const ref = useRef(null)
  const isInView = useInView(ref, { once: true, amount: 0.2 })

  return (
    <section ref={ref} className="py-20 bg-gradient-to-br from-purple-50 to-blue-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 50 }}
          animate={isInView ? { opacity: 1, y: 0 } : { opacity: 0, y: 50 }}
          transition={{ duration: 0.8 }}
          className="text-center mb-16"
        >
          <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">
            Creator Success Stories
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Real stories from creators and businesses who have transformed their content strategy 
            with AI video generation.
          </p>
        </motion.div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {stories.map((story, index) => (
            <motion.div
              key={story.name}
              initial={{ opacity: 0, y: 50 }}
              animate={isInView ? { opacity: 1, y: 0 } : { opacity: 0, y: 50 }}
              transition={{ duration: 0.6, delay: index * 0.2 }}
              className="bg-white rounded-2xl p-8 shadow-lg hover:shadow-2xl transition-all duration-300 relative"
            >
              {/* Quote Icon */}
              <Quote className="absolute top-6 right-6 w-8 h-8 text-purple-200" />
              
              {/* Rating */}
              <div className="flex items-center mb-6">
                {[...Array(story.rating)].map((_, i) => (
                  <Star key={i} className="w-5 h-5 text-yellow-400 fill-current" />
                ))}
              </div>

              {/* Story */}
              <blockquote className="text-gray-700 mb-6 leading-relaxed italic">
                "{story.story}"
              </blockquote>

              {/* Results */}
              <div className="grid grid-cols-1 gap-3 mb-6 p-4 bg-gradient-to-br from-purple-50 to-blue-50 rounded-xl">
                {Object.entries(story.results).map(([key, value]) => (
                  <div key={key} className="flex justify-between">
                    <span className="text-gray-600 text-sm capitalize">
                      {key.replace(/([A-Z])/g, ' $1')}
                    </span>
                    <span className="font-semibold text-purple-600">{value}</span>
                  </div>
                ))}
              </div>

              {/* Author */}
              <div className="flex items-center">
                <div className="w-12 h-12 bg-gradient-to-br from-purple-400 to-blue-400 rounded-full flex items-center justify-center text-white font-bold text-lg mr-4">
                  {story.name.split(' ').map(n => n[0]).join('')}
                </div>
                <div>
                  <div className="font-semibold text-gray-900">{story.name}</div>
                  <div className="text-sm text-gray-600">{story.role}</div>
                  <div className="text-sm text-purple-600">{story.company}</div>
                </div>
              </div>

              {/* Industry Badge */}
              <div className="absolute top-6 left-6 bg-purple-100 text-purple-700 px-3 py-1 rounded-full text-xs font-semibold">
                {story.industry}
              </div>
            </motion.div>
          ))}
        </div>

        {/* Navigation */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={isInView ? { opacity: 1, y: 0 } : { opacity: 0, y: 30 }}
          transition={{ duration: 0.6, delay: 0.6 }}
          className="flex justify-center mt-12 space-x-4"
        >
          <button className="w-12 h-12 bg-white rounded-full shadow-lg flex items-center justify-center hover:bg-purple-50 transition-colors duration-200">
            <ArrowLeft className="w-5 h-5 text-gray-600" />
          </button>
          <button className="w-12 h-12 bg-white rounded-full shadow-lg flex items-center justify-center hover:bg-purple-50 transition-colors duration-200">
            <ArrowRight className="w-5 h-5 text-gray-600" />
          </button>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 50 }}
          animate={isInView ? { opacity: 1, y: 0 } : { opacity: 0, y: 50 }}
          transition={{ duration: 0.8, delay: 0.8 }}
          className="mt-16 text-center"
        >
          <div className="bg-gradient-to-br from-purple-600 to-blue-600 rounded-2xl p-8 text-white">
            <h3 className="text-3xl font-bold mb-4">
              Your Success Story Starts Here
            </h3>
            <p className="text-xl text-purple-100 mb-8 max-w-2xl mx-auto">
              Join thousands of creators who are already achieving amazing results with AI video generation.
            </p>
            <button className="bg-white text-purple-600 px-8 py-3 rounded-lg font-semibold hover:bg-gray-100 transition-colors duration-200">
              Share Your Story
            </button>
          </div>
        </motion.div>
      </div>
    </section>
  )
}
