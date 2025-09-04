<template>
  <tr :class="{ 'bg-gray-50': !isEditing }">
    <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
      <input
        v-if="isEditing"
        v-model="editableContact.full_name"
        type="text"
        class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary focus:ring-primary sm:text-sm"
      />
      <span v-else>{{ contact.full_name }}</span>
    </td>
    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
      <input
        v-if="isEditing"
        v-model="editableContact.patient_relationship"
        type="text"
        class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary focus:ring-primary sm:text-sm"
      />
      <span v-else>{{ contact.patient_relationship }}</span>
    </td>
    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 hidden sm:table-cell">
      <input
        v-if="isEditing"
        v-model="editableContact.email"
        type="email"
        class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary focus:ring-primary sm:text-sm"
      />
      <span v-else>{{ contact.email }}</span>
    </td>
    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 hidden md:table-cell">
      <input
        v-if="isEditing"
        v-model="editableContact.phone_number"
        type="text"
        class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary focus:ring-primary sm:text-sm"
      />
      <span v-else>{{ contact.phone_number }}</span>
    </td>
    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
      <input
        v-if="isEditing"
        v-model="editableContact.cellphone"
        type="text"
        class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary focus:ring-primary sm:text-sm"
      />
      <span v-else>{{ contact.cellphone }}</span>
    </td>
    <td
      v-if="isEditing"
      class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium"
    >
      <div class="flex items-center space-x-2">
        <button
          class="text-red-600 hover:text-red-800"
          @click="$emit('delete', contact)"
        >
          <i-heroicons-trash-20-solid class="h-5 w-5" />
        </button>
      </div>
    </td>
  </tr>
</template>

<script setup>
import { ref, watch } from "vue";

const props = defineProps({
  contact: {
    type: Object,
    default: () => ({}),
  },
  isEditing: Boolean,
});

const editableContact = ref(props.contact ? { ...props.contact } : {});

watch(
  () => props.contact,
  (newVal) => {
    editableContact.value = newVal ? { ...newVal } : {};
  },
  { deep: true },
);

const emit = defineEmits(["delete", "update:contact"]);

let debounceTimer;
watch(
  editableContact,
  (newVal) => {
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(() => {
      emit("update:contact", newVal);
    }, 500);
  },
  { deep: true },
);
</script>
