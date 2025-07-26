'use client'

import { useState } from 'react'
import { motion } from 'framer-motion'
import Navigation from '../../components/Navigation'
import Footer from '../../components/Footer'
import { 
  Calendar, 
  Clock, 
  User, 
  ArrowRight, 
  Search,
  Filter,
  Tag
} from 'lucide-react'

const blogPosts = [
  {
    id: 1,
    title: 'The Future of AI Video Generation: What to Expect in 2025',
    excerpt: 'Explore the cutting-edge developments in AI video technology and how they will transform content creation in the coming year.',
    author: 'Sarah Chen',
    date: '2024-12-15',
    readTime: '8 min read',
    category: 'Technology',
    tags: ['AI', 'Future Tech', 'Video Generation'],
    image: '/api/placeholder/600/400',
    featured: true
  },
  {
    id: 2,
    title: 'Best Practices for Creating Engaging Marketing Videos with AI',
    excerpt: 'Learn proven strategies to create compelling marketing content that converts using AI video generation tools.',
    author: 'Marcus Rodriguez',
    date: '2024-12-12',
    readTime: '6 min read',
    category: 'Marketing',
    tags: ['Marketing', 'Best Practices', 'Video Strategy'],
    image: '/api/placeholder/600/400',
    featured: false
  },
  {
    id: 3,
    title: 'From Concept to Creation: A Complete Guide to AI Video Workflows',
    excerpt: 'Step-by-step guide to building efficient video production workflows using artificial intelligence.',
    author: 'Dr. Priya Patel',
    date: '2024-12-10',
    readTime: '12 min read',
    category: 'Tutorial',
    tags: ['Workflow', 'Tutorial', 'Production'],
    image: '/api/placeholder/600/400',
    featured: false
  },
  {
    id: 4,
    title: 'Case Study: How Enterprise Companies Are Scaling Video Content',
    excerpt: 'Real-world examples of how Fortune 500 companies are using AI to scale their video content production.',
    author: 'Alex Kim',
    date: '2024-12-08',
    readTime: '10 min read',
    category: 'Case Study',
    tags: ['Enterprise', 'Case Study', 'Scaling'],
    image: '/api/placeholder/600/400',
    featured: false
  },
  {
    id: 5,
    title: 'Understanding the Technology Behind AI Video Generation',
    excerpt: 'A deep dive into the machine learning models and algorithms that power modern AI video creation.',
    author: 'Dr. Priya Patel',
    date: '2024-12-05',
    readTime: '15 min read',
    category: 'Technical',
    tags: ['AI Technology', 'Machine Learning', 'Deep Dive'],
    image: '/api/placeholder/600/400',
    featured: false
  },
  {
    id: 6,
    title: '10 Creative Ways to Use AI Video in Your Content Strategy',
    excerpt: 'Discover innovative applications of AI video generation that go beyond traditional marketing content.',
    author: 'Emily Thompson',
    date: '2024-12-03',
    readTime: '7 min read',
    category: 'Creative',
    tags: ['Creativity', 'Content Strategy', 'Innovation'],
    image: '/api/placeholder/600/400',
    featured: false
  }
]

const categories = ['All', 'Technology', 'Marketing', 'Tutorial', 'Case Study', 'Technical', 'Creative']

