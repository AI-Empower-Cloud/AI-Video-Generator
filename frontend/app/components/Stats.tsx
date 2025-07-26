'use client'

import { motion } from 'framer-motion'
import { 
  TrendingUp, 
  Users, 
  Award, 
  Clock 
} from 'lucide-react'

const stats = [
  {
    id: 1,
    name: 'Videos Created',
    stat: '10,000+',
    icon: TrendingUp,
    change: '+12%',
    changeType: 'increase',
  },
  {
    id: 2,
    name: 'Active Users',
    stat: '2,500+',
    icon: Users,
    change: '+19%',
    changeType: 'increase',
  },
  {
    id: 3,
    name: 'Templates Available',
    stat: '50+',
    icon: Award,
    change: '+8%',
    changeType: 'increase',
  },
  {
    id: 4,
    name: 'Avg. Creation Time',
    stat: '5 min',
    icon: Clock,
    change: '-23%',
    changeType: 'decrease',
  },
]

export default function Stats() {
  return (
    <section className="py-20 bg-dark-900/50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-center mb-12"
        >
          <h2 className="text-3xl md:text-4xl font-bold text-white mb-4">
            Trusted by Creators Worldwide
          </h2>
          <p className="text-gray-400 text-lg max-w-2xl mx-auto">
            Join thousands of content creators, educators, and marketers who use our platform 
            to create professional videos every day.
          </p>
        </motion.div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          {stats.map((item, index) => (
            <motion.div
              key={item.id}
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: index * 0.1 }}
              whileHover={{ y: -5, scale: 1.02 }}
              className="glass-effect rounded-2xl p-6 border border-white/10 hover:border-white/20 transition-all duration-300"
            >
              <div className="flex items-center justify-between mb-4">
                <div className="w-12 h-12 bg-gradient-to-r from-primary-500 to-purple-600 rounded-lg flex items-center justify-center">
                  <item.icon className="w-6 h-6 text-white" />
                </div>
                <div className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                  item.changeType === 'increase'
                    ? 'bg-green-100 text-green-800 dark:bg-green-800/20 dark:text-green-300'
                    : 'bg-red-100 text-red-800 dark:bg-red-800/20 dark:text-red-300'
                }`}>
                  {item.change}
                </div>
              </div>
              <div className="text-3xl font-bold text-white mb-1">{item.stat}</div>
              <div className="text-sm text-gray-400">{item.name}</div>
            </motion.div>
          ))}
        </div>

        {/* Additional Metrics */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ delay: 0.5 }}
          className="mt-16 text-center"
        >
          <div className="inline-flex items-center space-x-8 glass-effect rounded-2xl px-8 py-6 border border-white/10">
            <div className="text-center">
              <div className="text-2xl font-bold text-white">99.9%</div>
              <div className="text-sm text-gray-400">Uptime</div>
            </div>
            <div className="w-px h-10 bg-gray-700"></div>
            <div className="text-center">
              <div className="text-2xl font-bold text-white">4.9/5</div>
              <div className="text-sm text-gray-400">Rating</div>
            </div>
            <div className="w-px h-10 bg-gray-700"></div>
            <div className="text-center">
              <div className="text-2xl font-bold text-white">24/7</div>
              <div className="text-sm text-gray-400">Support</div>
            </div>
          </div>
        </motion.div>
      </div>
    </section>
  )
}
