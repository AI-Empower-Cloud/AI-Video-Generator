'use client'

import { motion } from 'framer-motion'
import { useState } from 'react'
import { useSession } from 'next-auth/react'
import Navigation from '../../components/Navigation'
import { 
  Play, 
  Plus, 
  Search, 
  Filter, 
  Grid, 
  List, 
  Calendar,
  TrendingUp,
  Video,
  Clock,
  Star,
  Download,
  Share2,
  Edit,
  Trash2,
  MoreVertical
} from 'lucide-react'

const recentProjects = [
  {
    id: 1,
    title: 'Marketing Campaign Q4',
    thumbnail: '/thumbnails/project1.jpg',
    duration: '2:45',
    created: '2 days ago',
    status: 'completed',
    views: 1245,
    type: 'marketing'
  },
  {
    id: 2,
    title: 'Educational Series Ep. 1',
    thumbnail: '/thumbnails/project2.jpg',
    duration: '5:20',
    created: '1 week ago',
    status: 'rendering',
    views: 856,
    type: 'education'
  },
  {
    id: 3,
    title: 'Product Demo Video',
    thumbnail: '/thumbnails/project3.jpg',
    duration: '1:30',
    created: '3 days ago',
    status: 'draft',
    views: 0,
    type: 'corporate'
  },
  {
    id: 4,
    title: 'Social Media Promo',
    thumbnail: '/thumbnails/project4.jpg',
    duration: '0:30',
    created: '5 days ago',
    status: 'completed',
    views: 2341,
    type: 'social'
  }
]

const stats = [
  { label: 'Total Videos', value: '24', change: '+12%', icon: Video },
  { label: 'Total Views', value: '45.2K', change: '+23%', icon: TrendingUp },
  { label: 'Hours Saved', value: '156', change: '+45%', icon: Clock },
  { label: 'Avg Rating', value: '4.8', change: '+0.2', icon: Star },
]

