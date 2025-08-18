<template>
  <div class="p-4 sm:p-6 lg:p-8">
    <div v-if="loading" class="text-center">
      <p>{{ t("loading_patient_profile") }}</p>
    </div>
    <div v-else-if="error" class="text-center text-red-500">
      <p>{{ t("error_loading_patient_profile") }}</p>
    </div>
    <div v-else>
      <div v-if="patient || isNew">
        <div class="bg-white shadow overflow-hidden sm:rounded-lg">
          <div class="px-4 py-5 sm:px-6 flex justify-between items-center">
            <div class="flex items-center">
              <button
                v-if="isEditing"
                class="mr-2 p-1 rounded-full hover:bg-gray-200"
                @click="cancelEdit"
              >
                <i-heroicons-arrow-left-20-solid
                  class="h-6 w-6 text-gray-500"
                />
              </button>
              <button
                v-if="!isEditing && !isNew"
                class="mr-2 p-1 rounded-full hover:bg-gray-200"
                @click="router.push('/patients')"
              >
                <i-heroicons-arrow-left-20-solid
                  class="h-6 w-6 text-gray-500"
                />
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
                      specialtyStore.specialties.find(
                        (s) => s.id === patient.default_specialty_id,
                      )?.name || t("not_specified")
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
                    <v-select
                      v-if="isEditing"
                      id="referred_by_patient_id"
                      v-model="patient.referred_by_patient_id"
                      :options="referredByOptions"
                      label="name"
                      :reduce="(patient) => patient.id"
                      :searchable="true"
                      :loading="referredBySearchLoading"
                      class="block w-full mt-1 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary sm:text-sm"
                      @search="onReferredBySearch"
                    >
                      <template #option="option">
                        <div>{{ option.name }}</div>
                      </template>
                    </v-select>
                    <span v-else>{{
                      patientStore.patients.find(
                        (p) => p.id === patient.referred_by_patient_id,
                      )?.name || t("not_specified")
                    }}</span>
                  </dd>
                </div>
              </dl>
            </form>
          </div>
        </div>
      </div>
      <!-- v-if="patient || isNew"> -->

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
            <button
              :class="[
                activeTab === 'emergency_contacts'
                  ? 'border-primary text-primary'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300',
                'whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm',
              ]"
              @click="activeTab = 'emergency_contacts'"
            >
              {{ t("emergency_contacts") }}
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
        <div
          v-show="activeTab === 'emergency_contacts'"
          class="border-t border-gray-200 px-4 py-5 sm:p-0"
        >
          <div class="px-4 py-5 sm:px-6">
            <div class="flex justify-between items-center mb-4">
              <h4 class="text-lg leading-6 font-medium text-gray-900">
                {{ t("emergency_contacts") }}
              </h4>
              <button
                v-if="isEditing"
                type="button"
                class="px-3 py-2 text-sm font-medium text-white bg-primary rounded-md hover:bg-primary-dark focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary"
                @click="addEmergencyContact"
              >
                {{ t("add_emergency_contact") }}
              </button>
            </div>
            <div v-if="emergencyContacts && emergencyContacts.length > 0">
              <table class="min-w-full divide-y divide-gray-200">
                <thead class="bg-gray-50">
                  <tr>
                    <th
                      scope="col"
                      class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                    >
                      {{ t("full_name") }}
                    </th>
                    <th
                      scope="col"
                      class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                    >
                      {{ t("patient_relationship") }}
                    </th>
                    <th
                      scope="col"
                      class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                    >
                      {{ t("email_address") }}
                    </th>
                    <th
                      scope="col"
                      class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                    >
                      {{ t("phone_number") }}
                    </th>
                    <th
                      scope="col"
                      class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                    >
                      {{ t("cell_phone") }}
                    </th>
                    <th
                      v-if="isEditing"
                      scope="col"
                      class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                    >
                      {{ t("actions") }}
                    </th>
                  </tr>
                </thead>
                <tbody class="bg-white divide-y divide-gray-200">
                  <EmergencyContactForm
                    v-for="(contact, index) in emergencyContacts"
                    :key="contact.id"
                    :contact="contact"
                    :is-editing="isEditing"
                    @delete="deleteEmergencyContact(contact)"
                    @update:contact="updateEmergencyContact($event, index)"
                  />
                </tbody>
              </table>
            </div>
            <div v-else class="text-sm text-gray-500">
              {{ t("no_emergency_contacts") }}
            </div>
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
import EmergencyContactForm from "@/components/patients/EmergencyContactForm.vue";
import { usePatientStore } from "@/stores/patients";
import { useSpecialtyStore } from "@/stores/specialties";

import vSelect from "vue-select";
import "vue-select/dist/vue-select.css";

const { t } = useI18n();
const route = useRoute();
const router = useRouter();

const patient = ref(null);
const appointments = ref([]);
const emergencyContacts = ref([]); // New ref for emergency contacts
const deletedEmergencyContactIds = ref([]);
const errors = ref({});
const referredByOptions = ref([]);
const referredBySearchLoading = ref(false);

