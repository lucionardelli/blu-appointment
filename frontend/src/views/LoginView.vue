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
          <div class="relative">
            <input
              id="password"
              v-model="password"
              :type="showPassword ? 'text' : 'password'"
              required
              class="block w-full px-3 py-2 mt-1 placeholder-gray-400 border border-gray-300 rounded-md shadow-sm appearance-none focus:outline-none focus:ring-primary focus:border-primary sm:text-sm"
            />
            <button
              type="button"
              class="absolute inset-y-0 right-0 flex items-center px-3 text-gray-500"
              @click="showPassword = !showPassword"
            >
              <i-heroicons-eye-20-solid
                v-if="!showPassword"
                class="h-6 w-6 text-gray-500"
              />
              <i-heroicons-eye-slash-20-solid
                v-else
                class="h-6 w-6 text-gray-500"
              />
            </button>
          </div>
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
const showPassword = ref(false);
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
