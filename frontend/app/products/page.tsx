import Navigation from '../../components/Navigation'
import Footer from '../../components/Footer'
import ProductsHero from './components/ProductsHero'
import ProductSuite from './components/ProductSuite'
import ComparisonTable from './components/ComparisonTable'
import Integration from './components/Integration'
import ProductCTA from './components/ProductCTA'

export default function ProductsPage() {
  return (
    <>
      <Navigation />
      <main>
        <ProductsHero />
        <ProductSuite />
        <ComparisonTable />
        <Integration />
        <ProductCTA />
      </main>
      <Footer />
    </>
  )
}
