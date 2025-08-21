<template>
  <div class="dashboard">
    <div class="row">
      <div class="col-12">
        <h1 class="mb-4">🛰️ Change Detection Dashboard</h1>
      </div>
    </div>

    <!-- System Status -->
    <div class="row mb-4">
      <div class="col-md-3">
        <div class="card text-white bg-success">
          <div class="card-body">
            <h5 class="card-title">System Status</h5>
            <p class="card-text display-6">{{ systemStatus }}</p>
          </div>
        </div>
      </div>
      <div class="col-md-3">
        <div class="card text-white bg-primary">
          <div class="card-body">
            <h5 class="card-title">Active AOIs</h5>
            <p class="card-text display-6">{{ aoiCount }}</p>
          </div>
        </div>
      </div>
      <div class="col-md-3">
        <div class="card text-white bg-info">
          <div class="card-body">
            <h5 class="card-title">Processing Jobs</h5>
            <p class="card-text display-6">{{ processingJobs }}</p>
          </div>
        </div>
      </div>
      <div class="col-md-3">
        <div class="card text-white bg-warning">
          <div class="card-body">
            <h5 class="card-title">Active Alerts</h5>
            <p class="card-text display-6">{{ activeAlerts }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Quick Actions -->
    <div class="row mb-4">
      <div class="col-12">
        <div class="card">
          <div class="card-header">
            <h5 class="mb-0">Quick Actions</h5>
          </div>
          <div class="card-body">
            <div class="row">
              <div class="col-md-3 mb-2">
                <router-link to="/aoi" class="btn btn-primary w-100">
                  <i class="bi bi-plus-circle"></i> Create New AOI
                </router-link>
              </div>
              <div class="col-md-3 mb-2">
                <router-link to="/detection" class="btn btn-success w-100">
                  <i class="bi bi-camera"></i> Start Detection
                </router-link>
              </div>
              <div class="col-md-3 mb-2">
                <router-link to="/alerts" class="btn btn-warning w-100">
                  <i class="bi bi-bell"></i> Manage Alerts
                </router-link>
              </div>
              <div class="col-md-3 mb-2">
                <button class="btn btn-info w-100" @click="refreshData">
                  <i class="bi bi-arrow-clockwise"></i> Refresh Data
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Recent Activity -->
    <div class="row">
      <div class="col-md-6">
        <div class="card">
          <div class="card-header">
            <h5 class="mb-0">Recent AOI Changes</h5>
          </div>
          <div class="card-body">
            <div v-if="recentAOIChanges.length === 0" class="text-muted">
              No recent changes detected
            </div>
            <div v-else>
              <div v-for="change in recentAOIChanges" :key="change.id" class="d-flex justify-content-between align-items-center mb-2">
                <span>{{ change.description }}</span>
                <small class="text-muted">{{ formatDate(change.timestamp) }}</small>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="col-md-6">
        <div class="card">
          <div class="card-header">
            <h5 class="mb-0">System Alerts</h5>
          </div>
          <div class="card-body">
            <div v-if="systemAlerts.length === 0" class="text-muted">
              No system alerts
            </div>
            <div v-else>
              <div v-for="alert in systemAlerts" :key="alert.id" class="alert alert-sm" :class="getAlertClass(alert.level)">
                {{ alert.message }}
                <small class="d-block">{{ formatDate(alert.timestamp) }}</small>
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
  name: 'Dashboard',
  data() {
    return {
      processingJobs: 0,
      activeAlerts: 0,
      recentAOIChanges: [],
      systemAlerts: []
    }
  },
  computed: {
    ...mapGetters(['systemStatus', 'aoiCount'])
  },
  methods: {
    ...mapActions(['fetchAOIs']),
    
    async refreshData() {
      try {
        await this.fetchAOIs()
        // TODO: Fetch other data
      } catch (error) {
        console.error('Error refreshing data:', error)
      }
    },
    
    formatDate(dateString) {
      return new Date(dateString).toLocaleDateString()
    },
    
    getAlertClass(level) {
      const classes = {
        'info': 'alert-info',
        'warning': 'alert-warning',
        'error': 'alert-danger',
        'success': 'alert-success'
      }
      return classes[level] || 'alert-info'
    }
  },
  
  async mounted() {
    await this.refreshData()
  }
}
</script>

<style scoped>
.dashboard {
  padding: 20px;
}

.card {
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  border: none;
}

.card-header {
  background-color: #f8f9fa;
  border-bottom: 1px solid #dee2e6;
}

.btn {
  padding: 10px 20px;
}

.alert-sm {
  padding: 0.5rem;
  margin-bottom: 0.5rem;
  font-size: 0.875rem;
}
</style>

