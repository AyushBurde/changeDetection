const state = {
  aois: [],
  currentAOI: null,
  isLoading: false,
  error: null
}

const mutations = {
  SET_AOIS(state, aois) {
    state.aois = aois
  },
  ADD_AOI(state, aoi) {
    state.aois.push(aoi)
  },
  UPDATE_AOI(state, updatedAOI) {
    const index = state.aois.findIndex(aoi => aoi.id === updatedAOI.id)
    if (index !== -1) {
      state.aois[index] = updatedAOI
    }
  },
  DELETE_AOI(state, aoiId) {
    state.aois = state.aois.filter(aoi => aoi.id !== aoiId)
  },
  SET_CURRENT_AOI(state, aoi) {
    state.currentAOI = aoi
  },
  SET_LOADING(state, loading) {
    state.isLoading = loading
  },
  SET_ERROR(state, error) {
    state.error = error
  }
}

const actions = {
  async fetchAOIs({ commit }) {
    commit('SET_LOADING', true)
    try {
      // TODO: Replace with actual API call
      const response = await fetch('/api/v1/aoi')
      const aois = await response.json()
      commit('SET_AOIS', aois)
    } catch (error) {
      commit('SET_ERROR', error.message)
    } finally {
      commit('SET_LOADING', false)
    }
  },
  
  async createAOI({ commit }, aoiData) {
    commit('SET_LOADING', true)
    try {
      // TODO: Replace with actual API call
      const response = await fetch('/api/v1/aoi', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(aoiData)
      })
      const newAOI = await response.json()
      commit('ADD_AOI', newAOI)
      return newAOI
    } catch (error) {
      commit('SET_ERROR', error.message)
      throw error
    } finally {
      commit('SET_LOADING', false)
    }
  },
  
  async updateAOI({ commit }, aoiData) {
    commit('SET_LOADING', true)
    try {
      // TODO: Replace with actual API call
      const response = await fetch(`/api/v1/aoi/${aoiData.id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(aoiData)
      })
      const updatedAOI = await response.json()
      commit('UPDATE_AOI', updatedAOI)
      return updatedAOI
    } catch (error) {
      commit('SET_ERROR', error.message)
      throw error
    } finally {
      commit('SET_LOADING', false)
    }
  },
  
  async deleteAOI({ commit }, aoiId) {
    commit('SET_LOADING', true)
    try {
      // TODO: Replace with actual API call
      await fetch(`/api/v1/aoi/${aoiId}`, { method: 'DELETE' })
      commit('DELETE_AOI', aoiId)
    } catch (error) {
      commit('SET_ERROR', error.message)
      throw error
    } finally {
      commit('SET_LOADING', false)
    }
  },
  
  setCurrentAOI({ commit }, aoi) {
    commit('SET_CURRENT_AOI', aoi)
  },
  
  clearError({ commit }) {
    commit('SET_ERROR', null)
  }
}

const getters = {
  aois: state => state.aois,
  currentAOI: state => state.currentAOI,
  isLoading: state => state.isLoading,
  error: state => state.error,
  activeAOIs: state => state.aois.filter(aoi => aoi.is_active),
  aoiCount: state => state.aois.length
}

export default {
  namespaced: true,
  state,
  mutations,
  actions,
  getters
}

