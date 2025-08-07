<template>
  <div
    class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50"
    @click.self="$emit('close')"
  >
    <div
      class="relative top-20 mx-auto p-5 border w-full max-w-4xl shadow-lg rounded-md bg-white"
    >
      <button
        class="absolute top-0 right-0 mt-4 mr-4 text-gray-400 hover:text-gray-600"
        @click="$emit('close')"
      >
        <svg
          class="w-6 h-6"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
          xmlns="http://www.w3.org/2000/svg"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M6 18L18 6M6 6l12 12"
          ></path>
        </svg>
      </button>
      <AppointmentForm
        :initial-date="initialDate"
        :appointment-id="appointmentId"
        in-modal
        @save="handleSave"
        @cancel="$emit('close')"
      />
    </div>
  </div>
</template>

<script setup>
import { onMounted, onUnmounted } from "vue";
import AppointmentForm from "./AppointmentForm.vue";

defineProps({
  initialDate: {
    type: String,
    default: "",
  },
  appointmentId: {
    type: [String, Number],
    default: null,
  },
});

const emit = defineEmits(["close", "save"]);

const handleSave = () => {
  emit("save");
  emit("close");
};

const handleKeydown = (e) => {
  if (e.key === "Escape") {
    emit("close");
  }
};

onMounted(() => {
  document.addEventListener("keydown", handleKeydown);
});

onUnmounted(() => {
  document.removeEventListener("keydown", handleKeydown);
});
</script>
