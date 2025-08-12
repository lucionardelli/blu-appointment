import { defineStore } from "pinia";
import api from "@/services/api";

export const useSettingsStore = defineStore("settings", {
  state: () => ({
    workingHoursRaw: [], // Stores the raw data from the backend
    loading: false,
  }),
  getters: {
    businessHours: (state) => {
      const grouped = state.workingHoursRaw.reduce((acc, day) => {
        if (!day.is_closed) {
          const key = `${day.startTime}-${day.endTime}`;
          if (!acc[key]) {
            acc[key] = {
              startTime: day.startTime.slice(0, 5), // Remove seconds
              endTime: day.endTime.slice(0, 5), // Remove seconds
              daysOfWeek: [],
            };
          }
          acc[key].daysOfWeek.push(day.dayOfWeek);
        }
        return acc;
      }, {});
      return Object.values(grouped);
    },
  },
  actions: {
    async fetchWorkingHours() {
      this.loading = true;
      try {
        const response = await api.get("/appointments/working-hours/");
        this.workingHoursRaw = response.data;
      } catch (error) {
        console.error("Error fetching working hours, using defaults.", error);
      } finally {
        this.loading = false;
      }
    },
  },
});