export default function BlogPage() {
  const [searchTerm, setSearchTerm] = useState('')
  const [selectedCategory, setSelectedCategory] = useState('All')
  const [filteredPosts, setFilteredPosts] = useState(blogPosts)

  const handleSearch = (term: string) => {
    setSearchTerm(term)
    filterPosts(term, selectedCategory)
  }

  const handleCategoryFilter = (category: string) => {
    setSelectedCategory(category)
    filterPosts(searchTerm, category)
  }

  const filterPosts = (search: string, category: string) => {
    let filtered = blogPosts

    if (category !== 'All') {
      filtered = filtered.filter(post => post.category === category)
    }

    if (search) {
      filtered = filtered.filter(post =>
        post.title.toLowerCase().includes(search.toLowerCase()) ||
        post.excerpt.toLowerCase().includes(search.toLowerCase()) ||
        post.tags.some(tag => tag.toLowerCase().includes(search.toLowerCase()))
      )
    }

    setFilteredPosts(filtered)
  }

  const featuredPost = blogPosts.find(post => post.featured)
  const regularPosts = filteredPosts.filter(post => !post.featured)

  return (
    <>
      <Navigation />
      <main>
        {/* Hero Section */}
        <section className="relative min-h-[60vh] flex items-center justify-center bg-gradient-to-br from-purple-900 via-blue-900 to-indigo-900">
          <div className="absolute inset-0 overflow-hidden">
            <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-purple-500/20 rounded-full blur-3xl animate-pulse" />
            <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-blue-500/20 rounded-full blur-3xl animate-pulse delay-1000" />
          </div>

          <div className="relative z-10 max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
            <motion.div
              initial={{ opacity: 0, y: 50 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8 }}
            >
              <h1 className="text-5xl md:text-6xl font-bold text-white mb-6">
                AI Video
                <span className="bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent">
                  {' '}Insights
                </span>
              </h1>
              <p className="text-xl md:text-2xl text-gray-300 max-w-3xl mx-auto">
                Stay ahead of the curve with the latest insights, tutorials, and best practices 
                in AI-powered video generation.
              </p>
            </motion.div>
          </div>
        </section>

        {/* Search and Filter */}
        <section className="py-12 bg-gradient-to-br from-gray-50 to-blue-50">
          <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex flex-col md:flex-row gap-6 items-center justify-between">
              {/* Search */}
              <div className="relative flex-1 max-w-md">
                <Search className="absolute left-4 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
                <input
                  type="text"
                  placeholder="Search articles..."
                  value={searchTerm}
                  onChange={(e) => handleSearch(e.target.value)}
                  className="w-full pl-12 pr-4 py-3 bg-white border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                />
              </div>

              {/* Category Filter */}
              <div className="flex items-center space-x-2">
                <Filter className="w-5 h-5 text-gray-600" />
                <div className="flex flex-wrap gap-2">
                  {categories.map((category) => (
                    <button
                      key={category}
                      onClick={() => handleCategoryFilter(category)}
                      className={`px-4 py-2 rounded-lg font-medium transition-all duration-200 ${
                        selectedCategory === category
                          ? 'bg-purple-600 text-white'
                          : 'bg-white text-gray-700 hover:bg-purple-50 border border-gray-200'
                      }`}
                    >
                      {category}
                    </button>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Featured Post */}
        {featuredPost && selectedCategory === 'All' && !searchTerm && (
          <section className="py-16 bg-white">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
              <motion.div
                initial={{ opacity: 0, y: 50 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.8 }}
                className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center"
              >
                <div className="relative">
                  <div className="aspect-video bg-gradient-to-br from-purple-400 to-blue-500 rounded-2xl" />
                  <div className="absolute top-4 left-4 bg-yellow-400 text-black px-3 py-1 rounded-full text-sm font-semibold">
                    Featured
                  </div>
                </div>

                <div>
                  <div className="flex items-center space-x-4 mb-4">
                    <span className="bg-purple-100 text-purple-700 px-3 py-1 rounded-full text-sm font-medium">
                      {featuredPost.category}
                    </span>
                    <div className="flex items-center text-gray-500 text-sm">
                      <Calendar className="w-4 h-4 mr-1" />
                      {new Date(featuredPost.date).toLocaleDateString('en-US', { 
                        year: 'numeric', 
                        month: 'long', 
                        day: 'numeric' 
                      })}
                    </div>
                  </div>

                  <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
                    {featuredPost.title}
                  </h2>

                  <p className="text-lg text-gray-600 mb-6 leading-relaxed">
                    {featuredPost.excerpt}
                  </p>

                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-4">
                      <div className="flex items-center text-gray-500 text-sm">
                        <User className="w-4 h-4 mr-1" />
                        {featuredPost.author}
                      </div>
                      <div className="flex items-center text-gray-500 text-sm">
                        <Clock className="w-4 h-4 mr-1" />
                        {featuredPost.readTime}
                      </div>
                    </div>

                    <button className="bg-gradient-to-r from-purple-600 to-blue-600 text-white px-6 py-3 rounded-lg font-semibold hover:from-purple-700 hover:to-blue-700 transition-all duration-200 flex items-center space-x-2 group">
                      <span>Read Article</span>
                      <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform duration-200" />
                    </button>
                  </div>
                </div>
              </motion.div>
            </div>
          </section>
        )}

        {/* Blog Posts Grid */}
        <section className="py-20 bg-gradient-to-br from-gray-50 to-blue-50">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
              {regularPosts.map((post, index) => (
                <motion.article
                  key={post.id}
                  initial={{ opacity: 0, y: 50 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.6, delay: index * 0.1 }}
                  className="bg-white rounded-2xl shadow-lg overflow-hidden hover:shadow-xl transition-all duration-300 group"
                >
                  <div className="aspect-video bg-gradient-to-br from-purple-400 to-blue-500 relative">
                    <div className="absolute top-4 left-4 bg-white/90 text-purple-700 px-3 py-1 rounded-full text-sm font-medium">
                      {post.category}
                    </div>
                  </div>

                  <div className="p-6">
                    <h3 className="text-xl font-bold text-gray-900 mb-3 group-hover:text-purple-700 transition-colors duration-200 line-clamp-2">
                      {post.title}
                    </h3>

                    <p className="text-gray-600 mb-4 line-clamp-3">
                      {post.excerpt}
                    </p>

                    <div className="flex items-center justify-between mb-4">
                      <div className="flex items-center text-gray-500 text-sm">
                        <User className="w-4 h-4 mr-1" />
                        {post.author}
                      </div>
                      <div className="flex items-center text-gray-500 text-sm">
                        <Clock className="w-4 h-4 mr-1" />
                        {post.readTime}
                      </div>
                    </div>

                    <div className="flex items-center justify-between">
                      <div className="flex items-center text-gray-500 text-sm">
                        <Calendar className="w-4 h-4 mr-1" />
                        {new Date(post.date).toLocaleDateString('en-US', { 
                          month: 'short', 
                          day: 'numeric' 
                        })}
                      </div>

                      <button className="text-purple-600 hover:text-purple-700 font-semibold text-sm flex items-center space-x-1 group">
                        <span>Read More</span>
                        <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform duration-200" />
                      </button>
                    </div>

                    <div className="flex flex-wrap gap-2 mt-4">
                      {post.tags.slice(0, 2).map((tag) => (
                        <span key={tag} className="flex items-center text-xs text-gray-500 bg-gray-100 px-2 py-1 rounded-full">
                          <Tag className="w-3 h-3 mr-1" />
                          {tag}
                        </span>
                      ))}
                    </div>
                  </div>
                </motion.article>
              ))}
            </div>

            {filteredPosts.length === 0 && (
              <div className="text-center py-12">
                <h3 className="text-2xl font-bold text-gray-900 mb-4">No articles found</h3>
                <p className="text-gray-600 mb-6">Try adjusting your search terms or filters.</p>
                <button
                  onClick={() => {
                    setSearchTerm('')
                    setSelectedCategory('All')
                    setFilteredPosts(blogPosts)
                  }}
                  className="bg-purple-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-purple-700 transition-colors duration-200"
                >
                  Reset Filters
                </button>
              </div>
            )}
          </div>
        </section>

        {/* Newsletter Signup */}
        <section className="py-20 bg-gradient-to-br from-purple-600 to-blue-600">
          <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
            <motion.div
              initial={{ opacity: 0, y: 50 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8 }}
              className="text-white"
            >
              <h2 className="text-3xl md:text-4xl font-bold mb-6">
                Stay Updated with AI Video Trends
              </h2>
              <p className="text-xl text-purple-100 mb-8 max-w-2xl mx-auto">
                Get the latest insights, tutorials, and industry news delivered to your inbox weekly.
              </p>

              <div className="flex flex-col sm:flex-row gap-4 max-w-md mx-auto">
                <input
                  type="email"
                  placeholder="Enter your email"
                  className="flex-1 px-4 py-3 rounded-lg border-0 focus:outline-none focus:ring-2 focus:ring-white text-gray-900"
                />
                <button className="bg-white text-purple-600 px-6 py-3 rounded-lg font-semibold hover:bg-gray-100 transition-colors duration-200">
                  Subscribe
                </button>
              </div>

              <p className="text-purple-200 text-sm mt-4">
                No spam, unsubscribe at any time.
              </p>
            </motion.div>
          </div>
        </section>
      </main>
      <Footer />
    </>
  )
}
