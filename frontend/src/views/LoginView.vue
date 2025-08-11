<template>
  <div
    class="flex items-center justify-center min-h-screen bg-gray-100 font-sans"
  >
    <div class="w-full max-w-md p-8 space-y-6 bg-white rounded-lg shadow-md">
      <h1 class="text-2xl font-bold text-center text-gray-900">
        {{ t("login") }}
      </h1>
      <form class="space-y-6" @submit.prevent="login">
        <div>
          <label
            for="username"
            class="block text-sm font-medium text-gray-700"
            >{{ t("username") }}</label
          >
          <input
            id="username"
            v-model="username"
            type="text"
            required
            class="block w-full px-3 py-2 mt-1 placeholder-gray-400 border border-gray-300 rounded-md shadow-sm appearance-none focus:outline-none focus:ring-primary focus:border-primary sm:text-sm"
          />
        </div>
        <div>
          <label
            for="password"
            class="block text-sm font-medium text-gray-700"
            >{{ t("password") }}</label
          >
          <input
            id="password"
            v-model="password"
            type="password"
            required
            class="block w-full px-3 py-2 mt-1 placeholder-gray-400 border border-gray-300 rounded-md shadow-sm appearance-none focus:outline-none focus:ring-primary focus:border-primary sm:text-sm"
          />
        </div>
        <div>
          <button
            type="submit"
            class="w-full px-4 py-2 text-sm font-medium text-white bg-primary border border-transparent rounded-md shadow-sm hover:bg-primary-dark focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary"
          >
            {{ t("login") }}
          </button>
        </div>
      </form>
      <p v-if="error" class="text-sm text-center text-red-600">{{ error }}</p>
    </div>
  </div>
</template>

<script setup>
import { useI18n } from "vue-i18n";
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "@/stores/auth";

const { t } = useI18n();

const username = ref("");
const password = ref("");
const error = ref(null);
const router = useRouter();
const authStore = useAuthStore();

const login = async () => {
  try {
    await authStore.login(username.value, password.value);
    router.push("/");
  } catch {
    error.value = t("invalid_credentials");
  }
};
</script>
