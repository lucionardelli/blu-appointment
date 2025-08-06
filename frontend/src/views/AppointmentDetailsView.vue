<template>
  <div>
    <div v-if="appointment">
      <div class="bg-white shadow overflow-hidden sm:rounded-lg">
        <div class="px-4 py-5 sm:px-6">
          <h3 class="text-lg leading-6 font-medium text-gray-900">
            Appointment Details
          </h3>
        </div>
        <div class="border-t border-gray-200">
          <dl class="sm:divide-y sm:divide-gray-200">
            <div
              class="bg-gray-50 px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6"
            >
              <dt class="text-sm font-medium text-gray-500">Patient</dt>
              <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                {{ appointment.patient.name }}
              </dd>
            </div>
            <div
              class="bg-white px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6"
            >
              <dt class="text-sm font-medium text-gray-500">Specialty</dt>
              <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                {{ appointment.specialty.name }}
              </dd>
            </div>
            <div
              class="bg-gray-50 px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6"
            >
              <dt class="text-sm font-medium text-gray-500">Date & Time</dt>
              <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                {{ new Date(appointment.start_time).toLocaleString() }}
              </dd>
            </div>
            <div
              class="bg-white px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6"
            >
              <dt class="text-sm font-medium text-gray-500">Price</dt>
              <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                {{ appointment.price }}
              </dd>
            </div>
            <div
              class="bg-gray-50 px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6"
            >
              <dt class="text-sm font-medium text-gray-500">Amount Paid</dt>
              <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                {{ appointment.amount_paid }}
              </dd>
            </div>
            <div
              class="bg-white px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6"
            >
              <dt class="text-sm font-medium text-gray-500">Amount Due</dt>
              <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                {{ appointment.price - appointment.amount_paid }}
              </dd>
            </div>
            <div
              class="bg-gray-50 px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6"
            >
              <dt class="text-sm font-medium text-gray-500">Payment Status</dt>
              <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                {{ appointment.payment_status }}
              </dd>
            </div>
          </dl>
        </div>
      </div>
      <div class="mt-6 flex justify-end space-x-3">
        <button
          class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md shadow-sm hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary"
          @click="editAppointment"
        >
          Edit Appointment
        </button>
        <button
          class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md shadow-sm hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary"
          @click="rescheduleAppointment"
        >
          Reschedule Appointment
        </button>
        <button
          class="px-4 py-2 text-sm font-medium text-white bg-red-600 border border-transparent rounded-md shadow-sm hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
          @click="cancelAppointment"
        >
          Cancel Appointment
        </button>
        <button
          class="px-4 py-2 bg-primary text-white text-base font-medium rounded-md shadow-sm hover:bg-primary-dark focus:outline-none focus:ring-2 focus:ring-primary"
          @click="showPaymentModal = true"
        >
          Record Payment
        </button>
      </div>
    </div>
    <PaymentForm
      v-if="showPaymentModal"
      :appointment="appointment"
      :patient-credit="patientCredit"
      @close="showPaymentModal = false"
      @payment-saved="fetchAppointment"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import api from "@/services/api";
import PaymentForm from "@/components/appointments/PaymentForm.vue";

const route = useRoute();
const router = useRouter();
const appointment = ref(null);
const patientCredit = ref(0);
const showPaymentModal = ref(false);

const fetchAppointment = async () => {
  try {
    const response = await api.get(`/appointments/${route.params.id}`);
    appointment.value = response.data;
    fetchPatientCredit();
  } catch (error) {
    console.error("Error fetching appointment:", error);
  }
};

const fetchPatientCredit = async () => {
  try {
    const response = await api.get(`/patients/${appointment.value.patient_id}`);
    patientCredit.value = response.data.credit_balance || 0;
  } catch (error) {
    console.error("Error fetching patient credit:", error);
  }
};

const editAppointment = () => {
  router.push(`/appointments/${appointment.value.id}/edit`);
};

const rescheduleAppointment = () => {
  router.push(`/appointments/${appointment.value.id}/edit?reschedule=true`);
};

const cancelAppointment = async () => {
  if (confirm("Are you sure you want to cancel this appointment?")) {
    try {
      await api.put(`/appointments/${appointment.value.id}`, {
        ...appointment.value,
        cancelled: true,
      });
      fetchAppointment(); // Refresh data
    } catch (error) {
      console.error("Error cancelling appointment:", error);
    }
  }
};

onMounted(fetchAppointment);
</script>
