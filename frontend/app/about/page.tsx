import Navigation from '../../components/Navigation'
import Footer from '../../components/Footer'
import AboutHero from './components/AboutHero'
import Mission from './components/Mission'
import Team from './components/Team'
import Timeline from './components/Timeline'
import Values from './components/Values'

export default function AboutPage() {
  return (
    <>
      <Navigation />
      <main>
        <AboutHero />
        <Mission />
        <Values />
        <Timeline />
        <Team />
      </main>
      <Footer />
    </>
  )
}
