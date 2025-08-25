<template>
  <div>
    <div class="bg-white shadow overflow-hidden sm:rounded-lg">
      <div class="px-4 py-5 sm:px-6 flex justify-between items-center">
        <div class="flex items-center">
          <button
            class="mr-2 p-1 rounded-full hover:bg-gray-200"
            @click="goBack"
          >
            <i-heroicons-arrow-left-20-solid class="h-6 w-6 text-gray-500" />
          </button>
          <h3 class="text-lg leading-6 font-medium text-gray-900">
            {{ isNew ? t("new_specialty") : t("edit_specialty") }}
          </h3>
        </div>
        <button
          type="submit"
          class="px-4 py-2 text-sm font-medium text-white bg-primary border border-transparent rounded-md shadow-sm hover:bg-primary-dark focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary"
          @click="saveSpecialty"
        >
          {{ t("save") }}
        </button>
      </div>
      <div class="border-t border-gray-200">
        <form @submit.prevent="saveSpecialty">
          <dl class="sm:divide-y sm:divide-gray-200">
            <div
              class="bg-gray-50 px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6"
            >
              <dt class="text-sm font-medium text-gray-500">
                {{ t("name") }}
              </dt>
              <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                <input
                  id="name"
                  v-model="specialty.name"
                  type="text"
                  required
                  class="block w-full px-3 py-2 mt-1 placeholder-gray-400 border border-gray-300 rounded-md shadow-sm appearance-none focus:outline-none focus:ring-primary focus:border-primary sm:text-sm"
                />
              </dd>
            </div>
            <div
              class="bg-white px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6"
            >
              <dt class="text-sm font-medium text-gray-500">
                {{ t("default_duration") }}
              </dt>
              <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                <input
                  id="default_duration"
                  v-model="specialty.default_duration_minutes"
                  type="number"
                  required
                  class="block w-full px-3 py-2 mt-1 placeholder-gray-400 border border-gray-300 rounded-md shadow-sm appearance-none focus:outline-none focus:ring-primary focus:border-primary sm:text-sm"
                />
              </dd>
            </div>
            <div
              class="bg-gray-50 px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6"
            >
              <dt class="text-sm font-medium text-gray-500">
                {{ t("default_price") }}
              </dt>
              <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                <input
                  id="current_price"
                  v-model="specialty.current_price"
                  type="text"
                  inputmode="decimal"
                  pattern="^\d+(\.\d{0,2})?$"
                  required
                  class="block w-full pl-7 pr-3 py-2 placeholder-gray-400 border border-gray-300 rounded-md shadow-sm appearance-none focus:outline-none focus:ring-primary focus:border-primary sm:text-sm"
                  :placeholder="t('price')"
                />
              </dd>
            </div>
            <div
              class="bg-white px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6"
            >
              <dt class="text-sm font-medium text-gray-500">
                {{ t("color") }}
              </dt>
              <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                <Chrome
                  :model-value="specialtyColorObject"
                  @update:model-value="updateColor"
                />
              </dd>
            </div>
          </dl>
        </form>
      </div>
    </div>

    <div
      v-if="!isNew"
      class="mt-8 bg-white shadow overflow-hidden sm:rounded-lg"
    >
      <div class="px-4 py-5 sm:px-6">
        <h3 class="text-lg leading-6 font-medium text-gray-900">
          {{ t("pricing_history") }}
        </h3>
      </div>
      <div class="border-t border-gray-200">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th
                scope="col"
                class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
              >
                {{ t("date_of_change") }}
              </th>
              <th
                scope="col"
                class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
              >
                {{ t("price") }}
              </th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="priceEntry in pricingHistory" :key="priceEntry.id">
              <td
                class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900"
              >
                {{ formatDate(priceEntry.valid_from) }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {{ formatCurrency(priceEntry.price) }}
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import { Chrome } from "@ckpack/vue-color";
import { useRoute, useRouter } from "vue-router";
import api from "@/services/api";
import { formatDate, formatCurrency } from "@/utils/formatDate";
import { useI18n } from "vue-i18n";

const { t } = useI18n();
const route = useRoute();
const router = useRouter();

const specialty = ref({
  name: "",
  default_duration_minutes: 0,
  current_price: 0,
  color: "#4F46E5FF", // Default color with full opacity
});

function hexToRgba(hex) {
  const r = parseInt(hex.slice(1, 3), 16);
  const g = parseInt(hex.slice(3, 5), 16);
  const b = parseInt(hex.slice(5, 7), 16);
  const a = hex.length === 9 ? parseInt(hex.slice(7, 9), 16) / 255 : 1;
  return { r, g, b, a };
}

function rgbaToHex({ r, g, b, a }) {
  const toHex = (c) => c.toString(16).padStart(2, "0");
  return `#${toHex(r)}${toHex(g)}${toHex(b)}${toHex(Math.round(a * 255))}`.toUpperCase();
}

const specialtyColorObject = computed({
  get: () => {
    if (!specialty.value.color) {
      return { r: 0, g: 0, b: 0, a: 1 }; // Default to black if no color
    }
    return hexToRgba(specialty.value.color);
  },
  // eslint-disable-next-line no-unused-vars
  set: (newColor) => {
    // This setter is not directly used by Chrome
    // The updateColor method will handle the actual model update
  },
});

const updateColor = (newColor) => {
  const { r, g, b, a } = newColor.rgba;
  specialty.value.color = rgbaToHex({ r, g, b, a });
};

const pricingHistory = ref([]);

const isNew = computed(() => !route.params.id);

const fetchSpecialty = async () => {
  if (isNew.value) return;
  try {
    const response = await api.get(`/specialties/${route.params.id}/`);
    specialty.value = response.data;
  } catch (error) {
    console.error("Error fetching specialty:", error);
  }
};

const fetchPricingHistory = async () => {
  if (isNew.value) return;
  try {
    const response = await api.get(`/specialties/${route.params.id}/prices/`);
    pricingHistory.value = response.data;
  } catch (error) {
    console.error("Error fetching pricing history:", error);
  }
};

onMounted(() => {
  fetchSpecialty();
  fetchPricingHistory();
});

const saveSpecialty = async () => {
  try {
    if (isNew.value) {
      const response = await api.post("/specialties/", specialty.value);
      router.push(`/specialties/${response.data.id}`);
    } else {
      await api.put(`/specialties/${route.params.id}/`, specialty.value);
      // Re-fetch pricing history to show updated price if it changed
      fetchPricingHistory();
    }
  } catch (error) {
    console.error("Error saving specialty:", error);
  }
};

const goBack = () => {
  router.push("/specialties");
};
</script>
