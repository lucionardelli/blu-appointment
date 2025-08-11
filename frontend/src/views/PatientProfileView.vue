<template>
  <div>
    <div v-if="patient">
      <div class="bg-white shadow overflow-hidden sm:rounded-lg">
        <div class="px-4 py-5 sm:px-6 flex justify-between items-center">
          <div>
            <h3 class="text-lg leading-6 font-medium text-gray-900">
              {{ t("patient_profile") }}
            </h3>
            <p class="mt-1 max-w-2xl text-sm text-gray-500">
              {{ t("personal_details_and_appointment_history") }}
            </p>
          </div>
          <router-link
            :to="`/patients/${patient.id}/edit`"
            class="px-4 py-2 text-sm font-medium text-white bg-primary border border-transparent rounded-md shadow-sm hover:bg-primary-dark focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary"
            >{{ t("edit") }}</router-link
          >
        </div>
        <div class="border-t border-gray-200">
          <dl class="sm:divide-y sm:divide-gray-200">
            <div
              class="bg-gray-50 px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6"
            >
              <dt class="text-sm font-medium text-gray-500">
                {{ t("full_name") }}
              </dt>
              <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                {{ patient.name }}
                <span v-if="patient.nickname">({{ patient.nickname }})</span>
              </dd>
            </div>
            <div
              class="bg-gray-50 px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6"
            >
              <dt class="text-sm font-medium text-gray-500">
                {{ t("date_of_birth") }}
              </dt>
              <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                {{ patient.dob }}
              </dd>
            </div>
            <div
              class="bg-gray-50 px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6"
            >
              <dt class="text-sm font-medium text-gray-500">
                {{ t("email_address") }}
              </dt>
              <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                {{ patient.email }}
              </dd>
            </div>
            <div
              class="bg-white px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6"
            >
              <dt class="text-sm font-medium text-gray-500">
                {{ t("phone_number") }}
              </dt>
              <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                <div class="grid grid-cols-2 gap-4">
                  <div>
                    <span class="font-medium">{{ t("cell_phone") }}:</span>
                    {{ patient.cellphone || "N/A" }}
                  </div>
                  <div>
                    <span class="font-medium">{{ t("phone_number") }}:</span>
                    {{ patient.phone || "N/A" }}
                  </div>
                </div>
              </dd>
            </div>
            <div
              class="bg-white px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6"
            >
              <dt class="text-sm font-medium text-gray-500">
                {{ t("address") }}
              </dt>
              <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                {{ patient.address }}
              </dd>
            </div>
          </dl>
        </div>
      </div>

      <div
        v-if="patient.financialSummary"
        class="mt-8 bg-white shadow overflow-hidden sm:rounded-lg"
      >
        <div class="px-4 py-5 sm:px-6">
          <h3 class="text-lg leading-6 font-medium text-gray-900">
            {{ t("financial_summary") }}
          </h3>
        </div>
        <div class="border-t border-gray-200 px-4 py-5 sm:p-0">
          <dl class="sm:divide-y sm:divide-gray-200">
            <div class="sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6 sm:py-5">
              <dt class="text-sm font-medium text-gray-500">
                {{ t("total_paid") }}
              </dt>
              <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                {{ patient.financialSummary.total_paid }}
              </dd>
            </div>
            <div class="sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6 sm:py-5">
              <dt class="text-sm font-medium text-gray-500">
                {{ t("total_due") }}
              </dt>
              <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                {{ patient.financialSummary.total_due }}
              </dd>
            </div>
            <div class="sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6 sm:py-5">
              <dt class="text-sm font-medium text-gray-500">
                {{ t("balance") }}
              </dt>
              <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                {{ patient.financialSummary.balance }}
              </dd>
            </div>
          </dl>
        </div>
      </div>

      <div class="mt-8 bg-white shadow overflow-hidden sm:rounded-lg">
        <div class="px-4 py-5 sm:px-6">
          <nav class="-mb-px flex space-x-8" aria-label="Tabs">
            <button
              :class="[
                activeTab === 'appointments'
                  ? 'border-primary text-primary'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300',
                'whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm',
              ]"
              @click="activeTab = 'appointments'"
            >
              {{ t("appointment_history") }}
            </button>
            <button
              :class="[
                activeTab === 'medical_history'
                  ? 'border-primary text-primary'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300',
                'whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm',
              ]"
              @click="activeTab = 'medical_history'"
            >
              {{ t("medical_history") }}
            </button>
          </nav>
        </div>

        <div
          v-show="activeTab === 'appointments'"
          class="border-t border-gray-200"
        >
          <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
              <tr>
                <th
                  scope="col"
                  class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                >
                  {{ t("date") }}
                </th>
                <th
                  scope="col"
                  class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                >
                  {{ t("specialty") }}
                </th>
                <th
                  scope="col"
                  class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                >
                  {{ t("payment") }}
                </th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <tr
                v-for="appointment in filteredAppointments"
                :key="appointment.id"
                :class="{ 'line-through text-gray-500': appointment.cancelled }"
              >
                <td
                  class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900"
                >
                  {{ formatDate(appointment.start_time) }}
                  {{ formatTime(appointment.start_time) }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {{ appointment.specialty.name }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  <span :class="getPaymentStatus(appointment).color">
                    {{ getPaymentStatus(appointment).emoji }}
                    {{ getPaymentStatus(appointment).text }}
                  </span>
                  <span
                    v-if="appointment.cost - appointment.total_paid > 0"
                    class="ml-2"
                  >
                    {{ formatCurrency(appointment.total_paid) }} /
                    {{ formatCurrency(appointment.cost) }}
                    <span :class="getPaymentStatus(appointment).color">
                      ({{ t("due") }}:
                      {{
                        formatCurrency(
                          appointment.cost - appointment.total_paid,
                        )
                      }})
                    </span>
                  </span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        <div
          v-show="activeTab === 'medical_history'"
          class="border-t border-gray-200 px-4 py-5 sm:p-0"
        >
          <div class="px-4 py-5 sm:px-6">
            <!-- eslint-disable-next-line vue/no-v-html -->
            <div
              class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2 prose max-w-none"
              v-html="renderedMedicalHistory"
            ></div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import { useI18n } from "vue-i18n";
import { useRoute } from "vue-router";
import api from "@/services/api";
import MarkdownIt from "markdown-it";
import DOMPurify from "dompurify";
import { formatDate, formatCurrency, formatTime } from "@/utils/formatDate";

const { t } = useI18n();
const route = useRoute();
const patient = ref(null);
const appointments = ref([]);
const showCancelledAppointments = ref(false);
const md = new MarkdownIt();
const activeTab = ref("appointments");

const renderedMedicalHistory = computed(() => {
  if (patient.value && patient.value.medical_history) {
    return DOMPurify.sanitize(md.render(patient.value.medical_history));
  }
  return "";
});

const getPaymentStatus = (appointment) => {
  const now = new Date();
  const appointmentDate = new Date(appointment.start_time);
  const amountDue = appointment.cost - appointment.total_paid;

  if (amountDue <= 0) {
    return { text: t("paid"), color: "text-green-500", emoji: "✅" };
  }

  if (appointmentDate > now) {
    return { text: t("pending"), color: "text-balck-500", emoji: "" };
  } else {
    return { text: t("overdue"), color: "text-red-500", emoji: "🔴" };
  }
};

const filteredAppointments = computed(() => {
  if (showCancelledAppointments.value) {
    return appointments.value;
  } else {
    return appointments.value.filter((app) => !app.cancelled);
  }
});

const fetchPatient = async () => {
  try {
    const response = await api.get(`/patients/${route.params.id}`);
    patient.value = response.data;
  } catch (error) {
    console.error("Error fetching patient:", error);
  }
};

const fetchAppointments = async () => {
  try {
    const response = await api.get(`/patients/${route.params.id}/appointments`);
    appointments.value = response.data;
  } catch (error) {
    console.error("Error fetching appointments:", error);
  }
};

onMounted(() => {
  fetchPatient();
  fetchAppointments();
});
</script>
