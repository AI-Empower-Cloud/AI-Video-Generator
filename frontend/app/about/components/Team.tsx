'use client'

import { motion } from 'framer-motion'
import { useInView } from 'framer-motion'
import { useRef } from 'react'
import { Linkedin, Twitter, Github, Mail } from 'lucide-react'

const team = [
  {
    name: 'Sarah Chen',
    role: 'CEO & Co-Founder',
    bio: 'Former AI researcher at Google with 10+ years in machine learning and computer vision.',
    image: '/api/placeholder/300/400',
    social: {
      linkedin: '#',
      twitter: '#',
      email: 'sarah@aivideogen.com'
    }
  },
  {
    name: 'Marcus Rodriguez',
    role: 'CTO & Co-Founder',
    bio: 'Ex-Netflix engineer who led video processing infrastructure serving billions of users.',
    image: '/api/placeholder/300/400',
    social: {
      linkedin: '#',
      github: '#',
      email: 'marcus@aivideogen.com'
    }
  },
  {
    name: 'Dr. Priya Patel',
    role: 'Head of AI Research',
    bio: 'PhD in Computer Vision from Stanford, published 50+ papers on generative AI models.',
    image: '/api/placeholder/300/400',
    social: {
      linkedin: '#',
      twitter: '#',
      email: 'priya@aivideogen.com'
    }
  },
  {
    name: 'Alex Kim',
    role: 'Head of Product',
    bio: 'Former product lead at Adobe Creative Cloud, expert in creative tools and user experience.',
    image: '/api/placeholder/300/400',
    social: {
      linkedin: '#',
      twitter: '#',
      email: 'alex@aivideogen.com'
    }
  },
  {
    name: 'Emily Thompson',
    role: 'Head of Engineering',
    bio: 'Full-stack architect with experience scaling platforms to millions of users.',
    image: '/api/placeholder/300/400',
    social: {
      linkedin: '#',
      github: '#',
      email: 'emily@aivideogen.com'
    }
  },
  {
    name: 'David Okafor',
    role: 'Head of Design',
    bio: 'Award-winning designer who believes great design makes complex technology accessible.',
    image: '/api/placeholder/300/400',
    social: {
      linkedin: '#',
      twitter: '#',
      email: 'david@aivideogen.com'
    }
  }
]

export default function Team() {
  const ref = useRef(null)
  const isInView = useInView(ref, { once: true, amount: 0.2 })

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
            Meet Our Team
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            The brilliant minds behind the technology that's revolutionizing video creation.
          </p>
        </motion.div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {team.map((member, index) => (
            <motion.div
              key={member.name}
              initial={{ opacity: 0, y: 50 }}
              animate={isInView ? { opacity: 1, y: 0 } : { opacity: 0, y: 50 }}
              transition={{ duration: 0.6, delay: index * 0.1 }}
              className="group relative bg-white rounded-2xl overflow-hidden shadow-lg hover:shadow-2xl transition-all duration-300 border border-gray-100"
            >
              <div className="aspect-w-3 aspect-h-4 relative overflow-hidden">
                <div className="w-full h-80 bg-gradient-to-br from-purple-100 to-blue-100 flex items-center justify-center">
                  <div className="w-32 h-32 bg-gradient-to-br from-purple-400 to-blue-400 rounded-full flex items-center justify-center text-white text-4xl font-bold">
                    {member.name.split(' ').map(n => n[0]).join('')}
                  </div>
                </div>
                <div className="absolute inset-0 bg-gradient-to-t from-black/50 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
              </div>
              
              <div className="p-6">
                <h3 className="text-2xl font-bold text-gray-900 mb-2">
                  {member.name}
                </h3>
                <p className="text-purple-600 font-semibold mb-4">
                  {member.role}
                </p>
                <p className="text-gray-600 leading-relaxed mb-6">
                  {member.bio}
                </p>
                
                <div className="flex space-x-4">
                  {member.social.linkedin && (
                    <a 
                      href={member.social.linkedin}
                      className="w-10 h-10 bg-gray-100 rounded-full flex items-center justify-center hover:bg-purple-100 transition-colors duration-200"
                    >
                      <Linkedin className="w-5 h-5 text-gray-600 hover:text-purple-600" />
                    </a>
                  )}
                  {member.social.twitter && (
                    <a 
                      href={member.social.twitter}
                      className="w-10 h-10 bg-gray-100 rounded-full flex items-center justify-center hover:bg-blue-100 transition-colors duration-200"
                    >
                      <Twitter className="w-5 h-5 text-gray-600 hover:text-blue-600" />
                    </a>
                  )}
                  {member.social.github && (
                    <a 
                      href={member.social.github}
                      className="w-10 h-10 bg-gray-100 rounded-full flex items-center justify-center hover:bg-gray-200 transition-colors duration-200"
                    >
                      <Github className="w-5 h-5 text-gray-600 hover:text-gray-800" />
                    </a>
                  )}
                  {member.social.email && (
                    <a 
                      href={`mailto:${member.social.email}`}
                      className="w-10 h-10 bg-gray-100 rounded-full flex items-center justify-center hover:bg-green-100 transition-colors duration-200"
                    >
                      <Mail className="w-5 h-5 text-gray-600 hover:text-green-600" />
                    </a>
                  )}
                </div>
              </div>
            </motion.div>
          ))}
        </div>

        <motion.div
          initial={{ opacity: 0, y: 50 }}
          animate={isInView ? { opacity: 1, y: 0 } : { opacity: 0, y: 50 }}
          transition={{ duration: 0.8, delay: 0.8 }}
          className="mt-16 text-center"
        >
          <div className="bg-gradient-to-br from-gray-50 to-blue-50 rounded-2xl p-8 border border-gray-200">
            <h3 className="text-3xl font-bold text-gray-900 mb-4">
              We're Growing
            </h3>
            <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
              Join our team of innovators, creators, and technologists who are shaping the future of video content.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <button className="bg-purple-600 text-white px-8 py-3 rounded-lg font-semibold hover:bg-purple-700 transition-colors duration-200">
                View Open Positions
              </button>
              <button className="border-2 border-purple-600 text-purple-600 px-8 py-3 rounded-lg font-semibold hover:bg-purple-600 hover:text-white transition-colors duration-200">
                Learn About Our Culture
              </button>
            </div>
          </div>
        </motion.div>
      </div>
    </section>
  )
}