export default function Dashboard() {
  const { data: session } = useSession()
  const [viewMode, setViewMode] = useState<'grid' | 'list'>('grid')
  const [searchQuery, setSearchQuery] = useState('')
  const [filterType, setFilterType] = useState('all')

  if (!session) {
    return (
      <>
        <Navigation />
        <div className="min-h-screen flex items-center justify-center bg-dark-900">
          <div className="text-center">
            <h1 className="text-2xl font-bold text-white mb-4">Please sign in to access your dashboard</h1>
            <p className="text-gray-400">You need to be logged in to view your projects and analytics.</p>
          </div>
        </div>
      </>
    )
  }

  return (
    <>
      <Navigation />
      <div className="min-h-screen bg-dark-900 pt-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          {/* Header */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="mb-8"
          >
            <h1 className="text-3xl font-bold text-white mb-2">
              Welcome back, {session.user?.name?.split(' ')[0]}! 👋
            </h1>
            <p className="text-gray-400">
              Here's what's happening with your video projects today.
            </p>
          </motion.div>

          {/* Stats Cards */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
            className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8"
          >
            {stats.map((stat, index) => (
              <div key={stat.label} className="glass-effect rounded-xl p-6 border border-white/10">
                <div className="flex items-center justify-between mb-4">
                  <div className="w-10 h-10 bg-gradient-to-r from-primary-500 to-purple-600 rounded-lg flex items-center justify-center">
                    <stat.icon className="w-5 h-5 text-white" />
                  </div>
                  <span className="text-xs text-green-400 font-medium">{stat.change}</span>
                </div>
                <div className="text-2xl font-bold text-white mb-1">{stat.value}</div>
                <div className="text-sm text-gray-400">{stat.label}</div>
              </div>
            ))}
          </motion.div>

          {/* Quick Actions */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="mb-8"
          >
            <h2 className="text-xl font-semibold text-white mb-4">Quick Actions</h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <motion.button
                whileHover={{ scale: 1.02, y: -2 }}
                whileTap={{ scale: 0.98 }}
                className="group glass-effect rounded-xl p-6 border border-white/10 hover:border-primary-500/50 transition-all duration-300 text-left"
              >
                <div className="w-12 h-12 bg-gradient-to-r from-primary-500 to-blue-600 rounded-lg flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
                  <Plus className="w-6 h-6 text-white" />
                </div>
                <h3 className="text-lg font-semibold text-white mb-2">Create New Video</h3>
                <p className="text-gray-400 text-sm">Start from scratch or use a template</p>
              </motion.button>

              <motion.button
                whileHover={{ scale: 1.02, y: -2 }}
                whileTap={{ scale: 0.98 }}
                className="group glass-effect rounded-xl p-6 border border-white/10 hover:border-purple-500/50 transition-all duration-300 text-left"
              >
                <div className="w-12 h-12 bg-gradient-to-r from-purple-500 to-pink-600 rounded-lg flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
                  <Video className="w-6 h-6 text-white" />
                </div>
                <h3 className="text-lg font-semibold text-white mb-2">Browse Templates</h3>
                <p className="text-gray-400 text-sm">Explore our template library</p>
              </motion.button>

              <motion.button
                whileHover={{ scale: 1.02, y: -2 }}
                whileTap={{ scale: 0.98 }}
                className="group glass-effect rounded-xl p-6 border border-white/10 hover:border-green-500/50 transition-all duration-300 text-left"
              >
                <div className="w-12 h-12 bg-gradient-to-r from-green-500 to-teal-600 rounded-lg flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
                  <TrendingUp className="w-6 h-6 text-white" />
                </div>
                <h3 className="text-lg font-semibold text-white mb-2">View Analytics</h3>
                <p className="text-gray-400 text-sm">Track your video performance</p>
              </motion.button>
            </div>
          </motion.div>

          {/* Projects Section */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
          >
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-xl font-semibold text-white">Recent Projects</h2>
              
              {/* Controls */}
              <div className="flex items-center space-x-4">
                {/* Search */}
                <div className="relative">
                  <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
                  <input
                    type="text"
                    placeholder="Search projects..."
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    className="pl-10 pr-4 py-2 bg-dark-800 border border-gray-700 rounded-lg text-white placeholder-gray-400 focus:border-primary-500 focus:outline-none"
                  />
                </div>

                {/* Filter */}
                <select
                  value={filterType}
                  onChange={(e) => setFilterType(e.target.value)}
                  className="px-4 py-2 bg-dark-800 border border-gray-700 rounded-lg text-white focus:border-primary-500 focus:outline-none"
                >
                  <option value="all">All Types</option>
                  <option value="marketing">Marketing</option>
                  <option value="education">Education</option>
                  <option value="corporate">Corporate</option>
                  <option value="social">Social</option>
                </select>

                {/* View Mode */}
                <div className="flex bg-dark-800 rounded-lg border border-gray-700">
                  <button
                    onClick={() => setViewMode('grid')}
                    className={`p-2 rounded-l-lg transition-colors ${
                      viewMode === 'grid' ? 'bg-primary-500 text-white' : 'text-gray-400 hover:text-white'
                    }`}
                  >
                    <Grid className="w-4 h-4" />
                  </button>
                  <button
                    onClick={() => setViewMode('list')}
                    className={`p-2 rounded-r-lg transition-colors ${
                      viewMode === 'list' ? 'bg-primary-500 text-white' : 'text-gray-400 hover:text-white'
                    }`}
                  >
                    <List className="w-4 h-4" />
                  </button>
                </div>
              </div>
            </div>

            {/* Projects Grid/List */}
            <div className={viewMode === 'grid' ? 'grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6' : 'space-y-4'}>
              {recentProjects.map((project, index) => (
                <motion.div
                  key={project.id}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.4 + index * 0.1 }}
                  whileHover={{ y: -5, scale: 1.02 }}
                  className="group glass-effect rounded-xl border border-white/10 hover:border-white/20 transition-all duration-300 overflow-hidden"
                >
                  {viewMode === 'grid' ? (
                    <>
                      {/* Thumbnail */}
                      <div className="relative aspect-video bg-gradient-to-br from-dark-700 to-dark-800 flex items-center justify-center">
                        <Play className="w-12 h-12 text-white/50 group-hover:text-white transition-colors" />
                        <div className="absolute bottom-2 right-2 px-2 py-1 bg-black/50 rounded text-xs text-white">
                          {project.duration}
                        </div>
                        <div className={`absolute top-2 left-2 px-2 py-1 rounded-full text-xs font-medium ${
                          project.status === 'completed' ? 'bg-green-500/20 text-green-400' :
                          project.status === 'rendering' ? 'bg-yellow-500/20 text-yellow-400' :
                          'bg-gray-500/20 text-gray-400'
                        }`}>
                          {project.status}
                        </div>
                      </div>

                      {/* Content */}
                      <div className="p-4">
                        <h3 className="font-semibold text-white mb-2 group-hover:text-primary-300 transition-colors">
                          {project.title}
                        </h3>
                        <div className="flex items-center justify-between text-sm text-gray-400 mb-3">
                          <span>{project.created}</span>
                          <span>{project.views} views</span>
                        </div>

                        {/* Actions */}
                        <div className="flex items-center justify-between">
                          <div className="flex space-x-2">
                            <motion.button
                              whileHover={{ scale: 1.1 }}
                              whileTap={{ scale: 0.9 }}
                              className="p-1 hover:bg-white/10 rounded"
                            >
                              <Edit className="w-4 h-4 text-gray-400 hover:text-white" />
                            </motion.button>
                            <motion.button
                              whileHover={{ scale: 1.1 }}
                              whileTap={{ scale: 0.9 }}
                              className="p-1 hover:bg-white/10 rounded"
                            >
                              <Download className="w-4 h-4 text-gray-400 hover:text-white" />
                            </motion.button>
                            <motion.button
                              whileHover={{ scale: 1.1 }}
                              whileTap={{ scale: 0.9 }}
                              className="p-1 hover:bg-white/10 rounded"
                            >
                              <Share2 className="w-4 h-4 text-gray-400 hover:text-white" />
                            </motion.button>
                          </div>
                          <motion.button
                            whileHover={{ scale: 1.1 }}
                            whileTap={{ scale: 0.9 }}
                            className="p-1 hover:bg-white/10 rounded"
                          >
                            <MoreVertical className="w-4 h-4 text-gray-400 hover:text-white" />
                          </motion.button>
                        </div>
                      </div>
                    </>
                  ) : (
                    // List view
                    <div className="flex items-center p-4 space-x-4">
                      <div className="w-16 h-16 bg-gradient-to-br from-dark-700 to-dark-800 rounded-lg flex items-center justify-center flex-shrink-0">
                        <Play className="w-6 h-6 text-white/50" />
                      </div>
                      <div className="flex-1">
                        <h3 className="font-semibold text-white mb-1">{project.title}</h3>
                        <div className="flex items-center space-x-4 text-sm text-gray-400">
                          <span>{project.duration}</span>
                          <span>{project.created}</span>
                          <span>{project.views} views</span>
                          <span className={`px-2 py-1 rounded-full text-xs ${
                            project.status === 'completed' ? 'bg-green-500/20 text-green-400' :
                            project.status === 'rendering' ? 'bg-yellow-500/20 text-yellow-400' :
                            'bg-gray-500/20 text-gray-400'
                          }`}>
                            {project.status}
                          </span>
                        </div>
                      </div>
                      <div className="flex space-x-2">
                        <motion.button
                          whileHover={{ scale: 1.1 }}
                          whileTap={{ scale: 0.9 }}
                          className="p-2 hover:bg-white/10 rounded"
                        >
                          <Edit className="w-4 h-4 text-gray-400 hover:text-white" />
                        </motion.button>
                        <motion.button
                          whileHover={{ scale: 1.1 }}
                          whileTap={{ scale: 0.9 }}
                          className="p-2 hover:bg-white/10 rounded"
                        >
                          <MoreVertical className="w-4 h-4 text-gray-400 hover:text-white" />
                        </motion.button>
                      </div>
                    </div>
                  )}
                </motion.div>
              ))}
            </div>
          </motion.div>
        </div>
      </div>
    </>
  )
}
