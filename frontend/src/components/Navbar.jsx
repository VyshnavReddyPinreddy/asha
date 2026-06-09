import { Activity } from "lucide-react";
import { Link } from "react-router-dom";

function Navbar() {
  return (
    <nav className="sticky top-0 z-50 bg-white/90 backdrop-blur-md border-b border-sky-100">
      <div className="max-w-7xl mx-auto px-6 py-4 flex justify-between items-center">

        <div className="flex items-center gap-2">
          {/* <Activity className="text-sky-500" size={28} /> */}
          <h1 className="font-bold text-xl text-sky-600">
            ASHA Connect 
          </h1>
        </div>

        <div className="hidden md:flex gap-8 text-gray-600">
          <a href="#features">Features</a>
          <a href="#mission">Mission</a>
        </div>

        <Link
          to="/login"
          className="bg-sky-500 hover:bg-sky-600 text-white px-5 py-2 rounded-xl transition"
        >
          Login
        </Link>

      </div>
    </nav>
  );
}

export default Navbar;