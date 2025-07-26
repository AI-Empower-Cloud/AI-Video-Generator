import Navigation from '../components/Navigation'
import Footer from '../components/Footer'
import Hero from './components/Hero'
import Features from './components/Features'
import UseCases from './components/UseCases'
import Stats from './components/Stats'
import Testimonials from './components/Testimonials'
import CTA from './components/CTA'

export default function HomePage() {
  return (
    <>
      <Navigation />
      <main>
        <Hero />
        <Stats />
        <Features />
        <UseCases />
        <Testimonials />
        <CTA />
      </main>
      <Footer />
    </>
  )
}
