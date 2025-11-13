import axios from "axios";
import { useAuthStore } from "@/stores/auth";
import router from "@/router";

const instance = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  withCredentials: true,
});

let refreshPromise = null;

instance.interceptors.request.use(
  (config) => {
    const authEndpoints = ["/auth/token", "/auth/refresh", "/auth/logout"];
    if (config.url && !authEndpoints.some((endpoint) => config.url === endpoint)) {
      const q_index = config.url.indexOf("?");
      if (q_index === -1) {
        if (!config.url.endsWith("/")) {
          config.url += "/";
        }
      } else {
        const path = config.url.substring(0, q_index);
        if (!path.endsWith("/")) {
          const query = config.url.substring(q_index);
          config.url = path + "/" + query;
        }
      }
    }

    return config;
  },
  (error) => {
    return Promise.reject(error);
  },
);

instance.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    if (
      error.response?.status === 401 &&
      !originalRequest._retry &&
      originalRequest.url !== "/auth/refresh"
    ) {
      originalRequest._retry = true;
      const authStore = useAuthStore();

      if (!refreshPromise) {
        refreshPromise = instance.post("/auth/refresh")
          .then((response) => {
            const { user } = response.data;
            authStore.updateUser(user);
            return true;
          })
          .catch((refreshError) => {
            authStore.logout();
            router.push("/login");
            throw refreshError;
          })
          .finally(() => {
            refreshPromise = null;
          });
      }

      try {
        await refreshPromise;
        return instance(originalRequest);
      } catch (refreshError) {
        return Promise.reject(refreshError);
      }
    }
    return Promise.reject(error);
  },
);

export default instance;
