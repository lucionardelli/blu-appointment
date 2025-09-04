<template>
  <div
    class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50"
    @click.self="$emit('close')"
  >
    <div
      class="relative top-20 mx-auto p-5 border w-full max-w-md shadow-lg rounded-md bg-white"
    >
      <button
        class="absolute top-0 right-0 mt-2 mr-4 text-gray-400 hover:text-gray-600"
        @click="$emit('close')"
      >
        <i-heroicons-x-mark-20-solid class="w-6 h-6" />
      </button>
      <div class="mt-3 text-center">
        <h3 class="text-lg leading-6 font-medium text-gray-900">
          {{ isNew ? t("new_payment_method") : t("edit_payment_method") }}
        </h3>
        <div class="mt-2 px-7 py-3">
          <form @submit.prevent="savePaymentMethod">
            <div class="mb-4">
              <label
                for="name"
                class="block text-sm font-medium text-gray-700 text-left"
                >{{ t("name") }}</label
              >
              <input
                id="name"
                v-model="form.name"
                type="text"
                required
                class="block w-full px-3 py-2 mt-1 placeholder-gray-400 border border-gray-300 rounded-md shadow-sm appearance-none focus:outline-none focus:ring-primary focus:border-primary sm:text-sm"
              />
            </div>
            <div class="mb-4">
              <label class="flex items-center">
                <input
                  v-model="form.is_active"
                  type="checkbox"
                  class="rounded h-4 w-4 text-primary border-gray-300 focus:ring-primary"
                />
                <span class="ml-2 text-sm text-gray-600">{{
                  t("is_active")
                }}</span>
              </label>
            </div>
            <div class="items-center px-4 py-3">
              <button
                type="submit"
                class="px-4 py-2 text-sm font-medium text-white bg-primary border border-transparent rounded-md shadow-sm hover:bg-primary-dark focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary w-full"
              >
                {{ t("save") }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import { useI18n } from "vue-i18n";
import api from "@/services/api";
import { usePaymentMethodStore } from "@/stores/paymentMethods";

const { t } = useI18n();
const paymentMethodStore = usePaymentMethodStore();

const props = defineProps({
  paymentMethod: {
    type: Object,
    default: null,
  },
});

const emit = defineEmits(["close", "save"]);

const form = ref({
  name: "",
  is_active: true,
});

const isNew = computed(() => !props.paymentMethod);

onMounted(() => {
  if (props.paymentMethod) {
    form.value = { ...props.paymentMethod };
  }
});

const savePaymentMethod = async () => {
  try {
    if (isNew.value) {
      await api.post("/payment_methods/", form.value);
    } else {
      await api.put(`/payment_methods/${props.paymentMethod.id}/`, form.value);
    }
    paymentMethodStore.fetchPaymentMethods();
    emit("save");
  } catch (error) {
    console.error("Error saving payment method:", error);
  }
};
</script>
