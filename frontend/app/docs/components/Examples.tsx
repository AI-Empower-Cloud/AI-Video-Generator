'use client'

import { motion } from 'framer-motion'
import { useInView } from 'framer-motion'
import { useRef } from 'react'
import { Play, Copy, ExternalLink, Star, Clock, User } from 'lucide-react'

const examples = [
  {
    title: 'Text to Video',
    category: 'Basic',
    difficulty: 'Beginner',
    time: '5 min',
    description: 'Generate a video from a simple text prompt',
    language: 'JavaScript',
    code: `const video = await client.generate({
  prompt: "A serene lake at sunset with mountains in the background",
  duration: 15,
  style: "photorealistic"
});

console.log("Video URL:", video.url);`,
    preview: '/api/placeholder/400/225',
    tags: ['text-to-video', 'basic', 'beginner']
  },
  {
    title: 'Custom Style Transfer',
    category: 'Advanced',
    difficulty: 'Intermediate',
    time: '10 min',
    description: 'Apply custom artistic styles to generated videos',
    language: 'Python',
    code: `from aivideo import VideoGenerator

generator = VideoGenerator(api_key="your-key")

video = generator.create_with_style(
    prompt="A bustling city street",
    style_image="path/to/style.jpg",
    duration=30,
    style_strength=0.8
)

print(f"Generated: {video.download_url}")`,
    preview: '/api/placeholder/400/225',
    tags: ['style-transfer', 'advanced', 'python']
  },
  {
    title: 'Batch Video Generation',
    category: 'Production',
    difficulty: 'Advanced',
    time: '15 min',
    description: 'Generate multiple videos efficiently using batch processing',
    language: 'Node.js',
    code: `const prompts = [
  "Product showcase - smartphone",
  "Product showcase - laptop",
  "Product showcase - headphones"
];

const videos = await Promise.all(
  prompts.map(prompt => 
    client.generate({
      prompt,
      template: "product_showcase",
      duration: 20
    })
  )
);

videos.forEach((video, i) => {
  console.log(\`Video \${i + 1}: \${video.url}\`);
});`,
    preview: '/api/placeholder/400/225',
    tags: ['batch', 'production', 'nodejs']
  },
  {
    title: 'Real-time Generation',
    category: 'Advanced',
    difficulty: 'Expert',
    time: '20 min',
    description: 'Stream video generation progress with WebSockets',
    language: 'JavaScript',
    code: `const ws = new WebSocket('wss://api.aivideogen.com/stream');

ws.onopen = () => {
  ws.send(JSON.stringify({
    action: 'generate',
    prompt: "Dynamic ocean waves",
    realtime: true
  }));
};

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  if (data.type === 'progress') {
    console.log(\`Progress: \${data.percentage}%\`);
  } else if (data.type === 'complete') {
    console.log('Video ready:', data.url);
  }
};`,
    preview: '/api/placeholder/400/225',
    tags: ['realtime', 'websockets', 'advanced']
  },
  {
    title: 'Voice-over Integration',
    category: 'Audio',
    difficulty: 'Intermediate',
    time: '12 min',
    description: 'Add AI-generated voice-over to your videos',
    language: 'Python',
    code: `video = generator.create({
    prompt: "Educational content about space",
    duration: 60,
    voiceover: {
        text: "Welcome to our journey through space...",
        voice: "professional-female",
        speed: 1.0,
        background_music: True
    }
})

# Download with embedded audio
video.download("space_education.mp4")`,
    preview: '/api/placeholder/400/225',
    tags: ['voiceover', 'audio', 'education']
  },
  {
    title: 'Custom Workflows',
    category: 'Enterprise',
    difficulty: 'Expert',
    time: '25 min',
    description: 'Build complex video workflows with multiple steps',
    language: 'TypeScript',
    code: `interface VideoWorkflow {
  steps: WorkflowStep[];
  output: OutputConfig;
}

const workflow: VideoWorkflow = {
  steps: [
    {
      type: 'generate',
      prompt: 'Corporate presentation background'
    },
    {
      type: 'overlay',
      elements: ['logo.png', 'text_overlay.json']
    },
    {
      type: 'transitions',
      effects: ['fade_in', 'slide_left']
    }
  ],
  output: {
    format: 'mp4',
    quality: 'ultra',
    watermark: false
  }
};

const result = await client.executeWorkflow(workflow);`,
    preview: '/api/placeholder/400/225',
    tags: ['workflows', 'enterprise', 'typescript']
  }
]

const difficultyColors: Record<string, string> = {
  'Beginner': 'bg-green-100 text-green-800',
  'Intermediate': 'bg-yellow-100 text-yellow-800',
  'Advanced': 'bg-orange-100 text-orange-800',
  'Expert': 'bg-red-100 text-red-800'
}

