import Navigation from '../../components/Navigation'
import Footer from '../../components/Footer'
import DocsHero from './components/DocsHero'
import QuickStart from './components/QuickStart'
import APIReference from './components/APIReference'
import Examples from './components/Examples'
import SearchDocs from './components/SearchDocs'

export default function DocsPage() {
  return (
    <>
      <Navigation />
      <main>
        <DocsHero />
        <SearchDocs />
        <QuickStart />
        <APIReference />
        <Examples />
      </main>
      <Footer />
    </>
  )
}
