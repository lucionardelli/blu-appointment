<template>
  <div>
    <div v-if="user">
      <div class="bg-white shadow overflow-hidden sm:rounded-lg">
        <div class="px-4 py-5 sm:px-6 flex justify-between items-center">
          <div class="flex items-center">
            <button
              v-if="isEditing || showPasswordChange"
              class="mr-2 p-1 rounded-full hover:bg-gray-200"
              @click="cancelAction"
            >
              <i-heroicons-arrow-left-20-solid class="h-6 w-6 text-gray-500" />
            </button>
            <h3 class="text-lg leading-6 font-medium text-gray-900">
              <span v-if="isEditing">{{ t("edit_profile") }}</span>
              <span v-else-if="showPasswordChange">{{
                t("change_password")
              }}</span>
              <span v-else>{{ t("profile") }}</span>
            </h3>
          </div>
          <div class="flex items-center space-x-2">
            <button
              v-if="!isEditing && !showPasswordChange"
              class="px-4 py-2 text-sm font-medium text-primary border border-primary rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary hover:bg-gray-100"
              @click="showPasswordChange = true"
            >
              {{ t("change_password") }}
            </button>
            <button
              v-if="!isEditing && !showPasswordChange"
              class="px-4 py-2 text-sm font-medium text-white bg-primary border border-transparent rounded-md shadow-sm hover:bg-primary-dark focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary"
              @click="startEdit"
            >
              {{ t("edit") }}
            </button>
            <button
              v-else-if="isEditing"
              class="px-4 py-2 text-sm font-medium text-white bg-primary border border-transparent rounded-md shadow-sm hover:bg-primary-dark focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary"
              @click="saveUser"
            >
              {{ t("save") }}
            </button>
            <button
              v-else-if="showPasswordChange"
              class="px-4 py-2 text-sm font-medium text-white bg-primary border border-transparent rounded-md shadow-sm hover:bg-primary-dark focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary"
              @click="changePassword"
            >
              {{ t("save_password") }}
            </button>
          </div>
        </div>
        <div v-if="!showPasswordChange" class="border-t border-gray-200">
          <form @submit.prevent="saveUser">
            <dl class="sm:divide-y sm:divide-gray-200">
              <div
                class="bg-gray-50 px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6"
              >
                <dt class="text-sm font-medium text-gray-500">
                  {{ t("username") }}
                </dt>
                <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                  <span>{{ user.username }}</span>
                </dd>
              </div>
              <div
                class="bg-white px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6"
              >
                <dt class="text-sm font-medium text-gray-500">
                  {{ t("full_name") }}
                </dt>
                <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                  <input
                    v-if="isEditing"
                    id="name"
                    v-model="user.name"
                    type="text"
                    class="block w-full px-3 py-2 placeholder-gray-400 border border-gray-300 rounded-md shadow-sm appearance-none focus:outline-none focus:ring-primary focus:border-primary sm:text-sm"
                  />
                  <span v-else>{{ user.name }}</span>
                </dd>
              </div>
              <div
                class="bg-white px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6"
              >
                <dt class="text-sm font-medium text-gray-500">
                  {{ t("last_name") }}
                </dt>
                <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                  <input
                    v-if="isEditing"
                    id="last_name"
                    v-model="user.last_name"
                    type="text"
                    class="block w-full px-3 py-2 placeholder-gray-400 border border-gray-300 rounded-md shadow-sm appearance-none focus:outline-none focus:ring-primary focus:border-primary sm:text-sm"
                  />
                  <span v-else>{{ user.last_name }}</span>
                </dd>
              </div>
              <div
                class="bg-gray-50 px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6"
              >
                <dt class="text-sm font-medium text-gray-500">
                  {{ t("email_address") }}
                </dt>
                <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                  <input
                    v-if="isEditing"
                    id="email"
                    v-model="user.email"
                    type="email"
                    class="block w-full px-3 py-2 mt-1 placeholder-gray-400 border border-gray-300 rounded-md shadow-sm appearance-none focus:outline-none focus:ring-primary focus:border-primary sm:text-sm"
                  />
                  <span v-else>{{ user.email }}</span>
                </dd>
              </div>
              <div
                class="bg-white px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6"
              >
                <dt class="text-sm font-medium text-gray-500">
                  {{ t("default_timezone") }}
                </dt>
                <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                  <select
                    v-if="isEditing"
                    id="default_timezone"
                    v-model="user.default_timezone"
                    class="block w-full px-3 py-2 mt-1 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary sm:text-sm"
                  >
                    <option
                      v-for="tz in timezones"
                      :key="tz.code"
                      :value="tz.code"
                    >
                      {{ tz.name }}
                    </option>
                  </select>
                  <span v-else>{{
                    timezones.find((t) => t.code === user.default_timezone)
                      ?.name || user.default_timezone
                  }}</span>
                </dd>
              </div>
              <div
                class="bg-gray-50 px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6"
              >
                <dt class="text-sm font-medium text-gray-500">
                  {{ t("language") }}
                </dt>
                <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                  <select
                    v-if="isEditing"
                    id="language"
                    v-model="user.language"
                    class="block w-full px-3 py-2 mt-1 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary sm:text-sm"
                  >
                    <option
                      v-for="lang in languages"
                      :key="lang.code"
                      :value="lang.code"
                    >
                      {{ lang.flag }} {{ lang.name }}
                    </option>
                  </select>
                  <span v-else
                    >{{
                      languages.find((l) => l.code === user.language)?.flag
                    }}
                    {{
                      languages.find((l) => l.code === user.language)?.name ||
                      user.language
                    }}</span
                  >
                </dd>
              </div>
            </dl>
          </form>
        </div>

        <div v-else-if="showPasswordChange" class="border-t border-gray-200">
          <form @submit.prevent="changePassword">
            <dl class="sm:divide-y sm:divide-gray-200">
              <div
                class="bg-gray-50 px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6"
              >
                <dt class="text-sm font-medium text-gray-500">
                  {{ t("current_password") }}
                </dt>
                <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                  <input
                    id="current_password"
                    v-model="currentPassword"
                    type="password"
                    class="block w-full px-3 py-2 mt-1 placeholder-gray-400 border border-gray-300 rounded-md shadow-sm appearance-none focus:outline-none focus:ring-primary focus:border-primary sm:text-sm"
                  />
                  <p
                    v-if="passwordErrors.currentPassword"
                    class="mt-1 text-sm text-red-600"
                  >
                    {{ passwordErrors.currentPassword }}
                  </p>
                </dd>
              </div>
              <div
                class="bg-white px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6"
              >
                <dt class="text-sm font-medium text-gray-500">
                  {{ t("new_password") }}
                </dt>
                <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                  <input
                    id="new_password"
                    v-model="newPassword"
                    type="password"
                    class="block w-full px-3 py-2 mt-1 placeholder-gray-400 border border-gray-300 rounded-md shadow-sm appearance-none focus:outline-none focus:ring-primary focus:border-primary sm:text-sm"
                  />
                  <p
                    v-if="passwordErrors.newPassword"
                    class="mt-1 text-sm text-red-600"
                  >
                    {{ passwordErrors.newPassword }}
                  </p>
                </dd>
              </div>
              <div
                class="bg-gray-50 px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6"
              >
                <dt class="text-sm font-medium text-gray-500">
                  {{ t("confirm_new_password") }}
                </dt>
                <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                  <input
                    id="confirm_new_password"
                    v-model="confirmNewPassword"
                    type="password"
                    class="block w-full px-3 py-2 mt-1 placeholder-gray-400 border border-gray-300 rounded-md shadow-sm appearance-none focus:outline-none focus:ring-primary focus:border-primary sm:text-sm"
                  />
                  <p
                    v-if="passwordErrors.confirmNewPassword"
                    class="mt-1 text-sm text-red-600"
                  >
                    {{ passwordErrors.confirmNewPassword }}
                  </p>
                </dd>
              </div>
            </dl>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useI18n } from "vue-i18n";
