<script setup>
import { onMounted, ref } from 'vue';
import 'ol/ol.css';
import Map from 'ol/Map';
import View from 'ol/View';
import TileLayer from 'ol/layer/Tile';
import OSM from 'ol/source/OSM';
import { fromLonLat } from 'ol/proj';
import VectorLayer from 'ol/layer/Vector';
import VectorSource from 'ol/source/Vector';
import Draw from 'ol/interaction/Draw';

const mapContainer = ref(null);
const map = ref(null);
const draw = ref(null);
const source = new VectorSource();
const vector = new VectorLayer({
  source: source,
  style: {
    'fill-color': 'rgba(255, 255, 255, 0.2)',
    'stroke-color': '#ffcc33',
    'stroke-width': 2,
    'circle-radius': 7,
    'circle-fill-color': '#ffcc33',
  },
});

onMounted(() => {
  map.value = new Map({
    target: mapContainer.value,
    layers: [
      new TileLayer({
        source: new OSM(), // In prod, use High-Res Satellite like Mapbox/Bhoonidhi if available
      }),
      vector
    ],
    view: new View({
      center: fromLonLat([78.9629, 20.5937]), // India Center
      zoom: 5,
    }),
  });
});

const startDrawing = () => {
    if (draw.value) map.value.removeInteraction(draw.value);
    
    draw.value = new Draw({
        source: source,
        type: 'Polygon',
    });
    
    map.value.addInteraction(draw.value);
    
    draw.value.on('drawend', (event) => {
        const feature = event.feature;
        const coords = feature.getGeometry().getCoordinates();
        console.log("AOI Created", coords);
        
        // Emit event to parent to save AOI
        emit('aoi-created', coords);
        
        map.value.removeInteraction(draw.value);
    });
};

const emit = defineEmits(['aoi-created']);

defineExpose({ startDrawing });
</script>

<template>
  <div ref="mapContainer" class="w-full h-full rounded-xl overflow-hidden shadow-2xl border border-gray-700"></div>
</template>

<style scoped>
/* Custom overrides if needed */
</style>
