'use client'

import { motion } from 'framer-motion'
import { useInView } from 'framer-motion'
import { useRef } from 'react'
import { Lightbulb, Users, Globe } from 'lucide-react'

export default function Mission() {
  const ref = useRef(null)
  const isInView = useInView(ref, { once: true, amount: 0.3 })

  return (
    <section ref={ref} className="py-20 bg-gradient-to-br from-gray-50 to-blue-50">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 50 }}
          animate={isInView ? { opacity: 1, y: 0 } : { opacity: 0, y: 50 }}
          transition={{ duration: 0.8 }}
          className="text-center mb-16"
        >
          <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">
            Our Mission
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            We believe that everyone deserves access to professional-quality video creation tools. 
            Our mission is to break down the barriers between imagination and creation.
          </p>
        </motion.div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">
          <motion.div
            initial={{ opacity: 0, x: -50 }}
            animate={isInView ? { opacity: 1, x: 0 } : { opacity: 0, x: -50 }}
            transition={{ duration: 0.8, delay: 0.2 }}
          >
            <h3 className="text-3xl font-bold text-gray-900 mb-6">
              Empowering Creators Worldwide
            </h3>
            <p className="text-lg text-gray-600 mb-8">
              From content creators and marketers to educators and entrepreneurs, 
              we're building tools that amplify human creativity rather than replace it. 
              Our AI doesn't just generate videos—it understands context, emotion, 
              and storytelling to help you bring your vision to life.
            </p>
            
            <div className="space-y-6">
              <div className="flex items-start space-x-4">
                <Lightbulb className="w-8 h-8 text-purple-600 mt-1 flex-shrink-0" />
                <div>
                  <h4 className="text-xl font-semibold text-gray-900 mb-2">Innovation First</h4>
                  <p className="text-gray-600">
                    We're constantly pushing the boundaries of what's possible with AI video generation
                  </p>
                </div>
              </div>

              <div className="flex items-start space-x-4">
                <Users className="w-8 h-8 text-blue-600 mt-1 flex-shrink-0" />
                <div>
                  <h4 className="text-xl font-semibold text-gray-900 mb-2">Community Driven</h4>
                  <p className="text-gray-600">
                    Our platform evolves based on real user feedback and creative needs
                  </p>
                </div>
              </div>

              <div className="flex items-start space-x-4">
                <Globe className="w-8 h-8 text-green-600 mt-1 flex-shrink-0" />
                <div>
                  <h4 className="text-xl font-semibold text-gray-900 mb-2">Global Impact</h4>
                  <p className="text-gray-600">
                    Making professional video creation accessible to creators everywhere
                  </p>
                </div>
              </div>
            </div>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, x: 50 }}
            animate={isInView ? { opacity: 1, x: 0 } : { opacity: 0, x: 50 }}
            transition={{ duration: 0.8, delay: 0.4 }}
            className="relative"
          >
            <div className="relative z-10 bg-gradient-to-br from-purple-600 to-blue-600 rounded-2xl p-8 text-white">
              <h4 className="text-2xl font-bold mb-4">Our Vision</h4>
              <p className="text-lg mb-6">
                A world where anyone can create professional-quality videos as easily as writing a text message.
              </p>
              <div className="grid grid-cols-2 gap-4 text-center">
                <div>
                  <div className="text-3xl font-bold">10M+</div>
                  <div className="text-purple-200">Videos Created</div>
                </div>
                <div>
                  <div className="text-3xl font-bold">150+</div>
                  <div className="text-purple-200">Countries</div>
                </div>
                <div>
                  <div className="text-3xl font-bold">99.9%</div>
                  <div className="text-purple-200">Uptime</div>
                </div>
                <div>
                  <div className="text-3xl font-bold">24/7</div>
                  <div className="text-purple-200">Support</div>
                </div>
              </div>
            </div>
            <div className="absolute inset-0 bg-gradient-to-br from-purple-600 to-blue-600 rounded-2xl transform rotate-3 -z-10" />
          </motion.div>
        </div>
      </div>
    </section>
  )
}