import api from "@/services/api";

const { t } = useI18n();

const user = ref(null);
const isEditing = ref(false);
const showPasswordChange = ref(false);
const currentPassword = ref("");
const newPassword = ref("");
const confirmNewPassword = ref("");
const passwordErrors = ref({});

const getTimezoneOffset = (tz) => {
  if (tz === "UTC") return "UTC+0";
  try {
    const date = new Date();
    const utcDate = new Date(date.toLocaleString("en-US", { timeZone: "UTC" }));
    const tzDate = new Date(date.toLocaleString("en-US", { timeZone: tz }));
    const offsetMinutes = (tzDate.getTime() - utcDate.getTime()) / (1000 * 60);
    const offsetHours = offsetMinutes / 60;
    const sign = offsetHours > 0 ? "+" : "";
    return `UTC${sign}${offsetHours}`;
  } catch (error) {
    console.warn(`Could not determine offset for timezone ${tz}:`, error);
    return tz; // Fallback to just the timezone name
  }
};

const timezones = [
  "America/New_York",
  "America/Los_Angeles",
  "America/Chicago",
  "America/Denver",
  "America/Argentina/Buenos_Aires",
  "Europe/London",
  "Europe/Paris",
  "Asia/Tokyo",
  "Asia/Shanghai",
  "Asia/Singapore",
  "Asia/Dubai",
  "Australia/Sydney",
  "Pacific/Auckland",
  "UTC",
].map((tz) => ({ code: tz, name: `${tz} (${getTimezoneOffset(tz)})` }));

