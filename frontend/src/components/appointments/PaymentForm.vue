<template>
  <div
    class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full"
    @click.self="$emit('close')"
  >
    <div
      class="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white"
    >
      <div class="mt-3 text-center">
        <h3 class="text-lg leading-6 font-medium text-gray-900">
          Record Payment
        </h3>
        <div class="mt-2 px-7 py-3">
          <p class="text-sm text-gray-500">Amount Due: {{ amountDue }}</p>
          <div v-if="patientCredit > 0" class="mt-4">
            <label class="flex items-center">
              <input
                v-model="applyCredit"
                type="checkbox"
                class="form-checkbox h-5 w-5 text-indigo-600"
              />
              <span class="ml-2 text-sm text-gray-700"
                >Apply patient credit ({{ patientCredit }})</span
              >
            </label>
          </div>
          <div class="mt-4">
            <label
              for="payment_method"
              class="block text-sm font-medium text-gray-700"
              >Payment Method</label
            >
            <select
              id="payment_method"
              v-model="payment.payment_method"
              class="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-primary focus:border-primary sm:text-sm rounded-md"
            >
              <option>Cash</option>
              <option>Credit Card</option>
              <option>Mercadopago</option>
              <option>Gift Card</option>
              <option>Patient's Credit</option>
            </select>
          </div>
          <div class="mt-4">
            <label
              for="amount_paid"
              class="block text-sm font-medium text-gray-700"
              >Amount Paid</label
            >
            <input
              id="amount_paid"
              v-model.number="payment.amount_paid"
              type="number"
              class="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-primary focus:border-primary sm:text-sm rounded-md"
            />
          </div>
        </div>
        <div class="items-center px-4 py-3">
          <button
            class="px-4 py-2 bg-primary text-white text-base font-medium rounded-md w-full shadow-sm hover:bg-primary-dark focus:outline-none focus:ring-2 focus:ring-primary"
            @click="savePayment"
          >
            Save Payment
          </button>
          <button
            class="mt-2 px-4 py-2 bg-gray-200 text-gray-800 text-base font-medium rounded-md w-full shadow-sm hover:bg-gray-300 focus:outline-none focus:ring-2 focus:ring-primary"
            @click="$emit('close')"
          >
            Cancel
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from "vue";
import { api } from "@/services/api";

const props = defineProps({
  appointment: {
    type: Object,
    required: true,
  },
  patientCredit: {
    type: Number,
    default: 0,
  },
});

const emit = defineEmits(["close", "payment-saved"]);

const payment = ref({
  payment_method: "Cash",
  amount_paid: 0,
});

const applyCredit = ref(false);

const amountDue = computed(
  () => props.appointment.price - props.appointment.amount_paid,
);

const savePayment = async () => {
  try {
    // The backend will handle applying credit and calculating final amounts
    await api.post(`/appointments/${props.appointment.id}/payments`, {
      payment_method: payment.value.payment_method,
      amount_paid: payment.value.amount_paid,
      apply_credit: applyCredit.value, // Send a flag to the backend
    });

    emit("payment-saved");
    emit("close");
  } catch (error) {
    console.error("Error saving payment:", error);
  }
};
</script>
