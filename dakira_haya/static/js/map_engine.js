// دالة لإغلاق العرض والعودة للوضع الافتراضي
function stopAndReset() {
    // 1. مسح العلامات والنافذة المنبثقة
    if (currentElements.marker) currentElements.marker.remove();
    if (currentElements.popup) currentElements.popup.remove();
    
    // 2. مسح أي مسارات (خطوط) مرسومة
    const layers = map.getStyle().layers;
    layers.forEach(layer => {
        if (layer.id.startsWith('path-')) {
            map.removeLayer(layer.id);
            map.removeSource(layer.id);
        }
    });
    
    // 3. إخفاء العناصر التفاعلية
    const controls = document.getElementById('controls-overlay');
    if (controls) controls.style.display = 'none';
    
    // 4. العودة لمنظور الجزائر العام
    map.flyTo({ center: [3.0, 34.0], zoom: 5.5, pitch: 45 });
}