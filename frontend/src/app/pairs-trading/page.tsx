'use client';

import { useState } from 'react';
import { apiService, StockAnalysisRequest } from '@/lib/api';
import { TrendingUp, BarChart2, ArrowRight, Loader2 } from 'lucide-react';
import Image from 'next/image';

interface StatisticsData {
  mean: number;
  std: number;
  skew: number;
  kurtosis: number;
}

interface ComparativeResults {
  stocks: {
    stock1: string;
    stock2: string;
  };
  statistics: {
    stock1: StatisticsData;
    stock2: StatisticsData;
  };
  comparative_analysis: string[];
}

interface VisualizationResults {
  charts: {
    comprehensive_analysis: {
      image: string;
    };
  };
}

interface RegressionModel {
  r_squared: number;
  adf_statistic: number;
  adf_p_value: number;
}

interface CointegrationResults {
  regression_analysis: {
    model1: RegressionModel;
    model2: RegressionModel;
  };
  interpretation: string;
}

interface RegressionPlot {
  title: string;
  image: string;
  r_squared: number;
}

interface CointegrationPlotResults {
  regression_plots: {
    plot1: RegressionPlot;
    plot2: RegressionPlot;
  };
}

interface AnalysisResults {
  comparative?: ComparativeResults;
  visualizations?: VisualizationResults;
  cointegration?: CointegrationResults;
  cointegrationPlots?: CointegrationPlotResults;
}

