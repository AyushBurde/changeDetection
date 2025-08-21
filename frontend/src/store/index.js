import { createStore } from 'vuex'
import aoi from './modules/aoi'
import imagery from './modules/imagery'
import detection from './modules/detection'
import alerts from './modules/alerts'

export default createStore({
  state: {
    // Global application state
    isLoading: false,
    error: null,
    user: null,
    systemStatus: 'operational'
  },
  
  mutations: {
    SET_LOADING(state, loading) {
      state.isLoading = loading
    },
    SET_ERROR(state, error) {
      state.error = error
    },
    SET_USER(state, user) {
      state.user = user
    },
    SET_SYSTEM_STATUS(state, status) {
      state.systemStatus = status
    }
  },
  
  actions: {
    setLoading({ commit }, loading) {
      commit('SET_LOADING', loading)
    },
    setError({ commit }, error) {
      commit('SET_ERROR', error)
    },
    clearError({ commit }) {
      commit('SET_ERROR', null)
    },
    setUser({ commit }, user) {
      commit('SET_USER', user)
    },
    setSystemStatus({ commit }, status) {
      commit('SET_SYSTEM_STATUS', status)
    }
  },
  
  getters: {
    isLoading: state => state.isLoading,
    error: state => state.error,
    user: state => state.user,
    systemStatus: state => state.systemStatus
  },
  
  modules: {
    aoi,
    imagery,
    detection,
    alerts
  }
})

