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
    }
    return {
      user: user,
    };
  },
  getters: {
    isAuthenticated: (state) => !!state.user,
  },
  actions: {
    initialize() {
      // Check if user data is valid after initial load
      if (!this.user || !this.user.id) {
        console.warn(
          "Incomplete or invalid user data found in local storage. Logging out.",
        );
        this.logout();
      }
    },
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
        const { user } = response.data;
        this.user = user;
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
    async updateUser(user) {
      this.user = user;
      localStorage.setItem("user", JSON.stringify(user));
    },
    async logout() {
      try {
        await api.post("/auth/logout");
      } catch (error) {
        console.error("Logout failed:", error);
      } finally {
        this.user = null;
        localStorage.removeItem("user");

        // Reset Pinia stores
        const specialtyStore = useSpecialtyStore();
        specialtyStore.reset();
      }
    },
  },
});
