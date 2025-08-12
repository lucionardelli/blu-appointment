<template>
  <div>
    <div v-if="patient || isNew">
      <div class="bg-white shadow overflow-hidden sm:rounded-lg">
        <div class="px-4 py-5 sm:px-6 flex justify-between items-center">
          <div class="flex items-center">
            <button
              v-if="isEditing"
              class="mr-2 p-1 rounded-full hover:bg-gray-200"
              @click="cancelEdit"
            >
              <i-heroicons-arrow-left-20-solid class="h-6 w-6 text-gray-500" />
            </button>
            <button
              v-if="!isEditing && !isNew"
              class="mr-2 p-1 rounded-full hover:bg-gray-200"
              @click="router.push('/patients')"
            >
              <i-heroicons-arrow-left-20-solid class="h-6 w-6 text-gray-500" />
            </button>
            <h3 class="text-lg leading-6 font-medium text-gray-900">
              <span v-if="isNew">{{ t("new_patient") }}</span>
              <span v-else-if="isEditing">{{ t("edit_patient") }}</span>
              <span v-else>{{ t("patient_profile") }}</span>
            </h3>
          </div>
          <button
            v-if="!isEditing && !isNew"
            class="px-4 py-2 text-sm font-medium text-white bg-primary border border-transparent rounded-md shadow-sm hover:bg-primary-dark focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary"
            @click="startEdit"
          >
            {{ t("edit") }}
          </button>
          <button
            v-else
            class="px-4 py-2 text-sm font-medium text-white bg-primary border border-transparent rounded-md shadow-sm hover:bg-primary-dark focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary"
            @click="savePatient"
          >
            {{ t("save") }}
          </button>
        </div>
        <div class="border-t border-gray-200">
          <form @submit.prevent="savePatient">
            <dl class="sm:divide-y sm:divide-gray-200">
              <div
                class="bg-gray-50 px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6"
              >
                <dt class="text-sm font-medium text-gray-500">
                  {{ t("full_name") }}
                </dt>
                <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                  <div v-if="isEditing" class="grid grid-cols-2 gap-4">
                    <div>
                      <input
                        id="name"
                        v-model="patient.name"
                        type="text"
                        required
                        class="block w-full px-3 py-2 placeholder-gray-400 border border-gray-300 rounded-md shadow-sm appearance-none focus:outline-none focus:ring-primary focus:border-primary sm:text-sm"
                      />
                      <p v-if="errors.name" class="mt-1 text-sm text-red-600">
                        {{ errors.name }}
                      </p>
                    </div>
                    <div>
                      <label for="nickname" class="sr-only">{{
                        t("nickname")
                      }}</label>
                      <input
                        id="nickname"
                        v-model="patient.nickname"
                        type="text"
                        :placeholder="t('nickname')"
                        class="block w-full px-3 py-2 placeholder-gray-400 border border-gray-300 rounded-md shadow-sm appearance-none focus:outline-none focus:ring-primary focus:border-primary sm:text-sm"
                      />
                    </div>
                  </div>
                  <span v-else
                    >{{ patient.name }}
                    <span v-if="patient.nickname"
                      >({{ patient.nickname }})</span
                    ></span
                  >
                </dd>
              </div>
              <div
                class="bg-gray-50 px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6"
              >
                <dt class="text-sm font-medium text-gray-500">
                  {{ t("date_of_birth") }}
                </dt>
                <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                  <input
                    v-if="isEditing"
                    id="dob"
                    v-model="patient.dob"
                    type="date"
                    required
                    class="block w-full px-3 py-2 placeholder-gray-400 border border-gray-300 rounded-md shadow-sm appearance-none focus:outline-none focus:ring-primary focus:border-primary sm:text-sm"
                  />
                  <span v-else>{{ formatDate(patient.dob) }}</span>
                  <p v-if="errors.dob" class="mt-1 text-sm text-red-600">
                    {{ errors.dob }}
                  </p>
                </dd>
              </div>
              <div
                class="bg-gray-50 px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6"
              >
                <dt class="text-sm font-medium text-gray-500">
                  {{ t("email_address") }}
                </dt>
                <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                  <input
                    v-if="isEditing"
                    id="email"
                    v-model="patient.email"
                    type="email"
                    class="block w-full px-3 py-2 mt-1 placeholder-gray-400 border border-gray-300 rounded-md shadow-sm appearance-none focus:outline-none focus:ring-primary focus:border-primary sm:text-sm"
                  />
                  <span v-else>{{ patient.email }}</span>
                  <p v-if="errors.email" class="mt-1 text-sm text-red-600">
                    {{ errors.email }}
                  </p>
                </dd>
              </div>
              <div
                class="bg-white px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6"
              >
                <dt class="text-sm font-medium text-gray-500">
                  {{ t("phone_number") }}
                </dt>
                <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                  <input
                    v-if="isEditing"
                    id="phone"
                    v-model="patient.phone"
                    type="text"
                    class="block w-full px-3 py-2 mt-1 placeholder-gray-400 border border-gray-300 rounded-md shadow-sm appearance-none focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                  />
                  <span v-else>{{ patient.phone }}</span>
                </dd>
              </div>
              <div
                class="bg-gray-50 px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6"
              >
                <dt class="text-sm font-medium text-gray-500">
                  {{ t("cell_phone") }}
                </dt>
                <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                  <input
                    v-if="isEditing"
                    id="cellphone"
                    v-model="patient.cellphone"
                    type="text"
                    class="block w-full px-3 py-2 mt-1 placeholder-gray-400 border border-gray-300 rounded-md shadow-sm appearance-none focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                  />
                  <span v-else>{{ patient.cellphone }}</span>
                </dd>
              </div>
              <div
                class="bg-white px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6"
              >
                <dt class="text-sm font-medium text-gray-500">
                  {{ t("address") }}
                </dt>
                <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                  <input
                    v-if="isEditing"
                    id="address"
                    v-model="patient.address"
                    type="text"
                    class="block w-full px-3 py-2 mt-1 placeholder-gray-400 border border-gray-300 rounded-md shadow-sm appearance-none focus:outline-none focus:ring-primary focus:border-primary sm:text-sm"
                  />
                  <span v-else>{{ patient.address }}</span>
                </dd>
              </div>
              <div
                class="bg-gray-50 px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6"
              >
                <dt class="text-sm font-medium text-gray-500">
                  {{ t("default_specialty") }}
                </dt>
                <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                  <select
                    v-if="isEditing"
                    id="default_specialty"
                    v-model="patient.default_specialty_id"
                    class="block w-full px-3 py-2 mt-1 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary sm:text-sm"
                  >
                    <option :value="null">{{ t("not_specified") }}</option>
                    <option
                      v-for="specialty in specialties"
                      :key="specialty.id"
                      :value="specialty.id"
                    >
                      {{ specialty.name }}
                    </option>
                  </select>
                  <span v-else>{{
                    patient.default_specialty?.name || t("not_specified")
                  }}</span>
                </dd>
              </div>
              <div
                class="bg-white px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6"
              >
                <dt class="text-sm font-medium text-gray-500">
                  {{ t("how_they_found_us") }}
                </dt>
                <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                  <input
                    v-if="isEditing"
                    id="how_they_found_us"
                    v-model="patient.how_they_found_us"
                    type="text"
                    class="block w-full px-3 py-2 mt-1 placeholder-gray-400 border border-gray-300 rounded-md shadow-sm appearance-none focus:outline-none focus:ring-primary focus:border-primary sm:text-sm"
                  />
                  <span v-else>{{ patient.how_they_found_us }}</span>
                </dd>
              </div>
              <div
                class="bg-gray-50 px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6"
              >
                <dt class="text-sm font-medium text-gray-500">
                  {{ t("referred_by") }}
                </dt>
                <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                  <select
                    v-if="isEditing"
                    id="referred_by_patient_id"
                    v-model="patient.referred_by_patient_id"
                    class="block w-full px-3 py-2 mt-1 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary sm:text-sm"
                  >
                    <option :value="null">{{ t("not_specified") }}</option>
                    <option
                      v-for="p in filteredPatients"
                      :key="p.id"
                      :value="p.id"
                    >
                      {{ p.name }}
                    </option>
                  </select>
                  <span v-else>{{
                    patient.referred_by?.name || t("not_specified")
                  }}</span>
                </dd>
              </div>
            </dl>
          </form>
        </div>
      </div>

      <div
        v-if="patient.financialSummary && !isNew"
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
                {{ formatCurrency(patient.financialSummary.totalPaid) }}
              </dd>
            </div>
            <div class="sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6 sm:py-5">
              <dt class="text-sm font-medium text-gray-500">
                {{ t("total_due") }}
              </dt>
              <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                {{ formatCurrency(patient.financialSummary.totalDue) }}
              </dd>
            </div>
            <div class="sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6 sm:py-5">
              <dt class="text-sm font-medium text-gray-500">
                {{ t("balance") }}
              </dt>
              <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                {{ formatCurrency(patient.financialSummary.balance) }}
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
            <textarea
              v-if="isEditing"
              id="medical_history"
              v-model="patient.medical_history"
              rows="10"
              class="block w-full px-3 py-2 mt-1 placeholder-gray-400 border border-gray-300 rounded-md shadow-sm appearance-none focus:outline-none focus:ring-primary focus:border-primary sm:text-sm"
            ></textarea>
            <!-- eslint-disable vue/no-v-html -->
            <div
              v-else
              class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2 prose max-w-none"
              v-html="renderedMedicalHistory"
            ></div>
            <!-- eslint-enable vue/no-v-html -->
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import { useI18n } from "vue-i18n";
import { useRoute, useRouter } from "vue-router";
import api from "@/services/api";
import MarkdownIt from "markdown-it";
import DOMPurify from "dompurify";
import {
  formatDate,
  formatCurrency,
  formatTime,
  formatDateForInput,
} from "@/utils/formatDate";

