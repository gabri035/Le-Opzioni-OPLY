'use client';

import { useState } from 'react';
import { apiService, OptionChainRequest } from '@/lib/api';
import { BarChart3, Search, Loader2 } from 'lucide-react';

interface OptionInfo {
  strike: number;
  lastPrice: number;
  bid: number;
  ask: number;
  volume: number;
  openInterest: number;
  impliedVolatility: number;
}

interface OptionData {
  ticker: string;
  available_expiries: string[];
  expiry?: string;
  calls?: OptionInfo[];
  puts?: OptionInfo[];
}

interface ApiError {
  response?: {
    data?: {
      detail?: string;
    };
  };
}

export default function OptionChain() {
  const [formData, setFormData] = useState({
    ticker: 'AAPL',
    expiry: ''
  });

  const [loading, setLoading] = useState(false);
  const [loadingMessage, setLoadingMessage] = useState('');
  const [optionData, setOptionData] = useState<OptionData | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleFetchExpiries = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setLoadingMessage('Fetching available expiry dates...');
    setError(null);
    setOptionData(null);
    setFormData(prev => ({ ...prev, expiry: '' }));

    try {
      const requestData: OptionChainRequest = { ticker: formData.ticker };
      const response = await apiService.getOptionChain(requestData);
      setOptionData(response.data);
    } catch (err: unknown) {
      const apiError = err as ApiError;
      const errorMessage =
        apiError.response?.data?.detail ||
        'An error occurred while fetching expiry dates.';
      setError(errorMessage);
    } finally {
      setLoading(false);
      setLoadingMessage('');
    }
  };

  const handleExpiryChange = async (newExpiry: string) => {
    setFormData(prev => ({ ...prev, expiry: newExpiry }));

    if (!newExpiry) {
      if (optionData) {
        const { available_expiries, ticker } = optionData;
        setOptionData({ available_expiries, ticker });
      }
      return;
    }

    setLoading(true);
    setLoadingMessage(`Fetching option chain for ${newExpiry}...`);
    setError(null);
    
    try {
      const requestData: OptionChainRequest = { ticker: formData.ticker, expiry: newExpiry };
      const response = await apiService.getOptionChain(requestData);
      setOptionData(response.data);
    } catch (err: unknown) {
      const apiError = err as ApiError;
      const errorMessage =
        apiError.response?.data?.detail ||
        'An error occurred while fetching the option chain.';
      setError(errorMessage);
    } finally {
      setLoading(false);
      setLoadingMessage('');
    }
  };

  const formatNumber = (value: number | null | undefined) => {
    if (value === null || value === undefined) return 'N/A';
    return value.toFixed(2);
  };

  const formatVolume = (value: number | null | undefined) => {
    if (value === null || value === undefined) return 'N/A';
    return value.toLocaleString();
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            <BarChart3 className="inline-block mr-3 h-10 w-10 text-green-600" />
            Option Chain
          </h1>
          <p className="text-lg text-gray-600 max-w-3xl mx-auto">
            View live options data, analyze strike prices, and examine option volumes and open interest
          </p>
        </div>

        {/* Input Form */}
        <div className="bg-white rounded-xl shadow-lg p-6 mb-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">Option Chain Parameters</h2>
          
          <form onSubmit={handleFetchExpiries} className="space-y-6">
            <div className="grid md:grid-cols-3 gap-4">
              
              {/* Ticker */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Ticker Symbol
                </label>
                <input
                  type="text"
                  value={formData.ticker}
                  onChange={(e) => setFormData({...formData, ticker: e.target.value.toUpperCase()})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                  placeholder="AAPL"
                  required
                />
              </div>

              {/* Expiry Date */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Expiry Date
                </label>
                <select
                  value={formData.expiry}
                  onChange={(e) => handleExpiryChange(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                  disabled={!optionData?.available_expiries?.length}
                >
                  <option value="">Select expiry date...</option>
                  {optionData?.available_expiries?.map((date) => (
                    <option key={date} value={date}>{date}</option>
                  ))}
                </select>
              </div>

              {/* Submit Button */}
              <div className="flex items-end">
                <button
                  type="submit"
                  disabled={loading}
                  className="w-full bg-green-600 text-white px-4 py-2 rounded-lg font-medium hover:bg-green-700 focus:ring-2 focus:ring-green-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center space-x-2"
                >
                  {loading ? (
                    <>
                      <Loader2 className="h-5 w-5 animate-spin" />
                      <span>{loadingMessage || 'Loading...'}</span>
                    </>
                  ) : (
                    <>
                      <Search className="h-5 w-5" />
                      <span>Get Options</span>
                    </>
                  )}
                </button>
              </div>
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

        {/* Option Chain Data */}
        {optionData && optionData.calls && optionData.puts && (
          <div className="space-y-8">
            
            {/* Calls */}
            <div className="bg-white rounded-xl shadow-lg p-6">
              <h3 className="text-2xl font-bold text-gray-900 mb-6">
                Call Options - {optionData.ticker} ({optionData.expiry})
              </h3>
              
              <div className="overflow-x-auto">
                <table className="min-w-full divide-y divide-gray-200">
                  <thead className="bg-green-50">
                    <tr>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Strike</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Last Price</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Bid</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Ask</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Volume</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Open Interest</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Implied Vol</th>
                    </tr>
                  </thead>
                  <tbody className="bg-white divide-y divide-gray-200">
                    {optionData.calls?.slice(0, 20).map((option, index) => (
                      <tr key={index} className="hover:bg-gray-50">
                        <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                          ${formatNumber(option.strike)}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                          ${formatNumber(option.lastPrice)}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                          ${formatNumber(option.bid)}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                          ${formatNumber(option.ask)}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                          {formatVolume(option.volume)}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                          {formatVolume(option.openInterest)}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                          {option.impliedVolatility ? (option.impliedVolatility * 100).toFixed(1) + '%' : 'N/A'}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>

            {/* Puts */}
            <div className="bg-white rounded-xl shadow-lg p-6">
              <h3 className="text-2xl font-bold text-gray-900 mb-6">
                Put Options - {optionData.ticker} ({optionData.expiry})
              </h3>
              
              <div className="overflow-x-auto">
                <table className="min-w-full divide-y divide-gray-200">
                  <thead className="bg-red-50">
                    <tr>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Strike</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Last Price</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Bid</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Ask</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Volume</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Open Interest</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Implied Vol</th>
                    </tr>
                  </thead>
                  <tbody className="bg-white divide-y divide-gray-200">
                    {optionData.puts?.slice(0, 20).map((option, index) => (
                      <tr key={index} className="hover:bg-gray-50">
                        <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                          ${formatNumber(option.strike)}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                          ${formatNumber(option.lastPrice)}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                          ${formatNumber(option.bid)}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                          ${formatNumber(option.ask)}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                          {formatVolume(option.volume)}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                          {formatVolume(option.openInterest)}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                          {option.impliedVolatility ? (option.impliedVolatility * 100).toFixed(1) + '%' : 'N/A'}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>

          </div>
        )}

      </div>
    </div>
  );
} 