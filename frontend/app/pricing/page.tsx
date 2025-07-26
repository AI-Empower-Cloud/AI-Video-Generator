'use client'

import { motion } from 'framer-motion'
import { useState } from 'react'
import Navigation from '../../components/Navigation'
import Footer from '../../components/Footer'
import { 
  Check, 
  X, 
  Star, 
  Zap, 
  Crown, 
  Rocket,
  ArrowRight
} from 'lucide-react'

const plans = [
  {
    name: 'Free',
    price: 0,
    description: 'Perfect for trying out our platform',
    icon: Star,
    gradient: 'from-gray-500 to-gray-600',
    features: [
      '5 videos per month',
      'Basic templates',
      '720p export quality',
      'Canvas Editor access',
      'Community support',
      'Basic AI features'
    ],
    limitations: [
      'Limited export formats',
      'Watermark on videos',
      'No premium templates',
      'No priority support'
    ],
    cta: 'Get Started Free',
    popular: false
  },
  {
    name: 'Pro',
    price: 29,
    description: 'For serious content creators',
    icon: Zap,
    gradient: 'from-primary-500 to-blue-600',
    features: [
      '100 videos per month',
      'All templates included',
      '1080p & 4K export',
      'Advanced Canvas Editor',
      'Priority support',
      'Advanced AI features',
      'Custom branding',
      'Analytics dashboard',
      'API access',
      'Cloud storage (50GB)'
    ],
    limitations: [],
    cta: 'Start Pro Trial',
    popular: true
  },
  {
    name: 'Team',
    price: 99,
    description: 'For teams and agencies',
    icon: Crown,
    gradient: 'from-purple-500 to-pink-600',
    features: [
      'Unlimited videos',
      'All Pro features',
      'Team collaboration',
      'Brand management',
      'White-label options',
      'Dedicated support',
      'Custom integrations',
      'Advanced analytics',
      'SSO integration',
      'Cloud storage (500GB)',
      'Team training'
    ],
    limitations: [],
    cta: 'Contact Sales',
    popular: false
  },
  {
    name: 'Enterprise',
    price: 'Custom',
    description: 'For large organizations',
    icon: Rocket,
    gradient: 'from-orange-500 to-red-600',
    features: [
      'Everything in Team',
      'Custom deployment',
      'On-premise option',
      'Advanced security',
      'Compliance features',
      'Custom development',
      'SLA guarantee',
      'Dedicated manager',
      'Custom training',
      'Unlimited storage',
      '24/7 phone support'
    ],
    limitations: [],
    cta: 'Contact Us',
    popular: false
  }
]

const faqs = [
  {
    question: 'Can I change plans anytime?',
    answer: 'Yes! You can upgrade or downgrade your plan at any time. Changes take effect immediately, and we\'ll prorate the billing accordingly.'
  },
  {
    question: 'What payment methods do you accept?',
    answer: 'We accept all major credit cards, PayPal, and for Enterprise plans, we can arrange bank transfers or custom billing arrangements.'
  },
  {
    question: 'Is there a free trial for paid plans?',
    answer: 'Yes! Pro and Team plans come with a 14-day free trial. No credit card required to start your trial.'
  },
  {
    question: 'What happens to my videos if I cancel?',
    answer: 'Your videos remain accessible for 30 days after cancellation. You can export or download them during this period.'
  },
  {
    question: 'Do you offer educational discounts?',
    answer: 'Yes! We offer 50% discounts for students and educators. Contact our support team with your educational email for verification.'
  },
  {
    question: 'Can I use my own branding?',
    answer: 'Pro plans and above include custom branding options. You can remove our watermark and add your own logo and colors.'
  }
]

