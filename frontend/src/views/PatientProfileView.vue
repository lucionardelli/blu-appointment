<template>
  <div>
    <div v-if="patient">
      <div class="bg-white shadow overflow-hidden sm:rounded-lg">
        <div class="px-4 py-5 sm:px-6 flex justify-between items-center">
          <div>
            <h3 class="text-lg leading-6 font-medium text-gray-900">
              Patient Profile
            </h3>
            <p class="mt-1 max-w-2xl text-sm text-gray-500">
              Personal details and appointment history.
            </p>
          </div>
          <router-link
            :to="`/patients/${patient.id}/edit`"
            class="px-4 py-2 text-sm font-medium text-white bg-primary border border-transparent rounded-md shadow-sm hover:bg-primary-dark focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary"
            >Edit</router-link
          >
        </div>
        <div class="border-t border-gray-200">
          <dl class="sm:divide-y sm:divide-gray-200">
            <div
              class="bg-gray-50 px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6"
            >
              <dt class="text-sm font-medium text-gray-500">Full name</dt>
              <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                {{ patient.name }}
              </dd>
            </div>
            <div
              class="bg-white px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6"
            >
              <dt class="text-sm font-medium text-gray-500">Date of Birth</dt>
              <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                {{ patient.dob }}
              </dd>
            </div>
            <div
              class="bg-gray-50 px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6"
            >
              <dt class="text-sm font-medium text-gray-500">Email address</dt>
              <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                {{ patient.email }}
              </dd>
            </div>
            <div
              class="bg-white px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6"
            >
              <dt class="text-sm font-medium text-gray-500">Phone Number</dt>
              <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                {{ patient.phone }}
              </dd>
            </div>
            <div
              class="bg-gray-50 px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6"
            >
              <dt class="text-sm font-medium text-gray-500">Cell Phone</dt>
              <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                {{ patient.cellphone }}
              </dd>
            </div>
            <div
              class="bg-white px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6"
            >
              <dt class="text-sm font-medium text-gray-500">Address</dt>
              <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                {{ patient.address }}
              </dd>
            </div>
            <div
              class="bg-gray-50 px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6"
            >
              <dt class="text-sm font-medium text-gray-500">Medical History</dt>
              <dd
                class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2"
                v-html="renderedMedicalHistory"
              ></dd>
            </div>
          </dl>
        </div>
      </div>

      <div class="mt-8 bg-white shadow overflow-hidden sm:rounded-lg">
        <div class="px-4 py-5 sm:px-6">
          <h3 class="text-lg leading-6 font-medium text-gray-900">
            Financial Summary
          </h3>
        </div>
        <div class="border-t border-gray-200 px-4 py-5 sm:p-0">
          <dl class="sm:divide-y sm:divide-gray-200">
            <div class="sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6 sm:py-5">
              <dt class="text-sm font-medium text-gray-500">Total Paid</dt>
              <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                {{ financialSummary.totalPaid }}
              </dd>
            </div>
            <div class="sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6 sm:py-5">
              <dt class="text-sm font-medium text-gray-500">Total Due</dt>
              <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                {{ financialSummary.totalDue }}
              </dd>
            </div>
            <div class="sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6 sm:py-5">
              <dt class="text-sm font-medium text-gray-500">Balance</dt>
              <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                {{ financialSummary.balance }}
              </dd>
            </div>
          </dl>
        </div>
      </div>

      <div class="mt-8 bg-white shadow overflow-hidden sm:rounded-lg">
        <div class="px-4 py-5 sm:px-6">
          <h3 class="text-lg leading-6 font-medium text-gray-900">
            Appointment History
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
                  Date
                </th>
                <th
                  scope="col"
                  class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                >
                  Specialty
                </th>
                <th
                  scope="col"
                  class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                >
                  Price
                </th>
                <th
                  scope="col"
                  class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                >
                  Amount Paid
                </th>
                <th
                  scope="col"
                  class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                >
                  Amount Due
                </th>
                <th
                  scope="col"
                  class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                >
                  Payment Status
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
                  {{ formatCurrency(appointment.price) }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {{ formatCurrency(appointment.amount_paid) }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {{
                    formatCurrency(appointment.price - appointment.amount_paid)
                  }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {{ appointment.payment_status }}
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import { useRoute } from "vue-router";
import api from "@/services/api";
import MarkdownIt from "markdown-it";
import { formatDate, formatCurrency, formatTime } from "@/utils/formatDate";

const route = useRoute();
const patient = ref(null);
const appointments = ref([]);
const showCancelledAppointments = ref(false);
const md = new MarkdownIt();

const renderedMedicalHistory = computed(() => {
  if (patient.value && patient.value.medical_history) {
    return md.render(patient.value.medical_history);
  }
  return "";
});

const financialSummary = computed(() => {
  const totalPaid = appointments.value.reduce(
    (acc, appointment) => acc + appointment.amount_paid,
    0,
  );
  const totalDue = appointments.value.reduce(
    (acc, appointment) => acc + (appointment.price - appointment.amount_paid),
    0,
  );
  const balance = totalPaid - totalDue;
  return { totalPaid, totalDue, balance };
});

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
