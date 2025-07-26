'use client'

import { motion } from 'framer-motion'
import { useInView } from 'framer-motion'
import { useRef } from 'react'
import { 
  Palette, 
  Code, 
  Cloud, 
  Building, 
  Play, 
  Zap, 
  Shield, 
  Users,
  ArrowRight,
  Star
} from 'lucide-react'

const products = [
  {
    name: 'AI Studio',
    tagline: 'Professional Video Creation',
    description: 'Intuitive drag-and-drop interface for creating professional videos with AI assistance. Perfect for content creators, marketers, and small businesses.',
    icon: Palette,
    color: 'from-purple-600 to-pink-600',
    features: [
      'Visual editor with timeline',
      'AI-powered suggestions',
      'Template library',
      'Real-time collaboration',
      'Cloud storage included',
      '4K export capabilities'
    ],
    pricing: 'Starting at $29/month',
    cta: 'Try Studio Free',
    popular: false
  },
  {
    name: 'API Platform',
    tagline: 'Developer-First Integration',
    description: 'Powerful RESTful API and SDKs for integrating AI video generation into your applications. Built for developers who want full control.',
    icon: Code,
    color: 'from-blue-600 to-indigo-600',
    features: [
      'RESTful API with webhooks',
      'SDKs for all major languages',
      'Real-time generation status',
      'Batch processing',
      'Custom model training',
      '99.9% uptime SLA'
    ],
    pricing: 'Pay per use from $0.10/video',
    cta: 'View API Docs',
    popular: true
  },
  {
    name: 'Cloud Engine',
    tagline: 'Scalable Infrastructure',
    description: 'Enterprise-grade cloud infrastructure for high-volume video generation. Auto-scaling, global CDN, and advanced analytics included.',
    icon: Cloud,
    color: 'from-green-600 to-teal-600',
    features: [
      'Auto-scaling compute',
      'Global CDN distribution',
      'Advanced analytics',
      'Custom workflows',
      'Priority support',
      'White-label options'
    ],
    pricing: 'Custom pricing',
    cta: 'Contact Sales',
    popular: false
  },
  {
    name: 'Enterprise Suite',
    tagline: 'Complete Business Solution',
    description: 'Comprehensive video production suite with dedicated support, custom integrations, and on-premise deployment options.',
    icon: Building,
    color: 'from-orange-600 to-red-600',
    features: [
      'Dedicated infrastructure',
      'Custom AI model training',
      'On-premise deployment',
      '24/7 dedicated support',
      'Custom integrations',
      'Compliance & security'
    ],
    pricing: 'Contact for quote',
    cta: 'Schedule Demo',
    popular: false
  }
]

export default function ProductSuite() {
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
            Choose Your Perfect Solution
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            From simple video creation to enterprise-grade production workflows, 
            we have the right product for every need and scale.
          </p>
        </motion.div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {products.map((product, index) => {
            const Icon = product.icon
            return (
              <motion.div
                key={product.name}
                initial={{ opacity: 0, y: 50 }}
                animate={isInView ? { opacity: 1, y: 0 } : { opacity: 0, y: 50 }}
                transition={{ duration: 0.6, delay: index * 0.1 }}
                className="relative bg-white rounded-2xl shadow-lg hover:shadow-2xl transition-all duration-300 overflow-hidden border border-gray-200"
              >
                {product.popular && (
                  <div className="absolute top-4 right-4 bg-gradient-to-r from-yellow-400 to-orange-400 text-white px-3 py-1 rounded-full text-sm font-semibold flex items-center">
                    <Star className="w-4 h-4 mr-1" />
                    Most Popular
                  </div>
                )}

                <div className="p-8">
                  {/* Header */}
                  <div className="flex items-center mb-6">
                    <div className={`w-16 h-16 bg-gradient-to-r ${product.color} rounded-xl flex items-center justify-center mr-4`}>
                      <Icon className="w-8 h-8 text-white" />
                    </div>
                    <div>
                      <h3 className="text-2xl font-bold text-gray-900">{product.name}</h3>
                      <p className="text-purple-600 font-semibold">{product.tagline}</p>
                    </div>
                  </div>

                  {/* Description */}
                  <p className="text-gray-600 mb-6 leading-relaxed">
                    {product.description}
                  </p>

                  {/* Features */}
                  <div className="mb-8">
                    <h4 className="text-lg font-semibold text-gray-900 mb-4">Key Features</h4>
                    <div className="grid grid-cols-1 gap-3">
                      {product.features.map((feature, i) => (
                        <div key={i} className="flex items-center text-gray-600">
                          <div className="w-2 h-2 bg-purple-400 rounded-full mr-3 flex-shrink-0" />
                          <span className="text-sm">{feature}</span>
                        </div>
                      ))}
                    </div>
                  </div>

                  {/* Pricing */}
                  <div className="mb-6">
                    <div className="text-2xl font-bold text-gray-900 mb-2">{product.pricing}</div>
                    <div className="text-gray-500 text-sm">Billed monthly, cancel anytime</div>
                  </div>

                  {/* CTA */}
                  <button className={`w-full bg-gradient-to-r ${product.color} text-white py-3 px-6 rounded-lg font-semibold hover:shadow-lg transition-all duration-200 flex items-center justify-center space-x-2 group`}>
                    <span>{product.cta}</span>
                    <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform duration-200" />
                  </button>
                </div>

                {/* Bottom gradient */}
                <div className={`h-1 bg-gradient-to-r ${product.color}`} />
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
              Not Sure Which Product is Right for You?
            </h3>
            <p className="text-xl text-purple-100 mb-8 max-w-2xl mx-auto">
              Our experts can help you choose the perfect solution based on your specific needs and scale.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <button className="bg-white text-purple-600 px-8 py-3 rounded-lg font-semibold hover:bg-gray-100 transition-colors duration-200">
                Talk to an Expert
              </button>
              <button className="border-2 border-white text-white px-8 py-3 rounded-lg font-semibold hover:bg-white hover:text-purple-600 transition-colors duration-200">
                Compare All Products
              </button>
            </div>
          </div>
        </motion.div>
      </div>
    </section>
  )
}
