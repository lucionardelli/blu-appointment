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
            <v-select
              id="patient"
              v-model="appointment.patient_id"
              :options="patientsOptions"
              label="name"
              :reduce="(patient) => patient.id"
              :searchable="true"
              :loading="patientSearchLoading"
              class="block w-full mt-1 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary sm:text-sm"
              @search="onPatientSearch"
              @change="fetchPatientSnippet"
            >
              <template #no-options="{ searching, loading }">
                <template v-if="searching">
                  <span v-if="!loading">{{ t("no_matching_options") }}</span>
                  <span v-else>{{ t("loading") }}</span>
                </template>
                <span v-else>{{ t("start_typing_to_search") }}</span>
              </template>
            </v-select>
            <div
              v-if="patientSnippet"
              class="mt-2 p-4 bg-gray-100 rounded-md sm:flex sm:justify-between"
            >
              <p
                v-if="patientSnippet.nickname"
                class="ml-2 text-xs text-gray-600"
              >
                {{ t("nickname") }}: ({{ patientSnippet.nickname }})
              </p>
              <p class="text-sm text-gray-500">
                {{ t("age") }}:
                <span
                  :class="{
                    'text-red-500 font-semibold': patientSnippet.is_underage,
                  }"
                  >{{ patientSnippet.age }}</span
                >
              </p>
              <p class="text-sm text-gray-500">
                {{ t("past_appointments") }}:
                {{ patientSnippet.appointment_summary.past_appointments }}
              </p>
              <p
                v-if="
                  selectedSpecialtyName &&
                  patientSnippet.appointment_summary.specialty_counts[
                    selectedSpecialtyId
                  ] !== undefined
                "
                class="text-sm text-gray-500"
              >
                {{ t("appointments") }} {{ selectedSpecialtyName }}:
                {{
                  patientSnippet.appointment_summary.specialty_counts[
                    selectedSpecialtyId
                  ]["past"]
                }}
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
          <div
            v-if="appointment.suggested_treatment_duration_minutes"
            class="mt-2 p-3 bg-blue-100 border-l-4 border-blue-500 rounded-md"
          >
            <p class="text-sm text-blue-700">
              {{ t("suggested_treatment_duration") }}:
              <span class="font-semibold">
                {{ appointment.suggested_treatment_duration_minutes }}
                {{ t("minutes") }}
              </span>
            </p>
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
              <DatePicker
                v-model="appointment.start_time"
                :enable-time-picker="true"
                :minutes-increment="15"
                text-input
                auto-apply
                class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary focus:ring-primary sm:text-sm"
              />
            </div>
            <div>
              <label
                for="end_time"
                class="block text-sm font-medium text-gray-700"
                >{{ t("end_time") }}</label
              >
              <DatePicker
                v-model="appointment.end_time"
                :enable-time-picker="true"
                :minutes-increment="15"
                text-input
                auto-apply
                class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary focus:ring-primary sm:text-sm"
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
            <i-heroicons-arrow-left-20-solid class="h-6 w-6 text-gray-500" />
          </button>
          <h2 class="text-xl font-semibold text-gray-800">
            <span v-if="showPaymentForm">
              {{ t("new_payment") }}
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
        :patient-id="appointment.patient_id"
        :appointment="appointment"
        @save="handlePaymentSave"
        @cancel="showPaymentForm = false"
      />

      <div v-else>
        <table
          v-if="appointment.payments && appointment.payments.length"
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
            <tr v-for="payment in appointment.payments" :key="payment.id">
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
import DatePicker from "@vuepic/vue-datepicker";
import "@vuepic/vue-datepicker/dist/main.css";
import { formatDate, formatCurrency } from "@/utils/formatDate";
import PaymentForm from "./PaymentForm.vue";
import { useSpecialtyStore } from "@/stores/specialties";

import vSelect from "vue-select";
import "vue-select/dist/vue-select.css";

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
  suggested_treatment_duration_minutes: null,
  payments: [],
});

const specialtyStore = useSpecialtyStore();

const patientsOptions = ref([]);
const patientSearchLoading = ref(false);

const specialties = computed(() => specialtyStore.specialties);
const patientSnippet = ref(null);
const activeTab = ref("details");
const showPaymentForm = ref(false);

const isNew = computed(() => !props.appointmentId);

const selectedSpecialtyId = computed(() => appointment.value.specialty_id);

const selectedSpecialtyName = computed(() => {
  if (selectedSpecialtyId.value) {
    const specialty = specialties.value.find(
      (s) => s.id === selectedSpecialtyId.value,
    );
    return specialty ? specialty.name : null;
  }
  return null;
});

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

const handlePaymentSave = () => {
  showPaymentForm.value = false;
  fetchAppointment(); // Refetch appointment to update total_paid and payments
};

const onPatientSearch = async (search, loading) => {
  if (search.length) {
    loading(true);
    try {
      const response = await api.get("/patients", {
        params: { query: search, limit: 10 },
      });
      patientsOptions.value = response.data.items;
    } catch (error) {
      console.error("Error searching patients:", error);
    } finally {
      loading(false);
    }
  } else {
    patientsOptions.value = [];
  }
};

watch(
  () => appointment.value.patient_id,
  async (newPatientId) => {
    if (newPatientId) {
      await fetchPatientSnippet();
      const selectedPatient = patientsOptions.value.find(
        (p) => p.id === newPatientId,
      );
      if (!selectedPatient) {
        // If the selected patient is not in the current options, fetch it and add it
        try {
          const response = await api.get(`/patients/${newPatientId}`);
          patientsOptions.value.push(response.data);
        } catch (error) {
          console.error("Error fetching selected patient:", error);
        }
      }
      if (patientSnippet.value && patientSnippet.value.default_specialty_id) {
        appointment.value.specialty_id =
          patientSnippet.value.default_specialty_id;
      }
    }
  },
);

onMounted(async () => {
  if (!specialtyStore.specialties.length) {
    await specialtyStore.fetchSpecialties();
  }
  if (props.appointmentId) {
    await fetchAppointment();
    if (appointment.value.patient_id) {
      await fetchPatientSnippet();
    }
  } else if (props.initialDate) {
    const startDate = new Date(props.initialDate);
    appointment.value.start_time = format(startDate, "yyyy-MM-dd'T'HH:mm");
    if (props.initialEndDate) {
      const endDate = new Date(props.initialEndDate);
      appointment.value.end_time = format(endDate, "yyyy-MM-dd'T'HH:mm");
    } else {
      appointment.value.end_time = "";
    }
  }
  try {
    const response = await api.get("/patients", { params: { limit: 4 } });
    patientsOptions.value = response.data.items;
  } catch (error) {
    console.error("Error fetching initial patients:", error);
  }
});

watch(
  () => appointment.value.specialty_id,
  (newVal) => {
    if (!newVal) return;

    const selectedSpecialty = specialtyStore.specialties.find(
      (s) => s.id === newVal,
    );
    if (!selectedSpecialty) return;

    appointment.value.cost = selectedSpecialty.current_price;

    if (appointment.value.start_time && !appointment.value.end_time) {
      const startTime = new Date(appointment.value.start_time);
      const newEndTime = addMinutes(
        startTime,
        selectedSpecialty.default_duration,
      );
      appointment.value.end_time = format(newEndTime, "yyyy-MM-dd'T'HH:mm");
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

const saveAppointment = async () => {
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
