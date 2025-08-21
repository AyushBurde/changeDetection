const state = {
  imagery: [],
  currentImagery: null,
  isLoading: false,
  error: null
}

const mutations = {
  SET_IMAGERY(state, imagery) {
    state.imagery = imagery
  },
  ADD_IMAGERY(state, image) {
    state.imagery.push(image)
  },
  SET_CURRENT_IMAGERY(state, image) {
    state.currentImagery = image
  },
  SET_LOADING(state, loading) {
    state.isLoading = loading
  },
  SET_ERROR(state, error) {
    state.error = error
  }
}

const actions = {
  async fetchImagery({ commit }) {
    commit('SET_LOADING', true)
    try {
      // TODO: Replace with actual API call
      const response = await fetch('/api/v1/imagery')
      const imagery = await response.json()
      commit('SET_IMAGERY', imagery)
    } catch (error) {
      commit('SET_ERROR', error.message)
    } finally {
      commit('SET_LOADING', false)
    }
  },
  
  setCurrentImagery({ commit }, image) {
    commit('SET_CURRENT_IMAGERY', image)
  },
  
  clearError({ commit }) {
    commit('SET_ERROR', null)
  }
}

const getters = {
  imagery: state => state.imagery,
  currentImagery: state => state.currentImagery,
  isLoading: state => state.isLoading,
  error: state => state.error
}

export default {
  namespaced: true,
  state,
  mutations,
  actions,
  getters
}






