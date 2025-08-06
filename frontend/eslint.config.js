import globals from "globals";
import pluginVue from "eslint-plugin-vue";
import eslint from "@eslint/js";
import prettierConfig from "eslint-config-prettier";

export default [
  {
    ignores: [
      "build",
      "dist",
      "*.log",
      ".env",
      ".env.local",
      ".env.*.local",
      "node_modules",
      "*.local",
      "*.vue.d.ts",
      ".vscode",
      ".idea",
      "coverage",
      "*.css.map",
      "*.js.map",
      "package-lock.json",
    ],
  },
  eslint.configs.recommended,
  ...pluginVue.configs["flat/recommended"],
  prettierConfig,
  {
    languageOptions: {
      globals: {
        ...globals.browser,
        ...globals.node,
      },
      ecmaVersion: "latest",
      sourceType: "module",
    },
    rules: {
      // Vue-specific rules
      "vue/multi-word-component-names": "off",
      // Add any custom ESLint rules here
    },
  },
];
