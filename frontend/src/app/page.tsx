import Link from 'next/link';
import { TrendingUp, BarChart3, Calculator } from 'lucide-react';

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 to-blue-50">
      {/* Hero Section */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-16 pb-20">
        <div className="text-center">
          <h1 className="text-4xl md:text-6xl font-bold text-gray-900 mb-6">
            Welcome to <span className="text-purple-600">OPLY</span>
          </h1>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto mb-12">
            Advanced financial analysis platform for options strategies and pairs trading. 
            Analyze correlations, build strategies, and make data-driven investment decisions.
          </p>
        </div>

        {/* Main Navigation Cards */}
        <div className="grid md:grid-cols-1 lg:grid-cols-3 gap-8 max-w-6xl mx-auto">
          
          {/* Pairs Trading Card */}
          <Link href="/pairs-trading" className="group">
            <div className="bg-white rounded-2xl p-8 shadow-lg hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-2 border border-gray-100">
              <div className="text-center">
                <div className="inline-flex items-center justify-center w-16 h-16 bg-purple-100 rounded-xl mb-6 group-hover:bg-purple-200 transition-colors">
                  <TrendingUp className="h-8 w-8 text-purple-600" />
                </div>
                <h3 className="text-2xl font-bold text-gray-900 mb-4">Pairs Trading</h3>
                <p className="text-gray-600 mb-6">
                  Analyze correlations between stocks, perform cointegration tests, 
                  and discover statistical arbitrage opportunities with comprehensive visualizations.
                </p>
                <div className="text-sm text-purple-600 font-medium">
                  Input: Ticker 1 & 2, Date Range, Timeframe →
                </div>
              </div>
            </div>
          </Link>

          {/* Option Chain Card */}
          <Link href="/option-chain" className="group">
            <div className="bg-white rounded-2xl p-8 shadow-lg hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-2 border border-gray-100">
              <div className="text-center">
                <div className="inline-flex items-center justify-center w-16 h-16 bg-green-100 rounded-xl mb-6 group-hover:bg-green-200 transition-colors">
                  <BarChart3 className="h-8 w-8 text-green-600" />
                </div>
                <h3 className="text-2xl font-bold text-gray-900 mb-4">Option Chain</h3>
                <p className="text-gray-600 mb-6">
                  View live options data, analyze strike prices, and examine option volumes 
                  and open interest for comprehensive market analysis.
                </p>
                <div className="text-sm text-green-600 font-medium">
                  Input: Ticker, Expiry Date →
                </div>
              </div>
            </div>
          </Link>

          {/* Option Strategy Builder Card */}
          <Link href="/strategy-builder" className="group">
            <div className="bg-white rounded-2xl p-8 shadow-lg hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-2 border border-gray-100">
              <div className="text-center">
                <div className="inline-flex items-center justify-center w-16 h-16 bg-blue-100 rounded-xl mb-6 group-hover:bg-blue-200 transition-colors">
                  <Calculator className="h-8 w-8 text-blue-600" />
                </div>
                <h3 className="text-2xl font-bold text-gray-900 mb-4">Strategy Builder</h3>
                <p className="text-gray-600 mb-6">
                  Build complex options strategies, visualize payoff diagrams, 
                  and analyze Greeks for risk management and profit optimization.
                </p>
                <div className="text-sm text-blue-600 font-medium">
                  Input: Ticker, Options Legs, Expiry →
                </div>
              </div>
            </div>
          </Link>

        </div>

        {/* Features Section */}
        <div className="mt-20 text-center">
          <h2 className="text-3xl font-bold text-gray-900 mb-12">Platform Features</h2>
          <div className="grid md:grid-cols-3 gap-8">
            <div className="bg-white/60 backdrop-blur rounded-xl p-6 border border-white/20">
              <h3 className="text-lg font-semibold text-gray-900 mb-3">Statistical Analysis</h3>
              <p className="text-gray-600">Advanced cointegration tests, correlation analysis, and statistical modeling</p>
            </div>
            <div className="bg-white/60 backdrop-blur rounded-xl p-6 border border-white/20">
              <h3 className="text-lg font-semibold text-gray-900 mb-3">Real-time Data</h3>
              <p className="text-gray-600">Live market data integration with comprehensive options chains</p>
            </div>
            <div className="bg-white/60 backdrop-blur rounded-xl p-6 border border-white/20">
              <h3 className="text-lg font-semibold text-gray-900 mb-3">Interactive Charts</h3>
              <p className="text-gray-600">Dynamic visualizations for payoff diagrams and risk analysis</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