const languages = [
  { code: "en", name: "English", flag: "🇬🇧" },
  { code: "es", name: "Español", flag: "🇪🇸" },
];

// TODO: For a comprehensive list of timezones, consider fetching from an external API or using a dedicated library.
// This hardcoded list is for demonstration and common use cases.

const fetchUser = async () => {
  try {
    const response = await api.get("/users");
    user.value = response.data;
  } catch (error) {
    console.error("Error fetching user:", error);
  }
};

const validatePassword = () => {
  passwordErrors.value = {};
  if (newPassword.value && newPassword.value.length < 8) {
    passwordErrors.value.newPassword =
      "Password must be at least 8 characters long.";
  }
  if (newPassword.value && newPassword.value !== confirmNewPassword.value) {
    passwordErrors.value.confirmNewPassword =
      "New password and confirmation do not match.";
  }
  return Object.keys(passwordErrors.value).length === 0;
};

const saveUser = async () => {
  try {
    const userData = {
      default_timezone: user.value.default_timezone,
      language: user.value.language,
      name: user.value.name,
      last_name: user.value.last_name,
      email: user.value.email,
    };
    await api.put("/users", userData);
    isEditing.value = false;
    await fetchUser(); // Re-fetch user data to ensure consistency
  } catch (error) {
    console.error("Error saving user:", error);
    // Handle API errors, e.g., display a message to the user
  }
};

const changePassword = async () => {
  if (!validatePassword()) {
    return;
  }

  try {
    await api.put("/users/password", {
      old_password: currentPassword.value,
      new_password: newPassword.value,
    });
    showPasswordChange.value = false;
    currentPassword.value = "";
    newPassword.value = "";
    confirmNewPassword.value = "";
    passwordErrors.value = {};
    // Optionally, show a success message
    alert("Password changed successfully!");
  } catch (error) {
    console.error("Error changing password:", error);
    // Handle API errors, e.g., display a message to the user
    if (error.response && error.response.data && error.response.data.detail) {
      passwordErrors.value.currentPassword = error.response.data.detail;
    } else {
      alert("Failed to change password. Please try again.");
    }
  }
};

const startEdit = () => {
  isEditing.value = true;
};

const cancelAction = () => {
  isEditing.value = false;
  showPasswordChange.value = false;
  currentPassword.value = "";
  newPassword.value = "";
  confirmNewPassword.value = "";
  passwordErrors.value = {};
  fetchUser(); // Re-fetch user to revert any unsaved changes
};

onMounted(fetchUser);
</script>
