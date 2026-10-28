// نقوم بإنشاء المحرك الخاص بنا الذي يحتوي على كل منطق العرض
const OranMap = {
    map: null,
    init: function(divId, center, zoom) {
        this.map = L.map(divId).setView(center, zoom);
        
        L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}', {
            attribution: 'Tiles &copy; Esri &mdash; Esri, DeLorme, NAVTEQ, TomTom, Intermap, iPC, USGS, FAO, NPS, NRCAN, GeoBase, IGN, Kadaster NL, Ordnance Survey, Esri Japan, METI, Esri China (Hong Kong), and the GIS User Community',
            maxZoom: 18
        }).addTo(this.map); // ✅ تم التعديل هنا إلى this.map

        return this.map;
    },

    // دالة ذكية: تكتشف النوع وتضيفه تلقائياً
    addLayer: function(jsonData, color) {
        if (!jsonData || !jsonData.features || jsonData.features.length === 0) return;
        
        let type = jsonData.features[0].geometry.type;

        if (type.includes("Polygon")) {
            L.geoJSON(jsonData, { style: { color: color || "#1b5e20", weight: 2, fillOpacity: 0.5 } }).addTo(this.map);
        } else {
            L.geoJSON(jsonData, {
                onEachFeature: function(f, layer) {
                    if (f.properties) {
                        layer.bindPopup(`<b>${f.properties.Name || f.properties.name || ""}</b><br>${f.properties.Full_Addre || ""}`);
                    }
                }
            }).addTo(this.map);
        }
    }
};