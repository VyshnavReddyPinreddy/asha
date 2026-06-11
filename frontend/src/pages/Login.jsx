import { useState } from "react";
import { Eye, EyeOff, Activity } from "lucide-react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";
import toast from "react-hot-toast";
import { ArrowLeft } from "lucide-react";


function Login() {
  const navigate = useNavigate();

  const [showPassword, setShowPassword] = useState(false);

  const [formData, setFormData] = useState({
    username: "",
    password: "",
  });

  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setFormData((prev) => ({
      ...prev,
      [e.target.name]: e.target.value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      setLoading(true);

      const response = await api.post("/auth/login", {
        username: formData.username,
        password: formData.password,
      });

      toast.success("Login Successful");

      navigate("/assistant");
    } catch (error) {
      toast.error(
        error.response?.data?.detail ||
          "Login Failed"
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-white flex items-center justify-center px-6">

       <button
        type="button"
        onClick={() => navigate("/")}
        className="
          absolute
          top-6
          right-6
          flex
          items-center
          gap-2
          px-4
          py-2
          rounded-xl
          border
          border-sky-200
          text-sky-600
          hover:bg-sky-50
          transition
        "
      >
        Back to Home
      </button>

      <div className="w-full max-w-md">

        <div className="text-center mb-8">

          <div className="flex justify-center mb-4">
            <Activity
              size={42}
              className="text-sky-500"
            />
          </div>

          

          <h1 className="text-3xl font-bold text-gray-900">
            Welcome Back
          </h1>

          <p className="text-gray-500 mt-2">
            Login to ASHA Connect
          </p>

        </div>

        <div className="bg-white border border-sky-100 rounded-3xl p-8 shadow-lg">

          <form
            onSubmit={handleSubmit}
            className="space-y-5"
          >

            <div>
              <label className="block mb-2 font-medium">
                Username
              </label>

              <input
                type="text"
                name="username"
                required
                value={formData.username}
                onChange={handleChange}
                placeholder="Enter username"
                className="w-full border border-gray-200 rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-sky-400"
              />
            </div>

            <div>

              <label className="block mb-2 font-medium">
                Password
              </label>

              <div className="relative">

                <input
                  type={
                    showPassword
                      ? "text"
                      : "password"
                  }
                  name="password"
                  required
                  value={formData.password}
                  onChange={handleChange}
                  placeholder="Enter password"
                  className="w-full border border-gray-200 rounded-xl px-4 py-3 pr-12 focus:outline-none focus:ring-2 focus:ring-sky-400"
                />

                <button
                  type="button"
                  className="absolute right-4 top-4"
                  onClick={() =>
                    setShowPassword(
                      !showPassword
                    )
                  }
                >
                  {showPassword ? (
                    <EyeOff size={18} />
                  ) : (
                    <Eye size={18} />
                  )}
                </button>

              </div>

            </div>

            <div className="text-right">

              <button
                type="button"
                onClick={() =>
                  navigate("/forgot-password")
                }
                className="text-sky-600 text-sm hover:underline"
              >
                Forgot Password?
              </button>

            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full bg-sky-500 hover:bg-sky-600 text-white py-3 rounded-xl font-semibold transition"
            >
              {loading
                ? "Logging In..."
                : "Login"}
            </button>

          </form>

        </div>

      </div>

    </div>
  );
}

export default Login;