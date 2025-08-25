import i18n from "@/i18n";

export function formatDate(dateString) {
  if (!dateString) return "N/A";
  const date = new Date(dateString);
  const locale = i18n.global.locale.value;
  const options = {
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
  };
  return new Intl.DateTimeFormat(locale, options).format(date);
}

export function formatDateForInput(dateString) {
  if (!dateString) return "";
  const date = new Date(dateString);
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, "0");
  const day = String(date.getDate()).padStart(2, "0");
  return `${year}-${month}-${day}`;
}

export function formatTime(dateString) {
  if (!dateString) return "N/A";
  const date = new Date(dateString);
  const locale = i18n.global.locale.value;
  const options = {
    hour: "2-digit",
    minute: "2-digit",
    hour12: false,
  };
  return new Intl.DateTimeFormat(locale, options).format(date);
}

export function formatCurrency(amount) {
  const locale = i18n.global.locale.value;
  return new Intl.NumberFormat(locale, {
    style: "currency",
    currency: "USD",
  }).format(amount);
}
