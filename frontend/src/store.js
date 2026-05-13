import { reactive } from 'vue'

export const store = reactive({
  /** [{ name, code, url, description, icon_code }] */
  spaces: [],
  loading: true,
  error: null,
  activeSpace: null,
})

export function setActiveSpace(space) {
  store.activeSpace = space
}
