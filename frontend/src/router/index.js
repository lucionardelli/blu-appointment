import { createRouter, createWebHistory } from "vue-router";
import DashboardView from "../views/DashboardView.vue";
import LoginView from "../views/LoginView.vue";
import PatientsView from "../views/PatientsView.vue";
import UserProfileView from "../views/UserProfileView.vue";
import SpecialtiesView from "../views/SpecialtiesView.vue";
import SpecialtyForm from "../components/specialties/SpecialtyForm.vue";
import AppointmentsView from "../views/AppointmentsView.vue";
import { useAuthStore } from "../stores/auth";

const routes = [
  {
    path: "/",
    redirect: "/appointments",
  },
  {
    path: "/dashboard",
    name: "dashboard",
    component: DashboardView,
    meta: { requiresAuth: true },
  },
  {
    path: "/login",
    name: "login",
    component: LoginView,
  },
  {
    path: "/profile",
    name: "user-profile",
    component: UserProfileView,
    meta: { requiresAuth: true },
  },
  {
    path: "/patients",
    name: "patients",
    component: PatientsView,
    meta: { requiresAuth: true },
  },
  {
    path: "/patients/:id",
    name: "view-patient",
    component: () => import("../views/PatientProfileView.vue"),
    meta: { requiresAuth: true },
  },
  {
    path: "/specialties",
    name: "specialties",
    component: SpecialtiesView,
    meta: { requiresAuth: true },
  },
  {
    path: "/payment-methods",
    name: "payment-methods",
    component: () => import("../views/PaymentMethodsView.vue"),
    meta: { requiresAuth: true },
  },
  {
    path: "/working-hours",
    name: "working-hours",
    component: () => import("../views/WorkingHoursView.vue"),
    meta: { requiresAuth: true },
  },
  {
    path: "/specialties/:id",
    name: "edit-specialty",
    component: SpecialtyForm,
    meta: { requiresAuth: true },
  },
  {
    path: "/appointments",
    name: "appointments",
    component: AppointmentsView,
    meta: { requiresAuth: true },
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore();
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next({ name: "login" });
  } else {
    next();
  }
});

export default router;
