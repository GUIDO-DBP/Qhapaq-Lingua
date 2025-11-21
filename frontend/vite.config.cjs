const { defineConfig } = require('vite');
const reactPlugin = require('@vitejs/plugin-react-swc');

module.exports = defineConfig({
  plugins: [reactPlugin && reactPlugin.default ? reactPlugin.default() : reactPlugin()],
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:5000',
        changeOrigin: true,
        secure: false,
        rewrite: (path) => path
      }
    },
  },
});