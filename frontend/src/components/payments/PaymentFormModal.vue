<template>
  <div
    class="fixed inset-0 z-10 overflow-y-auto bg-gray-500 bg-opacity-75"
    aria-labelledby="modal-title"
    role="dialog"
    aria-modal="true"
  >
    <div
      class="flex items-end justify-center min-h-screen px-4 pt-4 pb-20 text-center sm:block sm:p-0"
    >
      <div
        class="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full"
      >
        <div class="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
          <div class="sm:flex sm:items-start">
            <div class="mt-3 text-center sm:mt-0 sm:ml-4 sm:text-left w-full">
              <h3
                id="modal-title"
                class="text-lg leading-6 font-medium text-gray-900"
              >
                {{ t("new_payment") }}
              </h3>
              <div class="mt-2">
                <PaymentForm
                  :patient-id="props.patientId"
                  @save="handleSave"
                  @cancel="handleCancel"
                />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import PaymentForm from "@/components/appointments/PaymentForm.vue";
import { useI18n } from "vue-i18n";

const { t } = useI18n();

const props = defineProps({
  patientId: {
    type: [String, Number],
    required: true,
  },
});

const emit = defineEmits(["save", "close"]);

const handleSave = () => {
  emit("save");
};

const handleCancel = () => {
  emit("close");
};
</script>
