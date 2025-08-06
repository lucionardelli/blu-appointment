<template>
  <component :is="layout">
    <router-view />
  </component>
</template>

<script setup>
import { computed } from "vue";
import { useRoute } from "vue-router";
import MainLayout from "@/layouts/MainLayout.vue";
import { useAuthStore } from "./stores/auth";

const route = useRoute();
const authStore = useAuthStore();

const layout = computed(() => {
  if (route.meta.requiresAuth && authStore.isAuthenticated) {
    return MainLayout;
  } else if (route.name === "login" && !authStore.isAuthenticated) {
    return "div"; // Use a simple div for the login view
  }
  return "div";
});
</script>
