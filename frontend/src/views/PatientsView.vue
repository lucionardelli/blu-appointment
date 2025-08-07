<template>
  <div>
    <div class="flex items-center justify-between mb-6">
      <h1 class="text-2xl font-semibold text-gray-900">Patients</h1>
      <router-link
        to="/patients/new"
        class="px-4 py-2 text-sm font-medium text-white bg-indigo-600 border border-transparent rounded-md shadow-sm hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
      >
        New Patient
      </router-link>
    </div>
    <div class="mb-4">
      <input
        v-model="searchQuery"
        type="text"
        placeholder="Search patients..."
        class="block w-full px-3 py-2 placeholder-gray-400 border border-gray-300 rounded-md shadow-sm appearance-none focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
      />
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
              Last Appointment
            </th>
            <th scope="col" class="relative px-6 py-3">
              <span class="sr-only">Edit</span>
            </th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          <tr v-for="patient in filteredPatients" :key="patient.id">
            <td class="px-6 py-4 whitespace-nowrap">
              <div class="text-sm font-medium text-gray-900">
                {{ patient.name }}
              </div>
            </td>
            <td class="hidden px-6 py-4 whitespace-nowrap md:table-cell">
              <div class="text-sm text-gray-500">
                {{ formatDate(patient.last_appointment) || "N/A" }}
              </div>
            </td>
            <td
              class="px-6 py-4 text-sm font-medium text-right whitespace-nowrap"
            >
              <router-link
                :to="`/patients/${patient.id}`"
                class="text-primary hover:text-primary-dark"
                >View</router-link
              >
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import api from "@/services/api";
import { formatDate } from "@/utils/formatDate";

const patients = ref([]);
const searchQuery = ref("");

const fetchPatients = async () => {
  try {
    const response = await api.get("/patients/");
    patients.value = response.data;
  } catch (error) {
    console.error("Error fetching patients:", error);
  }
};

onMounted(fetchPatients);

const filteredPatients = computed(() => {
  if (!searchQuery.value) {
    return patients.value;
  }
  return patients.value.filter((patient) =>
    patient.name.toLowerCase().includes(searchQuery.value.toLowerCase()),
  );
});
</script>
