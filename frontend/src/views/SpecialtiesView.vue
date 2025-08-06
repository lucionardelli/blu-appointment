<template>
  <div>
    <div class="flex items-center justify-between mb-6">
      <h1 class="text-2xl font-semibold text-gray-900">Specialties</h1>
      <router-link
        to="/specialties/new"
        class="px-4 py-2 text-sm font-medium text-white bg-indigo-600 border border-transparent rounded-md shadow-sm hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
      >
        New Specialty
      </router-link>
    </div>
    <div class="overflow-x-auto bg-white rounded-lg shadow">
      <table class="min-w-full divide-y divide-gray-200">
        <thead class="bg-gray-50">
          <tr>
            <th
              scope="col"
              class="px-6 py-3 text-xs font-medium tracking-wider text-left text-gray-500 uppercase"
            >
              Name
            </th>
            <th
              scope="col"
              class="hidden px-6 py-3 text-xs font-medium tracking-wider text-left text-gray-500 uppercase md:table-cell"
            >
              Default Duration (minutes)
            </th>
            <th
              scope="col"
              class="hidden px-6 py-3 text-xs font-medium tracking-wider text-left text-gray-500 uppercase md:table-cell"
            >
              Default Price
            </th>
            <th scope="col" class="relative px-6 py-3">
              <span class="sr-only">Edit</span>
            </th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          <tr v-for="specialty in specialties" :key="specialty.id">
            <td class="px-6 py-4 whitespace-nowrap">
              <div class="text-sm font-medium text-gray-900">
                {{ specialty.name }}
              </div>
            </td>
            <td class="hidden px-6 py-4 whitespace-nowrap md:table-cell">
              <div class="text-sm text-gray-500">
                {{ specialty.default_duration_minutes }}
              </div>
            </td>
            <td class="hidden px-6 py-4 whitespace-nowrap md:table-cell">
              <div class="text-sm text-gray-500">
                {{ formatCurrency(specialty.current_price) }}
              </div>
            </td>
            <td
              class="px-6 py-4 text-sm font-medium text-right whitespace-nowrap"
            >
              <router-link
                :to="`/specialties/${specialty.id}`"
                class="text-primary hover:text-primary-dark"
                >Edit</router-link
              >
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { formatCurrency } from "@/utils/formatDate";
import api from "@/services/api";

const specialties = ref([]);

const fetchSpecialties = async () => {
  try {
    const response = await api.get("/specialties/");
    specialties.value = response.data;
  } catch (error) {
    console.error("Error fetching specialties:", error);
  }
};

onMounted(fetchSpecialties);
</script>
