<template>
  <div class="p-4 sm:p-6 lg:p-8">
    <div class="flex items-center justify-between mb-6">
      <h1 class="text-2xl font-semibold text-gray-900">
        {{ t("payment_methods") }}
      </h1>
      <button
        class="px-4 py-2 text-sm font-medium text-white bg-primary border border-transparent rounded-md shadow-sm hover:bg-primary-dark focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary"
        @click="openPaymentMethodModal(null)"
      >
        {{ t("new_payment_method") }}
      </button>
    </div>
    <div class="overflow-x-auto">
      <table class="min-w-full divide-y divide-gray-200">
        <thead class="bg-gray-50">
          <tr>
            <th
              scope="col"
              class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
            >
              {{ t("name") }}
            </th>
            <th
              scope="col"
              class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
            >
              {{ t("is_active") }}
            </th>
            <th scope="col" class="relative px-6 py-3">
              <span class="sr-only">{{ t("edit") }}</span>
            </th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          <tr v-for="paymentMethod in paymentMethods" :key="paymentMethod.id">
            <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
              {{ paymentMethod.name }}
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
              <span
                :class="{
                  'bg-green-100 text-green-800': paymentMethod.is_active,
                  'bg-red-100 text-red-800': !paymentMethod.is_active,
                }"
                class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full"
              >
                {{ paymentMethod.is_active ? t("active") : t("inactive") }}
              </span>
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
              <button
                class="text-primary hover:text-primary-dark"
                @click="openPaymentMethodModal(paymentMethod)"
              >
                {{ t("edit") }}
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <PaymentMethodFormModal
      v-if="showModal"
      :payment-method="selectedPaymentMethod"
      @close="showModal = false"
      @save="handleSave"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useI18n } from "vue-i18n";
import api from "@/services/api";
import PaymentMethodFormModal from "@/components/payments/PaymentMethodFormModal.vue";

const { t } = useI18n();

const paymentMethods = ref([]);
const showModal = ref(false);
const selectedPaymentMethod = ref(null);

const fetchPaymentMethods = async () => {
  try {
    const response = await api.get("/payment_methods/");
    paymentMethods.value = response.data;
  } catch (error) {
    console.error("Error fetching payment methods:", error);
  }
};

const openPaymentMethodModal = (paymentMethod) => {
  selectedPaymentMethod.value = paymentMethod;
  showModal.value = true;
};

const handleSave = () => {
  showModal.value = false;
  fetchPaymentMethods();
};

onMounted(() => {
  fetchPaymentMethods();
});
</script>
