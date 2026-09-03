import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  base: './',
  publicDir: 'static',
  build: {
    outDir: 'public',
    emptyOutDir: true,
  },
})
