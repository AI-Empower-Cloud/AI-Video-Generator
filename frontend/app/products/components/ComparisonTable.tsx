'use client'

import { motion } from 'framer-motion'
import { useInView } from 'framer-motion'
import { useRef } from 'react'
import { Check, X, Star } from 'lucide-react'

const features = [
  'Video Generation',
  'Custom Styles',
  'API Access',
  'Cloud Storage',
  'Collaboration',
  'Advanced Analytics',
  'Priority Support',
  'Custom Integrations',
  'On-Premise Deployment',
  'Dedicated Support',
  'SLA Guarantee',
  'Custom Training'
]

const plans = [
  {
    name: 'AI Studio',
    price: '$29',
    period: '/month',
    description: 'Perfect for content creators and small teams',
    features: [true, true, false, true, true, false, false, false, false, false, false, false],
    popular: false,
    color: 'purple'
  },
  {
    name: 'API Platform',
    price: '$0.10',
    period: '/video',
    description: 'Pay-per-use for developers and applications',
    features: [true, true, true, true, false, true, false, false, false, false, true, false],
    popular: true,
    color: 'blue'
  },
  {
    name: 'Cloud Engine',
    price: 'Custom',
    period: '',
    description: 'Scalable infrastructure for growing businesses',
    features: [true, true, true, true, true, true, true, true, false, false, true, false],
    popular: false,
    color: 'green'
  },
  {
    name: 'Enterprise',
    price: 'Custom',
    period: '',
    description: 'Complete solution for large organizations',
    features: [true, true, true, true, true, true, true, true, true, true, true, true],
    popular: false,
    color: 'orange'
  }
]

export default function ComparisonTable() {
  const ref = useRef(null)
  const isInView = useInView(ref, { once: true, amount: 0.3 })

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
            Compare Plans
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Choose the perfect plan for your needs. All plans include our core AI video generation technology.
          </p>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={isInView ? { opacity: 1, y: 0 } : { opacity: 0, y: 30 }}
          transition={{ duration: 0.8, delay: 0.2 }}
          className="overflow-x-auto"
        >
          <table className="w-full bg-white rounded-2xl shadow-lg overflow-hidden">
            <thead>
              <tr className="bg-gradient-to-r from-gray-50 to-blue-50">
                <th className="px-6 py-8 text-left">
                  <span className="text-lg font-semibold text-gray-900">Features</span>
                </th>
                {plans.map((plan) => (
                  <th key={plan.name} className="px-6 py-8 text-center relative">
                    {plan.popular && (
                      <div className="absolute -top-3 left-1/2 transform -translate-x-1/2 bg-gradient-to-r from-yellow-400 to-orange-400 text-white px-3 py-1 rounded-full text-sm font-semibold flex items-center">
                        <Star className="w-4 h-4 mr-1" />
                        Popular
                      </div>
                    )}
                    <div className="text-2xl font-bold text-gray-900 mb-1">{plan.name}</div>
                    <div className="flex items-baseline justify-center mb-2">
                      <span className="text-3xl font-bold text-purple-600">{plan.price}</span>
                      <span className="text-gray-500 ml-1">{plan.period}</span>
                    </div>
                    <p className="text-sm text-gray-600 max-w-32 mx-auto">{plan.description}</p>
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {features.map((feature, index) => (
                <tr key={feature} className={index % 2 === 0 ? 'bg-gray-50' : 'bg-white'}>
                  <td className="px-6 py-4 text-gray-900 font-medium">
                    {feature}
                  </td>
                  {plans.map((plan) => (
                    <td key={`${plan.name}-${feature}`} className="px-6 py-4 text-center">
                      {plan.features[index] ? (
                        <Check className="w-6 h-6 text-green-500 mx-auto" />
                      ) : (
                        <X className="w-6 h-6 text-gray-300 mx-auto" />
                      )}
                    </td>
                  ))}
                </tr>
              ))}
              <tr className="bg-gradient-to-r from-gray-50 to-blue-50">
                <td className="px-6 py-6"></td>
                {plans.map((plan) => (
                  <td key={`${plan.name}-cta`} className="px-6 py-6 text-center">
                    <button className={`w-full py-3 px-6 rounded-lg font-semibold transition-all duration-200 ${
                      plan.popular 
                        ? 'bg-gradient-to-r from-purple-600 to-blue-600 text-white hover:from-purple-700 hover:to-blue-700' 
                        : 'border-2 border-purple-600 text-purple-600 hover:bg-purple-600 hover:text-white'
                    }`}>
                      {plan.price === 'Custom' ? 'Contact Sales' : 'Get Started'}
                    </button>
                  </td>
                ))}
              </tr>
            </tbody>
          </table>
        </motion.div>
      </div>
    </section>
  )
}
