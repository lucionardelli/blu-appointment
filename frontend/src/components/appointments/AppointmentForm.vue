<template>
  <div>
    <h1 class="text-2xl font-semibold text-gray-900">
      {{ isNew ? t("new_appointment") : t("edit_appointment") }}
    </h1>

    <div v-if="!isNew" class="mt-4 border-b border-gray-200">
      <nav class="-mb-px flex space-x-8" aria-label="Tabs">
        <button
          :class="[
            activeTab === 'details'
              ? 'border-primary text-primary'
              : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300',
            'whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm',
          ]"
          @click="activeTab = 'details'"
        >
          {{ t("appointment_details") }}
        </button>
        <button
          :class="[
            activeTab === 'payments'
              ? 'border-primary text-primary'
              : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300',
            'whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm',
          ]"
          @click="activeTab = 'payments'"
        >
          {{ t("payments") }}
        </button>
      </nav>
    </div>

    <div v-show="activeTab === 'details'" class="mt-6">
      <form @submit.prevent="saveAppointment">
        <div class="space-y-6">
          <div>
            <label
              for="patient"
              class="block text-sm font-medium text-gray-700"
              >{{ t("patient") }}</label
            >
            <select
              id="patient"
              v-model="appointment.patient_id"
              required
              class="block w-full px-3 py-2 mt-1 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary sm:text-sm"
              @change="fetchPatientSnippet"
            >
              <option
                v-for="patient in patients"
                :key="patient.id"
                :value="patient.id"
              >
                {{ patient.name }}
              </option>
            </select>
            <div
              v-if="patientSnippet"
              class="mt-2 p-4 bg-gray-100 rounded-md sm:flex sm:justify-between"
            >
              <div class="flex items-baseline">
                <h4 class="text-sm font-medium text-gray-900">
                  {{ patientSnippet.name }}
                </h4>
                <p class="ml-2 text-xs text-gray-600">
                  ({{ patientSnippet.nickname }})
                </p>
              </div>
              <p class="text-sm text-gray-500">
                {{ t("dob") }}: {{ formatDate(patientSnippet.dob) }}
                <span
                  :class="{
                    'text-red-500 font-semibold': patientSnippet.is_underage,
                  }"
                  >({{ patientSnippet.age }})</span
                >
              </p>
              <p class="text-sm text-gray-500">
                {{ t("last_appointment") }}:
                {{ formatDate(patientSnippet.last_appointment_date) || "N/A" }}
              </p>
              <p class="text-sm text-gray-500">
                {{ t("total_due") }}:
                {{ formatCurrency(patientSnippet.total_due || 0) }}
              </p>
            </div>
          </div>
          <div class="grid grid-cols-2 gap-6">
            <div>
              <label
                for="specialty"
                class="block text-sm font-medium text-gray-700"
                >{{ t("specialty") }}</label
              >
              <select
                id="specialty"
                v-model="appointment.specialty_id"
                required
                class="block w-full px-3 py-2 mt-1 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary sm:text-sm"
              >
                <option
                  v-for="specialty in specialties"
                  :key="specialty.id"
                  :value="specialty.id"
                >
                  {{ specialty.name }}
                </option>
              </select>
            </div>
            <div>
              <label
                for="price"
                class="block text-sm font-medium text-gray-700"
                >{{ t("price") }}</label
              >
              <input
                id="price"
                v-model="appointment.cost"
                type="number"
                step="500"
                required
                class="block w-full px-3 py-2 mt-1 placeholder-gray-400 border border-gray-300 rounded-md shadow-sm appearance-none focus:outline-none focus:ring-primary focus:border-primary sm:text-sm"
              />
            </div>
          </div>
          <div class="grid grid-cols-2 gap-6">
            <div>
              <label
                for="start_time"
                class="block text-sm font-medium text-gray-700"
                >{{ t("start_time") }}</label
              >
              <input
                id="start_time"
                v-model="appointment.start_time"
                type="datetime-local"
                required
                step="900"
                :min="currentDateTime"
                class="block w-full px-3 py-2 mt-1 placeholder-gray-400 border border-gray-300 rounded-md shadow-sm appearance-none focus:outline-none focus:ring-primary focus:border-primary sm:text-sm"
                @change="checkAvailability"
              />
              <p
                v-if="doubleBookingWarning"
                class="mt-2 text-sm text-yellow-600"
              >
                {{ doubleBookingWarning }}
              </p>
              <p
                v-if="outsideWorkingHoursWarning"
                class="mt-2 text-sm text-yellow-600"
              >
                {{ outsideWorkingHoursWarning }}
              </p>
            </div>
            <div>
              <label
                for="end_time"
                class="block text-sm font-medium text-gray-700"
                >{{ t("end_time") }}</label
              >
              <input
                id="end_time"
                v-model="appointment.end_time"
                type="datetime-local"
                required
                step="900"
                class="block w-full px-3 py-2 mt-1 placeholder-gray-400 border border-gray-300 rounded-md shadow-sm appearance-none focus:outline-none focus:ring-primary focus:border-primary sm:text-sm"
              />
            </div>
          </div>
        </div>
        <div class="flex justify-end mt-6">
          <button
            v-if="!props.inModal"
            type="button"
            class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md shadow-sm hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary"
            @click="router.push('/appointments')"
          >
            {{ t("cancel") }}
          </button>
          <button
            type="submit"
            class="px-4 py-2 ml-3 text-sm font-medium text-white bg-primary border border-transparent rounded-md shadow-sm hover:bg-primary-dark focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary"
          >
            {{ t("save") }}
          </button>
        </div>
      </form>
    </div>

    <div v-if="!isNew && activeTab === 'payments'" class="mt-6">
      <div class="flex justify-between items-center mb-4">
        <div class="flex items-center">
          <button
            v-if="showPaymentForm"
            class="mr-2 p-1 rounded-full hover:bg-gray-200"
            @click="showPaymentForm = false"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="h-6 w-6 text-gray-500"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M10 19l-7-7m0 0l7-7m-7 7h18"
              />
            </svg>
          </button>
          <h2 class="text-xl font-semibold text-gray-800">
            <span v-if="showPaymentForm">
              {{ t("payments") }} > {{ t("new_payment") }}
            </span>
            <span v-else>{{ t("payments") }}</span>
          </h2>
        </div>
        <button
          v-if="!showPaymentForm"
          class="px-4 py-2 text-sm font-medium text-white bg-primary border border-transparent rounded-md shadow-sm hover:bg-primary-dark focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary"
          @click="showPaymentForm = true"
        >
          {{ t("add_payment") }}
        </button>
      </div>

      <PaymentForm
        v-if="showPaymentForm"
        :appointment-id="props.appointmentId"
        :appointment="appointment"
        @save="handlePaymentSave"
        @cancel="showPaymentForm = false"
      />

      <div v-else>
        <table
          v-if="payments.length"
          class="min-w-full divide-y divide-gray-200"
        >
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
                {{ t("payment_method") }}
              </th>
              <th
                scope="col"
                class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider"
              >
                {{ t("amount") }}
              </th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="payment in payments" :key="payment.id">
              <td
                class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900"
              >
                {{ formatDate(payment.payment_date) }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {{ payment.method }}
              </td>
              <td
                class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 text-right"
              >
                {{ formatCurrency(payment.amount) }}
              </td>
            </tr>
          </tbody>
          <tfoot class="bg-gray-50">
            <tr>
              <td
                colspan="2"
                class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
              >
                {{ t("total_paid") }}
              </td>
              <td
                :class="paymentStatus.color"
                class="px-6 py-3 whitespace-nowrap text-sm font-semibold text-right"
              >
                {{ formatCurrency(appointment.total_paid) }} /
                {{ formatCurrency(appointment.cost) }}
                <span v-if="amountDue > 0" class="ml-2">
                  ({{ t("due") }}: {{ formatCurrency(amountDue) }})
                </span>
              </td>
            </tr>
          </tfoot>
        </table>
        <p v-else class="text-center text-gray-500 py-4">
          {{ t("no_payments_found") }}
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from "vue";
import { useI18n } from "vue-i18n";
import { useRouter } from "vue-router";
import api from "@/services/api";
import { format, addMinutes } from "date-fns";
import { formatDate, formatCurrency } from "@/utils/formatDate";
import PaymentForm from "./PaymentForm.vue";

const { t } = useI18n();

const props = defineProps({
  inModal: {
    type: Boolean,
    default: false,
  },
  initialDate: {
    type: String,
    default: "",
  },
  initialEndDate: {
    type: String,
    default: "",
  },
  appointmentId: {
    type: [String, Number],
    default: null,
  },
});

const emit = defineEmits(["save", "cancel"]);

const router = useRouter();
const appointment = ref({
  patient_id: null,
  specialty_id: null,
  start_time: "",
  end_time: "",
  cost: 0,
  total_paid: 0,
});
const patients = ref([]);
const specialties = ref([]);
const patientSnippet = ref(null);
const doubleBookingWarning = ref(null);
const outsideWorkingHoursWarning = ref(null);
const endTimeWarning = ref(null);
const workingHours = ref({ start: "09:00", end: "18:00" }); // Placeholder
const currentDateTime = ref(new Date());
const activeTab = ref("details");
const payments = ref([]);
const showPaymentForm = ref(false);

const isNew = computed(() => !props.appointmentId);

const amountDue = computed(() => {
  if (!appointment.value) {
    return 0;
  }
  return appointment.value.cost - appointment.value.total_paid;
});

const paymentStatus = computed(() => {
  if (!appointment.value) {
    return { color: "text-black" };
  }
  const now = new Date();
  const appointmentDate = new Date(appointment.value.start_time);

  if (amountDue.value <= 0) {
    return { color: "text-green-600" };
  }
  if (appointmentDate > now) {
    return { color: "text-black" };
  }
  return { color: "text-red-600" };
});

const fetchAppointment = async () => {
  if (isNew.value) return;
  try {
    const response = await api.get(`/appointments/${props.appointmentId}`);
    const fetchedAppointment = response.data;

    // Flatten nested patient and specialty objects
    appointment.value = {
      ...fetchedAppointment,
      patient_id: fetchedAppointment.patient?.id,
      specialty_id: fetchedAppointment.specialty?.id,
    };

    if (appointment.value.start_time) {
      appointment.value.start_time = format(
        new Date(appointment.value.start_time),
        "yyyy-MM-dd'T'HH:mm",
      );
    }
    if (appointment.value.end_time) {
      appointment.value.end_time = format(
        new Date(appointment.value.end_time),
        "yyyy-MM-dd'T'HH:mm",
      );
    }
  } catch (error) {
    console.error("Error fetching appointment:", error);
  }
};

const fetchPatients = async () => {
  try {
    const response = await api.get("/patients");
    patients.value = response.data;
  } catch (error) {
    console.error("Error fetching patients:", error);
  }
};

const fetchSpecialties = async () => {
  try {
    const response = await api.get("/specialties");
    specialties.value = response.data;
  } catch (error) {
    console.error("Error fetching specialties:", error);
  }
};

const fetchPayments = async () => {
  if (isNew.value) return;
  try {
    const response = await api.get(
      `/appointments/${props.appointmentId}/payments`,
    );
    payments.value = response.data.sort(
      (a, b) => new Date(b.payment_date) - new Date(a.payment_date),
    );
  } catch (error) {
    console.error("Error fetching payments:", error);
  }
};

const handlePaymentSave = () => {
  showPaymentForm.value = false;
  fetchPayments();
  fetchAppointment(); // Refetch appointment to update total_paid
};

watch(
  () => appointment.value.patient_id,
  (newPatientId) => {
    if (newPatientId) {
      fetchPatientSnippet();
      const selectedPatient = patients.value.find((p) => p.id === newPatientId);
      if (selectedPatient && selectedPatient.default_specialty_id) {
        appointment.value.specialty_id = selectedPatient.default_specialty_id;
      }
    }
  },
);

watch(
  () => appointment.value.specialty_id,
  (newVal) => {
    if (newVal) {
      const selectedSpecialty = specialties.value.find((s) => s.id === newVal);
      if (selectedSpecialty) {
        appointment.value.cost = selectedSpecialty.current_price;
        if (
          appointment.value.start_time &&
          selectedSpecialty.default_duration
        ) {
          const startTime = new Date(appointment.value.start_time);
          const endTime = addMinutes(
            startTime,
            selectedSpecialty.default_duration,
          );
          appointment.value.end_time = format(endTime, "yyyy-MM-dd'T'HH:mm");
        }
      }
    }
  },
);

watch(
  () => appointment.value.start_time,
  (newVal) => {
    if (newVal) {
      const parsedStartTime = new Date(newVal);
      if (appointment.value.specialty_id) {
        const selectedSpecialty = specialties.value.find(
          (s) => s.id === appointment.value.specialty_id,
        );
        if (selectedSpecialty && selectedSpecialty.default_duration) {
          const endTime = addMinutes(
            parsedStartTime,
            selectedSpecialty.default_duration,
          );
          appointment.value.end_time = format(endTime, "yyyy-MM-dd'T'HH:mm");
        }
      }
    }
  },
);

watch(
  () => appointment.value.end_time,
  (newVal) => {
    endTimeWarning.value = null;
    if (newVal && appointment.value.start_time) {
      const parsedStartTime = new Date(appointment.value.start_time);
      const parsedEndTime = new Date(newVal);
      if (
        parsedStartTime === "Invalid Date" ||
        parsedEndTime === "Invalid Date"
      ) {
        endTimeWarning.value = "Please enter valid start and end times.";
      }
      if (parsedEndTime <= parsedStartTime) {
        endTimeWarning.value = "End time must be after start time.";
      }
    }
  },
);

const fetchPatientSnippet = async () => {
  if (!appointment.value.patient_id) {
    patientSnippet.value = null;
    return;
  }
  try {
    const response = await api.get(`/patients/${appointment.value.patient_id}`);
    patientSnippet.value = response.data;
  } catch (error) {
    console.error("Error fetching patient snippet:", error);
  }
};

const checkAvailability = async () => {
  doubleBookingWarning.value = null;
  outsideWorkingHoursWarning.value = null;

  const start = new Date(appointment.value.start_time);
  const startTime = `${start.getHours().toString().padStart(2, "0")}:${start.getMinutes().toString().padStart(2, "0")}`;

  // Check for double booking
  try {
    const response = await api.get("/appointments");
    const existingAppointments = response.data;
    const isDoubleBooked = existingAppointments.some((other) => {
      if (other.id === appointment.value.id) return false;
      const otherStart = new Date(other.start_time);
      const otherEnd = new Date(other.end_time);
      return start >= otherStart && start < otherEnd;
    });
    if (isDoubleBooked) {
      doubleBookingWarning.value =
        "Warning: Another appointment is already scheduled at this time.";
    }
  } catch (error) {
    console.error("Error checking for double booking:", error);
  }

  // Check for outside working hours
  if (
    startTime < workingHours.value.start ||
    startTime > workingHours.value.end
  ) {
    outsideWorkingHoursWarning.value =
      "Warning: This appointment is outside working hours.";
  }
};

onMounted(async () => {
  await fetchPatients();
  await fetchSpecialties();

  if (props.appointmentId) {
    await fetchAppointment();
    await fetchPayments();
    if (appointment.value.patient_id) {
      await fetchPatientSnippet();
    }
  } else if (props.initialDate) {
    const startDate = new Date(props.initialDate);
    appointment.value.start_time = format(startDate, "yyyy-MM-dd'T'HH:mm");
    const endDate = props.initialEndDate
      ? new Date(props.initialEndDate)
      : addMinutes(startDate, 30);
    appointment.value.end_time = format(endDate, "yyyy-MM-dd'T'HH:mm");
  }
});

const saveAppointment = async () => {
  // Client-side validation
  const start = new Date(appointment.value.start_time);
  const end = new Date(appointment.value.end_time);
  const now = new Date();

  // 1. Start time not in the past
  if (start < now && isNew.value) {
    alert("Start time cannot be in the past for new appointments.");
    return;
  }

  // 2. End time must be after start time (already handled by watch, but good to have a final check)
  if (end <= start) {
    alert("End time must be after start time.");
    return;
  }

  // 3. End time should be in the same day (don't allow for start time to be after 23:45)
  if (start.toDateString() !== end.toDateString()) {
    alert("Appointment must end on the same day it starts.");
    return;
  }

  if (
    start.getHours() > 23 ||
    (start.getHours() === 23 && start.getMinutes() > 45)
  ) {
    alert(
      "Start time cannot be after 23:45 to ensure end time is on the same day.",
    );
    return;
  }

  try {
    if (isNew.value) {
      await api.post("/appointments", appointment.value);
    } else {
      await api.put(`/appointments/${props.appointmentId}`, {
        ...appointment.value,
        cost: appointment.value.cost,
      });
    }
    if (props.inModal) {
      emit("save");
    } else {
      router.push("/appointments");
    }
  } catch (error) {
    console.error("Error saving appointment:", error);
  }
};
</script>