export default function PricingPage() {
  const [isAnnual, setIsAnnual] = useState(true)
  const [expandedFaq, setExpandedFaq] = useState<number | null>(null)

  return (
    <>
      <Navigation />
      <main className="pt-16">
        {/* Hero Section */}
        <section className="py-20 bg-gradient-to-br from-dark-900 via-dark-800 to-dark-900">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
            <motion.div
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              className="mb-12"
            >
              <h1 className="text-4xl md:text-6xl font-bold text-white mb-6">
                Choose Your <span className="gradient-text">Creative Plan</span>
              </h1>
              <p className="text-xl text-gray-300 max-w-3xl mx-auto mb-8">
                Start free and scale as you grow. All plans include our core features 
                with increasing limits and advanced capabilities.
              </p>

              {/* Billing Toggle */}
              <div className="flex items-center justify-center space-x-4 mb-8">
                <span className={`text-sm ${!isAnnual ? 'text-white' : 'text-gray-400'}`}>
                  Monthly
                </span>
                <motion.button
                  onClick={() => setIsAnnual(!isAnnual)}
                  className={`relative w-16 h-8 rounded-full transition-colors ${
                    isAnnual ? 'bg-primary-500' : 'bg-gray-600'
                  }`}
                  whileTap={{ scale: 0.95 }}
                >
                  <motion.div
                    animate={{ x: isAnnual ? 32 : 4 }}
                    className="absolute top-1 w-6 h-6 bg-white rounded-full"
                  />
                </motion.button>
                <span className={`text-sm ${isAnnual ? 'text-white' : 'text-gray-400'}`}>
                  Annual
                </span>
                <span className="px-2 py-1 bg-green-500/20 text-green-400 rounded-full text-xs font-medium">
                  Save 20%
                </span>
              </div>
            </motion.div>

            {/* Pricing Cards */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
              {plans.map((plan, index) => (
                <motion.div
                  key={plan.name}
                  initial={{ opacity: 0, y: 30 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: index * 0.1 }}
                  whileHover={{ y: -10, scale: 1.02 }}
                  className={`relative glass-effect rounded-2xl p-6 border transition-all duration-300 ${
                    plan.popular 
                      ? 'border-primary-500 ring-2 ring-primary-500/20' 
                      : 'border-white/10 hover:border-white/20'
                  }`}
                >
                  {plan.popular && (
                    <div className="absolute -top-4 left-1/2 transform -translate-x-1/2">
                      <div className="px-4 py-2 bg-gradient-to-r from-primary-500 to-purple-600 rounded-full text-white text-sm font-medium">
                        Most Popular
                      </div>
                    </div>
                  )}

                  {/* Plan Header */}
                  <div className="text-center mb-6">
                    <div className={`w-12 h-12 bg-gradient-to-r ${plan.gradient} rounded-lg flex items-center justify-center mx-auto mb-4`}>
                      <plan.icon className="w-6 h-6 text-white" />
                    </div>
                    <h3 className="text-xl font-bold text-white mb-2">{plan.name}</h3>
                    <p className="text-gray-400 text-sm mb-4">{plan.description}</p>
                    
                    <div className="mb-4">
                      <span className="text-4xl font-bold text-white">
                        {typeof plan.price === 'number' ? (
                          <>
                            ${isAnnual ? Math.round(plan.price * 0.8) : plan.price}
                            <span className="text-lg text-gray-400 font-normal">/mo</span>
                          </>
                        ) : (
                          plan.price
                        )}
                      </span>
                      {typeof plan.price === 'number' && isAnnual && (
                        <div className="text-sm text-gray-400">
                          ${plan.price * 12 * 0.8}/year
                        </div>
                      )}
                    </div>
                  </div>

                  {/* Features */}
                  <div className="space-y-3 mb-6">
                    {plan.features.map((feature) => (
                      <div key={feature} className="flex items-center space-x-3">
                        <Check className="w-4 h-4 text-green-400 flex-shrink-0" />
                        <span className="text-sm text-gray-300">{feature}</span>
                      </div>
                    ))}
                    {plan.limitations.map((limitation) => (
                      <div key={limitation} className="flex items-center space-x-3">
                        <X className="w-4 h-4 text-red-400 flex-shrink-0" />
                        <span className="text-sm text-gray-400">{limitation}</span>
                      </div>
                    ))}
                  </div>

                  {/* CTA Button */}
                  <motion.button
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    className={`w-full py-3 rounded-lg font-semibold transition-all duration-300 ${
                      plan.popular
                        ? 'gradient-button text-white'
                        : 'glass-effect border border-white/20 text-white hover:bg-white/10'
                    }`}
                  >
                    {plan.cta}
                  </motion.button>
                </motion.div>
              ))}
            </div>

            {/* Enterprise CTA */}
            <motion.div
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.6 }}
              className="mt-16 text-center"
            >
              <div className="glass-effect rounded-2xl p-8 border border-white/10 max-w-2xl mx-auto">
                <h3 className="text-2xl font-bold text-white mb-4">
                  Need a custom solution?
                </h3>
                <p className="text-gray-400 mb-6">
                  Our Enterprise plan can be tailored to your specific needs with custom features, 
                  integrations, and deployment options.
                </p>
                <motion.button
                  whileHover={{ scale: 1.05, y: -2 }}
                  whileTap={{ scale: 0.95 }}
                  className="inline-flex items-center space-x-2 px-6 py-3 gradient-button text-white font-semibold rounded-lg"
                >
                  <span>Schedule a Demo</span>
                  <ArrowRight className="w-4 h-4" />
                </motion.button>
              </div>
            </motion.div>
          </div>
        </section>

        {/* FAQ Section */}
        <section className="py-20 bg-dark-800/50">
          <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
            <motion.div
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              className="text-center mb-12"
            >
              <h2 className="text-3xl md:text-4xl font-bold text-white mb-4">
                Frequently Asked Questions
              </h2>
              <p className="text-gray-400 text-lg">
                Got questions? We've got answers. If you can't find what you're looking for, 
                feel free to contact our support team.
              </p>
            </motion.div>

            <div className="space-y-4">
              {faqs.map((faq, index) => (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, y: 20 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true }}
                  transition={{ delay: index * 0.1 }}
                  className="glass-effect rounded-lg border border-white/10"
                >
                  <button
                    onClick={() => setExpandedFaq(expandedFaq === index ? null : index)}
                    className="w-full px-6 py-4 text-left flex items-center justify-between hover:bg-white/5 transition-colors"
                  >
                    <span className="text-white font-medium">{faq.question}</span>
                    <motion.div
                      animate={{ rotate: expandedFaq === index ? 180 : 0 }}
                      className="w-5 h-5 text-gray-400"
                    >
                      <ArrowRight className="w-5 h-5 transform rotate-90" />
                    </motion.div>
                  </button>
                  {expandedFaq === index && (
                    <motion.div
                      initial={{ height: 0, opacity: 0 }}
                      animate={{ height: 'auto', opacity: 1 }}
                      exit={{ height: 0, opacity: 0 }}
                      className="px-6 pb-4"
                    >
                      <p className="text-gray-400">{faq.answer}</p>
                    </motion.div>
                  )}
                </motion.div>
              ))}
            </div>
          </div>
        </section>
      </main>
      <Footer />
    </>
  )
}
