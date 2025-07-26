# AI Video Generator Frontend

A stunning, professional-grade frontend for the AI Video Generator platform built with Next.js, Tailwind CSS, and Framer Motion.

## ✨ Features

- **Modern Design**: Beautiful, animated interface inspired by RunwayML
- **Responsive Layout**: Perfect on all devices and screen sizes
- **Authentication**: Google and GitHub OAuth integration
- **Dashboard**: User profile and project management
- **Animations**: Smooth animations powered by Framer Motion
- **Dark Theme**: Professional dark theme with glassmorphism effects
- **TypeScript**: Full type safety and better development experience

## 🚀 Getting Started

### Prerequisites

- Node.js 18.0 or later
- npm or yarn

### Installation

1. **Install dependencies:**
   ```bash
   cd frontend
   npm install
   ```

2. **Set up environment variables:**
   ```bash
   cp .env.local.example .env.local
   ```
   
   Update the `.env.local` file with your OAuth credentials:
   - Get Google OAuth credentials from [Google Cloud Console](https://console.cloud.google.com/)
   - Get GitHub OAuth credentials from [GitHub Developer Settings](https://github.com/settings/developers)

3. **Run the development server:**
   ```bash
   npm run dev
   ```

4. **Open your browser:**
   Navigate to [http://localhost:3000](http://localhost:3000)

## 📁 Project Structure

```
frontend/
├── app/                    # Next.js 13+ App Router
│   ├── components/         # Page-specific components
│   ├── about/             # About page
│   ├── pricing/           # Pricing page
│   ├── dashboard/         # User dashboard
│   ├── api/               # API routes
│   ├── globals.css        # Global styles
│   ├── layout.tsx         # Root layout
│   ├── page.tsx           # Home page
│   └── providers.tsx      # App providers
├── components/            # Shared components
│   ├── Navigation.tsx     # Main navigation
│   └── Footer.tsx         # Footer component
├── public/               # Static assets
├── styles/               # Additional styles
└── package.json          # Dependencies
```

## 🎨 Pages

### ✅ Completed Pages

- **Home**: Hero section with animated features showcase
- **About**: Company mission, team, and values
- **Pricing**: Subscription plans with FAQ
- **Dashboard**: User profile and project management
- **Authentication**: Google and GitHub OAuth

### 🚧 Additional Pages (Ready to implement)

- **Use Cases**: Detailed use case examples
- **Docs**: API documentation and guides
- **Products**: Feature showcase and demos
- **Blog**: Content marketing and updates
- **Contact**: Support and contact forms

## 🛠️ Tech Stack

- **Framework**: Next.js 14 with App Router
- **Styling**: Tailwind CSS with custom design system
- **Animations**: Framer Motion for smooth interactions
- **Authentication**: NextAuth.js with OAuth providers
- **Icons**: Lucide React for consistent iconography
- **TypeScript**: Full type safety
- **Theme**: Custom dark theme with glassmorphism

## 🎯 Key Features

### Navigation
- Responsive navigation with mobile menu
- User authentication state management
- Smooth scroll animations
- Glass effect on scroll

### Hero Section
- Animated background with floating elements
- Call-to-action buttons with hover effects
- Video modal for demos
- Statistics showcase

### Dashboard
- Project management interface
- Analytics and stats
- Quick actions panel
- Grid and list view modes

### Pricing
- Interactive billing toggle (monthly/annual)
- Feature comparison
- FAQ section with animations
- Enterprise contact forms

## 🚀 Deployment

### Vercel (Recommended)

1. **Push to GitHub:**
   ```bash
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Deploy to Vercel:**
   - Connect your GitHub repository
   - Add environment variables
   - Deploy automatically

### Other Platforms

The app can be deployed to any platform that supports Next.js:
- Netlify
- AWS Amplify
- Railway
- Render

## 🔧 Development

### Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run lint` - Run ESLint

### Environment Variables

Required variables for full functionality:

```env
NEXTAUTH_URL=http://localhost:3000
NEXTAUTH_SECRET=your-secret-key
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
GITHUB_ID=your-github-client-id
GITHUB_SECRET=your-github-client-secret
```

## 🎨 Customization

### Colors

The app uses a custom color palette defined in `tailwind.config.js`:

- **Primary**: Blue gradient (#0ea5e9 to #0284c7)
- **Dark**: Custom gray scale for dark theme
- **Gradients**: Multiple gradient combinations

### Animations

Framer Motion animations are used throughout:

- Page transitions
- Hover effects
- Scroll animations
- Loading states

### Components

All components are modular and reusable:

- Consistent design patterns
- TypeScript interfaces
- Responsive by default
- Accessible markup

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:

- Create an issue on GitHub
- Contact our support team
- Check the documentation

---

Built with ❤️ by the AI Video Generator team
