'use client'

import { motion } from 'framer-motion'
import { useInView } from 'framer-motion'
import { useRef } from 'react'
import { Code, Smartphone, Globe, Zap, ArrowRight } from 'lucide-react'

const integrations = [
  {
    category: 'Development',
    icon: Code,
    color: 'from-blue-500 to-purple-500',
    tools: [
      { name: 'REST API', logo: '🔗', description: 'Full REST API with webhooks' },
      { name: 'JavaScript SDK', logo: '🟨', description: 'NPM package for Node.js' },
      { name: 'Python SDK', logo: '🐍', description: 'PyPI package for Python' },
      { name: 'React Components', logo: '⚛️', description: 'Ready-to-use React components' }
    ]
  },
  {
    category: 'Mobile',
    icon: Smartphone,
    color: 'from-green-500 to-teal-500',
    tools: [
      { name: 'iOS SDK', logo: '🍎', description: 'Native iOS integration' },
      { name: 'Android SDK', logo: '🤖', description: 'Native Android integration' },
      { name: 'React Native', logo: '📱', description: 'Cross-platform mobile' },
      { name: 'Flutter Plugin', logo: '🦋', description: 'Dart package for Flutter' }
    ]
  },
  {
    category: 'Platforms',
    icon: Globe,
    color: 'from-purple-500 to-pink-500',
    tools: [
      { name: 'WordPress', logo: '📝', description: 'Plugin for WordPress sites' },
      { name: 'Shopify', logo: '🛍️', description: 'E-commerce integration' },
      { name: 'Zapier', logo: '⚡', description: 'No-code automation' },
      { name: 'Webhooks', logo: '🔔', description: 'Real-time notifications' }
    ]
  },
  {
    category: 'Enterprise',
    icon: Zap,
    color: 'from-orange-500 to-red-500',
    tools: [
      { name: 'Salesforce', logo: '☁️', description: 'CRM integration' },
      { name: 'Microsoft Teams', logo: '💼', description: 'Collaboration tools' },
      { name: 'Slack', logo: '💬', description: 'Team communication' },
      { name: 'Custom SSO', logo: '🔐', description: 'Single sign-on solutions' }
    ]
  }
]

export default function Integration() {
  const ref = useRef(null)
  const isInView = useInView(ref, { once: true, amount: 0.2 })

  return (
    <section ref={ref} className="py-20 bg-gradient-to-br from-gray-50 to-blue-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 50 }}
          animate={isInView ? { opacity: 1, y: 0 } : { opacity: 0, y: 50 }}
          transition={{ duration: 0.8 }}
          className="text-center mb-16"
        >
          <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">
            Integrate Anywhere
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Our platform integrates seamlessly with your existing tools and workflows. 
            From simple APIs to enterprise solutions.
          </p>
        </motion.div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          {integrations.map((integration, index) => {
            const Icon = integration.icon
            return (
              <motion.div
                key={integration.category}
                initial={{ opacity: 0, y: 50 }}
                animate={isInView ? { opacity: 1, y: 0 } : { opacity: 0, y: 50 }}
                transition={{ duration: 0.6, delay: index * 0.1 }}
                className="bg-white rounded-2xl p-6 shadow-lg hover:shadow-xl transition-all duration-300 border border-gray-200"
              >
                <div className={`w-16 h-16 bg-gradient-to-r ${integration.color} rounded-xl flex items-center justify-center mb-6`}>
                  <Icon className="w-8 h-8 text-white" />
                </div>
                
                <h3 className="text-xl font-bold text-gray-900 mb-6">{integration.category}</h3>
                
                <div className="space-y-4">
                  {integration.tools.map((tool, i) => (
                    <div key={i} className="flex items-start space-x-3 p-3 rounded-lg hover:bg-gray-50 transition-colors duration-200">
                      <span className="text-2xl">{tool.logo}</span>
                      <div className="flex-1">
                        <div className="font-semibold text-gray-900 text-sm">{tool.name}</div>
                        <div className="text-gray-600 text-xs">{tool.description}</div>
                      </div>
                    </div>
                  ))}
                </div>
                
                <button className="w-full mt-6 text-purple-600 hover:text-purple-700 font-semibold text-sm flex items-center justify-center space-x-1 group">
                  <span>View All</span>
                  <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform duration-200" />
                </button>
              </motion.div>
            )
          })}
        </div>

        <motion.div
          initial={{ opacity: 0, y: 50 }}
          animate={isInView ? { opacity: 1, y: 0 } : { opacity: 0, y: 50 }}
          transition={{ duration: 0.8, delay: 0.6 }}
          className="mt-16"
        >
          <div className="bg-gradient-to-br from-purple-600 to-blue-600 rounded-2xl p-8 text-white">
            <div className="text-center mb-8">
              <h3 className="text-3xl font-bold mb-4">
                Need a Custom Integration?
              </h3>
              <p className="text-xl text-purple-100 max-w-2xl mx-auto">
                Our team can help you build custom integrations for your specific needs. 
                From API endpoints to white-label solutions.
              </p>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 text-center">
              <div>
                <div className="text-2xl font-bold mb-2">100+</div>
                <div className="text-purple-200">Pre-built Integrations</div>
              </div>
              <div>
                <div className="text-2xl font-bold mb-2">48hrs</div>
                <div className="text-purple-200">Custom Integration SLA</div>
              </div>
              <div>
                <div className="text-2xl font-bold mb-2">24/7</div>
                <div className="text-purple-200">Developer Support</div>
              </div>
            </div>
            
            <div className="flex flex-col sm:flex-row gap-4 justify-center mt-8">
              <button className="bg-white text-purple-600 px-8 py-3 rounded-lg font-semibold hover:bg-gray-100 transition-colors duration-200">
                Contact Integration Team
              </button>
              <button className="border-2 border-white text-white px-8 py-3 rounded-lg font-semibold hover:bg-white hover:text-purple-600 transition-colors duration-200">
                View Documentation
              </button>
            </div>
          </div>
        </motion.div>
      </div>
    </section>
  )
}
