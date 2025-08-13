import { defineStore } from "pinia";
import api from "@/services/api";

export const usePatientStore = defineStore("patients", {
  state: () => ({
    patients: [],
  }),
  actions: {
    async fetchPatients() {
      try {
        const response = await api.get("/patients");
        this.patients = response.data;
      } catch (error) {
        console.error("Error fetching patients:", error);
      }
    },
    addPatient(patient) {
      this.patients.push(patient);
    },
    updatePatient(updatedPatient) {
      const index = this.patients.findIndex((p) => p.id === updatedPatient.id);
      if (index !== -1) {
        this.patients[index] = updatedPatient;
      }
    },
    deletePatient(patientId) {
      this.patients = this.patients.filter((p) => p.id !== patientId);
    },
    reset() {
      this.patients = [];
    },
  },
});
