import { useState, useEffect } from "react";
import { Eye, EyeOff, Activity, ChevronLeft } from "lucide-react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";
import toast from "react-hot-toast";

function ForgotPassword() {
  const navigate = useNavigate();

  const [currentStage, setCurrentStage] = useState("email");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const [email, setEmail] = useState("");
  const [otp, setOtp] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");

  const [showPassword, setShowPassword] = useState(false);
  const [showConfirm, setShowConfirm] = useState(false);

  const [resendTimer, setResendTimer] = useState(0);

  useEffect(() => {
    if (resendTimer > 0) {
      const timer = setTimeout(
        () => setResendTimer(resendTimer - 1),
        1000
      );
      return () => clearTimeout(timer);
    }
  }, [resendTimer]);

  const validateEmail = (emailStr) => {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(emailStr);
  };

  const handleEmailSubmit = async (e) => {
    e.preventDefault();
    setError("");

    if (!email.trim()) {
      setError("Email is required");
      return;
    }

    if (!validateEmail(email)) {
      setError("Please enter a valid email");
      return;
    }

    try {
      setLoading(true);
      await api.post("/auth/forgot-password", {
        email,
      });
      toast.success("OTP sent to your email");
      setCurrentStage("otp");
      setResendTimer(60);
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          "Failed to send OTP"
      );
      toast.error(
        err.response?.data?.detail ||
          "Failed to send OTP"
      );
    } finally {
      setLoading(false);
    }
  };

  const handleResendOtp = async () => {
    setError("");

    try {
      setLoading(true);
      await api.post("/auth/forgot-password", {
        email,
      });
      toast.success("OTP sent to your email");
      setResendTimer(60);
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          "Failed to resend OTP"
      );
      toast.error(
        err.response?.data?.detail ||
          "Failed to resend OTP"
      );
    } finally {
      setLoading(false);
    }
  };

  const handleOtpSubmit = (e) => {
    e.preventDefault();
    setError("");

    if (!otp.trim()) {
      setError("OTP is required");
      return;
    }

    if (!/^\d{6}$/.test(otp)) {
      setError("OTP must be 6 digits");
      return;
    }

    setCurrentStage("password");
  };

  const handlePasswordSubmit = async (e) => {
    e.preventDefault();
    setError("");

    if (!newPassword || !confirmPassword) {
      setError("Both passwords are required");
      return;
    }

    if (newPassword.length < 8) {
      setError(
        "Password must be at least 8 characters long"
      );
      return;
    }

    if (newPassword !== confirmPassword) {
      setError("Passwords do not match");
      return;
    }

    try {
      setLoading(true);
      await api.post("/auth/reset-password", {
        email,
        otp,
        new_password: newPassword,
      });
      toast.success(
        "Password reset successful. Please login to continue"
      );
      navigate("/login");
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          "Failed to reset password"
      );
      toast.error(
        err.response?.data?.detail ||
          "Failed to reset password"
      );
    } finally {
      setLoading(false);
    }
  };

  const goBack = () => {
    if (currentStage === "otp") {
      setOtp("");
      setError("");
      setCurrentStage("email");
    } else if (currentStage === "password") {
      setNewPassword("");
      setConfirmPassword("");
      setError("");
      setCurrentStage("otp");
    }
  };

  return (
    <div className="min-h-screen bg-white flex items-center justify-center px-6">
      <button
        type="button"
        onClick={() => navigate("/login")}
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
        <ChevronLeft size={16} />
        Back to Login
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
            Reset Password
          </h1>

          <p className="text-gray-500 mt-2">
            {currentStage === "email" &&
              "Enter your registered email"}
            {currentStage === "otp" &&
              "Enter the OTP sent to your email"}
            {currentStage === "password" &&
              "Create a new password"}
          </p>
        </div>

        <div className="bg-white border border-sky-100 rounded-3xl p-8 shadow-lg">
          {currentStage === "email" && (
            <form
              onSubmit={handleEmailSubmit}
              className="space-y-5"
            >
              <div>
                <label className="block mb-2 font-medium">
                  Email Address
                </label>

                <input
                  type="email"
                  value={email}
                  onChange={(e) =>
                    setEmail(e.target.value)
                  }
                  placeholder="Enter your email"
                  required
                  className="w-full border border-gray-200 rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-sky-400"
                />
              </div>

              {error && (
                <div className="p-3 bg-red-50 border border-red-200 rounded-lg text-red-600 text-sm">
                  {error}
                </div>
              )}

              <button
                type="submit"
                disabled={loading}
                className="w-full bg-sky-500 hover:bg-sky-600 disabled:opacity-50 text-white py-3 rounded-xl font-semibold transition"
              >
                {loading
                  ? "Sending OTP..."
                  : "Send OTP"}
              </button>
            </form>
          )}

          {currentStage === "otp" && (
            <form
              onSubmit={handleOtpSubmit}
              className="space-y-5"
            >
              <div>
                <p className="text-sm text-gray-600 mb-4">
                  OTP sent to{" "}
                  <span className="font-medium">
                    {email}
                  </span>
                </p>

                <label className="block mb-2 font-medium">
                  Enter OTP
                </label>

                <input
                  type="text"
                  value={otp}
                  onChange={(e) => {
                    const val = e.target.value.replace(
                      /[^\d]/g,
                      ""
                    );
                    setOtp(val.slice(0, 6));
                  }}
                  placeholder="Enter 6-digit OTP"
                  maxLength="6"
                  required
                  className="w-full border border-gray-200 rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-sky-400 text-center text-lg tracking-widest"
                />
              </div>

              {error && (
                <div className="p-3 bg-red-50 border border-red-200 rounded-lg text-red-600 text-sm">
                  {error}
                </div>
              )}

              <button
                type="submit"
                disabled={loading}
                className="w-full bg-sky-500 hover:bg-sky-600 disabled:opacity-50 text-white py-3 rounded-xl font-semibold transition"
              >
                {loading
                  ? "Verifying..."
                  : "Verify OTP"}
              </button>

              <button
                type="button"
                onClick={handleResendOtp}
                disabled={resendTimer > 0 || loading}
                className="w-full text-sky-600 text-sm hover:underline disabled:text-gray-400"
              >
                {resendTimer > 0
                  ? `Resend OTP in ${resendTimer}s`
                  : "Resend OTP"}
              </button>

              <button
                type="button"
                onClick={goBack}
                className="w-full flex items-center justify-center gap-2 text-gray-600 py-2 rounded-xl hover:bg-gray-50 transition"
              >
                <ChevronLeft size={16} />
                Back
              </button>
            </form>
          )}

          {currentStage === "password" && (
            <form
              onSubmit={handlePasswordSubmit}
              className="space-y-5"
            >
              <div>
                <label className="block mb-2 font-medium">
                  New Password
                </label>

                <div className="relative">
                  <input
                    type={
                      showPassword
                        ? "text"
                        : "password"
                    }
                    value={newPassword}
                    onChange={(e) =>
                      setNewPassword(
                        e.target.value
                      )
                    }
                    placeholder="Enter new password"
                    required
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

                <p className="text-xs text-gray-500 mt-1">
                  Minimum 8 characters
                </p>
              </div>

              <div>
                <label className="block mb-2 font-medium">
                  Confirm Password
                </label>

                <div className="relative">
                  <input
                    type={
                      showConfirm
                        ? "text"
                        : "password"
                    }
                    value={confirmPassword}
                    onChange={(e) =>
                      setConfirmPassword(
                        e.target.value
                      )
                    }
                    placeholder="Confirm password"
                    required
                    className="w-full border border-gray-200 rounded-xl px-4 py-3 pr-12 focus:outline-none focus:ring-2 focus:ring-sky-400"
                  />

                  <button
                    type="button"
                    className="absolute right-4 top-4"
                    onClick={() =>
                      setShowConfirm(
                        !showConfirm
                      )
                    }
                  >
                    {showConfirm ? (
                      <EyeOff size={18} />
                    ) : (
                      <Eye size={18} />
                    )}
                  </button>
                </div>
              </div>

              {error && (
                <div className="p-3 bg-red-50 border border-red-200 rounded-lg text-red-600 text-sm">
                  {error}
                </div>
              )}

              <button
                type="submit"
                disabled={loading}
                className="w-full bg-sky-500 hover:bg-sky-600 disabled:opacity-50 text-white py-3 rounded-xl font-semibold transition"
              >
                {loading
                  ? "Resetting..."
                  : "Reset Password"}
              </button>

              <button
                type="button"
                onClick={goBack}
                className="w-full flex items-center justify-center gap-2 text-gray-600 py-2 rounded-xl hover:bg-gray-50 transition"
              >
                <ChevronLeft size={16} />
                Back
              </button>
            </form>
          )}
        </div>
      </div>
    </div>
  );
}

export default ForgotPassword;
