<template>
  <div>
    <div class="flex justify-between items-center mt-4">
      <h1 class="text-2xl font-semibold text-gray-900">
        {{ isNew ? t("new_appointment") : t("edit_appointment") }}
      </h1>
      <div class="flex items-center space-x-2">
        <button
          v-if="!isNew && !appointment.cancelled"
          type="button"
          class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md shadow-sm hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary"
          @click="cancelAppointment"
        >
          {{ t("cancel_appointment") }}
        </button>
        <button
          v-if="!isNew && appointment.cancelled"
          type="button"
          class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md shadow-sm hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary"
          @click="restoreAppointment"
        >
          {{ t("restore_appointment") }}
        </button>
        <button
          v-if="!isNew && appointment.cancelled"
          type="button"
          class="px-4 py-2 text-sm font-medium text-red-700 bg-white border border-red-300 rounded-md shadow-sm hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
          @click="deleteAppointment"
        >
          {{ t("delete") }}
        </button>
        <button
          v-if="!appointment.cancelled"
          type="submit"
          class="px-4 py-2 text-sm font-medium text-white bg-primary border border-transparent rounded-md shadow-sm hover:bg-primary-dark focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary"
          @click="saveAppointment"
        >
          {{ t("save") }}
        </button>
      </div>
    </div>

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

    <div
      v-show="activeTab === 'details'"
      class="mt-6"
      :class="{ 'text-gray-500': appointment.cancelled }"
    >
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
              :filter="(options, search) => options"
              :disabled="appointment.cancelled"
              :class="{ 'cursor-not-allowed': patientSearchLoading }"
              class="block w-full mt-1 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary sm:text-sm"
              @search="debouncedOnPatientSearch"
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
                  >{{ patientSnippet.age || ">18*" }}</span
                >
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
                {{ formatDate(patientSnippet.last_appointment) || "-" }}
              </p>
              <p class="text-sm text-gray-500">
                {{ t("total_due") }}:
                {{ formatCurrency(patientSnippet.total_due || 0) }}
              </p>
            </div>
          </div>
          <div
            v-if="suggestedTreatmentDuration"
            class="mt-2 p-3 bg-blue-100 border-l-4 border-blue-500 rounded-md"
          >
            <p class="text-sm text-blue-700">
              {{ t("suggested_treatment_duration") }}:
              <span class="font-semibold">
                {{ suggestedTreatmentDuration }}
                {{ t("minutes") }}
              </span>
            </p>
          </div>
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-6">
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
                :disabled="appointment.cancelled"
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
                step="1000"
                required
                :readonly="appointment.cancelled"
                class="block w-full px-3 py-2 mt-1 placeholder-gray-400 border border-gray-300 rounded-md shadow-sm appearance-none focus:outline-none focus:ring-primary focus:border-primary sm:text-sm"
              />
            </div>
          </div>
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-6">
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
                utc
                :locale="locale"
                :format="formatForPicker"
                :disabled="appointment.cancelled"
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
                utc
                :locale="locale"
                :format="formatForPicker"
                :disabled="appointment.cancelled"
                class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary focus:ring-primary sm:text-sm"
              />
            </div>
          </div>
        </div>
      </form>
    </div>

    <div v-if="!isNew && activeTab === 'payments'" class="mt-6">
      <h2 class="text-xl font-semibold text-gray-800 mb-4">
        {{ t("payments") }}
      </h2>
      <div>
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
                {{ t("payment_method") }}
              </th>
              <th
                scope="col"
                class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider"
              >
                {{ t("amount") }}
              </th>
              <th scope="col" class="relative px-6 py-3 w-1 whitespace-nowrap">
                <span class="sr-only">Pay</span>
              </th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr
              v-if="!appointment.cancelled && amountDue > 0"
              class="bg-green-50"
            >
              <td
                class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900"
              >
                {{ formatDate(new Date()) }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                <select
                  v-model="newPayment.payment_method_id"
                  class="w-full p-1 bg-transparent border-0 border-b-2 border-transparent focus:border-primary focus:ring-0 sm:text-sm"
                >
                  <option
                    v-for="pm in paymentMethods"
                    :key="pm.id"
                    :value="pm.id"
                  >
                    {{ pm.name }}
                  </option>
                </select>
              </td>
              <td
                class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 text-right"
              >
                <input
                  v-model="newPayment.amount"
                  type="number"
                  step="1000"
                  class="w-full p-1 bg-transparent border-0 border-b-2 border-transparent focus:border-primary focus:ring-0 sm:text-sm text-right"
                />
              </td>
              <td
                class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium"
              >
                <button
                  type="button"
                  class="inline-flex items-center px-2.5 py-1.5 border border-gray-300 shadow-sm text-xs font-medium rounded text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary"
                  @click="saveNewPayment"
                >
                  <i-heroicons-currency-dollar-20-solid
                    class="-ml-0.5 mr-2 h-4 w-4"
                  />
                  {{ t("add_payment") }}
                </button>
              </td>
            </tr>
            <tr v-for="payment in appointment.payments" :key="payment.id">
              <td
                class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900"
              >
                {{ formatDate(payment.payment_date) }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {{ payment.payment_method.name }}
              </td>
              <td
                class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 text-right"
              >
                {{ formatCurrency(payment.amount) }}
              </td>
              <td></td>
            </tr>
            <tr
              v-if="!appointment.payments || appointment.payments.length === 0"
            >
              <td colspan="4" class="px-6 py-4 text-center text-gray-500">
                {{ t("no_payments_found") }}
              </td>
            </tr>
          </tbody>
          <tfoot class="bg-gray-50">
            <tr>
              <td
                colspan="3"
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
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from "vue";
import { useI18n } from "vue-i18n";
import { useRouter } from "vue-router";
import api from "@/services/api";
import { addMinutes } from "date-fns";
import DatePicker from "@vuepic/vue-datepicker";
import "@vuepic/vue-datepicker/dist/main.css";
import { formatDate, formatTime, formatCurrency } from "@/utils/formatDate";
import { useSpecialtyStore } from "@/stores/specialties";
import debounce from "lodash/debounce";

import vSelect from "vue-select";
import "vue-select/dist/vue-select.css";

const { t, locale } = useI18n();

const formatForPicker = (date) => {
  if (!date) return "";
  return `${formatDate(date)} ${formatTime(date)}`;
};

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
  payments: [],
});