export default function Examples() {
  const ref = useRef(null)
  const isInView = useInView(ref, { once: true, amount: 0.2 })

  const copyToClipboard = (code: string) => {
    navigator.clipboard.writeText(code)
  }

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
            Code Examples
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Ready-to-use code examples to get you started quickly. Copy, paste, and customize for your needs.
          </p>
        </motion.div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {examples.map((example, index) => (
            <motion.div
              key={example.title}
              initial={{ opacity: 0, y: 50 }}
              animate={isInView ? { opacity: 1, y: 0 } : { opacity: 0, y: 50 }}
              transition={{ duration: 0.6, delay: index * 0.1 }}
              className="bg-gradient-to-br from-gray-50 to-blue-50 rounded-2xl overflow-hidden shadow-lg hover:shadow-2xl transition-all duration-300 border border-gray-200"
            >
              {/* Header */}
              <div className="p-6 bg-white border-b border-gray-200">
                <div className="flex items-start justify-between mb-4">
                  <div>
                    <h3 className="text-xl font-bold text-gray-900 mb-2">{example.title}</h3>
                    <p className="text-gray-600 text-sm leading-relaxed">{example.description}</p>
                  </div>
                  <div className="flex items-center space-x-2">
                    <Play className="w-5 h-5 text-purple-600 cursor-pointer hover:text-purple-700" />
                    <ExternalLink className="w-5 h-5 text-gray-400 cursor-pointer hover:text-gray-600" />
                  </div>
                </div>

                <div className="flex items-center space-x-4 text-sm">
                  <span className={`px-3 py-1 rounded-full font-semibold ${difficultyColors[example.difficulty]}`}>
                    {example.difficulty}
                  </span>
                  <div className="flex items-center text-gray-500">
                    <Clock className="w-4 h-4 mr-1" />
                    {example.time}
                  </div>
                  <div className="flex items-center text-gray-500">
                    <User className="w-4 h-4 mr-1" />
                    {example.category}
                  </div>
                </div>
              </div>

              {/* Preview */}
              <div className="relative h-32 bg-gradient-to-br from-purple-400 to-blue-500 flex items-center justify-center">
                <Play className="w-12 h-12 text-white opacity-80" />
                <div className="absolute top-4 left-4 bg-black/50 text-white px-2 py-1 rounded text-xs">
                  {example.language}
                </div>
              </div>

              {/* Code */}
              <div className="relative">
                <div className="bg-gray-900 p-6">
                  <div className="flex items-center justify-between mb-4">
                    <div className="flex space-x-2">
                      <div className="w-3 h-3 bg-red-500 rounded-full" />
                      <div className="w-3 h-3 bg-yellow-500 rounded-full" />
                      <div className="w-3 h-3 bg-green-500 rounded-full" />
                    </div>
                    <button
                      onClick={() => copyToClipboard(example.code)}
                      className="flex items-center space-x-1 text-gray-400 hover:text-white transition-colors duration-200"
                    >
                      <Copy className="w-4 h-4" />
                      <span className="text-sm">Copy</span>
                    </button>
                  </div>
                  
                  <pre className="text-green-400 text-sm leading-relaxed overflow-x-auto">
                    <code>{example.code}</code>
                  </pre>
                </div>
              </div>

              {/* Tags */}
              <div className="p-6 pt-4">
                <div className="flex flex-wrap gap-2">
                  {example.tags.map((tag) => (
                    <span
                      key={tag}
                      className="px-3 py-1 bg-purple-100 text-purple-700 rounded-full text-xs font-medium"
                    >
                      #{tag}
                    </span>
                  ))}
                </div>
                
                <button className="w-full mt-4 bg-gradient-to-r from-purple-600 to-blue-600 text-white py-3 px-6 rounded-lg font-semibold hover:from-purple-700 hover:to-blue-700 transition-all duration-200">
                  Try This Example
                </button>
              </div>
            </motion.div>
          ))}
        </div>

        <motion.div
          initial={{ opacity: 0, y: 50 }}
          animate={isInView ? { opacity: 1, y: 0 } : { opacity: 0, y: 50 }}
          transition={{ duration: 0.8, delay: 0.6 }}
          className="mt-16 text-center"
        >
          <div className="bg-gradient-to-br from-purple-600 to-blue-600 rounded-2xl p-8 text-white">
            <Star className="w-12 h-12 text-yellow-400 mx-auto mb-4" />
            <h3 className="text-3xl font-bold mb-4">
              Want More Examples?
            </h3>
            <p className="text-xl text-purple-100 mb-8 max-w-2xl mx-auto">
              Explore our complete example library with step-by-step tutorials, video guides, and community contributions.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <button className="bg-white text-purple-600 px-8 py-3 rounded-lg font-semibold hover:bg-gray-100 transition-colors duration-200">
                Browse All Examples
              </button>
              <button className="border-2 border-white text-white px-8 py-3 rounded-lg font-semibold hover:bg-white hover:text-purple-600 transition-colors duration-200">
                Submit Your Example
              </button>
            </div>
          </div>
        </motion.div>
      </div>
    </section>
  )
}
