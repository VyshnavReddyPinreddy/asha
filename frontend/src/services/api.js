import axios from "axios";
import toast from "react-hot-toast";

let authToastShown = false;

const api = axios.create({
  baseURL: "http://localhost:8000",
  withCredentials: true,
});

api.interceptors.response.use(
  (response) => response,

  (error) => {
    if (error.response?.status === 401 &&
      !authToastShown) {
      authToastShown = true;
      toast.error(
        "Session expired. Please login again."
      );

      setTimeout(() => {
        window.location.href = "/login";
      }, 2000);
    }

    return Promise.reject(error);
  }
);

export default api;