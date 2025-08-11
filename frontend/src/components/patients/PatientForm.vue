<template>
  <div>
    <div class="bg-white shadow overflow-hidden sm:rounded-lg">
      <div class="px-4 py-5 sm:px-6 flex justify-between items-center">
        <div>
          <h3 class="text-lg leading-6 font-medium text-gray-900">
            {{ isNew ? t("new_patient") : t("edit_patient") }}
          </h3>
          <p class="mt-1 max-w-2xl text-sm text-gray-500">
            {{ t("personal_details_and_appointment_history") }}
          </p>
        </div>
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
                <div class="grid grid-cols-2 gap-4">
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
                  id="dob"
                  v-model="patient.dob"
                  type="date"
                  required
                  class="block w-full px-3 py-2 placeholder-gray-400 border border-gray-300 rounded-md shadow-sm appearance-none focus:outline-none focus:ring-primary focus:border-primary sm:text-sm"
                />
                <p v-if="errors.dob" class="mt-1 text-sm text-red-600">
                  {{ errors.dob }}
                </p>
              </dd>
            </div>
            <div
              class="bg-white px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6"
            >
              <dt class="text-sm font-medium text-gray-500">
                {{ t("email_address") }}
              </dt>
              <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                <input
                  id="email"
                  v-model="patient.email"
                  type="email"
                  class="block w-full px-3 py-2 mt-1 placeholder-gray-400 border border-gray-300 rounded-md shadow-sm appearance-none focus:outline-none focus:ring-primary focus:border-primary sm:text-sm"
                />
                <p v-if="errors.email" class="mt-1 text-sm text-red-600">
                  {{ errors.email }}
                </p>
              </dd>
            </div>
            <div
              class="bg-gray-50 px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6"
            >
              <dt class="text-sm font-medium text-gray-500">
                {{ t("contact_info") }}
              </dt>
              <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                <div class="grid grid-cols-2 gap-4">
                  <div>
                    <label for="cellphone" class="sr-only">{{
                      t("cell_phone")
                    }}</label>
                    <input
                      id="cellphone"
                      v-model="patient.cellphone"
                      type="text"
                      :placeholder="t('cell_phone')"
                      class="block w-full px-3 py-2 mt-1 placeholder-gray-400 border border-gray-300 rounded-md shadow-sm appearance-none focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                    />
                  </div>
                  <div>
                    <label for="phone" class="sr-only">{{
                      t("phone_number")
                    }}</label>
                    <input
                      id="phone"
                      v-model="patient.phone"
                      type="text"
                      :placeholder="t('phone_number')"
                      class="block w-full px-3 py-2 mt-1 placeholder-gray-400 border border-gray-300 rounded-md shadow-sm appearance-none focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                    />
                  </div>
                </div>
              </dd>
            </div>
            <div
              class="bg-gray-50 px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6"
            >
              <dt class="text-sm font-medium text-gray-500">
                {{ t("address") }}
              </dt>
              <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                <input
                  id="address"
                  v-model="patient.address"
                  type="text"
                  class="block w-full px-3 py-2 mt-1 placeholder-gray-400 border border-gray-300 rounded-md shadow-sm appearance-none focus:outline-none focus:ring-primary focus:border-primary sm:text-sm"
                />
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
              </dd>
            </div>
          </dl>
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
                    :class="{
                      'line-through text-gray-500': appointment.cancelled,
                    }"
                  >
                    <td
                      class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900"
                    >
                      {{ formatDate(appointment.start_time) }}
                      {{ formatTime(appointment.start_time) }}
                    </td>
                    <td
                      class="px-6 py-4 whitespace-nowrap text-sm text-gray-500"
                    >
                      {{ appointment.specialty.name }}
                    </td>
                    <td
                      class="px-6 py-4 whitespace-nowrap text-sm text-gray-500"
                    >
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

          <div class="flex justify-end mt-6 px-4 py-5 sm:px-6">
            <router-link
              :to="`/patients/${route.params.id}`"
              class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md shadow-sm hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary"
            >
              {{ t("cancel") }}
            </router-link>
            <button
              type="submit"
              class="px-4 py-2 ml-3 text-sm font-medium text-white bg-primary border border-transparent rounded-md shadow-sm hover:bg-primary-dark focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary"
            >
              {{ t("save") }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import { useRoute, useRouter } from "vue-router";
import api from "@/services/api";
import { formatDateForInput } from "@/utils/formatDate";
import { useI18n } from "vue-i18n";
import MarkdownIt from "markdown-it";
import DOMPurify from "dompurify";

const { t } = useI18n();
const route = useRoute();
const router = useRouter();
const patient = ref({
  name: "",
  nickname: undefined,
  dob: undefined,
  cellphone: undefined,
  email: undefined,
  phone: undefined,
  address: undefined,
  medical_history: undefined,
  default_specialty_id: null,
});
const specialties = ref([]);
const errors = ref({});

const isNew = computed(() => !route.params.id);

const activeTab = ref("medical_history");
const md = new MarkdownIt();

const renderedMedicalHistory = computed(() => {
  if (patient.value && patient.value.medical_history) {
    return DOMPurify.sanitize(md.render(patient.value.medical_history));
  }
  return "";
});

const appointments = ref([]);
const showCancelledAppointments = ref(false);

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

const fetchAppointments = async () => {
  if (isNew.value) return;
  try {
    const response = await api.get(`/patients/${route.params.id}/appointments`);
    appointments.value = response.data;
  } catch (error) {
    console.error("Error fetching appointments:", error);
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

const fetchPatient = async () => {
  if (isNew.value) return;
  try {
    const response = await api.get(`/patients/${route.params.id}`);
    patient.value = { ...response.data };
    if (patient.value.dob) {
      patient.value.dob = formatDateForInput(patient.value.dob);
    }
  } catch (error) {
    console.error("Error fetching patient:", error);
  }
};

onMounted(() => {
  fetchPatient();
  fetchSpecialties();
  fetchAppointments();
});

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

  console.log("Saving patient:", patient.value);
  try {
    if (isNew.value) {
      await api.post("/patients", patient.value);
    } else {
      await api.put(`/patients/${route.params.id}`, patient.value);
    }
    router.push("/patients");
  } catch (error) {
    console.error("Error saving patient:", error);
  }
};
</script>
