<template>
  <header
    class="flex items-center justify-between px-6 py-4 bg-white border-b-4 border-primary"
  >
    <div class="flex items-center">
      <button
        class="text-gray-500 focus:outline-none lg:hidden"
        @click="$emit('toggle-sidebar')"
      >
        <svg
          class="w-6 h-6"
          viewBox="0 0 24 24"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
        >
          <path
            d="M4 6H20M4 12H20M4 18H11Z"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
          />
        </svg>
      </button>
    </div>
    <div class="flex items-center">
      <div class="relative">
        <button
          class="relative block w-8 h-8 overflow-hidden rounded-full shadow focus:outline-none"
          @click="dropdownOpen = !dropdownOpen"
        >
          <div
            :style="{ backgroundColor: userColor }"
            class="w-full h-full flex items-center justify-center text-white font-semibold"
          >
            {{ userInitials }}
          </div>
        </button>
        <div
          v-show="dropdownOpen"
          class="fixed inset-0 z-10 w-full h-full"
          @click="dropdownOpen = false"
        ></div>
        <div
          v-show="dropdownOpen"
          class="absolute right-0 z-10 w-48 mt-2 overflow-hidden bg-white rounded-md shadow-xl"
        >
          <router-link
            to="/profile"
            class="block px-4 py-2 text-sm text-gray-700 hover:bg-primary hover:text-white"
            >{{ t("profile") }}</router-link
          >
          <a
            href="#"
            class="block px-4 py-2 text-sm text-gray-700 hover:bg-primary hover:text-white"
            @click.prevent="logout"
            >{{ t("logout") }}</a
          >
        </div>
      </div>
    </div>
  </header>
</template>

<script setup>
import { ref, computed } from "vue";
import { useAuthStore } from "@/stores/auth";
import { useRouter } from "vue-router";
import { useI18n } from "vue-i18n";

const { t } = useI18n();

const dropdownOpen = ref(false);
const authStore = useAuthStore();
const router = useRouter();

const userInitials = computed(() => {
  if (authStore.user) {
    if (authStore.user.name && authStore.user.last_name) {
      return `${authStore.user.name[0]}${authStore.user.last_name[0]}`.toUpperCase();
    }
    if (authStore.user.name) {
      return `${authStore.user.name[0]}`.toUpperCase();
    }
    if (authStore.user.username) {
      return `${authStore.user.username[0]}`.toUpperCase();
    }
  }
  return "";
});

const userColor = computed(() => {
  if (authStore.user && authStore.user.name) {
    let hash = 0;
    for (let i = 0; i < authStore.user.name.length; i++) {
      hash = authStore.user.name.charCodeAt(i) + ((hash << 5) - hash);
    }
    let color = "#";
    for (let i = 0; i < 3; i++) {
      const value = (hash >> (i * 8)) & 0xff;
      color += ("00" + value.toString(16)).substr(-2);
    }
    return color;
  }
  return "#cccccc"; // Default color
});

const logout = () => {
  authStore.logout();
  router.push("/login");
};
</script>
