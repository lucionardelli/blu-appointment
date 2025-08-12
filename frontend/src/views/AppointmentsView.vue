<template>
  <div>
    <div class="flex items-center justify-between mb-6">
      <h1 class="text-2xl font-semibold text-gray-900">
        {{ t("appointments") }}
      </h1>
      <button
        class="px-4 py-2 text-sm font-medium text-white bg-primary border border-transparent rounded-md shadow-sm hover:bg-primary-dark focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary"
        @click="openNewAppointmentModal"
      >
        {{ t("new_appointment") }}
      </button>
    </div>
    <FullCalendar :options="calendarOptions" />
    <AppointmentFormModal
      v-if="showModal"
      :initial-date="selectedDate"
      :initial-end-date="selectedEndDate"
      :appointment-id="selectedAppointmentId"
      @close="showModal = false"
      @save="handleSave"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import { useI18n } from "vue-i18n";
import FullCalendar from "@fullcalendar/vue3";
import dayGridPlugin from "@fullcalendar/daygrid";
import timeGridPlugin from "@fullcalendar/timegrid";
import interactionPlugin from "@fullcalendar/interaction";
import api from "@/services/api";
import AppointmentFormModal from "@/components/appointments/AppointmentFormModal.vue";

const { t } = useI18n();

const appointments = ref([]);
const workingHours = ref({
  start: "09:00",
  end: "18:00",
}); // Placeholder
const showModal = ref(false);
const selectedDate = ref("");
const selectedEndDate = ref("");
const selectedAppointmentId = ref(null);

const fetchAppointments = async () => {
  try {
    const response = await api.get("/appointments");
    appointments.value = response.data;
  } catch (error) {
    console.error("Error fetching appointments:", error);
  }
};

onMounted(fetchAppointments);

const openNewAppointmentModal = () => {
  selectedAppointmentId.value = null; // Ensure it's null for new appointments
  selectedDate.value = ""; // Clear any previously selected date
  showModal.value = true;
};

const calendarOptions = computed(() => ({
  plugins: [dayGridPlugin, timeGridPlugin, interactionPlugin],
  initialView: "timeGridWeek",
  headerToolbar: {
    left: "prev,next today",
    center: "title",
    right: "dayGridMonth,timeGridWeek,timeGridDay",
  },
  events: appointments.value.map((appointment) => ({
    title: appointment.patient.nickname || appointment.patient.name,
    start: appointment.start_time,
    end: appointment.end_time,
    extendedProps: {
      appointment,
      specialty: appointment.specialty.name,
    },
    // Add visual cues
    backgroundColor: getEventColor(appointment),
    borderColor: getEventColor(appointment),
  })),
  selectable: true,
  select: (arg) => {
    selectedAppointmentId.value = null; // New appointment
    selectedDate.value = arg.startStr;
    selectedEndDate.value = arg.endStr;
    showModal.value = true;
  },
  dateClick: (arg) => {
    if (arg.jsEvent.target.closest(".fc-event")) {
      return;
    }
    selectedAppointmentId.value = null; // New appointment
    selectedDate.value = arg.dateStr;
    showModal.value = true;
  },
  eventClick: (info) => {
    selectedAppointmentId.value = info.event.extendedProps.appointment.id;
    selectedDate.value = info.event.extendedProps.appointment.start_time;
    selectedEndDate.value = info.event.extendedProps.appointment.end_time;
    showModal.value = true;
  },
  // Correctly placed eventContent function
  eventContent: (arg) => {
    const appointment = arg.event.extendedProps.appointment;
    const patientName =
      appointment.patient.nickname || appointment.patient.name;

    // Check duration
    const start = new Date(arg.event.start);
    const end = new Date(arg.event.end);
    const durationMinutes = (end - start) / (1000 * 60);
    const isShort = durationMinutes < 30;

    let mainContent = `<div class="flex-grow overflow-hidden text-ellipsis whitespace-nowrap"><b>${patientName}</b>`;
    if (appointment.specialty) {
      mainContent += `<div class="text-sm text-gray-600"><i>${appointment.specialty.name}</i></div>`;
    }
    mainContent += `</div>`;

    let icons = "";
    let tooltipWarnings = [];

    if (isDoubleBooked(appointment)) {
      if (isShort) {
        tooltipWarnings.push("Double-booked");
      } else {
        icons +=
          '<span class="text-yellow-500" title="Double-booked">⚠️</span>';
      }
    }
    if (isOutsideWorkingHours(appointment)) {
      if (isShort) {
        tooltipWarnings.push("Outside working hours");
      } else {
        icons +=
          '<span class="text-blue-500" title="Outside working hours">⏰</span>';
      }
    }

    let content = `<div class="flex items-center justify-between w-full">${mainContent}`;
    if (icons) {
      content += `<div class="flex-shrink-0 ml-1">${icons}</div>`;
    }
    content += `</div>`;

    if (appointment.cancelled) {
      content = `<div class="line-through text-gray-500">${content}</div>`;
    }

    let fullContent = `${patientName} (${appointment.specialty.name})`;
    if (tooltipWarnings.length > 0) {
      fullContent += ` - ${tooltipWarnings.join(", ")}`;
    }
    if (appointment.cancelled) {
      fullContent += " (Cancelled)";
    }

    return {
      html: `<div class="w-full" title="${fullContent.replace(/"/g, "'")}">${content}</div>`,
    };
  },
}));

const handleSave = () => {
  showModal.value = false;
  fetchAppointments();
};

// Move these to the BE as an attribute of the specialty
const specialtyColors = {
  1: "#10B981", // Therapy
  2: "#3B82F6", // Bluroom
};

const getEventColor = (appointment) => {
  const baseColor = specialtyColors[appointment.specialty.id] || "#4F46E5";
  // If appointment is on the past, show it as greyed out
  if (new Date(appointment.start_time) < new Date()) {
    return applyOpacity(baseColor, 0.2);
  }
  return appointment.cancelled ? applyOpacity(baseColor, 0.1) : baseColor;
};

function applyOpacity(hex, opacity) {
  // Simple hex to rgba converter
  const bigint = parseInt(hex.slice(1), 16);
  const r = (bigint >> 16) & 255;
  const g = (bigint >> 8) & 255;
  const b = bigint & 255;
  return `rgba(${r}, ${g}, ${b}, ${opacity})`;
}

const isDoubleBooked = (appointment) => {
  const start = new Date(appointment.start_time);
  const end = new Date(appointment.end_time);
  return appointments.value.some((other) => {
    if (other.id === appointment.id) return false;
    const otherStart = new Date(other.start_time);
    const otherEnd = new Date(other.end_time);
    return (
      (start >= otherStart && start < otherEnd) ||
      (end > otherStart && end <= otherEnd) ||
      (start <= otherStart && end >= otherEnd)
    );
  });
};

const isOutsideWorkingHours = (appointment) => {
  const start = new Date(appointment.start_time);
  const startTime = `${start.getHours().toString().padStart(2, "0")}:${start.getMinutes().toString().padStart(2, "0")}`;
  return (
    startTime < workingHours.value.start || startTime > workingHours.value.end
  );
};
</script>
