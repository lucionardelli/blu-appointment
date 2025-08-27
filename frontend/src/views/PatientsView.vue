<template>
  <div class="p-4 sm:p-6 lg:p-8">
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
    <div v-if="loading && !patients.length" class="text-center">
      <p>{{ t("loading_patients") }}</p>
    </div>
    <div v-else-if="error" class="text-center text-red-500">
      <p>{{ t("error_loading_patients") }}</p>
    </div>
    <div v-else>
      <div
        class="overflow-x-auto bg-white rounded-lg shadow"
        :class="{ 'opacity-50': loading }"
      >
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
            <tr v-for="patient in patients" :key="patient.id">
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
                  {{
                    specialties.find(
                      (s) => s.id === patient.default_specialty_id,
                    )?.name || t("not_specified")
                  }}
                </div>
              </td>
              <td class="hidden px-6 py-4 whitespace-nowrap md:table-cell">
                <div class="text-sm text-gray-500">
                  {{ formatDate(patient.last_appointment) || "-" }}
                </div>
              </td>
              <td class="hidden px-6 py-4 whitespace-nowrap md:table-cell">
                <div class="text-sm text-gray-500">
                  {{ formatDate(patient.next_appointment) || "-" }}
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
      <div
        class="flex items-center justify-between border-t border-gray-200 bg-white px-4 py-3 sm:px-6"
      >
        <div class="flex flex-1 justify-between sm:hidden">
          <button
            :disabled="currentPage === 1"
            class="relative inline-flex items-center rounded-md border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50"
            @click="changePage(currentPage - 1)"
          >
            {{ t("previous") }}
          </button>
          <button
            :disabled="currentPage === totalPages"
            class="relative ml-3 inline-flex items-center rounded-md border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50"
            @click="changePage(currentPage + 1)"
          >
            {{ t("next") }}
          </button>
        </div>
        <div
          class="hidden sm:flex sm:flex-1 sm:items-center sm:justify-between"
        >
          <div>
            <p v-if="totalPatientsCount > 0" class="text-sm text-gray-700">
              {{ t("showing") }}
              <span class="font-medium">{{
                totalPatientsCount > 0
                  ? (currentPage - 1) * itemsPerPage + 1
                  : 0
              }}</span>
              {{ t("to") }}
              <span class="font-medium">{{
                Math.min(currentPage * itemsPerPage, totalPatientsCount)
              }}</span>
              {{ t("of") }}
              <span class="font-medium">{{ totalPatientsCount }}</span>
              {{ t("results") }}
            </p>
            <p v-else class="text-sm text-gray-700">
              {{ t("no_patients_found") }}
            </p>
          </div>
          <div>
            <nav
              class="isolate inline-flex -space-x-px rounded-md shadow-sm"
              aria-label="Pagination"
            >
              <button
                :disabled="currentPage === 1"
                class="relative inline-flex items-center rounded-l-md px-2 py-2 text-gray-400 ring-1 ring-inset ring-gray-300 hover:bg-gray-50 focus:z-20 focus:outline-offset-0"
                @click="changePage(currentPage - 1)"
              >
                <span class="sr-only">{{ t("previous") }}</span>
                <i-heroicons-chevron-left-20-solid
                  class="h-5 w-5"
                  aria-hidden="true"
                />
              </button>
              <button
                v-for="page in visiblePages"
                :key="page"
                :disabled="page === '...'"
                :class="[
                  page === currentPage
                    ? 'relative z-10 inline-flex items-center bg-primary px-4 py-2 text-sm font-semibold text-white focus:z-20 focus:outline-offset-0'
                    : 'relative inline-flex items-center px-4 py-2 text-sm font-semibold text-gray-900 ring-1 ring-inset ring-gray-300 hover:bg-gray-50 focus:z-20 focus:outline-offset-0',
                ]"
                @click="typeof page === 'number' && changePage(page)"
              >
                {{ page }}
              </button>
              <button
                :disabled="currentPage === totalPages"
                class="relative inline-flex items-center rounded-r-md px-2 py-2 text-gray-400 ring-1 ring-inset ring-gray-300 hover:bg-gray-50 focus:z-20 focus:outline-offset-0"
                @click="changePage(currentPage + 1)"
              >
                <span class="sr-only">{{ t("next") }}</span>
                <i-heroicons-chevron-right-20-solid
                  class="h-5 w-5"
                  aria-hidden="true"
                />
              </button>
            </nav>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from "vue";
import { useI18n } from "vue-i18n";
import { formatDate } from "@/utils/formatDate";
import { useSpecialtyStore } from "@/stores/specialties";
import api from "@/services/api";
import debounce from "lodash/debounce";

const { t } = useI18n();

const patients = ref([]);
const searchQuery = ref("");
const loading = ref(true);
const error = ref(false);
const currentPage = ref(1);
const itemsPerPage = ref(10);
const totalPatientsCount = ref(0);

const specialtyStore = useSpecialtyStore();
const specialties = computed(() => specialtyStore.specialties);

const totalPages = computed(() => {
  return Math.ceil(totalPatientsCount.value / itemsPerPage.value);
});

const fetchPatients = async () => {
  try {
    loading.value = true;
    const response = await api.get("/patients/", {
      params: {
        query: searchQuery.value,
        skip: (currentPage.value - 1) * itemsPerPage.value,
        limit: itemsPerPage.value,
      },
    });
    patients.value = response.data.items;
    totalPatientsCount.value = response.data.total_count;
    if (!specialtyStore.specialties.length) {
      await specialtyStore.fetchSpecialties();
    }
  } catch (err) {
    error.value = true;
    console.error("Error loading patients or specialties:", err);
  } finally {
    loading.value = false;
  }
};

const debouncedFetchPatients = debounce(fetchPatients, 300);

watch(searchQuery, () => {
  currentPage.value = 1;
  debouncedFetchPatients();
});

const changePage = (page) => {
  if (page >= 1 && page <= totalPages.value) {
    currentPage.value = page;
    fetchPatients();
  }
};

onMounted(() => {
  fetchPatients();
});

const visiblePages = computed(() => {
  const pages = [];
  const total = totalPages.value;
  const current = currentPage.value;
  if (total <= 7) {
    for (let i = 1; i <= total; i++) pages.push(i);
  } else {
    pages.push(1);
    if (current > 4) pages.push("...");
    const startShowing = Math.max(2, current - 1);
    const endShowing = Math.min(total - 1, current + 1);
    for (let i = startShowing; i <= endShowing; i++) {
      pages.push(i);
    }
    if (current < total - 3) pages.push("...");
    pages.push(total);
  }
  return pages;
});
</script>
