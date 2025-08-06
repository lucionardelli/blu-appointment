<template>
  <div>
    <h1 class="text-2xl font-semibold text-gray-900">Edit Specialty</h1>
    <form class="mt-6" @submit.prevent="saveSpecialty">
      <div class="space-y-6">
        <div>
          <label for="name" class="block text-sm font-medium text-gray-700"
            >Name</label
          >
          <input
            id="name"
            v-model="specialty.name"
            type="text"
            required
            class="block w-full px-3 py-2 mt-1 placeholder-gray-400 border border-gray-300 rounded-md shadow-sm appearance-none focus:outline-none focus:ring-primary focus:border-primary sm:text-sm"
          />
        </div>
        <div>
          <label
            for="default_duration"
            class="block text-sm font-medium text-gray-700"
            >Default Duration (minutes)</label
          >
          <input
            id="default_duration"
            v-model="specialty.default_duration_minutes"
            type="number"
            required
            class="block w-full px-3 py-2 mt-1 placeholder-gray-400 border border-gray-300 rounded-md shadow-sm appearance-none focus:outline-none focus:ring-primary focus:border-primary sm:text-sm"
          />
        </div>
        <div>
          <label
            for="current_price"
            class="block text-sm font-medium text-gray-700"
            >Default Price</label
          >
          <input
            id="current_price"
            v-model="specialty.current_price"
            type="text"
            inputmode="decimal"
            pattern="^\d+(\.\d{0,2})?$"
            required
            class="block w-full pl-7 pr-3 py-2 placeholder-gray-400 border border-gray-300 rounded-md shadow-sm appearance-none focus:outline-none focus:ring-primary focus:border-primary sm:text-sm"
            placeholder="0.00"
          />
        </div>
      </div>
      <div class="flex justify-end mt-6">
        <router-link
          to="/specialties"
          class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md shadow-sm hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary"
        >
          Cancel
        </router-link>
        <button
          type="submit"
          class="px-4 py-2 ml-3 text-sm font-medium text-white bg-primary border border-transparent rounded-md shadow-sm hover:bg-primary-dark focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary"
        >
          Save
        </button>
      </div>
    </form>

    <div class="mt-8 bg-white shadow overflow-hidden sm:rounded-lg">
      <div class="px-4 py-5 sm:px-6">
        <h3 class="text-lg leading-6 font-medium text-gray-900">
          Pricing History
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
                Date of Change
              </th>
              <th
                scope="col"
                class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
              >
                Price
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
      <!--
      <div class="px-4 py-5 sm:px-6 bg-gray-50">
        <h4 class="text-md font-medium text-gray-900 mb-4">Add New Price Entry</h4>
        <div class="flex items-center space-x-4">
          <input
            type="number"
            v-model.number="newPrice"
            placeholder="New Price"
            class="block w-1/3 px-3 py-2 placeholder-gray-400 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary sm:text-sm"
          />
          <button
            @click="addPriceEntry"
            class="px-4 py-2 text-sm font-medium text-white bg-primary border border-transparent rounded-md shadow-sm hover:bg-primary-dark focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary"
          >
            Add Price
          </button>
        </div>
      </div>
      -->
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import api from "@/services/api";
import { formatDate, formatCurrency } from "@/utils/formatDate";

const route = useRoute();
const router = useRouter();
const specialty = ref({ name: "", default_duration: 0 });
const pricingHistory = ref([]);

const fetchSpecialty = async () => {
  try {
    const response = await api.get(`/specialties/${route.params.id}`);
    specialty.value = response.data;
  } catch (error) {
    console.error("Error fetching specialty:", error);
  }
};

const fetchPricingHistory = async () => {
  try {
    const response = await api.get(`/specialties/${route.params.id}/prices`);
    console.log("Pricing history:", response.data);
    pricingHistory.value = response.data;
    console.log("Pricing history fetched successfully", pricingHistory.value);
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
    await api.put(`/specialties/${route.params.id}`, specialty.value);
    router.push("/specialties");
  } catch (error) {
    console.error("Error saving specialty:", error);
  }
};

/*
I don't think we want to add price entries directly in the table. Is counter-intuitive.
const addPriceEntry = async () => {
  try {
    await api.post(`/specialties/${route.params.id}/prices`, { price: newPrice.value });
    newPrice.value = 0; // Reset input
    fetchPricingHistory(); // Refresh history
  } catch (error) {
    console.error('Error adding price entry:', error);
  }
};
*/
</script>
