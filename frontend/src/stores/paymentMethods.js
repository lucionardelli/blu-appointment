import { defineStore } from "pinia";
import api from "@/services/api";

export const usePaymentMethodStore = defineStore("paymentMethods", {
  state: () => ({
    paymentMethods: [],
  }),
  actions: {
    async fetchPaymentMethods() {
      try {
        const response = await api.get("/payment_methods/");
        this.paymentMethods = response.data;
      } catch (error) {
        console.error("Error fetching payment methods:", error);
      }
    },
    addPaymentMethod(paymentMethod) {
      this.paymentMethods.push(paymentMethod);
    },
    updatePaymentMethod(updatedPaymentMethod) {
      const index = this.paymentMethods.findIndex(
        (pm) => pm.id === updatedPaymentMethod.id,
      );
      if (index !== -1) {
        this.paymentMethods[index] = updatedPaymentMethod;
      }
    },
    async deletePaymentMethod(paymentMethodId) {
      try {
        await api.delete(`/payment_methods/${paymentMethodId}`);
        this.paymentMethods = this.paymentMethods.filter(
          (pm) => pm.id !== paymentMethodId,
        );
      } catch (error) {
        console.error("Error deleting payment method:", error);
        throw error;
      }
    },
    reset() {
      this.paymentMethods = [];
    },
  },
});