const suggestedTreatmentDuration = ref(null);

const specialtyStore = useSpecialtyStore();

const patientsOptions = ref([]);
const patientSearchLoading = ref(false);

const specialties = computed(() => specialtyStore.specialties);
const patientSnippet = ref(null);
const activeTab = ref("details");

const newPayment = ref({
  amount: 0,
  payment_method_id: null,
});
const paymentMethods = ref([]);

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

watch(amountDue, (newAmount) => {
  newPayment.value.amount = newAmount > 0 ? newAmount : 0;
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
    const response = await api.get(`/appointments/${props.appointmentId}/`);
    const fetchedAppointment = response.data;

    if (fetchedAppointment.patient) {
      patientSnippet.value = fetchedAppointment.patient;
    }

    // Flatten nested patient and specialty objects
    appointment.value = {
      ...fetchedAppointment,
      patient_id: fetchedAppointment.patient?.id,
      specialty_id: fetchedAppointment.specialty?.id,
    };

    if (
      fetchedAppointment.patient &&
      !patientsOptions.value.some((p) => p.id === fetchedAppointment.patient.id)
    ) {
      patientsOptions.value.push(fetchedAppointment.patient);
    }

    if (appointment.value.start_time) {
      appointment.value.start_time = new Date(appointment.value.start_time);
    }
    if (appointment.value.end_time) {
      appointment.value.end_time = new Date(appointment.value.end_time);
    }
  } catch (error) {
    console.error("Error fetching appointment:", error);
  }
};

const fetchPaymentMethods = async () => {
  try {
    const response = await api.get("/payment_methods/");
    paymentMethods.value = response.data;
    if (
      paymentMethods.value.length > 0 &&
      !newPayment.value.payment_method_id
    ) {
      newPayment.value.payment_method_id = paymentMethods.value[0].id;
    }
  } catch (error) {
    console.error("Error fetching payment methods:", error);
  }
};

const saveNewPayment = async () => {
  if (!newPayment.value.amount || !newPayment.value.payment_method_id) {
    console.error("Amount and payment method are required.");
    return;
  }
  try {
    const payload = {
      ...newPayment.value,
      patient_id: appointment.value.patient_id,
      appointment_id: props.appointmentId,
    };
    await api.post("/payments/", payload);
    await fetchAppointment();
  } catch (error) {
    console.error("Error saving payment:", error);
  }
};

const onPatientSearch = async (search, loading) => {
  if (search.length) {
    loading(true);
    try {
      const response = await api.get("/patients/", {
        params: { query: search, limit: 10 },
      });
      const newOptions = response.data.items;

      if (appointment.value.patient_id) {
        const isSelectedInNewOptions = newOptions.some(
          (p) => p.id === appointment.value.patient_id,
        );
        if (!isSelectedInNewOptions) {
          const existingPatient = patientsOptions.value.find(
            (p) => p.id === appointment.value.patient_id,
          );
          if (existingPatient) {
            newOptions.unshift(existingPatient);
          } else {
            // Fallback to fetch the patient if not in current options
            const response = await api.get(
              `/patients/${appointment.value.patient_id}/`,
            );
            newOptions.unshift(response.data);
          }
        }
      }
      patientsOptions.value = newOptions;
    } catch (error) {
      console.error("Error searching patients:", error);
    } finally {
      loading(false);
    }
  }
};