const { t } = useI18n();
const route = useRoute();
const router = useRouter();

const patient = ref(null);
const patients = ref([]);
const specialties = ref([]);
const appointments = ref([]);
const errors = ref({});

const isNew = ref(false);
const isEditing = ref(false);
const activeTab = ref("appointments");
const showCancelledAppointments = ref(false);
const md = new MarkdownIt();

const filteredPatients = computed(() => {
  if (patient.value) {
    return patients.value.filter((p) => p.id !== patient.value.id);
  }
  return patients.value;
});

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

const fetchSpecialties = async () => {
  try {
    const response = await api.get("/specialties/");
    specialties.value = response.data;
  } catch (error) {
    console.error("Error fetching specialties:", error);
  }
};

const fetchPatients = async () => {
  try {
    const response = await api.get("/patients/");
    patients.value = response.data;
  } catch (error) {
    console.error("Error fetching patients:", error);
  }
};

const fetchPatient = async () => {
  if (route.params.id === "new") {
    isNew.value = true;
    isEditing.value = true;
    activeTab.value = "medical_history"; // Default to medical history for new patient
    patient.value = {
      name: "",
      nickname: undefined,
      dob: undefined,
      cellphone: undefined,
      email: undefined,
      phone: undefined,
      address: undefined,
      medical_history: undefined,
      default_specialty_id: null,
      how_they_found_us: undefined,
      referred_by_patient_id: null,
    };
    return;
  }
  try {
    const response = await api.get(`/patients/${route.params.id}`);
    patient.value = response.data;
    // Format DOB for input if editing
    if (patient.value.dob) {
      patient.value.dob = formatDateForInput(patient.value.dob);
    }
  } catch (error) {
    console.error("Error fetching patient:", error);
  }
};