export default function PairsTrading() {
  const [formData, setFormData] = useState({
    ticker1: 'MSFT',
    ticker2: 'TSLA',
    startDate: '2022-01-01',
    endDate: '2024-12-31',
    period: '1d'
  });

  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState<AnalysisResults>({});
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const requestData: StockAnalysisRequest = {
        stocks1: [formData.ticker1],
        stocks2: [formData.ticker2],
        start_date: formData.startDate,
        end_date: formData.endDate,
        period: formData.period
      };

      // Run all analyses in parallel
      const [comparative, visualizations, cointegration, cointegrationPlots] = await Promise.all([
        apiService.comparativeAnalysis(requestData),
        apiService.generateVisualizations(requestData),
        apiService.cointegrationAnalysis(requestData),
        apiService.cointegrationPlots(requestData)
      ]);

      setResults({
        comparative: comparative.data,
        visualizations: visualizations.data,
        cointegration: cointegration.data,
        cointegrationPlots: cointegrationPlots.data
      });
    } catch (err: unknown) {
      const errorMessage = err instanceof Error && 'response' in err && err.response 
        ? (err.response as { data?: { detail?: string } }).data?.detail || 'An error occurred during analysis'
        : 'An error occurred during analysis';
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            <TrendingUp className="inline-block mr-3 h-10 w-10 text-purple-600" />
            Pairs Trading Analysis
          </h1>
          <p className="text-lg text-gray-600 max-w-3xl mx-auto">
            Analyze correlations between stocks, perform cointegration tests, and discover statistical arbitrage opportunities
          </p>
        </div>

        {/* Input Form */}
        <div className="bg-white rounded-xl shadow-lg p-6 mb-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">Analysis Parameters</h2>
          
          <form onSubmit={handleSubmit} className="space-y-6">
            <div className="grid md:grid-cols-2 lg:grid-cols-5 gap-4">
              
              {/* Ticker 1 */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Ticker 1
                </label>
                <input
                  type="text"
                  value={formData.ticker1}
                  onChange={(e) => setFormData({...formData, ticker1: e.target.value.toUpperCase()})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                  placeholder="MSFT"
                  required
                />
              </div>

              {/* Ticker 2 */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Ticker 2
                </label>
                <input
                  type="text"
                  value={formData.ticker2}
                  onChange={(e) => setFormData({...formData, ticker2: e.target.value.toUpperCase()})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                  placeholder="TSLA"
                  required
                />
              </div>

              {/* Start Date */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Start Date
                </label>
                <input
                  type="date"
                  value={formData.startDate}
                  onChange={(e) => setFormData({...formData, startDate: e.target.value})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                  required
                />
              </div>

              {/* End Date */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  End Date
                </label>
                <input
                  type="date"
                  value={formData.endDate}
                  onChange={(e) => setFormData({...formData, endDate: e.target.value})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                  required
                />
              </div>

              {/* Period/Timeframe */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Timeframe
                </label>
                <select
                  value={formData.period}
                  onChange={(e) => setFormData({...formData, period: e.target.value})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                >
                  <option value="1d">Daily (1D)</option>
                  <option value="1wk">Weekly (1W)</option>
                  <option value="1h">Hourly (1H)</option>
                </select>
              </div>
            </div>

            <div className="flex justify-center">
              <button
                type="submit"
                disabled={loading}
                className="bg-purple-600 text-white px-8 py-3 rounded-lg font-medium hover:bg-purple-700 focus:ring-2 focus:ring-purple-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed flex items-center space-x-2"
              >
                {loading ? (
                  <>
                    <Loader2 className="h-5 w-5 animate-spin" />
                    <span>Analyzing...</span>
                  </>
                ) : (
                  <>
                    <span>Run Analysis</span>
                    <ArrowRight className="h-5 w-5" />
                  </>
                )}
              </button>
            </div>
          </form>
        </div>

        {/* Error Display */}
        {error && (
          <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-8">
            <div className="text-red-800">
              <strong>Error:</strong> {error}
            </div>
          </div>
        )}

        {/* Results Section */}
        {results.comparative && (
          <div className="space-y-8">
            
            {/* Comparative Analysis */}
            <div className="bg-white rounded-xl shadow-lg p-6">
              <h3 className="text-2xl font-bold text-gray-900 mb-6">
                <BarChart2 className="inline-block mr-2 h-6 w-6 text-blue-600" />
                Comparative Analysis
              </h3>
              
              {/* Statistics Table */}
              <div className="grid md:grid-cols-2 gap-6 mb-6">
                <div>
                  <h4 className="text-lg font-semibold text-gray-800 mb-3">{formData.ticker1} Statistics</h4>
                  <div className="space-y-2 text-sm">
                    <div className="flex justify-between">
                      <span>Mean:</span>
                      <span className="font-mono">{results.comparative.statistics.stock1.mean?.toFixed(6)}</span>
                    </div>
                    <div className="flex justify-between">
                      <span>Std Dev:</span>
                      <span className="font-mono">{results.comparative.statistics.stock1.std?.toFixed(6)}</span>
                    </div>
                    <div className="flex justify-between">
                      <span>Skewness:</span>
                      <span className="font-mono">{results.comparative.statistics.stock1.skew?.toFixed(4)}</span>
                    </div>
                    <div className="flex justify-between">
                      <span>Kurtosis:</span>
                      <span className="font-mono">{results.comparative.statistics.stock1.kurtosis?.toFixed(4)}</span>
                    </div>
                  </div>
                </div>
                
                <div>
                  <h4 className="text-lg font-semibold text-gray-800 mb-3">{formData.ticker2} Statistics</h4>
                  <div className="space-y-2 text-sm">
                    <div className="flex justify-between">
                      <span>Mean:</span>
                      <span className="font-mono">{results.comparative.statistics.stock2.mean?.toFixed(6)}</span>
                    </div>
                    <div className="flex justify-between">
                      <span>Std Dev:</span>
                      <span className="font-mono">{results.comparative.statistics.stock2.std?.toFixed(6)}</span>
                    </div>
                    <div className="flex justify-between">
                      <span>Skewness:</span>
                      <span className="font-mono">{results.comparative.statistics.stock2.skew?.toFixed(4)}</span>
                    </div>
                    <div className="flex justify-between">
                      <span>Kurtosis:</span>
                      <span className="font-mono">{results.comparative.statistics.stock2.kurtosis?.toFixed(4)}</span>
                    </div>
                  </div>
                </div>
              </div>

              {/* Comparative Insights */}
              <div className="bg-blue-50 rounded-lg p-4">
                <h4 className="text-lg font-semibold text-blue-900 mb-3">Analysis Insights</h4>
                <div className="space-y-2">
                  {results.comparative.comparative_analysis.map((insight: string, index: number) => (
                    <p key={index} className="text-blue-800 text-sm">{insight}</p>
                  ))}
                </div>
              </div>
            </div>

            {/* Visualizations */}
            {results.visualizations && (
              <div className="bg-white rounded-xl shadow-lg p-6">
                <h3 className="text-2xl font-bold text-gray-900 mb-6">Price and Returns Analysis</h3>
                <div className="text-center">
                  <Image
                    src={`data:image/png;base64,${results.visualizations.charts.comprehensive_analysis.image}`}
                    alt="Comprehensive Analysis Charts"
                    width={800}
                    height={600}
                    className="mx-auto max-w-full h-auto rounded-lg shadow-md"
                  />
                </div>
              </div>
            )}

            {/* Cointegration Analysis */}
            {results.cointegration && (
              <div className="bg-white rounded-xl shadow-lg p-6">
                <h3 className="text-2xl font-bold text-gray-900 mb-6">Cointegration Analysis</h3>
                
                <div className="grid md:grid-cols-2 gap-6">
                  <div className="bg-green-50 rounded-lg p-4">
                    <h4 className="text-lg font-semibold text-green-900 mb-3">
                      {formData.ticker2} ~ {formData.ticker1}
                    </h4>
                    <div className="space-y-2 text-sm">
                      <div className="flex justify-between">
                        <span>R²:</span>
                        <span className="font-mono">{results.cointegration.regression_analysis.model1.r_squared?.toFixed(4)}</span>
                      </div>
                      <div className="flex justify-between">
                        <span>ADF Statistic:</span>
                        <span className="font-mono">{results.cointegration.regression_analysis.model1.adf_statistic?.toFixed(4)}</span>
                      </div>
                      <div className="flex justify-between">
                        <span>p-value:</span>
                        <span className="font-mono">{results.cointegration.regression_analysis.model1.adf_p_value?.toFixed(6)}</span>
                      </div>
                    </div>
                  </div>

                  <div className="bg-blue-50 rounded-lg p-4">
                    <h4 className="text-lg font-semibold text-blue-900 mb-3">
                      {formData.ticker1} ~ {formData.ticker2}
                    </h4>
                    <div className="space-y-2 text-sm">
                      <div className="flex justify-between">
                        <span>R²:</span>
                        <span className="font-mono">{results.cointegration.regression_analysis.model2.r_squared?.toFixed(4)}</span>
                      </div>
                      <div className="flex justify-between">
                        <span>ADF Statistic:</span>
                        <span className="font-mono">{results.cointegration.regression_analysis.model2.adf_statistic?.toFixed(4)}</span>
                      </div>
                      <div className="flex justify-between">
                        <span>p-value:</span>
                        <span className="font-mono">{results.cointegration.regression_analysis.model2.adf_p_value?.toFixed(6)}</span>
                      </div>
                    </div>
                  </div>
                </div>

                {/* Cointegration Conclusion */}
                <div className="mt-6 bg-yellow-50 rounded-lg p-4">
                  <h4 className="text-lg font-semibold text-yellow-900 mb-2">Cointegration Test Result</h4>
                  <p className="text-yellow-800">
                    {results.cointegration.interpretation}
                  </p>
                </div>
              </div>
            )}

            {/* Regression Plots */}
            {results.cointegrationPlots && (
              <div className="bg-white rounded-xl shadow-lg p-6">
                <h3 className="text-2xl font-bold text-gray-900 mb-6">Regression Analysis Plots</h3>
                
                <div className="grid lg:grid-cols-2 gap-6">
                  <div>
                    <h4 className="text-lg font-semibold text-gray-800 mb-3">
                      {results.cointegrationPlots.regression_plots.plot1.title}
                    </h4>
                    <Image
                      src={`data:image/png;base64,${results.cointegrationPlots.regression_plots.plot1.image}`}
                      alt="Regression Plot 1"
                      width={500}
                      height={400}
                      className="w-full rounded-lg shadow-md"
                    />
                    <p className="text-sm text-gray-600 mt-2">
                      R² = {results.cointegrationPlots.regression_plots.plot1.r_squared?.toFixed(4)}
                    </p>
                  </div>

                  <div>
                    <h4 className="text-lg font-semibold text-gray-800 mb-3">
                      {results.cointegrationPlots.regression_plots.plot2.title}
                    </h4>
                    <Image
                      src={`data:image/png;base64,${results.cointegrationPlots.regression_plots.plot2.image}`}
                      alt="Regression Plot 2"
                      width={500}
                      height={400}
                      className="w-full rounded-lg shadow-md"
                    />
                    <p className="text-sm text-gray-600 mt-2">
                      R² = {results.cointegrationPlots.regression_plots.plot2.r_squared?.toFixed(4)}
                    </p>
                  </div>
                </div>
              </div>
            )}

          </div>
        )}

      </div>
    </div>
  );
} 