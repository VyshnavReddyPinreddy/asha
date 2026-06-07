import { ArrowRight } from "lucide-react";

function Hero() {
  return (
    <section className="py-28 px-6">

      <div className="max-w-7xl mx-auto text-center">

        <div className="inline-block px-4 py-2 bg-sky-100 text-sky-600 rounded-full mb-8">
          AI Powered Healthcare Assistant
        </div>

        <h1 className="text-5xl md:text-7xl font-bold text-gray-900 leading-tight">

          Empowering
          <span className="text-sky-500"> ASHA Workers </span>
          with Intelligent Healthcare Insights

        </h1>

        <p className="mt-8 max-w-3xl mx-auto text-lg text-gray-600">
          Transform voice and natural language queries into actionable
          healthcare data. Built for ASHA workers and ANMs. 
        </p>

        <div className="flex flex-col md:flex-row justify-center gap-4 mt-10">

          <button className="bg-sky-500 hover:bg-sky-600 text-white px-8 py-4 rounded-xl flex items-center gap-2 justify-center">
            Get Started
            <ArrowRight size={18} />
          </button>

          <button className="border border-sky-300 text-sky-600 px-8 py-4 rounded-xl">
            Learn More
          </button>

        </div>

      </div>

    </section>
  );
}

export default Hero;