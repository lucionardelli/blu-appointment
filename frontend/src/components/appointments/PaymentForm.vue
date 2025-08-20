<template>
  <div class="mt-4">
    <form class="mt-4 space-y-4" @submit.prevent="submitPayment">
      <div class="grid grid-cols-2 gap-6">
        <div>
          <label for="amount" class="block text-sm font-medium text-gray-700">{{
            t("amount")
          }}</label>
          <div class="relative mt-1 rounded-md shadow-sm">
            <input
              id="amount"
              v-model="payment.amount"
              type="number"
              step="0.01"
              required
              class="block w-full pr-12 px-3 py-2 placeholder-gray-400 border border-gray-300 rounded-md appearance-none focus:outline-none focus:ring-primary focus:border-primary sm:text-sm"
            />
            <div v-if="dueAmount > 0" class="absolute inset-y-0 right-0 flex items-center pr-2">
              <button
                type="button"
                class="px-2 py-1 text-xs font-medium text-white bg-primary border border-transparent rounded-md shadow-sm hover:bg-primary-dark focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary"
                @click="payInFull"
              >
                {{ t("pay_in_full") }}
              </button>
            </div>
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
            v-model="payment.method_id"
            required
            class="block w-full px-3 py-2 mt-1 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary sm:text-sm"
          >
            <option
              v-for="pm in paymentMethods"
              :key="pm.value"
              :value="pm.value"
            >
              {{ pm.name }}
            </option>
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
import { ref, computed, onMounted } from "vue";
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
  method_id: null,
  patient_id: props.patientId,
  appointment_id: props.appointmentId,
});

const paymentMethods = ref([]);

const fetchPaymentMethods = async () => {
  try {
    const response = await api.get("/payment_methods/");
    paymentMethods.value = response.data;
    if (paymentMethods.value.length > 0) {
      payment.value.method_id = paymentMethods.value[0].value;
    }
  } catch (error) {
    console.error("Error fetching payment methods:", error);
  }
};

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

onMounted(() => {
  fetchPaymentMethods();
});
</script>
