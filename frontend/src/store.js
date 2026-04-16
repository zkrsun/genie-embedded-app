import { reactive } from 'vue'

/**
 * Lightweight shared state — avoids prop-drilling between
 * App.vue (navbar) ↔ HomeView ↔ GenieView.
 */
export const store = reactive({
  /** [{ bu: string, spaces: [{ name, url }] }] */
  buList: [],
  loading: true,
  error: null,
  /** The space the user clicked on HomeView */
  activeSpace: null,   // { name, url, bu }
})
