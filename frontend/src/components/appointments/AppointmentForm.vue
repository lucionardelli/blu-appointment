<template>
  <div>
    <h1 class="text-2xl font-semibold text-gray-900">
      {{ isNew ? "New Appointment" : "Edit Appointment" }}
    </h1>
    <form class="mt-6" @submit.prevent="saveAppointment">
      <div class="space-y-6">
        <div>
          <label for="patient" class="block text-sm font-medium text-gray-700"
            >Patient</label
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
            <h4 class="text-sm font-medium text-gray-900">
              {{ patientSnippet.name }}
            </h4>
            <p class="text-sm text-gray-500">
              DOB: {{ formatDate(patientSnippet.dob) }}
            </p>
            <p class="text-sm text-gray-500">
              Last Appointment:
              {{ formatDate(patientSnippet.last_appointment_date) || "N/A" }}
            </p>
            <p class="text-sm text-gray-500">
              Total Due: {{ formatCurrency(patientSnippet.total_due || 0) }}
            </p>
          </div>
        </div>
        <div class="grid grid-cols-2 gap-6">
          <div>
            <label
              for="specialty"
              class="block text-sm font-medium text-gray-700"
              >Specialty</label
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
            <label for="price" class="block text-sm font-medium text-gray-700"
              >Price</label
            >
            <input
              id="price"
              v-model="appointment.price"
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
              >Start Time</label
            >
            <input
              id="start_time"
              v-model="appointment.start_time"
              type="datetime-local"
              required
              step="900"
              class="block w-full px-3 py-2 mt-1 placeholder-gray-400 border border-gray-300 rounded-md shadow-sm appearance-none focus:outline-none focus:ring-primary focus:border-primary sm:text-sm"
              @change="checkAvailability"
            />
            <p v-if="doubleBookingWarning" class="mt-2 text-sm text-yellow-600">
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
              >End Time</label
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
        <router-link
          to="/appointments"
          class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md shadow-sm hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary"
        >
          Cancel
        </router-link>
        <button
          type="submit"
          class="px-4 py-2 ml-3 text-sm font-medium text-white bg-primary border border-transparent rounded-md shadow-sm hover:bg-primary-dark focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary"
        >
          Save
        </button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from "vue";
import { useRoute, useRouter } from "vue-router";
import api from "@/services/api";
import { format, addMinutes } from "date-fns";
import { formatDate, formatCurrency } from "@/utils/formatDate";

const route = useRoute();
const router = useRouter();
const appointment = ref({
  patient_id: null,
  specialty_id: null,
  start_time: "",
  end_time: "",
  price: 0,
});
const patients = ref([]);
const specialties = ref([]);
const patientSnippet = ref(null);
const doubleBookingWarning = ref(null);
const outsideWorkingHoursWarning = ref(null);
const endTimeWarning = ref(null);
const workingHours = ref({ start: "09:00", end: "18:00" }); // Placeholder

const isNew = computed(() => !route.params.id);

const fetchAppointment = async () => {
  if (isNew.value) return;
  try {
    const response = await api.get(`/appointments/${route.params.id}`);
    appointment.value = response.data;
    if (appointment.value.start_time) {
      appointment.value.start_time = format(
        new Date(appointment.value.start_time),
        "yyyy-MM-dd'T'HH:mm",
      );
    }
    if (appointment.value.end_time) {
      appointment.value.end_time = format(
        new Date(appointment.value.end_time),
        "yyyy-MM-ddTHH:mm",
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

watch(
  () => appointment.value.specialty_id,
  (newVal) => {
    if (newVal) {
      const selectedSpecialty = specialties.value.find((s) => s.id === newVal);
      if (selectedSpecialty) {
        appointment.value.price = selectedSpecialty.current_price;
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

onMounted(() => {
  fetchAppointment();
  fetchPatients();
  fetchSpecialties();
});

const saveAppointment = async () => {
  try {
    if (isNew.value) {
      await api.post("/appointments", appointment.value);
    } else {
      await api.put(`/appointments/${route.params.id}`, appointment.value);
    }
    router.push("/appointments");
  } catch (error) {
    console.error("Error saving appointment:", error);
  }
};
</script>
