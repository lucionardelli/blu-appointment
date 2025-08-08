<template>
  <div class="relative">
    <button
      class="flex items-center justify-center w-10 h-10 bg-gray-200 rounded-full focus:outline-none"
      @click="toggleDropdown"
    >
      <span class="text-lg">{{ currentLanguageEmoji }}</span>
    </button>
    <div
      v-if="isDropdownOpen"
      class="absolute right-0 mt-2 py-2 w-48 bg-white rounded-md shadow-xl z-20"
    >
      <a
        href="#"
        class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
        @click.prevent="switchLanguage('en')"
      >
        <span class="mr-2">🇬🇧</span> English
      </a>
      <a
        href="#"
        class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
        @click.prevent="switchLanguage('es')"
      >
        <span class="mr-2">🇪🇸</span> Español
      </a>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from "vue";
import { useI18n } from "vue-i18n";

const { locale } = useI18n();
const isDropdownOpen = ref(false);

const currentLanguageEmoji = computed(() => {
  return locale.value === "es" ? "🇪🇸" : "🇬🇧";
});

const toggleDropdown = () => {
  isDropdownOpen.value = !isDropdownOpen.value;
};

const switchLanguage = (lang) => {
  locale.value = lang;
  localStorage.setItem("language", lang);
  isDropdownOpen.value = false;
};
</script>
