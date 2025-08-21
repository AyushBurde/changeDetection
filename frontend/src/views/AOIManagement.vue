<template>
  <div class="aoi-management">
    <div class="row">
      <div class="col-12">
        <h1 class="mb-4">🗺️ AOI Management</h1>
      </div>
    </div>

    <!-- AOI List -->
    <div class="row mb-4">
      <div class="col-12">
        <div class="card">
          <div class="card-header d-flex justify-content-between align-items-center">
            <h5 class="mb-0">Areas of Interest</h5>
            <button class="btn btn-primary" @click="showCreateModal = true">
              <i class="bi bi-plus-circle"></i> Create New AOI
            </button>
          </div>
          <div class="card-body">
            <div v-if="isLoading" class="text-center">
              <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Loading...</span>
              </div>
            </div>
            <div v-else-if="aois.length === 0" class="text-center text-muted">
              <p>No AOIs created yet. Create your first AOI to get started.</p>
            </div>
            <div v-else>
              <div class="table-responsive">
                <table class="table table-hover">
                  <thead>
                    <tr>
                      <th>Name</th>
                      <th>Area (ha)</th>
                      <th>Status</th>
                      <th>Monitoring</th>
                      <th>Created</th>
                      <th>Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="aoi in aois" :key="aoi.id">
                      <td>{{ aoi.name }}</td>
                      <td>{{ aoi.area_hectares.toFixed(2) }}</td>
                      <td>
                        <span class="badge" :class="aoi.is_active ? 'bg-success' : 'bg-secondary'">
                          {{ aoi.is_active ? 'Active' : 'Inactive' }}
                        </span>
                      </td>
                      <td>{{ aoi.monitoring_frequency }}</td>
                      <td>{{ formatDate(aoi.created_at) }}</td>
                      <td>
                        <button class="btn btn-sm btn-outline-primary me-1" @click="editAOI(aoi)">
                          <i class="bi bi-pencil"></i>
                        </button>
                        <button class="btn btn-sm btn-outline-danger" @click="deleteAOI(aoi.id)">
                          <i class="bi bi-trash"></i>
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

    <!-- Create/Edit Modal -->
    <div class="modal fade" :class="{ show: showCreateModal }" :style="{ display: showCreateModal ? 'block' : 'none' }" tabindex="-1">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">{{ editingAOI ? 'Edit AOI' : 'Create New AOI' }}</h5>
            <button type="button" class="btn-close" @click="closeModal"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="saveAOI">
              <div class="row">
                <div class="col-md-6 mb-3">
                  <label class="form-label">Name *</label>
                  <input v-model="aoiForm.name" type="text" class="form-control" required>
                </div>
                <div class="col-md-6 mb-3">
                  <label class="form-label">Description</label>
                  <textarea v-model="aoiForm.description" class="form-control" rows="3"></textarea>
                </div>
              </div>
              
              <div class="row">
                <div class="col-md-6 mb-3">
                  <label class="form-label">Monitoring Frequency</label>
                  <select v-model="aoiForm.monitoring_frequency" class="form-select">
                    <option value="daily">Daily</option>
                    <option value="weekly">Weekly</option>
                    <option value="monthly">Monthly</option>
                  </select>
                </div>
                <div class="col-md-6 mb-3">
                  <label class="form-label">Change Threshold (%)</label>
                  <input v-model="aoiForm.change_threshold" type="number" class="form-control" min="0" max="100" step="0.1">
                </div>
              </div>
              
              <div class="mb-3">
                <label class="form-label">Geometry</label>
                <div class="border rounded p-3 bg-light">
                  <p class="text-muted mb-2">Draw your AOI on the map below:</p>
                  <div id="map" style="height: 300px; width: 100%;"></div>
                </div>
              </div>
              
              <div class="form-check mb-3">
                <input v-model="aoiForm.alert_enabled" class="form-check-input" type="checkbox" id="alertEnabled">
                <label class="form-check-label" for="alertEnabled">
                  Enable alerts for this AOI
                </label>
              </div>
            </form>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="closeModal">Cancel</button>
            <button type="button" class="btn btn-primary" @click="saveAOI">
              {{ editingAOI ? 'Update' : 'Create' }} AOI
            </button>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Modal backdrop -->
    <div v-if="showCreateModal" class="modal-backdrop fade show"></div>
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'

export default {
  name: 'AOIManagement',
  data() {
    return {
      showCreateModal: false,
      editingAOI: null,
      aoiForm: {
        name: '',
        description: '',
        monitoring_frequency: 'weekly',
        change_threshold: 15,
        alert_enabled: true
      }
    }
  },
  computed: {
    ...mapGetters('aoi', ['aois', 'isLoading', 'error'])
  },
  methods: {
    ...mapActions('aoi', ['fetchAOIs', 'createAOI', 'updateAOI', 'deleteAOI']),
    
    async refreshData() {
      try {
        await this.fetchAOIs()
      } catch (error) {
        console.error('Error fetching AOIs:', error)
      }
    },
    
    editAOI(aoi) {
      this.editingAOI = aoi
      this.aoiForm = { ...aoi }
      this.showCreateModal = true
    },
    
    async saveAOI() {
      try {
        if (this.editingAOI) {
          await this.updateAOI({ ...this.aoiForm, id: this.editingAOI.id })
        } else {
          await this.createAOI(this.aoiForm)
        }
        this.closeModal()
        await this.refreshData()
      } catch (error) {
        console.error('Error saving AOI:', error)
      }
    },
    
    async deleteAOI(aoiId) {
      if (confirm('Are you sure you want to delete this AOI?')) {
        try {
          await this.deleteAOI(aoiId)
          await this.refreshData()
        } catch (error) {
          console.error('Error deleting AOI:', error)
        }
      }
    },
    
    closeModal() {
      this.showCreateModal = false
      this.editingAOI = null
      this.aoiForm = {
        name: '',
        description: '',
        monitoring_frequency: 'weekly',
        change_threshold: 15,
        alert_enabled: true
      }
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
.aoi-management {
  padding: 20px;
}

.modal.show {
  background-color: rgba(0, 0, 0, 0.5);
}

#map {
  border: 1px solid #dee2e6;
}
</style>






