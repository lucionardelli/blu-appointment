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
              <dt class="text-sm font-medium text-gray-500">Payment</dt>
              <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                <div class="flex justify-between items-center">
                  <div>
                    <span :class="paymentStatus.color">
                      {{ paymentStatus.emoji }} {{ paymentStatus.text }}
                    </span>
                    <span class="ml-2">
                      {{ formatCurrency(appointment.total_paid) }} /
                      {{ formatCurrency(appointment.cost) }}
                      <span v-if="amountDue > 0" class="text-red-500">
                        (Due: {{ formatCurrency(amountDue) }})
                      </span>
                    </span>
                  </div>
                  <button
                    class="px-4 py-2 bg-primary text-white text-base font-medium rounded-md shadow-sm hover:bg-primary-dark focus:outline-none focus:ring-2 focus:ring-primary"
                    @click="showPaymentModal = true"
                  >
                    Record Payment
                  </button>
                </div>
              </dd>
            </div>
          </dl>
        </div>
      </div>
      <div class="mt-6 flex justify-between space-x-3">
        <div>
          <button
            class="px-4 py-2 text-sm font-medium text-white bg-red-600 border border-transparent rounded-md shadow-sm hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
            @click="cancelAppointment"
          >
            Cancel Appointment
          </button>
          <button
            class="ml-3 px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md shadow-sm hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary"
            @click="rescheduleAppointment"
          >
            Reschedule
          </button>
        </div>
        <button
          class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md shadow-sm hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary"
          @click="editAppointment"
        >
          Edit Appointment
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
import { ref, onMounted, computed } from "vue";
import { useRoute, useRouter } from "vue-router";
import api from "@/services/api";
import PaymentForm from "@/components/appointments/PaymentForm.vue";
import { formatCurrency } from "@/utils/formatDate";

const route = useRoute();
const router = useRouter();
const appointment = ref(null);
const patientCredit = ref(0);
const showPaymentModal = ref(false);

const amountDue = computed(() => {
  if (!appointment.value) return 0;
  return appointment.value.cost - appointment.value.total_paid;
});

const paymentStatus = computed(() => {
  if (!appointment.value) return {};
  const now = new Date();
  const appointmentDate = new Date(appointment.value.start_time);

  if (amountDue.value <= 0) {
    return { text: "Paid", color: "text-green-500", emoji: "✅" };
  }

  if (appointmentDate > now) {
    return { text: "Pending", color: "text-orange-500", emoji: "🟠" };
  } else {
    return { text: "Overdue", color: "text-red-500", emoji: "🔴" };
  }
});

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
    const response = await api.get(`/patients/${appointment.value.patient.id}`);
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
