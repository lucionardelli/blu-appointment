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
    <div class="flex items-center justify-between mt-8 px-6">
      <div class="flex items-center">
        <span v-if="!isCollapsed" class="text-2xl font-semibold text-white"
          >Blu</span
        >
        <span v-else class="text-2xl font-semibold text-white">B</span>
      </div>
      <button
        class="p-1 text-gray-200 hover:bg-primary-dark hover:bg-opacity-25 hover:text-white rounded-md focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary"
        @click="toggleCollapse"
      >
        <i-heroicons-arrow-right-start-on-rectangle-20-solid
          v-if="isCollapsed"
          class="w-6 h-6"
        />
        <i-heroicons-arrow-left-end-on-rectangle-20-solid
          v-else
          class="w-6 h-6"
        />
      </button>
    </div>
    <nav class="mt-10 px-3">
      <router-link
        v-slot="{ isActive }"
        to="/appointments"
        :title="isCollapsed ? t('appointments') : ''"
        class="flex items-center mt-4"
      >
        <div
          :class="[
            isActive
              ? 'bg-white text-primary'
              : 'text-gray-200 hover:bg-primary-dark hover:bg-opacity-25 hover:text-white',
            'flex items-center w-full h-full rounded-md px-3 py-2',
          ]"
        >
          <i-heroicons-calendar-days-20-solid class="w-6 h-6" />
          <span v-if="!isCollapsed" class="mx-3">{{ t("appointments") }}</span>
        </div>
      </router-link>
      <router-link
        v-slot="{ isActive }"
        to="/patients"
        :title="isCollapsed ? t('patients') : ''"
        class="flex items-center mt-4"
      >
        <div
          :class="[
            isActive
              ? 'bg-white text-primary'
              : 'text-gray-200 hover:bg-primary-dark hover:bg-opacity-25 hover:text-white',
            'flex items-center w-full h-full rounded-md px-3 py-2',
          ]"
        >
          <i-heroicons-user-group-20-solid class="w-6 h-6" />
          <span v-if="!isCollapsed" class="mx-3">{{ t("patients") }}</span>
        </div>
      </router-link>
      <router-link
        v-slot="{ isActive }"
        to="/dashboard"
        :title="isCollapsed ? t('dashboard') : ''"
        class="flex items-center mt-4"
      >
        <div
          :class="[
            isActive
              ? 'bg-white text-primary'
              : 'text-gray-200 hover:bg-primary-dark hover:bg-opacity-25 hover:text-white',
            'flex items-center w-full h-full rounded-md px-3 py-2',
          ]"
        >
          <i-heroicons-chart-pie-20-solid class="w-6 h-6" />
          <span v-if="!isCollapsed" class="mx-3">{{ t("dashboard") }}</span>
        </div>
      </router-link>
      <div class="mt-4">
        <button
          class="flex items-center justify-between w-full px-3 py-2 text-gray-200 hover:bg-primary-dark hover:bg-opacity-25 hover:text-white rounded-md focus:outline-none"
          @click="configurationMenuOpen = !configurationMenuOpen"
        >
          <div class="flex items-center">
            <i-heroicons-cog-8-tooth-20-solid class="w-6 h-6" />
            <span v-if="!isCollapsed" class="mx-3">{{ t("configuration") }}</span>
          </div>
          <i-heroicons-chevron-down-20-solid
            v-if="!isCollapsed"
            :class="{
              'transform rotate-180': configurationMenuOpen,
            }"
            class="w-5 h-5 transition-transform duration-200"
          />
        </button>
        <div v-if="configurationMenuOpen && !isCollapsed" class="pl-8">
          <router-link
            v-slot="{ isActive }"
            to="/specialties"
            class="flex items-center mt-2"
          >
            <div
              :class="[
                isActive
                  ? 'bg-white text-primary'
                  : 'text-gray-200 hover:bg-primary-dark hover:bg-opacity-25 hover:text-white',
                'flex items-center w-full h-full rounded-md px-3 py-2',
              ]"
            >
              <i-heroicons-briefcase-20-solid class="w-6 h-6" />
              <span class="mx-3">{{ t("specialties") }}</span>
            </div>
          </router-link>
          <router-link
            v-slot="{ isActive }"
            to="/payment-methods"
            class="flex items-center mt-2"
          >
            <div
              :class="[
                isActive
                  ? 'bg-white text-primary'
                  : 'text-gray-200 hover:bg-primary-dark hover:bg-opacity-25 hover:text-white',
                'flex items-center w-full h-full rounded-md px-3 py-2',
              ]"
            >
              <i-heroicons-credit-card-20-solid class="w-6 h-6" />
              <span class="mx-3">{{ t("payment_methods") }}</span>
            </div>
          </router-link>
          <router-link
            v-slot="{ isActive }"
            to="/working-hours"
            class="flex items-center mt-2"
          >
            <div
              :class="[
                isActive
                  ? 'bg-white text-primary'
                  : 'text-gray-200 hover:bg-primary-dark hover:bg-opacity-25 hover:text-white',
                'flex items-center w-full h-full rounded-md px-3 py-2',
              ]"
            >
              <i-heroicons-clock-20-solid class="w-6 h-6" />
              <span class="mx-3">{{ t("working_hours") }}</span>
            </div>
          </router-link>
        </div>
      </div>
    </nav>
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
const configurationMenuOpen = ref(false);

const toggleCollapse = () => {
  isCollapsed.value = !isCollapsed.value;
};
</script>
