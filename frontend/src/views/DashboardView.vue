<template>
  <div class="p-4 sm:p-6 lg:p-8">
    <div v-if="loading" class="text-center">
      <p>{{ t("dashboard_loading") }}</p>
    </div>
    <div v-else-if="error" class="text-center text-red-500">
      <p>{{ t("dashboard_error") }}</p>
    </div>
    <div v-else class="space-y-4">
      <!-- Appointments Row -->
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <!-- Appointments Today -->
        <div class="bg-blue-100 overflow-hidden shadow rounded-lg">
          <div class="p-5">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <svg
                  class="h-6 w-6 text-blue-500"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"
                  />
                </svg>
              </div>
              <div class="ml-5 w-0 flex-1">
                <dl>
                  <dt class="text-sm font-medium text-blue-600 truncate">
                    {{ t("appointments_today") }}
                  </dt>
                  <dd class="text-2xl font-bold text-blue-900">
                    {{ metrics.appointments_today }}
                  </dd>
                </dl>
              </div>
            </div>
          </div>
        </div>

        <!-- Appointments This Week -->
        <div class="bg-green-100 overflow-hidden shadow rounded-lg">
          <div class="p-5">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <svg
                  class="h-6 w-6 text-green-500"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"
                  />
                </svg>
              </div>
              <div class="ml-5 w-0 flex-1">
                <dl>
                  <dt class="text-sm font-medium text-green-600 truncate">
                    {{ t("appointments_this_week") }}
                  </dt>
                  <dd class="text-2xl font-bold text-green-900">
                    {{ metrics.appointments_this_week }}
                  </dd>
                </dl>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Financials Card -->
      <div class="bg-white overflow-hidden shadow rounded-lg">
        <div class="p-5">
          <h3 class="text-lg font-medium text-gray-900 mb-4">
            {{ t("financial_overview") }}
          </h3>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <!-- Last Month -->
            <div>
              <h4 class="text-md font-semibold text-gray-700 mb-2">
                {{ t("last_month") }}
              </h4>
              <dl class="space-y-2">
                <div
                  class="flex justify-between items-baseline p-2 bg-gray-100 rounded"
                >
                  <dt class="text-sm font-medium text-gray-500">
                    {{ t("expected_revenue") }}
                  </dt>
                  <dd class="text-md font-semibold text-gray-900">
                    {{ formatCurrency(metrics.expected_revenue_last_month) }}
                  </dd>
                </div>
                <div
                  class="flex justify-between items-baseline p-2 bg-gray-100 rounded"
                >
                  <dt class="text-sm font-medium text-gray-500">
                    {{ t("total_charged") }}
                  </dt>
                  <dd class="text-md font-semibold text-green-600">
                    {{ formatCurrency(metrics.total_charged_last_month) }}
                  </dd>
                </div>
                <div
                  class="flex justify-between items-baseline p-2 bg-gray-100 rounded"
                >
                  <dt class="text-sm font-medium text-gray-500">
                    {{ t("total_due") }}
                  </dt>
                  <dd class="text-md font-semibold text-red-600">
                    {{ formatCurrency(metrics.total_due_last_month) }}
                  </dd>
                </div>
              </dl>
            </div>
            <!-- This Month -->
            <div>
              <h4 class="text-md font-semibold text-gray-700 mb-2">
                {{ t("this_month") }}
              </h4>
              <dl class="space-y-2">
                <div
                  class="flex justify-between items-baseline p-2 bg-gray-50 rounded"
                >
                  <dt class="text-sm font-medium text-gray-500">
                    {{ t("expected_revenue") }}
                  </dt>
                  <dd class="text-md font-semibold text-gray-900">
                    {{ formatCurrency(metrics.expected_revenue_this_month) }}
                  </dd>
                </div>
                <div
                  class="flex justify-between items-baseline p-2 bg-gray-50 rounded"
                >
                  <dt class="text-sm font-medium text-gray-500">
                    {{ t("total_charged") }}
                  </dt>
                  <dd class="text-md font-semibold text-green-600">
                    {{ formatCurrency(metrics.total_charged_this_month) }}
                  </dd>
                </div>
                <div
                  class="flex justify-between items-baseline p-2 bg-gray-50 rounded"
                >
                  <dt class="text-sm font-medium text-gray-500">
                    {{ t("total_due") }}
                  </dt>
                  <dd class="text-md font-semibold text-red-600">
                    {{ formatCurrency(metrics.total_due_this_month) }}
                  </dd>
                </div>
              </dl>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useI18n } from "vue-i18n";
import metricsService from "../services/metricsService";

const { t } = useI18n();
const metrics = ref({});
const loading = ref(true);
const error = ref(false);

const fetchMetrics = async () => {
  try {
    loading.value = true;
    const response = await metricsService.getDashboardMetrics();
    metrics.value = response;
  } catch (err) {
    error.value = true;
    console.error(err);
  } finally {
    loading.value = false;
  }
};

const formatCurrency = (value) => {
  if (value === undefined || value === null) {
    return "$0.00";
  }
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
  }).format(value);
};

onMounted(() => {
  fetchMetrics();
});
</script>
