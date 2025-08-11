<template>
  <div
    :class="sidebarOpen ? 'block' : 'hidden'"
    class="fixed inset-0 z-20 transition-opacity bg-black opacity-50 lg:hidden"
    @click="emit('toggle-sidebar')"
  ></div>
  <div
    :class="[
      sidebarOpen ? 'translate-x-0 ease-out' : '-translate-x-full ease-in',
      isCollapsed ? 'w-20' : 'w-64',
    ]"
    class="fixed inset-y-0 left-0 z-30 overflow-y-auto transition duration-300 transform bg-primary lg:translate-x-0 lg:static lg:inset-0 rounded-r-lg"
  >
    <div class="flex items-center justify-center mt-8">
      <div class="flex items-center">
        <span v-if="!isCollapsed" class="text-2xl font-semibold text-white"
          >Blu</span
        >
        <span v-else class="text-2xl font-semibold text-white">B</span>
      </div>
    </div>
    <nav class="mt-10">
      <router-link
        class="flex items-center px-6 py-2 mt-4 text-gray-200 hover:bg-primary-dark hover:bg-opacity-25 hover:text-white"
        to="/appointments"
        :title="isCollapsed ? t('appointments') : ''"
      >
        <svg
          class="w-6 h-6"
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"
          />
        </svg>
        <span v-if="!isCollapsed" class="mx-3">{{ t("appointments") }}</span>
      </router-link>
      <router-link
        class="flex items-center px-6 py-2 mt-4 text-gray-200 hover:bg-primary-dark hover:bg-opacity-25 hover:text-white"
        to="/patients"
        :title="isCollapsed ? t('patients') : ''"
      >
        <svg
          class="w-6 h-6"
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.653-.28-1.25-.743-1.667M11 12a4 4 0 11-8 0 4 4 0 018 0z"
          />
        </svg>
        <span v-if="!isCollapsed" class="mx-3">{{ t("patients") }}</span>
      </router-link>
      <router-link
        class="flex items-center px-6 py-2 mt-4 text-gray-200 hover:bg-primary-dark hover:bg-opacity-25 hover:text-white"
        to="/dashboard"
        :title="isCollapsed ? t('dashboard') : ''"
      >
        <svg
          class="w-6 h-6"
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M11 3.055A9.001 9.001 0 1020.945 13H11V3.055z"
          />
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M20.488 9H15V3.512A9.025 9.025 0 0120.488 9z"
          />
        </svg>
        <span v-if="!isCollapsed" class="mx-3">{{ t("dashboard") }}</span>
      </router-link>
      <router-link
        class="flex items-center px-6 py-2 mt-4 text-gray-200 hover:bg-primary-dark hover:bg-opacity-25 hover:text-white"
        to="/specialties"
        :title="isCollapsed ? t('specialties') : ''"
      >
        <svg
          class="w-6 h-6"
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M5 8h14M5 8a2 2 0 110-4h14a2 2 0 110 4M5 8v10a2 2 0 002 2h10a2 2 0 002-2V8m-9 4h4"
          />
        </svg>
        <span v-if="!isCollapsed" class="mx-3">{{ t("specialties") }}</span>
      </router-link>
    </nav>
    <div class="absolute bottom-0 left-0 w-full p-4">
      <button
        class="w-full flex items-center justify-center py-2 text-gray-200 hover:bg-primary-dark hover:bg-opacity-25 hover:text-white rounded-md focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary"
        @click="toggleCollapse"
      >
        <svg
          v-if="isCollapsed"
          class="w-6 h-6"
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M13 5l7 7-7 7M5 12h14"
          />
        </svg>
        <svg
          v-else
          class="w-6 h-6"
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M11 19l-7-7 7-7m8 14l-7-7 7-7"
          />
        </svg>
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useI18n } from "vue-i18n";

const { t } = useI18n();

const { sidebarOpen } = defineProps({
  sidebarOpen: {
    type: Boolean,
    required: true,
  },
});

const emit = defineEmits(["toggle-sidebar"]);

const isCollapsed = ref(false);

const toggleCollapse = () => {
  isCollapsed.value = !isCollapsed.value;
};
</script>
