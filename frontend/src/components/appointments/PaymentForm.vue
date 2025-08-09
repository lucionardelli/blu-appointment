<template>
  <div class="mt-4">
    <div class="flex items-center mb-4">
      <button
        class="mr-2 p-1 rounded-full hover:bg-gray-200"
        @click="$emit('cancel')"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          class="h-6 w-6 text-gray-500"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M10 19l-7-7m0 0l7-7m-7 7h18"
          />
        </svg>
      </button>
      <h2 class="text-xl font-semibold text-gray-800">
        {{ t("payments") }} > {{ t("new_payment") }}
      </h2>
    </div>
    <form class="mt-4 space-y-4" @submit.prevent="submitPayment">
      <div class="grid grid-cols-2 gap-6">
        <div>
          <label for="amount" class="block text-sm font-medium text-gray-700">{{
            t("amount")
          }}</label>
          <div class="flex items-center mt-1">
            <input
              id="amount"
              v-model="payment.amount"
              type="number"
              step="0.01"
              required
              class="block w-full px-3 py-2 placeholder-gray-400 border border-gray-300 rounded-md shadow-sm appearance-none focus:outline-none focus:ring-primary focus:border-primary sm:text-sm"
            />
            <button
              type="button"
              class="ml-2 px-3 py-2 text-sm font-medium text-white bg-primary border border-transparent rounded-md shadow-sm hover:bg-primary-dark focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary"
              @click="payInFull"
            >
              {{ t("pay_in_full") }}
            </button>
          </div>
        </div>
        <div>
          <label
            for="payment_method"
            class="block text-sm font-medium text-gray-700"
            >{{ t("payment_method") }}</label
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
      </div>
      <div class="flex justify-end space-x-2">
        <button
          type="button"
          class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md shadow-sm hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary"
          @click="$emit('cancel')"
        >
          {{ t("cancel") }}
        </button>
        <button
          type="submit"
          class="px-4 py-2 text-sm font-medium text-white bg-primary border border-transparent rounded-md shadow-sm hover:bg-primary-dark focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary"
        >
          {{ t("save_payment") }}
        </button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, computed } from "vue";
import { useI18n } from "vue-i18n";
import api from "@/services/api";

const { t } = useI18n();

const props = defineProps({
  appointmentId: {
    type: [String, Number],
    required: true,
  },
  appointment: {
    type: Object,
    required: true,
  },
});

const emit = defineEmits(["save", "cancel"]);

const dueAmount = computed(() => {
  return props.appointment.cost - (props.appointment.total_paid || 0);
});

const payment = ref({
  amount: 0,
  method: "CASH",
});

const payInFull = () => {
  if (dueAmount.value <= 0) {
    console.warn("No amount due to pay in full.");
    return;
  }
  payment.value.amount = dueAmount.value;
};

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
