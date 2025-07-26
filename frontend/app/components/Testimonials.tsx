'use client'

import { motion } from 'framer-motion'
import { Star, Quote } from 'lucide-react'

const testimonials = [
  {
    id: 1,
    name: 'Sarah Chen',
    role: 'Educational Content Creator',
    company: 'EduTech Academy',
    avatar: '/avatars/sarah.jpg',
    rating: 5,
    quote: 'This platform has completely transformed how I create educational content. The AI stitching feature saves me hours of work, and the results are always professional quality.',
    videoCount: '200+ videos created'
  },
  {
    id: 2,
    name: 'Marcus Rodriguez',
    role: 'Marketing Director',
    company: 'StartupBoost',
    avatar: '/avatars/marcus.jpg',
    rating: 5,
    quote: 'Our marketing team can now produce high-quality videos in minutes instead of days. The templates are incredibly versatile and the export quality is outstanding.',
    videoCount: '150+ campaigns launched'
  },
  {
    id: 3,
    name: 'Dr. Emily Watson',
    role: 'Corporate Trainer',
    company: 'Global Corp Solutions',
    avatar: '/avatars/emily.jpg',
    rating: 5,
    quote: 'The Canvas Editor is intuitive and powerful. I can create professional training materials without any technical background. My team loves the interactive elements.',
    videoCount: '80+ training modules'
  },
  {
    id: 4,
    name: 'Alex Thompson',
    role: 'Podcast Producer',
    company: 'Creative Minds Podcast',
    avatar: '/avatars/alex.jpg',
    rating: 5,
    quote: 'The audio integration features are fantastic. Creating podcast promotional content and episode snippets has never been easier. The waveform visualization is a game-changer.',
    videoCount: '300+ episodes promoted'
  },
  {
    id: 5,
    name: 'Lisa Park',
    role: 'Social Media Manager',
    company: 'Trendy Brands',
    avatar: '/avatars/lisa.jpg',
    rating: 5,
    quote: 'Perfect for social media content creation! The platform understands different platform requirements and automatically optimizes videos for each channel.',
    videoCount: '500+ social posts'
  },
  {
    id: 6,
    name: 'David Kumar',
    role: 'Freelance Designer',
    company: 'Independent',
    avatar: '/avatars/david.jpg',
    rating: 5,
    quote: 'As a freelancer, this tool has expanded my service offerings significantly. I can now take on video projects with confidence, delivering professional results every time.',
    videoCount: '120+ client projects'
  }
]

export default function Testimonials() {
  return (
    <section className="py-20 bg-dark-800/30">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-center mb-16"
        >
          <h2 className="text-3xl md:text-4xl font-bold text-white mb-4">
            Loved by Creators Worldwide
          </h2>
          <p className="text-gray-400 text-lg max-w-3xl mx-auto">
            Don't just take our word for it. Here's what creators, educators, and professionals 
            are saying about their experience with our platform.
          </p>
        </motion.div>

        {/* Testimonials Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {testimonials.map((testimonial, index) => (
            <motion.div
              key={testimonial.id}
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: index * 0.1 }}
              whileHover={{ y: -5, scale: 1.02 }}
              className="group glass-effect rounded-2xl p-6 border border-white/10 hover:border-white/20 transition-all duration-300"
            >
              {/* Quote Icon */}
              <div className="flex items-center justify-between mb-4">
                <Quote className="w-8 h-8 text-primary-400/50" />
                <div className="flex items-center space-x-1">
                  {[...Array(testimonial.rating)].map((_, i) => (
                    <Star key={i} className="w-4 h-4 text-yellow-400 fill-yellow-400" />
                  ))}
                </div>
              </div>

              {/* Quote */}
              <blockquote className="text-gray-300 mb-6 leading-relaxed">
                "{testimonial.quote}"
              </blockquote>

              {/* Author */}
              <div className="flex items-center space-x-4">
                <div className="w-12 h-12 bg-gradient-to-r from-primary-500 to-purple-600 rounded-full flex items-center justify-center">
                  <span className="text-white font-semibold text-sm">
                    {testimonial.name.split(' ').map(n => n[0]).join('')}
                  </span>
                </div>
                <div className="flex-1">
                  <div className="font-semibold text-white text-sm">
                    {testimonial.name}
                  </div>
                  <div className="text-gray-400 text-xs">
                    {testimonial.role}
                  </div>
                  <div className="text-gray-500 text-xs">
                    {testimonial.company}
                  </div>
                </div>
              </div>

              {/* Stats */}
              <div className="mt-4 pt-4 border-t border-white/10">
                <div className="text-xs text-primary-400 font-medium">
                  {testimonial.videoCount}
                </div>
              </div>
            </motion.div>
          ))}
        </div>

        {/* Trust Indicators */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ delay: 0.8 }}
          className="mt-16 text-center"
        >
          <div className="glass-effect rounded-2xl p-8 border border-white/10">
            <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
              <div className="text-center">
                <div className="text-3xl font-bold text-white mb-2">4.9/5</div>
                <div className="flex justify-center mb-2">
                  {[...Array(5)].map((_, i) => (
                    <Star key={i} className="w-4 h-4 text-yellow-400 fill-yellow-400" />
                  ))}
                </div>
                <div className="text-sm text-gray-400">Average Rating</div>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold text-white mb-2">10K+</div>
                <div className="text-sm text-gray-400">Happy Creators</div>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold text-white mb-2">50K+</div>
                <div className="text-sm text-gray-400">Videos Created</div>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold text-white mb-2">99.9%</div>
                <div className="text-sm text-gray-400">Uptime</div>
              </div>
            </div>
          </div>
        </motion.div>

        {/* CTA */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ delay: 1.0 }}
          className="text-center mt-12"
        >
          <motion.button
            whileHover={{ scale: 1.05, y: -2 }}
            whileTap={{ scale: 0.95 }}
            className="px-8 py-4 gradient-button text-white font-semibold rounded-xl text-lg"
          >
            Join Our Community
          </motion.button>
        </motion.div>
      </div>
    </section>
  )
}
