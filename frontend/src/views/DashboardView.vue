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
                <i-heroicons-calendar-days-20-solid
                  class="h-6 w-6 text-blue-500"
                />
              </div>
              <div class="ml-5 w-0 flex-1">
                <dl>
                  <dt class="text-sm font-medium text-blue-600 truncate">
                    {{ t("appointments_today") }}
                  </dt>
                  <dd class="text-2xl font-bold text-blue-900">
                    {{ appointments_today }}
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
                <i-heroicons-clock-20-solid class="h-6 w-6 text-green-500" />
              </div>
              <div class="ml-5 w-0 flex-1">
                <dl>
                  <dt class="text-sm font-medium text-green-600 truncate">
                    {{ t("appointments_this_week") }}
                  </dt>
                  <dd class="text-2xl font-bold text-green-900">
                    {{ appointments_this_week }}
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
            <!-- Month 1 -->
            <div>
              <DatePicker
                :key="locale"
                v-model="month1"
                month-picker
                :clearable="false"
                teleport="body"
                auto-apply
                :locale="locale"
                format="MMMM yyyy"
                class="mb-2"
              />
              <dl v-if="metrics1" class="space-y-2">
                <div
                  class="flex justify-between items-baseline p-2 bg-gray-100 rounded"
                >
                  <dt class="text-sm font-medium text-gray-500">
                    {{ t("expected_revenue") }}
                  </dt>
                  <dd class="text-md font-semibold text-gray-900">
                    {{ formatCurrency(metrics1.total_revenue) }}
                  </dd>
                </div>
                <div
                  class="flex justify-between items-baseline p-2 bg-gray-100 rounded"
                >
                  <dt class="text-sm font-medium text-gray-500">
                    {{ t("total_charged") }}
                  </dt>
                  <dd class="text-md font-semibold text-green-600">
                    {{ formatCurrency(metrics1.total_charged) }}
                  </dd>
                </div>
                <div
                  class="flex justify-between items-baseline p-2 bg-gray-100 rounded"
                >
                  <dt class="text-sm font-medium text-gray-500">
                    {{ t("total_due") }}
                  </dt>
                  <dd class="text-md font-semibold text-red-600">
                    {{ formatCurrency(metrics1.total_due) }}
                  </dd>
                </div>
              </dl>
            </div>
            <!-- Month 2 -->
            <div>
              <DatePicker
                :key="locale"
                v-model="month2"
                month-picker
                :clearable="false"
                teleport="body"
                auto-apply
                :locale="locale"
                format="MMMM yyyy"
                class="mb-2"
              />
              <dl v-if="metrics2" class="space-y-2">
                <div
                  class="flex justify-between items-baseline p-2 bg-gray-50 rounded"
                >
                  <dt class="text-sm font-medium text-gray-500">
                    {{ t("expected_revenue") }}
                  </dt>
                  <dd class="text-md font-semibold text-gray-900">
                    {{ formatCurrency(metrics2.total_revenue) }}
                  </dd>
                </div>
                <div
                  class="flex justify-between items-baseline p-2 bg-gray-50 rounded"
                >
                  <dt class="text-sm font-medium text-gray-500">
                    {{ t("total_charged") }}
                  </dt>
                  <dd class="text-md font-semibold text-green-600">
                    {{ formatCurrency(metrics2.total_charged) }}
                  </dd>
                </div>
                <div
                  class="flex justify-between items-baseline p-2 bg-gray-50 rounded"
                >
                  <dt class="text-sm font-medium text-gray-500">
                    {{ t("total_due") }}
                  </dt>
                  <dd class="text-md font-semibold text-red-600">
                    {{ formatCurrency(metrics2.total_due) }}
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
import { ref, onMounted, watch } from "vue";
import { useI18n } from "vue-i18n";
import metricsService from "../services/metricsService";
import DatePicker from "@vuepic/vue-datepicker";
import "@vuepic/vue-datepicker/dist/main.css";
import { startOfMonth, endOfMonth, subMonths, format } from "date-fns";

const { t, locale } = useI18n();
const loading = ref(true);
const error = ref(false);

const today = new Date();
const lastMonth = subMonths(today, 1);
const month1 = ref({
  month: lastMonth.getMonth(),
  year: lastMonth.getFullYear(),
});
const month2 = ref({
  month: today.getMonth(),
  year: today.getFullYear(),
});

const metrics1 = ref(null);
const metrics2 = ref(null);
const appointments_today = ref(0);
const appointments_this_week = ref(0);

const fetchFinancialMetrics = async (month, metricsRef) => {
  try {
    const startDate = startOfMonth(new Date(month.year, month.month));
    const endDate = endOfMonth(startDate);
    const response = await metricsService.getAppointmentMetrics(
      format(startDate, "yyyy-MM-dd"),
      format(endDate, "yyyy-MM-dd"),
    );
    metricsRef.value = response;
  } catch (err) {
    error.value = true;
    console.error(err);
  }
};

const fetchDashboardMetrics = async () => {
  try {
    const response = await metricsService.getDashboardMetrics();
    appointments_today.value = response.appointments_today;
    appointments_this_week.value = response.appointments_this_week;
  } catch (err) {
    error.value = true;
    console.error(err);
  }
};

watch(month1, (newMonth) => {
  fetchFinancialMetrics(newMonth, metrics1);
});

watch(month2, (newMonth) => {
  fetchFinancialMetrics(newMonth, metrics2);
});

const formatCurrency = (value) => {
  if (value === undefined || value === null) {
    return "$0.00";
  }
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
  }).format(value);
};

onMounted(async () => {
  loading.value = true;
  await Promise.all([
    fetchDashboardMetrics(),
    fetchFinancialMetrics(month1.value, metrics1),
    fetchFinancialMetrics(month2.value, metrics2),
  ]);
  loading.value = false;
});
</script>
