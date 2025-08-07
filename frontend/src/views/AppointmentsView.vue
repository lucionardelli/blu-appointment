<template>
  <div>
    <div class="flex items-center justify-between mb-6">
      <h1 class="text-2xl font-semibold text-gray-900">Appointments</h1>
      <router-link
        to="/appointments/new"
        class="px-4 py-2 text-sm font-medium text-white bg-primary border border-transparent rounded-md shadow-sm hover:bg-primary-dark focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary"
      >
        New Appointment
      </router-link>
    </div>
    <FullCalendar :options="calendarOptions" />
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import { useRouter } from "vue-router";
import FullCalendar from "@fullcalendar/vue3";
import dayGridPlugin from "@fullcalendar/daygrid";
import timeGridPlugin from "@fullcalendar/timegrid";
import interactionPlugin from "@fullcalendar/interaction";
import api from "@/services/api";

const appointments = ref([]);
const workingHours = ref({
  start: "09:00",
  end: "18:00",
}); // Placeholder
const router = useRouter();

const fetchAppointments = async () => {
  try {
    const response = await api.get("/appointments");
    appointments.value = response.data;
  } catch (error) {
    console.error("Error fetching appointments:", error);
  }
};

onMounted(fetchAppointments);

const calendarOptions = computed(() => ({
  plugins: [dayGridPlugin, timeGridPlugin, interactionPlugin],
  initialView: "timeGridWeek",
  headerToolbar: {
    left: "prev,next today",
    center: "title",
    right: "dayGridMonth,timeGridWeek,timeGridDay",
  },
  events: appointments.value.map((appointment) => ({
    patient: appointment.patient.name,
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
  eventClick: (info) => {
    router.push(`/appointments/${info.event.extendedProps.appointment.id}`);
  },
  // Correctly placed eventContent function
  eventContent: (arg) => {
    const appointment = arg.event.extendedProps.appointment;
    let content = `<div><b>${appointment.patient.name}</b></div>`;

    if (appointment.specialty) {
      content += `<div class="text-sm text-gray-600"><i>${appointment.specialty.name}</i></div>`;
    }
    if (isDoubleBooked(appointment)) {
      content +=
        '<span class="ml-1 text-yellow-500" title="Double-booked">⚠️</span>';
    }
    if (isOutsideWorkingHours(appointment)) {
      content +=
        '<span class="ml-1 text-blue-500" title="Outside working hours">⏰</span>';
    }
    if (appointment.cancelled) {
      content = `<div class="line-through text-gray-500">${content}</div>`;
    }
    return { html: content };
  },
}));

// Move these to the BE as an attribute of the specialty
const specialtyColors = {
  1: "#10B981", // Therapy
  2: "#3B82F6", // Bluroom
};

const getEventColor = (appointment) => {
  const baseColor = specialtyColors[appointment.specialty.id] || "#4F46E5";
  return appointment.cancelled ? applyOpacity(baseColor, 0.4) : baseColor;
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
