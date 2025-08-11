<template>
  <component :is="layout">
    <div class="absolute top-4 right-4 flex items-center space-x-4">
      <LanguageSwitcher />
    </div>
    <router-view />
  </component>
</template>

<script setup>
import { computed, watch, onMounted } from "vue";
import { useRoute } from "vue-router";
import { useI18n } from "vue-i18n";
import MainLayout from "@/layouts/MainLayout.vue";
import LanguageSwitcher from "@/components/LanguageSwitcher.vue";
import { useAuthStore } from "./stores/auth";

const route = useRoute();
const authStore = useAuthStore();
const { locale } = useI18n();

const layout = computed(() => {
  if (route.meta.requiresAuth && authStore.isAuthenticated) {
    return MainLayout;
  } else if (route.name === "login" && !authStore.isAuthenticated) {
    return "div"; // Use a simple div for the login view
  }
  return "div";
});

watch(
  () => authStore.user,
  (user) => {
    if (user) {
      locale.value = user.language;
    } else {
      locale.value = "en";
    }
  },
  { immediate: true },
);

onMounted(() => {
  authStore.initialize();
});
</script>
