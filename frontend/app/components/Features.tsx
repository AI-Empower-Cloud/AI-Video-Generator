'use client'

import { motion } from 'framer-motion'
import { 
  Video, 
  Scissors, 
  Palette, 
  Zap, 
  Brain, 
  Music,
  Type,
  Image,
  Download,
  Share2,
  Globe,
  Shield
} from 'lucide-react'

const features = [
  {
    name: 'Canvas Video Editor',
    description: 'Drag-and-drop visual editor with timeline-based editing, layer management, and real-time preview.',
    icon: Video,
    gradient: 'from-blue-500 to-cyan-500',
  },
  {
    name: 'AI Video Stitching',
    description: 'Automated video composition that intelligently combines multiple media elements into professional videos.',
    icon: Scissors,
    gradient: 'from-purple-500 to-pink-500',
  },
  {
    name: 'Smart Templates',
    description: 'Pre-built templates for educational content, marketing videos, presentations, and more.',
    icon: Palette,
    gradient: 'from-green-500 to-emerald-500',
  },
  {
    name: 'Lightning Fast',
    description: 'Optimized rendering pipeline with GPU acceleration for quick video generation and export.',
    icon: Zap,
    gradient: 'from-yellow-500 to-orange-500',
  },
  {
    name: 'AI-Powered Tools',
    description: 'Advanced AI features including voice synthesis, lip-sync, subtitle generation, and scene analysis.',
    icon: Brain,
    gradient: 'from-indigo-500 to-purple-500',
  },
  {
    name: 'Audio Integration',
    description: 'Built-in audio processing with music library, sound effects, and advanced audio mixing capabilities.',
    icon: Music,
    gradient: 'from-red-500 to-pink-500',
  },
  {
    name: 'Text & Typography',
    description: 'Rich text editing with custom fonts, animations, and professional typography tools.',
    icon: Type,
    gradient: 'from-gray-500 to-gray-700',
  },
  {
    name: 'Media Library',
    description: 'Extensive library of stock images, videos, icons, and graphics for your projects.',
    icon: Image,
    gradient: 'from-teal-500 to-cyan-500',
  },
  {
    name: 'Multiple Export Formats',
    description: 'Export to MP4, WebM, GIF, and other formats with customizable quality settings.',
    icon: Download,
    gradient: 'from-blue-500 to-indigo-500',
  },
  {
    name: 'Easy Sharing',
    description: 'Direct sharing to social media platforms, cloud storage, and video hosting services.',
    icon: Share2,
    gradient: 'from-green-500 to-blue-500',
  },
  {
    name: 'Global CDN',
    description: 'Fast video delivery worldwide with our global content delivery network.',
    icon: Globe,
    gradient: 'from-orange-500 to-red-500',
  },
  {
    name: 'Enterprise Security',
    description: 'Enterprise-grade security with encryption, compliance, and privacy protection.',
    icon: Shield,
    gradient: 'from-gray-600 to-gray-800',
  },
]

export default function Features() {
  return (
    <section className="py-20 bg-dark-800/50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-center mb-16"
        >
          <h2 className="text-3xl md:text-4xl font-bold text-white mb-4">
            Everything You Need to Create Amazing Videos
          </h2>
          <p className="text-gray-400 text-lg max-w-3xl mx-auto">
            Our comprehensive suite of tools and features makes video creation accessible to everyone, 
            from beginners to professional creators.
          </p>
        </motion.div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {features.map((feature, index) => (
            <motion.div
              key={feature.name}
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: index * 0.1 }}
              whileHover={{ y: -5, scale: 1.02 }}
              className="group glass-effect rounded-2xl p-6 border border-white/10 hover:border-white/20 transition-all duration-300"
            >
              <div className={`w-12 h-12 bg-gradient-to-r ${feature.gradient} rounded-lg flex items-center justify-center mb-4 group-hover:scale-110 transition-transform duration-300`}>
                <feature.icon className="w-6 h-6 text-white" />
              </div>
              <h3 className="text-xl font-semibold text-white mb-2 group-hover:text-transparent group-hover:bg-clip-text group-hover:bg-gradient-to-r group-hover:from-primary-400 group-hover:to-purple-400 transition-all duration-300">
                {feature.name}
              </h3>
              <p className="text-gray-400 leading-relaxed">
                {feature.description}
              </p>
            </motion.div>
          ))}
        </div>

        {/* Call to Action */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ delay: 0.8 }}
          className="text-center mt-16"
        >
          <motion.button
            whileHover={{ scale: 1.05, y: -2 }}
            whileTap={{ scale: 0.95 }}
            className="group relative px-8 py-4 gradient-button text-white font-semibold rounded-xl text-lg"
          >
            <span>Explore All Features</span>
          </motion.button>
        </motion.div>
      </div>
    </section>
  )
}
