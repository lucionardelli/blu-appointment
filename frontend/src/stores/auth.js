import { defineStore } from "pinia";
import axios from "axios";

const API_URL = "http://localhost:5000/api/v1";

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
      // Mock login for development
      if (username === "DrWho" && password === "Tardis") {
        const mockUser = { name: "The Doctor", username: "DrWho" };
        const mockToken = "mock-tardis-token";
        this.user = mockUser;
        this.token = mockToken;
        localStorage.setItem("user", JSON.stringify(mockUser));
        localStorage.setItem("token", mockToken);
        return true;
      }

      try {
        const response = await axios.post(`${API_URL}/auth/login`, {
          username,
          password,
        });
        const { access_token, user } = response.data;
        this.token = access_token;
        this.user = user;
        localStorage.setItem("token", access_token);
        localStorage.setItem("user", JSON.stringify(user));
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