const fetchAppointments = async () => {
  if (isNew.value) return;
  try {
    const response = await api.get(`/patients/${route.params.id}/appointments`);
    appointments.value = response.data;
  } catch (error) {
    console.error("Error fetching appointments:", error);
  }
};

const savePatient = async () => {
  errors.value = {};

  if (!patient.value.name) {
    errors.value.name = "Name is required.";
  }
  if (!patient.value.dob) {
    errors.value.dob = "Date of Birth is required.";
  }
  if (
    patient.value.email &&
    !/^[\w-.]+@([\w-]+\.)+[\w-]{2,4}$/.test(patient.value.email)
  ) {
    errors.value.email = "Invalid email format.";
  }

  if (Object.keys(errors.value).length > 0) {
    return;
  }

  try {
    if (isNew.value) {
      const response = await api.post("/patients/", patient.value);
      isEditing.value = false;
      isNew.value = false;
      router.push({ name: "view-patient", params: { id: response.data.id } });
    } else {
      await api.put(`/patients/${route.params.id}`, patient.value);
      isEditing.value = false; // Exit edit mode after saving
    }
  } catch (error) {
    console.error("Error saving patient:", error);
  }
};

const startEdit = () => {
  isEditing.value = true;
  activeTab.value = "medical_history"; // Switch to medical history tab when editing
};

const cancelEdit = () => {
  if (isNew.value) {
    router.push("/patients"); // Go back to patients list if creating new
  } else {
    isEditing.value = false; // Exit edit mode
    fetchPatient(); // Re-fetch patient to revert changes
  }
};

onMounted(async () => {
  await fetchSpecialties();
  await fetchPatients();
  await fetchPatient();
  await fetchAppointments();
});
</script>
