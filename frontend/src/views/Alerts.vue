<template>
  <div class="alerts">
    <div class="row">
      <div class="col-12">
        <h1 class="mb-4">🔔 Alerts & Notifications</h1>
      </div>
    </div>

    <!-- Alert Rules -->
    <div class="row mb-4">
      <div class="col-12">
        <div class="card">
          <div class="card-header d-flex justify-content-between align-items-center">
            <h5 class="mb-0">Alert Rules</h5>
            <button class="btn btn-primary" @click="showCreateModal = true">
              <i class="bi bi-plus-circle"></i> Create Alert Rule
            </button>
          </div>
          <div class="card-body">
            <div v-if="isLoading" class="text-center">
              <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Loading...</span>
              </div>
            </div>
            <div v-else-if="alertRules.length === 0" class="text-center text-muted">
              <p>No alert rules configured. Create your first rule to get started.</p>
            </div>
            <div v-else>
              <div class="table-responsive">
                <table class="table table-hover">
                  <thead>
                    <tr>
                      <th>Name</th>
                      <th>AOI</th>
                      <th>Condition</th>
                      <th>Threshold</th>
                      <th>Status</th>
                      <th>Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="rule in alertRules" :key="rule.id">
                      <td>{{ rule.name }}</td>
                      <td>{{ rule.aoi_name }}</td>
                      <td>{{ rule.condition }}</td>
                      <td>{{ rule.threshold }}</td>
                      <td>
                        <span class="badge" :class="rule.is_active ? 'bg-success' : 'bg-secondary'">
                          {{ rule.is_active ? 'Active' : 'Inactive' }}
                        </span>
                      </td>
                      <td>
                        <button class="btn btn-sm btn-outline-primary me-1" @click="editRule(rule)">
                          <i class="bi bi-pencil"></i>
                        </button>
                        <button class="btn btn-sm btn-outline-danger" @click="deleteRule(rule.id)">
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

    <!-- Recent Alerts -->
    <div class="row">
      <div class="col-12">
        <div class="card">
          <div class="card-header">
            <h5 class="mb-0">Recent Alerts</h5>
          </div>
          <div class="card-body">
            <div v-if="alerts.length === 0" class="text-center text-muted">
              <p>No recent alerts</p>
            </div>
            <div v-else>
              <div v-for="alert in alerts" :key="alert.id" class="alert" :class="getAlertClass(alert.level)">
                <div class="d-flex justify-content-between align-items-start">
                  <div>
                    <h6 class="alert-heading">{{ alert.title }}</h6>
                    <p class="mb-1">{{ alert.message }}</p>
                    <small class="text-muted">
                      AOI: {{ alert.aoi_name }} | {{ formatDate(alert.created_at) }}
                    </small>
                  </div>
                  <button class="btn-close" @click="dismissAlert(alert.id)"></button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Create/Edit Modal -->
    <div class="modal fade" :class="{ show: showCreateModal }" :style="{ display: showCreateModal ? 'block' : 'none' }" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">{{ editingRule ? 'Edit Alert Rule' : 'Create Alert Rule' }}</h5>
            <button type="button" class="btn-close" @click="closeModal"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="saveRule">
              <div class="mb-3">
                <label class="form-label">Rule Name *</label>
                <input v-model="ruleForm.name" type="text" class="form-control" required>
              </div>
              
              <div class="mb-3">
                <label class="form-label">AOI *</label>
                <select v-model="ruleForm.aoi_id" class="form-select" required>
                  <option value="">Select an AOI</option>
                  <option v-for="aoi in aois" :key="aoi.id" :value="aoi.id">
                    {{ aoi.name }}
                  </option>
                </select>
              </div>
              
              <div class="row">
                <div class="col-md-6 mb-3">
                  <label class="form-label">Condition</label>
                  <select v-model="ruleForm.condition" class="form-select">
                    <option value="change_percentage">Change Percentage</option>
                    <option value="vegetation_loss">Vegetation Loss</option>
                    <option value="urban_expansion">Urban Expansion</option>
                    <option value="water_changes">Water Changes</option>
                  </select>
                </div>
                <div class="col-md-6 mb-3">
                  <label class="form-label">Threshold</label>
                  <input v-model="ruleForm.threshold" type="number" class="form-control" min="0" step="0.1">
                </div>
              </div>
              
              <div class="mb-3">
                <label class="form-label">Notification Method</label>
                <div class="form-check">
                  <input v-model="ruleForm.email_enabled" class="form-check-input" type="checkbox" id="emailEnabled">
                  <label class="form-check-label" for="emailEnabled">Email Notifications</label>
                </div>
                <div class="form-check">
                  <input v-model="ruleForm.webhook_enabled" class="form-check-input" type="checkbox" id="webhookEnabled">
                  <label class="form-check-label" for="webhookEnabled">Webhook Notifications</label>
                </div>
              </div>
              
              <div class="form-check mb-3">
                <input v-model="ruleForm.is_active" class="form-check-input" type="checkbox" id="ruleActive">
                <label class="form-check-label" for="ruleActive">
                  Rule is active
                </label>
              </div>
            </form>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="closeModal">Cancel</button>
            <button type="button" class="btn btn-primary" @click="saveRule">
              {{ editingRule ? 'Update' : 'Create' }} Rule
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
  name: 'Alerts',
  data() {
    return {
      showCreateModal: false,
      editingRule: null,
      ruleForm: {
        name: '',
        aoi_id: '',
        condition: 'change_percentage',
        threshold: 15,
        email_enabled: true,
        webhook_enabled: false,
        is_active: true
      }
    }
  },
  computed: {
    ...mapGetters('alerts', ['alerts', 'alertRules', 'isLoading']),
    ...mapGetters('aoi', ['aois'])
  },
  methods: {
    ...mapActions('alerts', ['fetchAlerts', 'fetchAlertRules', 'createAlertRule', 'updateAlertRule', 'deleteAlertRule']),
    ...mapActions('aoi', ['fetchAOIs']),
    
    async refreshData() {
      try {
        await Promise.all([
          this.fetchAlerts(),
          this.fetchAlertRules(),
          this.fetchAOIs()
        ])
      } catch (error) {
        console.error('Error refreshing data:', error)
      }
    },
    
    editRule(rule) {
      this.editingRule = rule
      this.ruleForm = { ...rule }
      this.showCreateModal = true
    },
    
    async saveRule() {
      try {
        if (this.editingRule) {
          await this.updateAlertRule({ ...this.ruleForm, id: this.editingRule.id })
        } else {
          await this.createAlertRule(this.ruleForm)
        }
        this.closeModal()
        await this.refreshData()
      } catch (error) {
        console.error('Error saving rule:', error)
      }
    },
    
    async deleteRule(ruleId) {
      if (confirm('Are you sure you want to delete this alert rule?')) {
        try {
          await this.deleteAlertRule(ruleId)
          await this.refreshData()
        } catch (error) {
          console.error('Error deleting rule:', error)
        }
      }
    },
    
    async dismissAlert(alertId) {
      // TODO: Implement alert dismissal
      console.log('Dismiss alert:', alertId)
    },
    
    closeModal() {
      this.showCreateModal = false
      this.editingRule = null
      this.ruleForm = {
        name: '',
        aoi_id: '',
        condition: 'change_percentage',
        threshold: 15,
        email_enabled: true,
        webhook_enabled: false,
        is_active: true
      }
    },
    
    getAlertClass(level) {
      const classes = {
        'info': 'alert-info',
        'warning': 'alert-warning',
        'error': 'alert-danger',
        'success': 'alert-success'
      }
      return classes[level] || 'alert-info'
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
.alerts {
  padding: 20px;
}

.modal.show {
  background-color: rgba(0, 0, 0, 0.5);
}

.alert {
  margin-bottom: 1rem;
}

.alert-heading {
  margin-bottom: 0.5rem;
}
</style>






