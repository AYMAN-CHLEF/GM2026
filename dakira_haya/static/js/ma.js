// 1. تهيئة الخريطة الأساسية
const map = new maplibregl.Map({
    container: 'map',
    style: {
        "version": 8,
        "sources": {
            "satellite": { 
                "type": "raster", 
                "tiles": ["https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}"], 
                "tileSize": 256,
                "attribution": "Map data © Google"
            }
        },
        "layers": [
            {
                "id": "sat-layer", 
                "type": "raster", 
                "source": "satellite"
            }
        ]
    },
    center: [3.0, 34.0], 
    zoom: 5.5, 
    pitch: 45, 
    antialias: true 
});

// 2. إدارة العناصر العالمية
window.currentElements = { marker: null, popup: null };

// 3. دالة إضافة العلامات
function addFigureToMap(coords, name, info, color = "#1b5e20") {
    const el = document.createElement('div');
    el.className = 'custom-marker';
    el.style.cssText = `background-color:${color}; width:30px; height:30px; border-radius:50%; border:3px solid #FFD700; cursor:pointer; box-shadow:0 0 10px rgba(0,0,0,0.5);`;
    
    return new maplibregl.Marker(el)
        .setLngLat(coords)
        .setPopup(new maplibregl.Popup({ offset: 25 }).setHTML(`<div style="text-align:right; font-family:'Cairo';"><h3>${name}</h3><p>${info}</p></div>`))
        .addTo(map);
}

// 4. نظام التحكم في التجربة
let isPlaying = false;
let isMuted = false;

// استخدام المسار الذي تم تمريره من ملف الـ HTML
const audioPlayer = new Audio(window.AUDIO_PATH || '');
audioPlayer.loop = true;

document.addEventListener('DOMContentLoaded', () => {
    
    // زر التشغيل/الإيقاف
    document.getElementById('toggle-btn').addEventListener('click', function() {
        const icon = this.querySelector('i');
        isPlaying = !isPlaying; 
        
        if (isPlaying) {
            icon.className = 'fas fa-pause';
            if (typeof window.runScienceExperience === 'function') {
                window.runScienceExperience(map);
            }
        } else {
            icon.className = 'fas fa-play';
            if (typeof stopAndReset === 'function') stopAndReset();
        }
    });

    // زر الصوت
    document.getElementById('audio-btn').addEventListener('click', function() {
        const icon = this.querySelector('i');
        isMuted = !isMuted;
        
        icon.className = isMuted ? 'fas fa-volume-mute' : 'fas fa-volume-up';
        
        if (isMuted) {
            audioPlayer.pause();
            console.log("الصوت: مكتوم");
        } else {
            audioPlayer.play().catch(e => console.log("يجب التفاعل مع الصفحة أولاً لتشغيل الصوت"));
            console.log("الصوت: مفعل");
        }
    });
});

// 5. تهيئة التشغيل عند جاهزية الخريطة
map.on('load', () => {
    console.log("خريطة أطلس الذاكرة جاهزة.");
    const loader = document.getElementById('loading-overlay');
    if (loader) loader.style.display = 'none';
});