import { ref, computed } from "vue";

export function useSort(data, initialSortKey, initialSortOrder = "asc") {
  const sortKey = ref(initialSortKey);
  const sortOrder = ref(initialSortOrder);

  const sortedData = computed(() => {
    if (!sortKey.value) {
      return data.value;
    }

    return [...data.value].sort((a, b) => {
      let aValue = a[sortKey.value];
      let bValue = b[sortKey.value];

      // Handle nested properties
      if (sortKey.value.includes(".")) {
        aValue = sortKey.value.split(".").reduce((o, i) => o[i], a);
        bValue = sortKey.value.split(".").reduce((o, i) => o[i], b);
      }

      if (aValue < bValue) {
        return sortOrder.value === "asc" ? -1 : 1;
      }
      if (aValue > bValue) {
        return sortOrder.value === "asc" ? 1 : -1;
      }
      return 0;
    });
  });

  function sortBy(key) {
    if (sortKey.value === key) {
      sortOrder.value = sortOrder.value === "asc" ? "desc" : "asc";
    } else {
      sortKey.value = key;
      sortOrder.value = "asc";
    }
  }

  return {
    sortKey,
    sortOrder,
    sortedData,
    sortBy,
  };
}
