import Navigation from '../../components/Navigation'
import Footer from '../../components/Footer'
import UseCasesHero from './components/UseCasesHero'
import IndustryUseCases from './components/IndustryUseCases'
import CreatorStories from './components/CreatorStories'
import UseCaseExamples from './components/UseCaseExamples'
import GetStartedCTA from './components/GetStartedCTA'

export default function UseCasesPage() {
  return (
    <>
      <Navigation />
      <main>
        <UseCasesHero />
        <IndustryUseCases />
        <UseCaseExamples />
        <CreatorStories />
        <GetStartedCTA />
      </main>
      <Footer />
    </>
  )
}
