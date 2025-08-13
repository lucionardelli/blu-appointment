<template>
  <div>
    <div class="flex items-center justify-between mb-6">
      <h1 class="text-2xl font-semibold text-gray-900">{{ t("patients") }}</h1>
      <router-link
        to="/patients/new"
        class="px-4 py-2 text-sm font-medium text-white bg-primary border border-transparent rounded-md shadow-sm hover:bg-primary-dark focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary"
      >
        {{ t("new_patient") }}
      </router-link>
    </div>
    <div class="mb-4">
      <input
        v-model="searchQuery"
        type="text"
        :placeholder="t('search_patients')"
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
              {{ t("name") }}
            </th>
            <th
              scope="col"
              class="hidden px-6 py-3 text-xs font-medium tracking-wider text-left text-gray-500 uppercase md:table-cell"
            >
              {{ t("default_specialty") }}
            </th>
            <th
              scope="col"
              class="hidden px-6 py-3 text-xs font-medium tracking-wider text-left text-gray-500 uppercase md:table-cell"
            >
              {{ t("last_appointment") }}
            </th>
            <th
              scope="col"
              class="hidden px-6 py-3 text-xs font-medium tracking-wider text-left text-gray-500 uppercase md:table-cell"
            >
              {{ t("next_appointment") }}
            </th>
            <th scope="col" class="relative px-6 py-3">
              <span class="sr-only">{{ t("view") }}</span>
            </th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          <tr v-for="patient in filteredPatients" :key="patient.id">
            <td class="px-6 py-4 whitespace-nowrap">
              <div class="text-sm font-medium text-gray-900">
                {{ patient.name }}
                <span v-if="patient.nickname" class="text-gray-500"
                  >({{ patient.nickname }})</span
                >
              </div>
            </td>
            <td class="hidden px-6 py-4 whitespace-nowrap md:table-cell">
              <div class="text-sm text-gray-500">
                {{ specialties.find(s => s.id === patient.default_specialty_id)?.name || t("not_specified") }}
              </div>
            </td>
            <td class="hidden px-6 py-4 whitespace-nowrap md:table-cell">
              <div class="text-sm text-gray-500">
                {{ formatDate(patient.last_appointment) || "N/A" }}
              </div>
            </td>
            <td class="hidden px-6 py-4 whitespace-nowrap md:table-cell">
              <div class="text-sm text-gray-500">
                {{ formatDate(patient.next_appointment) || "N/A" }}
              </div>
            </td>
            <td
              class="px-6 py-4 text-sm font-medium text-right whitespace-nowrap"
            >
              <router-link
                :to="`/patients/${patient.id}`"
                class="text-primary hover:text-primary-dark"
                >{{ t("view") }}</router-link
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
import { useI18n } from "vue-i18n";
import { formatDate } from "@/utils/formatDate";
import { usePatientStore } from "@/stores/patients";
import { useSpecialtyStore } from "@/stores/specialties";

const { t } = useI18n();

const searchQuery = ref("");

const patientStore = usePatientStore();
const specialtyStore = useSpecialtyStore();

const patients = computed(() => patientStore.patients);
const specialties = computed(() => specialtyStore.specialties);

onMounted(() => {
  patientStore.fetchPatients();
});

const filteredPatients = computed(() => {
  if (!searchQuery.value) {
    return patientStore.patients;
  }
  return patientStore.patients.filter(
    (patient) =>
      patient.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      (patient.nickname &&
        patient.nickname
          .toLowerCase()
          .includes(searchQuery.value.toLowerCase())),
  );
});
</script>
