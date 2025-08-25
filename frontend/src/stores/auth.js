import { defineStore } from "pinia";
import api from "@/services/api";
import { useSpecialtyStore } from "@/stores/specialties";

export const useAuthStore = defineStore("auth", {
  state: () => {
    let user = null;
    try {
      user = JSON.parse(localStorage.getItem("user"));
    } catch (e) {
      console.error("Error parsing user from local storage:", e);
      // If parsing fails, user will remain null, triggering logout if needed
    }
    return {
      user: user,
      token: localStorage.getItem("token") || null,
    };
  },
  getters: {
    isAuthenticated: (state) => !!state.token && !!state.user,
  },
  actions: {
    initialize() {
      // Check if user data is valid after initial load
      if (this.token && (!this.user || !this.user.id)) {
        console.warn(
          "Incomplete or invalid user data found in local storage. Logging out.",
        );
        this.logout();
      }
    },
    async login(username, password) {
      try {
        const response = await api.post(
          "/auth/token/",
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
        const { access_token, user } = response.data;
        this.token = access_token;
        this.user = user;
        localStorage.setItem("token", access_token);
        localStorage.setItem("user", JSON.stringify(this.user));

        // Fetch initial data for specialties
        const specialtyStore = useSpecialtyStore();
        await specialtyStore.fetchSpecialties();

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

      // Reset Pinia stores
      const specialtyStore = useSpecialtyStore();
      specialtyStore.reset();
    },
  },
});
