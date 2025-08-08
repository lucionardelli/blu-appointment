<template>
  <div class="mt-4">
    <h3 class="text-lg font-medium text-gray-900">New Payment</h3>
    <form class="mt-4 space-y-4" @submit.prevent="submitPayment">
      <div>
        <label for="amount" class="block text-sm font-medium text-gray-700"
          >Amount</label
        >
        <input
          id="amount"
          v-model="payment.amount"
          type="number"
          step="0.01"
          required
          class="block w-full px-3 py-2 mt-1 placeholder-gray-400 border border-gray-300 rounded-md shadow-sm appearance-none focus:outline-none focus:ring-primary focus:border-primary sm:text-sm"
        />
      </div>
      <div>
        <label
          for="payment_method"
          class="block text-sm font-medium text-gray-700"
          >Payment Method</label
        >
        <select
          id="payment_method"
          v-model="payment.method"
          required
          class="block w-full px-3 py-2 mt-1 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary sm:text-sm"
        >
          <option value="CASH">Cash</option>
          <option value="CREDIT_CARD">Card</option>
          <option value="TRANSFER">Transfer</option>
          <option value="MERCADOPAGO">Mercado Pago</option>
          <option value="GIFT_CARD">Gift Card</option>
          <option value="PATIENT_CREDIT">Patient Credit</option>
        </select>
      </div>
      <div>
        <label for="notes" class="block text-sm font-medium text-gray-700"
          >Notes</label
        >
        <textarea
          id="notes"
          v-model="payment.notes"
          rows="3"
          class="block w-full px-3 py-2 mt-1 placeholder-gray-400 border border-gray-300 rounded-md shadow-sm appearance-none focus:outline-none focus:ring-primary focus:border-primary sm:text-sm"
        ></textarea>
      </div>
      <div class="flex justify-end space-x-2">
        <button
          type="button"
          class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md shadow-sm hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary"
          @click="$emit('cancel')"
        >
          Cancel
        </button>
        <button
          type="submit"
          class="px-4 py-2 text-sm font-medium text-white bg-primary border border-transparent rounded-md shadow-sm hover:bg-primary-dark focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary"
        >
          Save Payment
        </button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref } from "vue";
import api from "@/services/api";

const props = defineProps({
  appointmentId: {
    type: [String, Number],
    required: true,
  },
});

const emit = defineEmits(["save", "cancel"]);

const payment = ref({
  amount: 0,
  method: "cash",
  notes: "",
});

const submitPayment = async () => {
  try {
    await api.post(
      `/appointments/${props.appointmentId}/payments`,
      payment.value,
    );
    emit("save");
  } catch (error) {
    console.error("Error saving payment:", error);
    // Handle error display to user
  }
};
</script>
