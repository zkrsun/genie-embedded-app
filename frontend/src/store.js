import { reactive } from 'vue'

export const store = reactive({
  /** [{ name, code, domains: [{ name, code, spaces: [{ name, code, url }] }] }] */
  buList: [],
  loading: true,
  error: null,
  activeSpace: null,
})

export function setActiveSpace(space) {
  store.activeSpace = space
}
