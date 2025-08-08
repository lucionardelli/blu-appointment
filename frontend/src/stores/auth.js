import { defineStore } from "pinia";
import api from "@/services/api";

export const useAuthStore = defineStore("auth", {
  state: () => ({
    user: JSON.parse(localStorage.getItem("user")),
    token: localStorage.getItem("token") || null,
  }),
  getters: {
    isAuthenticated: (state) => !!state.token,
  },
  actions: {
    async login(username, password) {
      try {
        const response = await api.post(
          "/auth/token",
          new URLSearchParams({
            username: username,
            password: password,
          }),
          {
            headers: {
              "Content-Type": "application/x-www-form-urlencoded",
            },
          },
        );
        const { access_token } = response.data;
        this.token = access_token;
        // For now, we don't have user details from the /token endpoint
        // You might need a separate endpoint to fetch user details after login
        this.user = { username: username }; // Placeholder
        localStorage.setItem("token", access_token);
        localStorage.setItem("user", JSON.stringify(this.user));
        return true;
      } catch (error) {
        console.error("Login failed:", error);
        this.logout();
        throw error;
      }
    },
    logout() {
      this.user = null;
      this.token = null;
      localStorage.removeItem("token");
      localStorage.removeItem("user");
    },
  },
});
