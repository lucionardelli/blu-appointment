<template>
  <div class="flex h-screen bg-gray-100">
    <TheSidebar
      :sidebar-open="sidebarOpen"
      @toggle-sidebar="sidebarOpen = !sidebarOpen"
    />
    <div class="flex-1 flex flex-col overflow-hidden">
      <TheHeader @toggle-sidebar="sidebarOpen = !sidebarOpen" />
      <main class="flex-1 overflow-x-hidden overflow-y-auto bg-gray-200">
        <div class="container mx-auto px-2 py-4 sm:px-6 sm:py-8">
          <router-view />
        </div>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import TheSidebar from "@/components/TheSidebar.vue";
import TheHeader from "@/components/TheHeader.vue";

const sidebarOpen = ref(false);
</script>
