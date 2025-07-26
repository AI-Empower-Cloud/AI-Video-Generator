'use client'

import { motion } from 'framer-motion'
import { useInView } from 'framer-motion'
import { useRef } from 'react'
import { 
  ShoppingBag, 
  GraduationCap, 
  Briefcase, 
  Heart, 
  Gamepad2, 
  Building, 
  Megaphone,
  Users
} from 'lucide-react'

const industries = [
  {
    icon: ShoppingBag,
    title: 'E-commerce & Retail',
    description: 'Product demonstrations, unboxing videos, and promotional content that drive sales.',
    useCases: ['Product demos', 'Unboxing videos', 'Sale announcements', 'Brand stories'],
    color: 'from-purple-500 to-pink-500'
  },
  {
    icon: GraduationCap,
    title: 'Education & Training',
    description: 'Interactive learning content, course materials, and professional development videos.',
    useCases: ['Online courses', 'Training modules', 'Educational content', 'Skill tutorials'],
    color: 'from-blue-500 to-indigo-500'
  },
  {
    icon: Briefcase,
    title: 'Corporate & Business',
    description: 'Internal communications, presentations, and professional development content.',
    useCases: ['Company updates', 'HR training', 'Product launches', 'Team building'],
    color: 'from-green-500 to-teal-500'
  },
  {
    icon: Heart,
    title: 'Healthcare & Wellness',
    description: 'Patient education, wellness content, and medical training materials.',
    useCases: ['Patient education', 'Wellness tips', 'Medical training', 'Health awareness'],
    color: 'from-red-500 to-pink-500'
  },
  {
    icon: Gamepad2,
    title: 'Entertainment & Gaming',
    description: 'Game trailers, character animations, and interactive storytelling content.',
    useCases: ['Game trailers', 'Character videos', 'Story content', 'Fan engagement'],
    color: 'from-orange-500 to-yellow-500'
  },
  {
    icon: Building,
    title: 'Real Estate',
    description: 'Property tours, market updates, and client testimonials for real estate professionals.',
    useCases: ['Property tours', 'Market updates', 'Client testimonials', 'Agent profiles'],
    color: 'from-indigo-500 to-purple-500'
  },
  {
    icon: Megaphone,
    title: 'Marketing & Advertising',
    description: 'Campaign videos, social media content, and brand storytelling at scale.',
    useCases: ['Ad campaigns', 'Social content', 'Brand videos', 'Testimonials'],
    color: 'from-cyan-500 to-blue-500'
  },
  {
    icon: Users,
    title: 'Non-Profit & Social',
    description: 'Awareness campaigns, fundraising videos, and community engagement content.',
    useCases: ['Awareness campaigns', 'Fundraising videos', 'Volunteer recruitment', 'Impact stories'],
    color: 'from-emerald-500 to-green-500'
  }
]

export default function IndustryUseCases() {
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
            Industries We Serve
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            From startups to Fortune 500 companies, our AI video generation platform 
            transforms how industries communicate, educate, and engage.
          </p>
        </motion.div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          {industries.map((industry, index) => {
            const Icon = industry.icon
            return (
              <motion.div
                key={industry.title}
                initial={{ opacity: 0, y: 50 }}
                animate={isInView ? { opacity: 1, y: 0 } : { opacity: 0, y: 50 }}
                transition={{ duration: 0.6, delay: index * 0.1 }}
                className="group bg-white rounded-2xl p-6 shadow-lg hover:shadow-2xl transition-all duration-300 border border-gray-100"
              >
                <div className={`w-16 h-16 bg-gradient-to-br ${industry.color} rounded-xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300`}>
                  <Icon className="w-8 h-8 text-white" />
                </div>
                
                <h3 className="text-xl font-bold text-gray-900 mb-3 group-hover:text-purple-700 transition-colors duration-300">
                  {industry.title}
                </h3>
                
                <p className="text-gray-600 mb-4 leading-relaxed">
                  {industry.description}
                </p>
                
                <div className="space-y-2">
                  {industry.useCases.map((useCase, i) => (
                    <div key={i} className="flex items-center text-sm text-gray-500">
                      <div className="w-1.5 h-1.5 bg-purple-400 rounded-full mr-3" />
                      {useCase}
                    </div>
                  ))}
                </div>
                
                <button className="mt-6 w-full bg-gradient-to-r from-purple-600 to-blue-600 text-white py-2 px-4 rounded-lg font-semibold opacity-0 group-hover:opacity-100 transition-all duration-300 hover:from-purple-700 hover:to-blue-700">
                  Explore Examples
                </button>
              </motion.div>
            )
          })}
        </div>

        <motion.div
          initial={{ opacity: 0, y: 50 }}
          animate={isInView ? { opacity: 1, y: 0 } : { opacity: 0, y: 50 }}
          transition={{ duration: 0.8, delay: 0.8 }}
          className="mt-16 text-center"
        >
          <div className="bg-gradient-to-br from-purple-600 to-blue-600 rounded-2xl p-8 text-white">
            <h3 className="text-3xl font-bold mb-4">
              Don't See Your Industry?
            </h3>
            <p className="text-xl text-purple-100 mb-8 max-w-2xl mx-auto">
              Our platform is flexible enough to handle any use case. Let's discuss how we can help your specific industry.
            </p>
            <button className="bg-white text-purple-600 px-8 py-3 rounded-lg font-semibold hover:bg-gray-100 transition-colors duration-200">
              Schedule a Demo
            </button>
          </div>
        </motion.div>
      </div>
    </section>
  )
}
