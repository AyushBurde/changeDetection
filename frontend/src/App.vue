<script setup>
import { ref } from 'vue';
import MapComponent from './components/MapComponent.vue';
import { Layers, Activity, AlertTriangle, Plus, Search, Play } from 'lucide-vue-next';
import axios from 'axios';

const mapRef = ref(null);
const loading = ref(false);
const alertResult = ref(null);

// Configure Axios
const api = axios.create({
    baseURL: 'http://localhost:8000/api/v1',
    headers: { 'Content-Type': 'application/json' }
});

const triggerDraw = () => {
    if(mapRef.value) mapRef.value.startDrawing();
};

const handleAoiCreated = async (geometry) => {
    // Save AOI locally for demo (in real app, POST /aoi)
    console.log("AOI Created", geometry);
    aois.value.unshift({
        id: Date.now(),
        name: `New Region (${new Date().toLocaleTimeString()})`,
        status: 'Scanning...',
        last_scan: 'Just now'
    });
    
    // Auto-trigger simulation
    await runSimulation(aois.value[0]);
};

const runSimulation = async (aoi) => {
    loading.value = true;
    alertResult.value = null;
    
    try {
        // Call the Detection API (Simulated mode on backend)
        const response = await api.post('/detection/run', {
            aoi_id: String(aoi.id),
            before_date: "2023-01-01", 
            after_date: "2023-02-01"
            // Intentionally not sending file paths so backend triggers simulation
        });

        const result = response.data.result;
        
        // Update UI
        loading.value = false;
        aoi.status = 'Alert';
        aoi.last_scan = 'Just now';
        
        alertResult.value = {
            percentage: result.change_percentage,
            message: "Significant vegetation loss detected (Simulated)",
            email_sent: result.email_sent,
            email: result.email_recipient,
            bbox: [0,0,0,0] // Not used in simple alert
        };

    } catch (e) {
        console.error("Simulation failed", e);
        loading.value = false;
        
        let errorMsg = e.message;
        if(e.response && e.response.data) {
             errorMsg = JSON.stringify(e.response.data);
        }
        
        alertResult.value = {
             percentage: 0,
             message: "Analysis Failed: " + errorMsg
        };
    }
};

const aois = ref([
    { id: 1, name: 'Bangalore Urban', status: 'Stable', last_scan: '2h ago' },
    { id: 2, name: 'Western Ghats sec-4', status: 'Alert', last_scan: '10m ago' },
]);
</script>

<template>
  <div class="flex h-screen bg-gray-900 text-gray-100 font-sans overflow-hidden">
    <!-- Sidebar -->
    <aside class="w-80 bg-gray-800 border-r border-gray-700 flex flex-col z-20 shadow-xl">
      <div class="p-6 border-b border-gray-700 flex items-center space-x-3">
        <div class="w-8 h-8 bg-gradient-to-tr from-blue-500 to-teal-400 rounded-lg animate-pulse"></div>
        <h1 class="text-xl font-bold tracking-tight bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-teal-300">
          ISRO Watch
        </h1>
      </div>

      <div class="p-4">
        <button @click="triggerDraw" class="w-full py-3 px-4 bg-blue-600 hover:bg-blue-500 text-white rounded-lg flex items-center justify-center space-x-2 transition-all shadow-lg hover:shadow-blue-500/25">
          <Plus size="18" />
          <span>New AOI</span>
        </button>
      </div>

      <div class="flex-1 overflow-y-auto px-4 space-y-4">
        <div class="text-xs font-semibold text-gray-500 uppercase tracking-widest mb-2">Monitored Areas</div>
        
        <div v-for="aoi in aois" :key="aoi.id" 
             @click="runSimulation(aoi)"
             class="group p-4 bg-gray-700/50 hover:bg-gray-700 rounded-xl cursor-pointer transition-all border border-transparent hover:border-gray-600 relative overflow-hidden">
             
          <div v-if="loading && aoi.status === 'Scanning...'" class="absolute inset-0 bg-blue-500/10 animate-pulse"></div>
             
          <div class="flex justify-between items-start mb-2 relative z-10">
            <h3 class="font-medium text-gray-200 group-hover:text-white">{{ aoi.name }}</h3>
            <Activity size="14" :class="aoi.status === 'Alert' ? 'text-red-400' : 'text-green-400'" />
          </div>
          <div class="flex items-center text-xs text-gray-400 space-x-2 relative z-10">
            <span>Last scan: {{ aoi.last_scan }}</span>
            <span v-if="aoi.status === 'Alert'" class="px-1.5 py-0.5 rounded bg-red-500/20 text-red-300 text-[10px]">Change Detected</span>
          </div>
        </div>
      </div>

      <div class="p-4 border-t border-gray-700 bg-gray-800/80 backdrop-blur">
         <div class="flex items-center space-x-3 text-sm text-gray-400">
            <div class="w-2 h-2 rounded-full bg-green-500 animate-ping"></div>
            <span>System Operational</span>
         </div>
         <div class="mt-2 text-[10px] text-gray-500">Backend: {{ loading ? 'Processing...' : 'Ready' }}</div>
      </div>
    </aside>

    <!-- Main Content -->
    <main class="flex-1 relative">
       <!-- Toolbar Overlay -->
       <div class="absolute top-6 left-6 right-6 z-10 flex justify-between pointer-events-none">
          <div class="bg-gray-800/90 backdrop-blur text-white px-4 py-2 rounded-lg shadow-lg pointer-events-auto border border-gray-700 flex items-center space-x-4">
              <span class="text-sm font-medium text-gray-300">Active Layer: Sentinel-2 MSI</span>
              <Layers size="16" class="text-gray-400" />
          </div>
          
          <div class="pointer-events-auto">
             <!-- Dynamic Alert Banner -->
             <div v-if="alertResult" class="bg-red-500/90 backdrop-blur text-white px-6 py-4 rounded-xl shadow-2xl border border-red-400 animate-bounce flex items-center space-x-4">
                <div class="bg-white/20 p-2 rounded-full"><AlertTriangle size="24" /></div>
                <div>
                    <div class="font-bold text-lg">ALERT TRIGGERED</div>
                    <div class="text-sm opacity-90">{{ alertResult.message }}</div>
                    <div class="flex items-center space-x-2 mt-2">
                        <div class="text-xs font-mono bg-black/20 inline-block px-2 rounded">Change: {{ alertResult.percentage }}%</div>
                        <div v-if="alertResult.email_sent" class="text-xs bg-white text-red-600 font-bold px-2 rounded flex items-center">
                            📧 Email Sent to {{ alertResult.email }}
                        </div>
                    </div>
                </div>
             </div>
          </div>
       </div>

       <!-- Pass event listener to MapComponent -->
       <MapComponent ref="mapRef" @aoi-created="handleAoiCreated" />
    </main>
  </div>
</template>

<style>
/* Global scrollbar styling */
::-webkit-scrollbar {
  width: 6px;
}
::-webkit-scrollbar-track {
  background: transparent;
}
::-webkit-scrollbar-thumb {
  background: #374151;
  border-radius: 3px;
}
</style>
