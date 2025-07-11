import Image from 'next/image';
import Link from 'next/link';

export default function AboutPage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 to-blue-50 flex flex-col items-center py-16 px-4">
      <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-8 text-center">Who we are</h1>
      <div className="flex flex-col md:flex-row items-center max-w-4xl w-full bg-white/80 rounded-2xl shadow-lg p-8 md:p-12 gap-8">
        <div className="flex-shrink-0">
          <Image
            src="/about-pic.png"
            alt="Gabriele Gatto"
            width={280}
            height={340}
            className="rounded-xl border border-gray-200 shadow-md object-cover"
            priority
          />
        </div>
        <div className="flex-1 text-gray-800 text-lg space-y-6">
          <p>
            A dynamic team that blends quantitative expertise with cutting-edge technology.
          </p>
          <p>
            Our specialists excel in financial-market analysis and algorithmic trading. Our strength lies in harnessing advanced tools to turn complex data into actionable, innovative solutions. We use Python for sophisticated processing, collaborate on GitHub for open-source projects, and leverage MQL5 to automate trading strategies.
          </p>
          <p>
            <span className="font-semibold">Gabriele Gatto</span> is the creative engine behind our innovative project. With a solid background in quantitative finance and a deep passion for programming, he has seamlessly fused advanced analytics with cutting-edge technology.
          </p>
          <p>
            By harnessing Python, he has developed sophisticated algorithms for financial-market analysis, while his activity on GitHub reflects an unwavering commitment to collaborative excellence and open-source development. His expertise with MQL5 showcases his ability to translate quantitative strategies into automated trading solutions. Expanding his web-development skills led to the creation of Callz, our flagship quantitative-analysis tool.
          </p>
          <p>
            Investment specialist, holder of a Master’s degree in Economics and Finance from Università Cattolica di Milano, he now works for an Italian private-finance firm.
          </p>
          <blockquote className="border-l-4 border-purple-400 pl-4 italic text-gray-700">
            His mission is simple: “to make the complexity of financial markets accessible and transparent.”
          </blockquote>
          <p>
            His Italian-language master’s thesis—focused on pairs trading and a statistical study for options trading implemented in Python—is available for download, completely open source, on his GitHub repository at the following link: <br />
            <Link href="https://github.com/gabri035/LeOpzioni" target="_blank" className="text-purple-700 underline font-medium">LeOpzioni</Link>
          </p>
        </div>
      </div>
    </div>
  );
} 