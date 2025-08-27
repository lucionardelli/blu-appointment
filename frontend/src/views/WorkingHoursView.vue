<template>
  <div class="p-4 sm:p-6 lg:p-8">
    <div class="flex items-center justify-between mb-6">
      <h1 class="text-2xl font-semibold text-gray-900">
        {{ t("working_hours") }}
      </h1>
      <button
        class="px-4 py-2 text-sm font-medium text-white bg-primary border border-transparent rounded-md shadow-sm hover:bg-primary-dark focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary"
        @click="saveWorkingHours"
      >
        {{ t("save") }}
      </button>
    </div>
    <div class="space-y-4">
      <div v-for="day in workingHours" :key="day.id">
        <h2 class="text-lg font-medium text-gray-900">
          {{ t(day.dayOfWeek) }}
        </h2>
        <div class="mt-2 p-4 bg-white rounded-md shadow-sm">
          <div class="flex items-center justify-between">
            <div class="flex items-center">
              <input
                :id="`is_closed_${day.id}`"
                v-model="day.is_closed"
                type="checkbox"
                class="rounded h-4 w-4 text-primary border-gray-300 focus:ring-primary"
              />
              <label
                :for="`is_closed_${day.id}`"
                class="ml-2 text-sm text-gray-600"
                >{{ t("closed") }}</label
              >
            </div>
            <div v-if="!day.is_closed" class="flex items-center space-x-4">
              <div>
                <label
                  :for="`start_time_${day.id}`"
                  class="block text-sm font-medium text-gray-700"
                  >{{ t("start_time") }}</label
                >
                <DatePicker
                  v-model="day.startTime"
                  time-picker
                  :minutes-increment="15"
                  text-input
                  auto-apply
                  utc
                  :locale="locale"
                  class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary focus:ring-primary sm:text-sm"
                />
              </div>
              <div>
                <label
                  :for="`end_time_${day.id}`"
                  class="block text-sm font-medium text-gray-700"
                  >{{ t("end_time") }}</label
                >
                <DatePicker
                  v-model="day.endTime"
                  time-picker
                  :minutes-increment="15"
                  text-input
                  auto-apply
                  utc
                  :locale="locale"
                  class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary focus:ring-primary sm:text-sm"
                />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useI18n } from "vue-i18n";
import { useSettingsStore } from "@/stores/settings";
import DatePicker from "@vuepic/vue-datepicker";
import "@vuepic/vue-datepicker/dist/main.css";

const { t, locale } = useI18n();
const settingsStore = useSettingsStore();

const workingHours = ref([]);

const fetchWorkingHours = async () => {
  await settingsStore.fetchWorkingHours();
  workingHours.value = settingsStore.workingHoursRaw.map((day) => {
    const [startHours, startMinutes] = day.startTime.split(":").map(Number);
    const [endHours, endMinutes] = day.endTime.split(":").map(Number);
    return {
      ...day,
      startTime: { hours: startHours, minutes: startMinutes },
      endTime: { hours: endHours, minutes: endMinutes },
    };
  });
};

const saveWorkingHours = async () => {
  try {
    const formattedWorkingHours = workingHours.value.map((day) => {
      const formatTime = (time) => {
        if (!time) {
          return "00:00:00";
        }
        const hours = String(time.hours).padStart(2, "0");
        const minutes = String(time.minutes).padStart(2, "0");
        return `${hours}:${minutes}:00`;
      };

      return {
        ...day,
        startTime: formatTime(day.startTime),
        endTime: formatTime(day.endTime),
      };
    });
    await settingsStore.updateWorkingHours(formattedWorkingHours);
  } catch (error) {
    console.error("Error saving working hours:", error);
  }
};

onMounted(() => {
  fetchWorkingHours();
});
</script>
