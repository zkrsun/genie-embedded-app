import { reactive } from 'vue'

const _saved = sessionStorage.getItem('activeSpace')

export const store = reactive({
  /** [{ name, code, domains: [{ name, code, spaces: [{ name, code, url }] }] }] */
  buList: [],
  loading: true,
  error: null,
  /** The space the user clicked on HomeView */
  activeSpace: _saved ? JSON.parse(_saved) : null,
})

export function setActiveSpace(space) {
  store.activeSpace = space
  if (space) {
    sessionStorage.setItem('activeSpace', JSON.stringify(space))
  } else {
    sessionStorage.removeItem('activeSpace')
  }
}
