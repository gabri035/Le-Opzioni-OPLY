# OPLY Frontend

Modern Next.js frontend for the OPLY financial analysis platform.

## Features

- **Homepage**: Central navigation hub with feature overview
- **Pairs Trading**: Stock correlation analysis and cointegration testing
- **Option Chain**: Live options data viewer
- **Strategy Builder**: Multi-leg options strategy simulator with Greeks analysis
- **About**: Project information and thesis download

## Tech Stack

- **Framework**: Next.js 15 with App Router
- **Language**: TypeScript
- **Styling**: Tailwind CSS 4
- **Charts**: Recharts
- **Icons**: Lucide React
- **HTTP Client**: Axios

## Getting Started

### Prerequisites

- Node.js 18+ 
- npm or yarn

### Installation

1. Clone the repository and navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Set up environment variables:
```bash
# Create .env.local file
echo "NEXT_PUBLIC_API_URL=https://leopzioni.onrender.com" > .env.local
```

4. Run the development server:
```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) to view the application.

## Environment Variables

Create a `.env.local` file in the frontend directory:

```env
# Replace with your actual Render deployment URL
NEXT_PUBLIC_API_URL=https://leopzioni.onrender.com

# For local development:
# NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Deployment to Vercel

### Method 1: Vercel CLI

1. Install Vercel CLI:
```bash
npm i -g vercel
```

2. Deploy:
```bash
vercel
```

3. Set environment variable in Vercel dashboard:
   - Go to your project in Vercel dashboard
   - Navigate to Settings > Environment Variables
   - Add: `NEXT_PUBLIC_API_URL` = `https://leopzioni.onrender.com`

### Method 2: GitHub Integration

1. Push your code to GitHub
2. Import project in Vercel dashboard
3. Connect your GitHub repository
4. Set environment variables in project settings
5. Deploy automatically on every push

### Environment Variables in Vercel

In your Vercel project settings, add:

| Name | Value | Environment |
|------|-------|-------------|
| `NEXT_PUBLIC_API_URL` | `https://leopzioni.onrender.com` | Production, Preview, Development |

## API Integration

The frontend communicates with the FastAPI backend through the `/lib/api.ts` service layer:

- Stock analysis endpoints
- Options data and strategy simulation
- Company information retrieval
- Real-time chart generation

## Project Structure

```
frontend/
├── src/
│   ├── app/                    # Next.js App Router pages
│   │   ├── about/             # About page
│   │   ├── option-chain/      # Option chain viewer
│   │   ├── pairs-trading/     # Pairs trading analysis
│   │   ├── strategy-builder/  # Options strategy builder
│   │   ├── layout.tsx         # Root layout with navigation
│   │   └── page.tsx           # Homepage
│   └── lib/
│       └── api.ts            # API service layer
├── public/                   # Static assets
├── vercel.json              # Vercel configuration
└── README.md               # This file
```

## Key Pages

### Homepage (`/`)
- Landing page with feature cards
- Navigation to main sections
- Platform overview

### Pairs Trading (`/pairs-trading`)
- Input form for tickers and date ranges
- Statistical analysis results
- Cointegration testing with ADF tests
- Interactive charts and visualizations

### Option Chain (`/option-chain`)
- Options data viewer
- Expiry date selection
- Calls and puts tables with pricing

### Strategy Builder (`/strategy-builder`)
- Multi-leg options strategy creator
- Payoff diagram visualization
- Greeks analysis (Delta, Gamma, Vega, Theta, Rho)
- Real-time strategy simulation

### About (`/about`)
- Project information
- Technology stack details
- Thesis download section

## Performance Optimizations

- Next.js App Router for optimized routing
- TypeScript for type safety
- Tailwind CSS for optimized styling
- Recharts for performant data visualization
- Axios with request/response interceptors

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## Support

For questions or issues:
- Email: info@oply.finance
- GitHub Issues: Create an issue in the repository
