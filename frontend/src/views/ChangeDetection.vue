<template>
  <div class="change-detection">
    <div class="row">
      <div class="col-12">
        <h1 class="mb-4">🔍 Change Detection</h1>
      </div>
    </div>

    <!-- New Detection Job -->
    <div class="row mb-4">
      <div class="col-12">
        <div class="card">
          <div class="card-header">
            <h5 class="mb-0">Start New Change Detection</h5>
          </div>
          <div class="card-body">
            <form @submit.prevent="startDetection">
              <div class="row">
                <div class="col-md-4 mb-3">
                  <label class="form-label">AOI *</label>
                  <select v-model="detectionForm.aoi_id" class="form-select" required>
                    <option value="">Select an AOI</option>
                    <option v-for="aoi in aois" :key="aoi.id" :value="aoi.id">
                      {{ aoi.name }}
                    </option>
                  </select>
                </div>
                <div class="col-md-4 mb-3">
                  <label class="form-label">Start Date *</label>
                  <input v-model="detectionForm.start_date" type="date" class="form-control" required>
                </div>
                <div class="col-md-4 mb-3">
                  <label class="form-label">End Date *</label>
                  <input v-model="detectionForm.end_date" type="date" class="form-control" required>
                </div>
              </div>
              
              <div class="row">
                <div class="col-md-6 mb-3">
                  <label class="form-label">Detection Algorithm</label>
                  <select v-model="detectionForm.algorithm" class="form-select">
                    <option value="spectral">Spectral Change Detection</option>
                    <option value="ndvi">NDVI Change Analysis</option>
                    <option value="machine_learning">Machine Learning</option>
                  </select>
                </div>
                <div class="col-md-6 mb-3">
                  <label class="form-label">Sensitivity</label>
                  <select v-model="detectionForm.sensitivity" class="form-select">
                    <option value="low">Low</option>
                    <option value="medium">Medium</option>
                    <option value="high">High</option>
                  </select>
                </div>
              </div>
              
              <button type="submit" class="btn btn-primary" :disabled="isStarting">
                <span v-if="isStarting" class="spinner-border spinner-border-sm me-2"></span>
                Start Detection
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>

    <!-- Active Jobs -->
    <div class="row mb-4">
      <div class="col-12">
        <div class="card">
          <div class="card-header">
            <h5 class="mb-0">Active Detection Jobs</h5>
          </div>
          <div class="card-body">
            <div v-if="activeJobs.length === 0" class="text-center text-muted">
              <p>No active detection jobs</p>
            </div>
            <div v-else>
              <div class="row">
                <div v-for="job in activeJobs" :key="job.id" class="col-md-6 mb-3">
                  <div class="card border-primary">
                    <div class="card-body">
                      <h6 class="card-title">{{ job.aoi_name }}</h6>
                      <p class="card-text">
                        <small class="text-muted">
                          Started: {{ formatDate(job.created_at) }}<br>
                          Progress: {{ job.progress || 0 }}%
                        </small>
                      </p>
                      <div class="progress mb-2">
                        <div class="progress-bar" :style="{ width: (job.progress || 0) + '%' }"></div>
                      </div>
                      <button class="btn btn-sm btn-outline-primary" @click="viewJobDetails(job)">
                        View Details
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Completed Jobs -->
    <div class="row">
      <div class="col-12">
        <div class="card">
          <div class="card-header">
            <h5 class="mb-0">Completed Detection Jobs</h5>
          </div>
          <div class="card-body">
            <div v-if="completedJobs.length === 0" class="text-center text-muted">
              <p>No completed detection jobs</p>
            </div>
            <div v-else>
              <div class="table-responsive">
                <table class="table table-hover">
                  <thead>
                    <tr>
                      <th>AOI</th>
                      <th>Algorithm</th>
                      <th>Changes Detected</th>
                      <th>Confidence</th>
                      <th>Completed</th>
                      <th>Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="job in completedJobs" :key="job.id">
                      <td>{{ job.aoi_name }}</td>
                      <td>{{ job.algorithm }}</td>
                      <td>
                        <span class="badge bg-success">{{ job.changes_detected || 0 }}</span>
                      </td>
                      <td>{{ (job.confidence || 0).toFixed(1) }}%</td>
                      <td>{{ formatDate(job.completed_at) }}</td>
                      <td>
                        <button class="btn btn-sm btn-outline-primary me-1" @click="viewResults(job)">
                          <i class="bi bi-eye"></i> Results
                        </button>
                        <button class="btn btn-sm btn-outline-success" @click="exportResults(job)">
                          <i class="bi bi-download"></i> Export
                        </button>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'

export default {
  name: 'ChangeDetection',
  data() {
    return {
      isStarting: false,
      detectionForm: {
        aoi_id: '',
        start_date: '',
        end_date: '',
        algorithm: 'spectral',
        sensitivity: 'medium'
      }
    }
  },
  computed: {
    ...mapGetters('detection', ['activeJobs', 'completedJobs', 'isLoading']),
    ...mapGetters('aoi', ['aois'])
  },
  methods: {
    ...mapActions('detection', ['createDetectionJob', 'fetchDetectionJobs']),
    ...mapActions('aoi', ['fetchAOIs']),
    
    async startDetection() {
      this.isStarting = true
      try {
        await this.createDetectionJob(this.detectionForm)
        this.resetForm()
        await this.refreshData()
      } catch (error) {
        console.error('Error starting detection:', error)
      } finally {
        this.isStarting = false
      }
    },
    
    resetForm() {
      this.detectionForm = {
        aoi_id: '',
        start_date: '',
        end_date: '',
        algorithm: 'spectral',
        sensitivity: 'medium'
      }
    },
    
    async refreshData() {
      try {
        await Promise.all([
          this.fetchDetectionJobs(),
          this.fetchAOIs()
        ])
      } catch (error) {
        console.error('Error refreshing data:', error)
      }
    },
    
    viewJobDetails(job) {
      // TODO: Implement job details view
      console.log('View job details:', job)
    },
    
    viewResults(job) {
      // TODO: Implement results view
      console.log('View results:', job)
    },
    
    exportResults(job) {
      // TODO: Implement export functionality
      console.log('Export results:', job)
    },
    
    formatDate(dateString) {
      return new Date(dateString).toLocaleDateString()
    }
  },
  
  async mounted() {
    await this.refreshData()
  }
}
</script>

<style scoped>
.change-detection {
  padding: 20px;
}

.progress {
  height: 8px;
}

.progress-bar {
  background-color: #007bff;
}
</style>