const onReferredBySearch = async (search, loading) => {
  if (search.length) {
    loading(true);
    try {
      const response = await api.get("/patients/search", {
        params: { query: search, limit: 10 },
      });
      referredByOptions.value = response.data.items;
    } catch (error) {
      console.error("Error searching referred by patients:", error);
    } finally {
      loading(false);
    }
  } else {
    referredByOptions.value = [];
  }
};
const loading = ref(true);
const error = ref(false);

const patientStore = usePatientStore();
const specialtyStore = useSpecialtyStore();

const specialties = computed(() => specialtyStore.specialties);

const isNew = ref(false);
const isEditing = ref(false);
const activeTab = ref("medical_history"); // Default to medical history for new patient, or appointments for existing
const showCancelledAppointments = ref(false);
const md = new MarkdownIt();

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
    emergencyContacts.value = []; // Initialize empty for new patient
    return;
  }
  try {
    const response = await api.get(`/patients/${route.params.id}`);
    patient.value = response.data;
    // Format DOB for input if editing
    if (patient.value.dob) {
      patient.value.dob = formatDateForInput(patient.value.dob);
    }
    // Populate emergency contacts
    emergencyContacts.value = patient.value.emergency_contacts || [];
  } catch (err) {
    error.value = true;
    console.error("Error fetching patient:", err);
  }
};

const fetchAppointments = async () => {
  if (isNew.value) return;
  try {
    const response = await api.get(`/patients/${route.params.id}/appointments`);
    appointments.value = response.data;
  } catch (err) {
    error.value = true;
    console.error("Error fetching appointments:", err);
  }
};

const addEmergencyContact = () => {
  emergencyContacts.value.push({
    id: Date.now(), // Temporary ID for new contacts
    full_name: undefined,
    patient_relationship: undefined,
    email: undefined,
    phone_number: undefined,
    cellphone: undefined,
    isNew: true, // Flag to indicate a new contact
  });
};

const updateEmergencyContact = (contact, index) => {
  emergencyContacts.value[index] = contact;
};

const deleteEmergencyContact = (contact) => {
  if (contact.id && !contact.isNew) {
    deletedEmergencyContactIds.value.push(contact.id);
  }
  emergencyContacts.value = emergencyContacts.value.filter(
    (c) => c.id !== contact.id,
  );
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
    !/^["\w-.]+@([\w-]+\.)+[\w-]{2,4}$/.test(patient.value.email)
  ) {
    errors.value.email = "Invalid email format.";
  }

  if (Object.keys(errors.value).length > 0) {
    return;
  }

  try {
    let patientData;
    if (isNew.value) {
      const response = await api.post("/patients/", patient.value);
      patientData = response.data;
    } else {
      const response = await api.put(
        `/patients/${route.params.id}`,
        patient.value,
      );
      patientData = response.data;
    }

    // Delete emergency contacts
    for (const contactId of deletedEmergencyContactIds.value) {
      await api.delete(
        `/patients/${patientData.id}/emergency_contacts/${contactId}`,
      );
    }
    deletedEmergencyContactIds.value = [];

    // Save emergency contacts
    const savedContacts = [];
    for (const contact of emergencyContacts.value) {
      if (contact.isNew) {
        // remove temporary ID and isNew flag
        const newContact = { ...contact };
        delete newContact.id;
        delete newContact.isNew;
        const response = await api.post(
          `/patients/${patientData.id}/emergency_contacts`,
          newContact,
        );
        savedContacts.push(response.data);
      } else if (contact.id) {
        const response = await api.put(
          `/patients/${patientData.id}/emergency_contacts/${contact.id}`,
          contact,
        );
        savedContacts.push(response.data);
      }
    }
    emergencyContacts.value = savedContacts;

    isEditing.value = false;
    if (isNew.value) {
      isNew.value = false;
      patientStore.addPatient(patientData); // Add the new patient to the store
      router.push({ name: "view-patient", params: { id: patientData.id } });
    } else {
      patientStore.updatePatient(patientData); // Update the patient in the store
      // Re-fetch patient to get the latest financial summary and other data, but not emergency contacts
      const response = await api.get(`/patients/${route.params.id}`);
      patient.value = response.data;
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
  loading.value = true;
  try {
    await fetchPatient();
    await fetchAppointments();
    if (!specialtyStore.specialties.length) {
      await specialtyStore.fetchSpecialties();
    }

    // Initial load for referred by v-select options
    const response = await api.get("/patients/search", {
      params: { limit: 10 },
    });
    referredByOptions.value = response.data.items;

    // If a referred_by_patient_id is already set, ensure it's in the options
    if (patient.value && patient.value.referred_by_patient_id) {
      const selectedReferredBy = referredByOptions.value.find(
        (p) => p.id === patient.value.referred_by_patient_id,
      );
      if (!selectedReferredBy) {
        try {
          const responseSelected = await api.get(
            `/patients/${patient.value.referred_by_patient_id}`,
          );
          referredByOptions.value.push(responseSelected.data);
        } catch (errorSelected) {
          console.error(
            "Error fetching selected referred by patient:",
            errorSelected,
          );
        }
      }
    }
  } catch (err) {
    error.value = true;
    console.error("Error loading patient profile:", err);
  } finally {
    loading.value = false;
  }
});
</script>
