import axios from "axios";
import { useAuthStore } from "@/stores/auth";
import router from "@/router";

const instance = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
});

instance.interceptors.request.use(
  (config) => {
    const authStore = useAuthStore();
    if (authStore.token) {
      config.headers.Authorization = `Bearer ${authStore.token}`;
    }

    if (config.url) {
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
  (error) => {
    if (error.response && error.response.status === 401) {
      const authStore = useAuthStore();
      authStore.logout();
      router.push("/login");
    }
    return Promise.reject(error);
  },
);

export default instance;
