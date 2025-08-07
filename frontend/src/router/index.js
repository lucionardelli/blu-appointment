import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import LoginView from "../views/LoginView.vue";
import PatientsView from "../views/PatientsView.vue";
import PatientForm from "../components/patients/PatientForm.vue";
import SpecialtiesView from "../views/SpecialtiesView.vue";
import SpecialtyForm from "../components/specialties/SpecialtyForm.vue";
import AppointmentsView from "../views/AppointmentsView.vue";
import { useAuthStore } from "../stores/auth";

const routes = [
  {
    path: "/",
    name: "home",
    component: HomeView,
    meta: { requiresAuth: true },
  },
  {
    path: "/login",
    name: "login",
    component: LoginView,
  },
  {
    path: "/patients",
    name: "patients",
    component: PatientsView,
    meta: { requiresAuth: true },
  },
  {
    path: "/patients/new",
    name: "new-patient",
    component: PatientForm,
    meta: { requiresAuth: true },
  },
  {
    path: "/patients/:id",
    name: "view-patient",
    component: () => import("../views/PatientProfileView.vue"),
    meta: { requiresAuth: true },
  },
  {
    path: "/patients/:id/edit",
    name: "edit-patient",
    component: PatientForm,
    meta: { requiresAuth: true },
  },
  {
    path: "/specialties",
    name: "specialties",
    component: SpecialtiesView,
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
