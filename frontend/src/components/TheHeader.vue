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
          <img
            class="object-cover w-full h-full"
            src="https://images.unsplash.com/photo-1528892952291-009c663ce843?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=296&q=80"
            alt="Your avatar"
          />
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
            >Profile</router-link
          >
          <a
            href="#"
            class="block px-4 py-2 text-sm text-gray-700 hover:bg-primary hover:text-white"
            @click.prevent="logout"
            >Logout</a
          >
        </div>
      </div>
    </div>
  </header>
</template>

<script setup>
import { ref } from "vue";
import { useAuthStore } from "@/stores/auth";
import { useRouter } from "vue-router";

const dropdownOpen = ref(false);
const authStore = useAuthStore();
const router = useRouter();

const logout = () => {
  authStore.logout();
  router.push("/login");
};
</script>
