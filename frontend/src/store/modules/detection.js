const state = {
  detectionJobs: [],
  currentJob: null,
  results: [],
  isLoading: false,
  error: null
}

const mutations = {
  SET_DETECTION_JOBS(state, jobs) {
    state.detectionJobs = jobs
  },
  ADD_DETECTION_JOB(state, job) {
    state.detectionJobs.push(job)
  },
  UPDATE_DETECTION_JOB(state, updatedJob) {
    const index = state.detectionJobs.findIndex(job => job.id === updatedJob.id)
    if (index !== -1) {
      state.detectionJobs[index] = updatedJob
    }
  },
  SET_CURRENT_JOB(state, job) {
    state.currentJob = job
  },
  SET_RESULTS(state, results) {
    state.results = results
  },
  SET_LOADING(state, loading) {
    state.isLoading = loading
  },
  SET_ERROR(state, error) {
    state.error = error
  }
}

const actions = {
  async fetchDetectionJobs({ commit }) {
    commit('SET_LOADING', true)
    try {
      // TODO: Replace with actual API call
      const response = await fetch('/api/v1/detection/jobs')
      const jobs = await response.json()
      commit('SET_DETECTION_JOBS', jobs)
    } catch (error) {
      commit('SET_ERROR', error.message)
    } finally {
      commit('SET_LOADING', false)
    }
  },
  
  async createDetectionJob({ commit }, jobData) {
    commit('SET_LOADING', true)
    try {
      // TODO: Replace with actual API call
      const response = await fetch('/api/v1/detection/jobs', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(jobData)
      })
      const newJob = await response.json()
      commit('ADD_DETECTION_JOB', newJob)
      return newJob
    } catch (error) {
      commit('SET_ERROR', error.message)
      throw error
    } finally {
      commit('SET_LOADING', false)
    }
  },
  
  async fetchResults({ commit }, jobId) {
    commit('SET_LOADING', true)
    try {
      // TODO: Replace with actual API call
      const response = await fetch(`/api/v1/detection/jobs/${jobId}/results`)
      const results = await response.json()
      commit('SET_RESULTS', results)
      return results
    } catch (error) {
      commit('SET_ERROR', error.message)
      throw error
    } finally {
      commit('SET_LOADING', false)
    }
  },
  
  setCurrentJob({ commit }, job) {
    commit('SET_CURRENT_JOB', job)
  },
  
  clearError({ commit }) {
    commit('SET_ERROR', null)
  }
}

const getters = {
  detectionJobs: state => state.detectionJobs,
  currentJob: state => state.currentJob,
  results: state => state.results,
  isLoading: state => state.isLoading,
  error: state => state.error,
  activeJobs: state => state.detectionJobs.filter(job => job.status === 'running'),
  completedJobs: state => state.detectionJobs.filter(job => job.status === 'completed')
}

export default {
  namespaced: true,
  state,
  mutations,
  actions,
  getters
}






