/**
 * oran.js - النسخة المُطهرة والمستقرة والمُصححة
 */

document.addEventListener("DOMContentLoaded", function() {

    // 1. الإعدادات الأساسية
    const map = L.map('map', {
        zoomControl: false,
        maxZoom: 28,
        minZoom: 1
    }).fitBounds([
        [35.20024, -1.37657], 
        [35.98634, 0.26862]
    ]);

    // حماية: إضافة L.Hash فقط إذا كانت المكتبة محملة
    if (typeof L.Hash !== 'undefined') {
        new L.Hash(map);
    }

    // 2. دالة التفاعل مع كل عنصر (onEachFeature)
    function onEachFeature(feature, layer) {
        const p = feature.properties || {};
        
        // شرط التمييز: البطاقة تظهر فقط إذا كان العنصر "نقطة" (Point)
        if (feature.geometry && feature.geometry.type === "Point" && p.hasOwnProperty('Photo_Filename')) {
            
            const name = p['Name'] || "معلم تاريخي";
            const photoName = p['Photo_Filename'] || "";
            const mapUrl = p['Map'] || "#";
            
            // المسار الصحيح للصور
            const fullImgPath = photoName ? `/static/images/${photoName}` : null;
            
            // توليد الـ QR كود ديناميكياً
            const qrCodeUrl = `https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=${encodeURIComponent(mapUrl)}`;

            // بناء المحتوى
            const content = `
            <div class="custom-popup" style="direction: rtl; text-align: right; width: 250px; font-family: sans-serif;">
                <div class="popup-name" style="background:#1b5e20; color:#d4af37; padding:8px; border-radius:8px; font-weight:bold; text-align:center; margin-bottom:10px;">
                    ${name}
                </div>
                
                <div style="width:100%; height:160px; background:#f0f0f0; border-radius:10px; overflow:hidden; border:1px solid #ddd; margin-bottom:10px;">
                    ${fullImgPath ? 
                        `<img src="${fullImgPath}" class="popup-main-img" style="width:100%; height:100%; object-fit:cover;" onerror="this.style.display='none';">` : 
                        `<div style="display:flex; align-items:center; justify-content:center; height:100%; color:#888;">لا توجد صورة</div>`
                    }
                </div>

                <div class="popup-address" style="margin-bottom:10px; font-size: 13px; color: #444;">📍 ${p['Full_Addre'] || 'وهران، الجزائر'}</div>

                <div style="display:flex; align-items:center; gap:10px; background:rgba(0,0,0,0.05); padding:8px; border-radius:8px;">
                    <div class="qr-container" style="background:white; padding:5px; border-radius:5px; border: 1px solid #ddd;">
                        <img src="${qrCodeUrl}" style="width:50px; height:50px;" alt="QR">
                    </div>
                    <div style="flex:1; display:flex; flex-direction:column; gap:5px;">
                        <a href="${mapUrl}" target="_blank" style="background:#4285F4; color:white; text-decoration:none; padding:4px 8px; border-radius:5px; font-size:11px; font-weight:bold; text-align:center;">🗺️ الموقع</a>
                        <a href="https://wa.me/?text=${encodeURIComponent('شاهد ' + name + ' هنا: ' + mapUrl)}" target="_blank" style="background:#25D366; color:white; text-decoration:none; padding:4px 8px; border-radius:5px; font-size:11px; font-weight:bold; text-align:center;">📱 واتساب</a>
                    </div>
                </div>
            </div>`;

            layer.bindPopup(content, { maxWidth: 300 });
            
        } else {
            // إذا كان العنصر عبارة عن بلدية (Polygon)
            if (p['Name']) {
                layer.bindPopup(`<div style="font-weight:bold; text-align:center;">${p['Name']}</div>`);
            }
        }
    }

    // 3. إضافة طبقة الخريطة الأساسية (Esri World Topo Map - مجانية ومستقرة جداً)
    L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}', {
        attribution: 'Tiles &copy; Esri',
        maxZoom: 18
    }).addTo(map);

    // 4. تعريف الطبقات
    const layers = [
        { data: window.json__1, name: 'pane__1', style: {color: 'rgba(0,0,0,0.5)', fillColor: 'rgba(76,73,72,0.5)', fillOpacity: 0.5, weight: 2} },
        { data: window.json__2, name: 'pane__2', icon: '_2.svg' },
        { data: window.json__3, name: 'pane__3', icon: '_3.svg' },
        { data: window.json__4, name: 'pane__4', icon: '_4.svg' },
        { data: window.json__5, name: 'pane__5', icon: '_5.svg' },
        { data: window.json__6, name: 'pane__6', icon: '_6.svg' }
    ];

    layers.forEach((l) => {
        if (!l.data) return; // حماية من الملفات غير المعرفة
        
        L.geoJson(l.data, {
            onEachFeature: onEachFeature,
            pointToLayer: l.icon ? (f, ll) => L.marker(ll, { 
                icon: L.icon({ 
                    iconUrl: `/static/markers/${l.icon}`, // تم تعديل المسار هنا لتجنب خطأ staticUrl
                    iconSize: [25, 25] 
                }) 
            }) : null,
            style: l.style || null
        }).addTo(map);
    });

    // 5. أدوات التحكم
    L.control.zoom({ position: 'topleft' }).addTo(map);
    L.control.scale({ position: 'bottomleft', metric: true, imperial: false }).addTo(map);
});