const debouncedOnPatientSearch = debounce(onPatientSearch, 300);

watch(
  [
    () => appointment.value.patient_id,
    () => appointment.value.specialty_id,
    () => appointment.value.start_time,
  ],
  async ([patientId, specialtyId, startTime]) => {
    if (patientId && specialtyId && startTime) {
      try {
        const response = await api.get("/appointments/suggested-duration/", {
          params: {
            patient_id: patientId,
            specialty_id: specialtyId,
            before_time: startTime.toISOString(),
          },
        });
        suggestedTreatmentDuration.value = response.data;
      } catch (error) {
        console.error("Error fetching suggested duration:", error);
        suggestedTreatmentDuration.value = null;
      }
    } else {
      suggestedTreatmentDuration.value = null;
    }
  },
  { deep: true },
);

watch(
  () => appointment.value.patient_id,
  async (newPatientId) => {
    if (newPatientId) {
      if (!patientSnippet.value || patientSnippet.value.id !== newPatientId) {
        await fetchPatientSnippet();
      }
      const selectedPatient = patientsOptions.value.find(
        (p) => p.id === newPatientId,
      );
      if (!selectedPatient) {
        // If the selected patient is not in the current options, fetch it and add it
        try {
          const response = await api.get(`/patients/${newPatientId}/`);
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
  fetchPaymentMethods();
  if (props.appointmentId) {
    await fetchAppointment();
  } else {
    try {
      const response = await api.get("/patients/", { params: { limit: 4 } });
      patientsOptions.value = response.data.items;
    } catch (error) {
      console.error("Error fetching initial patients:", error);
    }
    if (props.initialDate) {
      const startDate = new Date(props.initialDate);
      appointment.value.start_time = startDate;
      if (props.initialEndDate) {
        const endDate = new Date(props.initialEndDate);
        appointment.value.end_time = endDate;
      } else {
        appointment.value.end_time = "";
      }
    }
  }
});

watch(
  () => appointment.value.specialty_id,
  async (newVal, oldVal) => {
    if (!newVal) return; // We are actually 'clearing' the specialty

    if (!isNew.value && oldVal === null) return; // Initial load for existing appointment
    const selectedSpecialty = specialtyStore.specialties.find(
      (s) => s.id === newVal,
    );
    if (!selectedSpecialty) return; // Invalid specialty selected

    if (newVal !== oldVal) {
      let newCost = selectedSpecialty.current_price;

      // Check for patient-specific special price
      if (appointment.value.patient_id) {
        try {
          const response = await api.get(
            `/patients/${appointment.value.patient_id}/special-prices`,
          );
          const patientSpecialPrices = response.data;
          const specialPriceEntry = patientSpecialPrices.find(
            (p) => p.specialty_id === newVal,
          );
          if (specialPriceEntry) {
            newCost = specialPriceEntry.price;
          }
        } catch (error) {
          console.error("Error fetching patient special prices:", error);
        }
      }

      appointment.value.cost = newCost;

      const startTime = new Date(appointment.value.start_time);
      const newEndTime = addMinutes(
        startTime,
        selectedSpecialty.default_duration_minutes,
      );
      appointment.value.end_time = newEndTime;
    }
  },
);

const fetchPatientSnippet = async () => {
  if (!appointment.value.patient_id) {
    patientSnippet.value = null;
    return;
  }
  try {
    const response = await api.get(
      `/patients/${appointment.value.patient_id}/`,
    );
    patientSnippet.value = response.data;
  } catch (error) {
    console.error("Error fetching patient snippet:", error);
  }
};

const saveAppointment = async () => {
  try {
    if (isNew.value) {
      await api.post("/appointments/", appointment.value);
    } else {
      await api.put(`/appointments/${props.appointmentId}/`, {
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

const cancelAppointment = async () => {
  if (window.confirm(t("confirm_cancel_appointment"))) {
    try {
      await api.patch(`/appointments/${props.appointmentId}/cancel/`);
      if (props.inModal) {
        emit("save");
      } else {
        router.push("/appointments");
      }
    } catch (error) {
      console.error("Error cancelling appointment:", error);
    }
  }
};

const restoreAppointment = async () => {
  try {
    await api.patch(`/appointments/${props.appointmentId}/restore`);
    if (props.inModal) {
      emit("save");
    } else {
      router.push("/appointments");
    }
  } catch (error) {
    console.error("Error restoring appointment:", error);
  }
};

const deleteAppointment = async () => {
  if (window.confirm(t("confirm_delete_appointment"))) {
    try {
      await api.delete(`/appointments/${props.appointmentId}/`);
      if (props.inModal) {
        emit("save");
      } else {
        router.push("/appointments");
      }
    } catch (error) {
      console.error("Error deleting appointment:", error);
    }
  }
};
</script>
