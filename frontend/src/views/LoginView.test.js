/* global vi */
import { describe, it, expect } from "vitest";
import { mount } from "@vue/test-utils";
import LoginView from "./LoginView.vue";
import { createTestingPinia } from "@pinia/testing";
import { createRouter, createWebHistory } from "vue-router";
import { routes } from "@/router";

// Mock i18n for testing
vi.mock("vue-i18n", () => ({
  useI18n: () => ({
    t: (key) => key, // Mock the translation function to return the key itself
  }),
}));

describe("LoginView", () => {
  const router = createRouter({
    history: createWebHistory(),
    routes: routes,
  });

  it("renders the login form", async () => {
    router.push("/");
    await router.isReady();

    const wrapper = mount(LoginView, {
      global: {
        plugins: [createTestingPinia(), router],
      },
    });

    expect(wrapper.find("h1").text()).toBe("login");
    expect(wrapper.find("input#username").exists()).toBe(true);
    expect(wrapper.find("input#password").exists()).toBe(true);
    expect(wrapper.find('button[type="submit"]').text()).toBe("login");
  });

  it("toggles password visibility", async () => {
    router.push("/");
    await router.isReady();

    const wrapper = mount(LoginView, {
      global: {
        plugins: [createTestingPinia(), router],
      },
    });

    const passwordInput = wrapper.find("input#password");
    const toggleButton = wrapper.find('button[type="button"]');

    expect(passwordInput.attributes("type")).toBe("password");

    await toggleButton.trigger("click");
    expect(passwordInput.attributes("type")).toBe("text");

    await toggleButton.trigger("click");
    expect(passwordInput.attributes("type")).toBe("password");
  });
});
