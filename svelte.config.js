import adapter from "@sveltejs/adapter-static";
import { vitePreprocess } from "@sveltejs/vite-plugin-svelte";

/** @type {import('@sveltejs/kit').Config} */
const config = {
  preprocess: vitePreprocess(),

  kit: {
    adapter: adapter({
      pages: "build",
      assets: "build",
      fallback: "index.html",
      strict: true,
    }),
    paths: {
      base: process.env.BASE_PATH || '',
    },
    prerender: {
      entries: ['*'], // Prerender all pages
      handleHttpError: 'ignore', // or 'error' based on your preference
    },
  },
};

export default config;