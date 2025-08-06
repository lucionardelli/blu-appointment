<template>
  <div>
    <h1 class="text-2xl font-semibold text-gray-900">
      {{ isNew ? "New Patient" : "Edit Patient" }}
    </h1>
    <form class="mt-6" @submit.prevent="savePatient">
      <div class="space-y-6">
        <div>
          <label for="name" class="block text-sm font-medium text-gray-700"
            >Name</label
          >
          <input
            id="name"
            v-model="patient.name"
            type="text"
            required
            class="block w-full px-3 py-2 mt-1 placeholder-gray-400 border border-gray-300 rounded-md shadow-sm appearance-none focus:outline-none focus:ring-primary focus:border-primary sm:text-sm"
          />
          <p v-if="errors.name" class="mt-1 text-sm text-red-600">
            {{ errors.name }}
          </p>
        </div>
        <div>
          <label for="dob" class="block text-sm font-medium text-gray-700"
            >Date of Birth</label
          >
          <input
            id="dob"
            v-model="patient.dob"
            type="date"
            required
            class="block w-full px-3 py-2 mt-1 placeholder-gray-400 border border-gray-300 rounded-md shadow-sm appearance-none focus:outline-none focus:ring-primary focus:border-primary sm:text-sm"
          />
          <p v-if="errors.dob" class="mt-1 text-sm text-red-600">
            {{ errors.dob }}
          </p>
        </div>
        <div>
          <label for="cellphone" class="block text-sm font-medium text-gray-700"
            >Cell Phone</label
          >
          <input
            id="cellphone"
            v-model="patient.cellphone"
            type="text"
            class="block w-full px-3 py-2 mt-1 placeholder-gray-400 border border-gray-300 rounded-md shadow-sm appearance-none focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
          />
        </div>
        <div>
          <label for="email" class="block text-sm font-medium text-gray-700"
            >Email</label
          >
          <input
            id="email"
            v-model="patient.email"
            type="email"
            class="block w-full px-3 py-2 mt-1 placeholder-gray-400 border border-gray-300 rounded-md shadow-sm appearance-none focus:outline-none focus:ring-primary focus:border-primary sm:text-sm"
          />
          <p v-if="errors.email" class="mt-1 text-sm text-red-600">
            {{ errors.email }}
          </p>
        </div>
        <div>
          <label for="phone" class="block text-sm font-medium text-gray-700"
            >Phone Number</label
          >
          <input
            id="phone"
            v-model="patient.phone"
            type="text"
            class="block w-full px-3 py-2 mt-1 placeholder-gray-400 border border-gray-300 rounded-md shadow-sm appearance-none focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
          />
        </div>
        <div>
          <label for="address" class="block text-sm font-medium text-gray-700"
            >Address</label
          >
          <input
            id="address"
            v-model="patient.address"
            type="text"
            class="block w-full px-3 py-2 mt-1 placeholder-gray-400 border border-gray-300 rounded-md shadow-sm appearance-none focus:outline-none focus:ring-primary focus:border-primary sm:text-sm"
          />
        </div>
        <div>
          <label
            for="medical_history"
            class="block text-sm font-medium text-gray-700"
            >Medical History</label
          >
          <textarea
            id="medical_history"
            v-model="patient.medical_history"
            rows="4"
            class="block w-full px-3 py-2 mt-1 placeholder-gray-400 border border-gray-300 rounded-md shadow-sm appearance-none focus:outline-none focus:ring-primary focus:border-primary sm:text-sm"
          ></textarea>
        </div>
      </div>
      <div class="flex justify-end mt-6">
        <router-link
          to="/patients"
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
import { ref, onMounted, computed } from "vue";
import { useRoute, useRouter } from "vue-router";
import api from "@/services/api";
import { format } from "date-fns";

const route = useRoute();
const router = useRouter();
const patient = ref({
  name: "",
  dob: "",
  cellphone: "",
  email: "",
  phone: "",
  address: "",
  medical_history: "",
});

const errors = ref({});

const isNew = computed(() => !route.params.id);

const fetchPatient = async () => {
  if (isNew.value) return;
  try {
    const response = await api.get(`/patients/${route.params.id}`);
    patient.value = { ...response.data };
    if (patient.value.dob) {
      patient.value.dob = format(new Date(patient.value.dob), "yyyy-MM-dd");
    }
  } catch (error) {
    console.error("Error fetching patient:", error);
  }
};

onMounted(fetchPatient);

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
