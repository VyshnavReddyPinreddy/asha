import Navbar from "../components/Navbar";
import Hero from "../components/Hero";
import Features from "../components/Features";
import Mission from "../components/Mission";
import Footer from "../components/Footer";

function Landing() {
  return (
    <div className="bg-white min-h-screen">
      <Navbar />
      <Hero />
      <Features />
      <Mission />
      <Footer />
    </div>
  );
}

export default Landing;