window.event_science = { 
    title: "السيرة الكاملة للعلامة عبد الحميد بن باديس",
    icon_url: "https://img.icons8.com/color/96/scholar.png",
    bg_card: "/static/images/science_bg.jpg", 
    animation_steps: [
        { name: "المولد والبيئة (قسنطينة 1889)", coords: [6.6118, 36.3676], action: "ولد في بيت علم وجاه. حفظ القرآن في سن الـ13 على يد الشيخ محمد المادي، مما شكل قاعدته الروحية الأولى.", image: "/static/images/step1.jpg" },
        { name: "جامع الزيتونة (تونس 1908)", coords: [10.1706, 36.7972], action: "درس على يد كبار العلماء مثل العلامة الطاهر بن عاشور. هنا تبلورت فكرته عن النهضة الإسلامية الشاملة.", image: "/static/images/step2.jpg" },
        { name: "رحلة الحجاز والمدينة (1913)", coords: [39.6111, 24.4672], action: "في المدينة المنورة، التقى بشيخه البشير الإبراهيمي ووضعوا 'خطة الـ30 سنة' لبعث الأمة الجزائرية من جديد.", image: "/static/images/step3.jpg" },
        { name: "العودة وبداية التغيير (قسنطينة)", coords: [6.6110, 36.3670], action: "بدأ بإلقاء دروس التفسير في الجامع الأخضر، محارباً الخرافات والجمود الفكري الذي فرضه الاستعمار.", image: "/static/images/step4.jpg" },
        { name: "سلاح الصحافة (المنتقد والشهاب)", coords: [6.6135, 36.3685], action: "أسس جريدة 'المنتقد' ثم 'الشهاب' لتكون منبراً فكرياً يوقظ الوعي الوطني ويرد على ادعاءات المستعمر.", image: "/static/images/step5.jpg" },
        { name: "تأسيس الجمعية (العاصمة 1931)", coords: [3.0588, 36.7538], action: "جمع شمل العلماء وأسس 'جمعية العلماء المسلمين'. كان يطوف القرى والمدن لفتح المدارس العربية الحرة.", image: "/static/images/step6.jpg" },
        { name: "المؤتمر الإسلامي (1936)", coords: [3.0440, 36.7520], action: "قاد الوفد الجزائري إلى باريس للمطالبة بحقوق الشعب الجزائري، رافضاً سياسة الإدماج والفرنسة.", image: "/static/images/step7.jpg" },
        { name: "مواجهة الاستعمار", coords: [6.6118, 36.3676], action: "تعرض لمحاولات اغتيال وضغوطات شديدة، لكنه ظل يردد: 'إن الأمة الجزائرية ليست هي فرنسا، ولا يمكن أن تكون فرنسا'.", image: "/static/images/step8.jpg" },
        { name: "الوفاة والوداع الأخير (1940)", coords: [6.6118, 36.3676], action: "في 16 أفريل 1940، رحل الشيخ تاركاً وراءه جيلاً متعلماً حمل شعلة الثورة التحريرية لاحقاً.", image: "/static/images/step9.jpg" }
    ]
};

