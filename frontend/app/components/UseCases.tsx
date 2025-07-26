'use client'

import { motion } from 'framer-motion'
import { 
  GraduationCap, 
  Megaphone, 
  Briefcase, 
  Mic, 
  Users, 
  Globe,
  ArrowRight,
  PlayCircle
} from 'lucide-react'

const useCases = [
  {
    id: 1,
    title: 'Educational Content',
    description: 'Create engaging educational videos with animations, explanations, and interactive elements.',
    icon: GraduationCap,
    gradient: 'from-blue-500 to-indigo-600',
    features: ['Animated Explanations', 'Interactive Elements', 'Quiz Integration', 'Progress Tracking'],
    image: '/images/education-use-case.jpg',
    stats: { created: '2,500+', rating: '4.9/5' }
  },
  {
    id: 2,
    title: 'Marketing Videos',
    description: 'Professional marketing content for social media, ads, and promotional campaigns.',
    icon: Megaphone,
    gradient: 'from-pink-500 to-red-600',
    features: ['Brand Templates', 'Social Media Formats', 'Call-to-Action', 'Analytics Integration'],
    image: '/images/marketing-use-case.jpg',
    stats: { created: '5,000+', rating: '4.8/5' }
  },
  {
    id: 3,
    title: 'Corporate Presentations',
    description: 'Professional presentations for business meetings, training, and conferences.',
    icon: Briefcase,
    gradient: 'from-gray-500 to-gray-700',
    features: ['Corporate Branding', 'Data Visualization', 'Professional Themes', 'Export Options'],
    image: '/images/corporate-use-case.jpg',
    stats: { created: '1,800+', rating: '4.9/5' }
  },
  {
    id: 4,
    title: 'Podcast Content',
    description: 'Create engaging podcast intros, outros, and promotional content.',
    icon: Mic,
    gradient: 'from-purple-500 to-pink-500',
    features: ['Audio Sync', 'Waveform Visualization', 'Podcast Templates', 'Social Clips'],
    image: '/images/podcast-use-case.jpg',
    stats: { created: '900+', rating: '4.7/5' }
  },
  {
    id: 5,
    title: 'Social Media',
    description: 'Short-form content optimized for Instagram, TikTok, YouTube Shorts, and more.',
    icon: Users,
    gradient: 'from-green-500 to-teal-600',
    features: ['Multiple Formats', 'Trending Templates', 'Hashtag Suggestions', 'Auto-Captions'],
    image: '/images/social-use-case.jpg',
    stats: { created: '8,000+', rating: '4.8/5' }
  },
  {
    id: 6,
    title: 'Global Content',
    description: 'Multi-language support with automatic translation and localization.',
    icon: Globe,
    gradient: 'from-orange-500 to-yellow-600',
    features: ['Auto Translation', 'Voice Cloning', 'Cultural Adaptation', '50+ Languages'],
    image: '/images/global-use-case.jpg',
    stats: { created: '1,200+', rating: '4.6/5' }
  }
]

export default function UseCases() {
  return (
    <section className="py-20 bg-dark-900">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-center mb-16"
        >
          <h2 className="text-3xl md:text-4xl font-bold text-white mb-4">
            Built for Every Use Case
          </h2>
          <p className="text-gray-400 text-lg max-w-3xl mx-auto">
            Whether you're an educator, marketer, business professional, or content creator, 
            our platform adapts to your specific needs and workflow.
          </p>
        </motion.div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {useCases.map((useCase, index) => (
            <motion.div
              key={useCase.id}
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: index * 0.1 }}
              whileHover={{ y: -10, scale: 1.02 }}
              className="group glass-effect rounded-2xl border border-white/10 hover:border-white/20 transition-all duration-300 overflow-hidden"
            >
              {/* Image/Icon Header */}
              <div className="relative h-48 bg-gradient-to-br from-dark-700 to-dark-800 flex items-center justify-center">
                <div className={`w-16 h-16 bg-gradient-to-r ${useCase.gradient} rounded-2xl flex items-center justify-center group-hover:scale-110 transition-transform duration-300`}>
                  <useCase.icon className="w-8 h-8 text-white" />
                </div>
                <div className="absolute top-4 right-4 flex items-center space-x-2">
                  <div className="px-2 py-1 bg-black/20 rounded-full text-xs text-white">
                    {useCase.stats.created}
                  </div>
                  <div className="px-2 py-1 bg-black/20 rounded-full text-xs text-white">
                    ⭐ {useCase.stats.rating}
                  </div>
                </div>
              </div>

              {/* Content */}
              <div className="p-6">
                <h3 className="text-xl font-semibold text-white mb-2 group-hover:text-transparent group-hover:bg-clip-text group-hover:bg-gradient-to-r group-hover:from-primary-400 group-hover:to-purple-400 transition-all duration-300">
                  {useCase.title}
                </h3>
                <p className="text-gray-400 text-sm mb-4 leading-relaxed">
                  {useCase.description}
                </p>

                {/* Features */}
                <div className="grid grid-cols-2 gap-2 mb-6">
                  {useCase.features.map((feature, idx) => (
                    <div key={idx} className="flex items-center space-x-2">
                      <div className="w-1.5 h-1.5 bg-primary-400 rounded-full"></div>
                      <span className="text-xs text-gray-400">{feature}</span>
                    </div>
                  ))}
                </div>

                {/* CTA */}
                <motion.button
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  className="group/btn flex items-center space-x-2 text-primary-400 hover:text-primary-300 transition-colors text-sm font-medium"
                >
                  <PlayCircle className="w-4 h-4" />
                  <span>View Examples</span>
                  <ArrowRight className="w-4 h-4 group-hover/btn:translate-x-1 transition-transform" />
                </motion.button>
              </div>
            </motion.div>
          ))}
        </div>

        {/* Bottom CTA */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ delay: 0.8 }}
          className="text-center mt-16"
        >
          <div className="glass-effect rounded-2xl p-8 border border-white/10">
            <h3 className="text-2xl font-bold text-white mb-4">
              Ready to Start Creating?
            </h3>
            <p className="text-gray-400 mb-6 max-w-2xl mx-auto">
              Join thousands of creators who are already making amazing videos with our platform. 
              Start with a free template or build from scratch.
            </p>
            <div className="flex flex-col sm:flex-row items-center justify-center space-y-4 sm:space-y-0 sm:space-x-4">
              <motion.button
                whileHover={{ scale: 1.05, y: -2 }}
                whileTap={{ scale: 0.95 }}
                className="px-8 py-3 gradient-button text-white font-semibold rounded-lg"
              >
                Start Creating
              </motion.button>
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className="px-8 py-3 glass-effect border border-white/20 text-white font-semibold rounded-lg hover:bg-white/10 transition-colors"
              >
                Browse Templates
              </motion.button>
            </div>
          </div>
        </motion.div>
      </div>
    </section>
  )
}
