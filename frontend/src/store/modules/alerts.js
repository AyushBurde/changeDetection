const state = {
  alerts: [],
  alertRules: [],
  isLoading: false,
  error: null
}

const mutations = {
  SET_ALERTS(state, alerts) {
    state.alerts = alerts
  },
  ADD_ALERT(state, alert) {
    state.alerts.push(alert)
  },
  UPDATE_ALERT(state, updatedAlert) {
    const index = state.alerts.findIndex(alert => alert.id === updatedAlert.id)
    if (index !== -1) {
      state.alerts[index] = updatedAlert
    }
  },
  SET_ALERT_RULES(state, rules) {
    state.alertRules = rules
  },
  ADD_ALERT_RULE(state, rule) {
    state.alertRules.push(rule)
  },
  UPDATE_ALERT_RULE(state, updatedRule) {
    const index = state.alertRules.findIndex(rule => rule.id === updatedRule.id)
    if (index !== -1) {
      state.alertRules[index] = updatedRule
    }
  },
  DELETE_ALERT_RULE(state, ruleId) {
    state.alertRules = state.alertRules.filter(rule => rule.id !== ruleId)
  },
  SET_LOADING(state, loading) {
    state.isLoading = loading
  },
  SET_ERROR(state, error) {
    state.error = error
  }
}

const actions = {
  async fetchAlerts({ commit }) {
    commit('SET_LOADING', true)
    try {
      // TODO: Replace with actual API call
      const response = await fetch('/api/v1/alerts')
      const alerts = await response.json()
      commit('SET_ALERTS', alerts)
    } catch (error) {
      commit('SET_ERROR', error.message)
    } finally {
      commit('SET_LOADING', false)
    }
  },
  
  async fetchAlertRules({ commit }) {
    commit('SET_LOADING', true)
    try {
      // TODO: Replace with actual API call
      const response = await fetch('/api/v1/alerts/rules')
      const rules = await response.json()
      commit('SET_ALERT_RULES', rules)
    } catch (error) {
      commit('SET_ERROR', error.message)
    } finally {
      commit('SET_LOADING', false)
    }
  },
  
  async createAlertRule({ commit }, ruleData) {
    commit('SET_LOADING', true)
    try {
      // TODO: Replace with actual API call
      const response = await fetch('/api/v1/alerts/rules', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(ruleData)
      })
      const newRule = await response.json()
      commit('ADD_ALERT_RULE', newRule)
      return newRule
    } catch (error) {
      commit('SET_ERROR', error.message)
      throw error
    } finally {
      commit('SET_LOADING', false)
    }
  },
  
  async updateAlertRule({ commit }, ruleData) {
    commit('SET_LOADING', true)
    try {
      // TODO: Replace with actual API call
      const response = await fetch(`/api/v1/alerts/rules/${ruleData.id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(ruleData)
      })
      const updatedRule = await response.json()
      commit('UPDATE_ALERT_RULE', updatedRule)
      return updatedRule
    } catch (error) {
      commit('SET_ERROR', error.message)
      throw error
    } finally {
      commit('SET_LOADING', false)
    }
  },
  
  async deleteAlertRule({ commit }, ruleId) {
    commit('SET_LOADING', true)
    try {
      // TODO: Replace with actual API call
      await fetch(`/api/v1/alerts/rules/${ruleId}`, { method: 'DELETE' })
      commit('DELETE_ALERT_RULE', ruleId)
    } catch (error) {
      commit('SET_ERROR', error.message)
      throw error
    } finally {
      commit('SET_LOADING', false)
    }
  },
  
  clearError({ commit }) {
    commit('SET_ERROR', null)
  }
}

const getters = {
  alerts: state => state.alerts,
  alertRules: state => state.alertRules,
  isLoading: state => state.isLoading,
  error: state => state.error,
  activeAlerts: state => state.alerts.filter(alert => alert.status === 'active'),
  activeRules: state => state.alertRules.filter(rule => rule.is_active)
}

export default {
  namespaced: true,
  state,
  mutations,
  actions,
  getters
}