window.runScienceExperience = function(map) {
    let data = window.event_science;
    let stepIdx = 0;
    let currentRouteId = null;
    let markers = [];

    const style = document.createElement('style');
    // زر العودة للخلف
    const backBtn = document.createElement('button');
    backBtn.innerHTML = '<i class="fas fa-arrow-right"></i> خروج';
    backBtn.style.cssText = "position:absolute; top:20px; left:20px; z-index:1000; padding:10px 20px; background:#c62828; color:white; border:none; border-radius:25px; cursor:pointer; font-family:'Cairo';";
    backBtn.onclick = () => window.location.href = '/liste/'; // مسار صفحة القائمة الخاصة بك
    document.body.appendChild(backBtn);
    style.innerHTML = `
        @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
        
        .science-card-custom {
            width: 280px; padding: 12px; border-radius: 15px; border: 3px solid #1b5e20;
            background: url('${data.bg_card}') no-repeat center; background-size: cover;
            font-family: 'Cairo', sans-serif; text-align: center; position: relative;
            animation: bounceIn 0.8s forwards; box-shadow: 0 15px 35px rgba(0,0,0,0.4);
        }

        .step-img-frame { 
            width: 100%; height: 180px; overflow: hidden; border-radius: 10px; 
            border: 2px solid #1b5e20; background-color: rgba(0,0,0,0.1); 
            display: flex; align-items: center; justify-content: center;
        }

        .step-img-custom { max-width: 100%; max-height: 100%; object-fit: contain; display: block; }
        
        .card-shine { position: absolute; top: 0; left: -100%; width: 50%; height: 100%; background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent); animation: shine 3s infinite; }

        /* تنسيقات النافذة النهائية المتطورة */
        .final-container {
            position: relative; width: 100%; height: 100%; display: flex; align-items: center; justify-content: center;
            font-family: 'Cairo', sans-serif; overflow: hidden;
        }
        .final-msg-card {
            background: url('${data.bg_card}') no-repeat center; background-size: cover;
            padding: 35px; border-radius: 20px; border: 6px solid #1b5e20;
            width: 500px; text-align: center; font-family: 'Cairo'; color: #1a1a1a;
            box-shadow: 0 0 50px rgba(0,0,0,0.6); animation: bounceIn 1s forwards; z-index: 100;
        }
        .side-photo { position: absolute; border-radius: 50%; border: 3px solid #1b5e20; object-fit: cover; z-index: 50; box-shadow: 0 4px 15px rgba(0,0,0,0.3); }
        .deco-circle { position: absolute; border: 2px dashed #FFD700; border-radius: 50%; opacity: 0.5; z-index: 10; }

        @keyframes rotateCW { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
        @keyframes rotateCCW { from { transform: rotate(360deg); } to { transform: rotate(0deg); } }
        @keyframes bounceIn { 0% { transform: scale(0.5); opacity: 0; } 100% { transform: scale(1); opacity: 1; } }
        @keyframes shine { 0% { left: -100%; } 100% { left: 150%; } }
    `;
    document.head.appendChild(style);

    function drawPersistentPath(start, end) {
        if (currentRouteId && map.getLayer(currentRouteId)) {
            map.removeLayer(currentRouteId); map.removeSource(currentRouteId);
        }
        currentRouteId = 'path-' + Date.now();
        map.addSource(currentRouteId, { 'type': 'geojson', 'data': { 'type': 'Feature', 'geometry': { 'type': 'LineString', 'coordinates': [start, end] } } });
        map.addLayer({
            'id': currentRouteId, 'type': 'line', 'source': currentRouteId,
            'paint': { 'line-color': '#FFD700', 'line-width': 6, 'line-dasharray': [1, 1], 'line-opacity': 0.9 }
        });
    }

    function playNext() {
        if (stepIdx >= data.animation_steps.length) {
            if (currentRouteId && map.getLayer(currentRouteId)) {
                map.removeLayer(currentRouteId); map.removeSource(currentRouteId);
            }
            
            // 1. العودة للخريطة بالكامل
            map.flyTo({ center: [10, 32], zoom: 4.5, pitch: 0, speed: 0.2 });
            
            map.once('moveend', () => {
                // 2. إظهار كافة المواقف (Markers) أولاً
                data.animation_steps.forEach((s, i) => {
                    setTimeout(() => {
                        let m = new maplibregl.Marker({color: "#1b5e20"}).setLngLat(s.coords).addTo(map);
                        markers.push(m);
                    }, i * 300);
                });

                // 3. إظهار الرسالة النهائية بعد اكتمال ظهور المواقف
                setTimeout(() => {
                    const ov = document.getElementById('overlay');
                    ov.style.display = 'flex';
                    ov.innerHTML = `
                        <div class="final-container">
                            <div class="deco-circle" style="width:300px; height:300px; right:5%; animation: rotateCW 15s linear infinite;"></div>
                            <div class="deco-circle" style="width:450px; height:450px; right:2%; animation: rotateCW 20s linear infinite;"></div>
                            <div class="deco-circle" style="width:600px; height:600px; right:-5%; animation: rotateCW 25s linear infinite;"></div>

                            <div class="deco-circle" style="width:300px; height:300px; left:5%; animation: rotateCCW 15s linear infinite;"></div>
                            <div class="deco-circle" style="width:450px; height:450px; left:2%; animation: rotateCCW 20s linear infinite;"></div>
                            <div class="deco-circle" style="width:600px; height:600px; left:-5%; animation: rotateCCW 25s linear infinite;"></div>

                            <img src="/static/images/step1.jpg" class="side-photo" style="width:90px; height:90px; right:12%; top:15%;">
                            <img src="/static/images/step3.jpg" class="side-photo" style="width:110px; height:110px; right:8%; top:45%;">
                            <img src="/static/images/step5.jpg" class="side-photo" style="width:90px; height:90px; right:12%; bottom:15%;">
                            
                            <img src="/static/images/step2.jpg" class="side-photo" style="width:90px; height:90px; left:12%; top:15%;">
                            <img src="/static/images/step4.jpg" class="side-photo" style="width:110px; height:110px; left:8%; top:45%;">
                            <img src="/static/images/step6.jpg" class="side-photo" style="width:90px; height:90px; left:12%; bottom:15%;">

                            <div class="final-msg-card">
                                <img src="https://upload.wikimedia.org/wikipedia/commons/7/77/Flag_of_Algeria.svg" style="width:70px; margin-bottom:10px;">
                                <img src="/static/images/step9.jpg" style="width:140px; height:140px; border-radius:50%; border:5px solid #1b5e20; object-fit:cover; margin-bottom:15px; display:block; margin-left:auto; margin-right:auto;">
                                <h2 style="color:#1b5e20; margin-top:0;">رسالة العلامة إلى شباب الجزائر</h2>
                                <div style="font-size:1.1rem; line-height:1.6; font-style:italic; border-top:2px solid #1b5e20; padding-top:15px; margin-bottom:20px;">
                                    "يا شباب الجزائر، إنما أنتم آمالنا، فكونوا على قدر الأمانة.. تعلموا، فإن العلم سلاح الأحرار، وحافظوا على هويتكم، فإنها حصنكم المنيع."
                                </div>
                                <button onclick="location.reload()" style="background:#1b5e20; color:white; border:none; padding:12px 50px; border-radius:30px; cursor:pointer; font-weight:bold; font-family:'Cairo';">بناء المستقبل</button>
                            </div>
                        </div>`;
                }, 4000);
            });
            return;
        }

        const step = data.animation_steps[stepIdx];
        const prevStep = stepIdx > 0 ? data.animation_steps[stepIdx-1] : null;

        if (prevStep) drawPersistentPath(prevStep.coords, step.coords);

        map.flyTo({ center: step.coords, zoom: 16, pitch: 65, speed: 0.18, curve: 1.5 });

        map.once('moveend', () => {
            setTimeout(() => {
                const popup = new maplibregl.Popup({ offset: 40, closeButton: false, anchor: 'bottom' })
                    .setLngLat(step.coords)
                    .setHTML(`
                        <div class="science-card-custom">
                            <div class="card-shine"></div>
                            <div class="step-img-frame"><img src="${step.image}" class="step-img-custom"></div>
                            <h3 style="color:#1b5e20; margin:10px 0 5px 0; font-size:1.1rem;">${step.name}</h3>
                            <p style="font-size:0.9rem; line-height:1.4;">${step.action}</p>
                        </div>
                    `).addTo(map);

                stepIdx++;
                setTimeout(() => { popup.remove(); playNext(); }, 9000);
            }, 1000);
        });
    }
    playNext();
};