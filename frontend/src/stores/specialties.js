import { defineStore } from "pinia";
import api from "@/services/api";

export const useSpecialtyStore = defineStore("specialties", {
  state: () => ({
    specialties: [],
  }),
  actions: {
    async fetchSpecialties() {
      try {
        const response = await api.get("/specialties/");
        this.specialties = response.data;
      } catch (error) {
        console.error("Error fetching specialties:", error);
      }
    },
    addSpecialty(specialty) {
      this.specialties.push(specialty);
    },
    updateSpecialty(updatedSpecialty) {
      const index = this.specialties.findIndex(
        (s) => s.id === updatedSpecialty.id,
      );
      if (index !== -1) {
        this.specialties[index] = updatedSpecialty;
      }
    },
    deleteSpecialty(specialtyId) {
      this.specialties = this.specialties.filter((s) => s.id !== specialtyId);
    },
    reset() {
      this.specialties = [];
    },
  },
});
