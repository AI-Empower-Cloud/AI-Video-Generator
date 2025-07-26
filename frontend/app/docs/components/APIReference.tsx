'use client'

import { motion } from 'framer-motion'
import { useInView } from 'framer-motion'
import { useRef } from 'react'
import { Code, Database, Zap, Shield, Globe, Key } from 'lucide-react'

const apiSections = [
  {
    title: 'Authentication',
    icon: Key,
    description: 'Secure API key authentication',
    endpoints: [
      { method: 'POST', path: '/auth/token', description: 'Get access token' },
      { method: 'GET', path: '/auth/validate', description: 'Validate token' }
    ]
  },
  {
    title: 'Video Generation',
    icon: Zap,
    description: 'Core video generation endpoints',
    endpoints: [
      { method: 'POST', path: '/api/v1/generate', description: 'Create new video' },
      { method: 'GET', path: '/api/v1/status/{id}', description: 'Check generation status' },
      { method: 'GET', path: '/api/v1/download/{id}', description: 'Download completed video' }
    ]
  },
  {
    title: 'Projects',
    icon: Database,
    description: 'Project management endpoints',
    endpoints: [
      { method: 'GET', path: '/api/v1/projects', description: 'List all projects' },
      { method: 'POST', path: '/api/v1/projects', description: 'Create new project' },
      { method: 'GET', path: '/api/v1/projects/{id}', description: 'Get project details' },
      { method: 'PUT', path: '/api/v1/projects/{id}', description: 'Update project' },
      { method: 'DELETE', path: '/api/v1/projects/{id}', description: 'Delete project' }
    ]
  },
  {
    title: 'Assets',
    icon: Globe,
    description: 'Asset management endpoints',
    endpoints: [
      { method: 'POST', path: '/api/v1/assets/upload', description: 'Upload media file' },
      { method: 'GET', path: '/api/v1/assets', description: 'List assets' },
      { method: 'DELETE', path: '/api/v1/assets/{id}', description: 'Delete asset' }
    ]
  }
]

const methodColors: Record<string, string> = {
  'GET': 'bg-green-100 text-green-800 border-green-200',
  'POST': 'bg-blue-100 text-blue-800 border-blue-200',
  'PUT': 'bg-yellow-100 text-yellow-800 border-yellow-200',
  'DELETE': 'bg-red-100 text-red-800 border-red-200'
}

export default function APIReference() {
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
            API Reference
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Complete reference for our RESTful API. Generate videos programmatically with simple HTTP requests.
          </p>
        </motion.div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {apiSections.map((section, index) => {
            const Icon = section.icon
            return (
              <motion.div
                key={section.title}
                initial={{ opacity: 0, y: 50 }}
                animate={isInView ? { opacity: 1, y: 0 } : { opacity: 0, y: 50 }}
                transition={{ duration: 0.6, delay: index * 0.1 }}
                className="bg-white rounded-2xl p-8 shadow-lg border border-gray-100"
              >
                <div className="flex items-center mb-6">
                  <div className="w-12 h-12 bg-gradient-to-r from-purple-600 to-blue-600 rounded-xl flex items-center justify-center mr-4">
                    <Icon className="w-6 h-6 text-white" />
                  </div>
                  <div>
                    <h3 className="text-2xl font-bold text-gray-900">{section.title}</h3>
                    <p className="text-gray-600">{section.description}</p>
                  </div>
                </div>

                <div className="space-y-4">
                  {section.endpoints.map((endpoint, i) => (
                    <div key={i} className="border border-gray-200 rounded-lg p-4 hover:border-purple-300 transition-colors duration-200">
                      <div className="flex items-center justify-between mb-2">
                        <div className="flex items-center space-x-3">
                          <span className={`px-3 py-1 rounded-lg text-sm font-semibold border ${methodColors[endpoint.method]}`}>
                            {endpoint.method}
                          </span>
                          <code className="text-sm font-mono text-gray-700 bg-gray-100 px-2 py-1 rounded">
                            {endpoint.path}
                          </code>
                        </div>
                      </div>
                      <p className="text-gray-600 text-sm">{endpoint.description}</p>
                    </div>
                  ))}
                </div>

                <button className="mt-6 w-full bg-gradient-to-r from-purple-600 to-blue-600 text-white py-3 px-6 rounded-lg font-semibold hover:from-purple-700 hover:to-blue-700 transition-all duration-200">
                  View Full Documentation
                </button>
              </motion.div>
            )
          })}
        </div>

        <motion.div
          initial={{ opacity: 0, y: 50 }}
          animate={isInView ? { opacity: 1, y: 0 } : { opacity: 0, y: 50 }}
          transition={{ duration: 0.8, delay: 0.4 }}
          className="mt-16"
        >
          <div className="bg-gray-900 rounded-2xl p-8 text-white">
            <h3 className="text-2xl font-bold mb-6 flex items-center">
              <Code className="w-8 h-8 mr-3" />
              Example Request
            </h3>
            
            <div className="bg-black rounded-lg p-6 overflow-x-auto">
              <pre className="text-green-400 text-sm">
                <code>{`curl -X POST "https://api.aivideogen.com/v1/generate" \\
  -H "Authorization: Bearer YOUR_API_KEY" \\
  -H "Content-Type: application/json" \\
  -d '{
    "prompt": "A peaceful sunset over mountains",
    "duration": 30,
    "style": "cinematic",
    "resolution": "1920x1080",
    "fps": 30
  }'`}</code>
              </pre>
            </div>

            <div className="mt-6 grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="text-center">
                <Shield className="w-8 h-8 text-green-400 mx-auto mb-2" />
                <h4 className="font-semibold mb-1">Secure</h4>
                <p className="text-gray-300 text-sm">Enterprise-grade security</p>
              </div>
              <div className="text-center">
                <Zap className="w-8 h-8 text-yellow-400 mx-auto mb-2" />
                <h4 className="font-semibold mb-1">Fast</h4>
                <p className="text-gray-300 text-sm">Sub-second response times</p>
              </div>
              <div className="text-center">
                <Globe className="w-8 h-8 text-blue-400 mx-auto mb-2" />
                <h4 className="font-semibold mb-1">Global</h4>
                <p className="text-gray-300 text-sm">Worldwide CDN</p>
              </div>
            </div>
          </div>
        </motion.div>
      </div>
    </section>
  )
}
