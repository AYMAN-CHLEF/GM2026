// 1. تهيئة الخريطة
var map = L.map('map').setView([34.5, 3.5], 6);

// استبدل السطر القديم بهذا:
L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}', {
    attribution: 'Tiles &copy; Esri &mdash; Esri, DeLorme, NAVTEQ, TomTom, Intermap, iPC, USGS, FAO, NPS, NRCAN, GeoBase, IGN, Kadaster NL, Ordnance Survey, Esri Japan, METI, Esri China (Hong Kong), and the GIS User Community',
    maxZoom: 18
}).addTo(map);

var myChart;
    // --- مكتبة المعارك ومراكز القيادة التاريخية الشاملة ---
var battleDataLibrary = {
    "type": "FeatureCollection",
    "features": [
        // --- الولاية الأولى (الأوراس) ---
        {
            "type": "Feature",
            "properties": {
                "Name": "معركة الجرف الكبرى",
                "Type": "battle",
                "Wilaya": "الولاية الأولى (الأوراس)",
                "Date": "22 سبتمبر 1955",
                "Leader": "بشير شيحاني / عباس لغرور",
                "Description": "أكبر معركة في بداية الثورة، واجه فيها 400 مجاهد أكثر من 20 ألف جندي فرنسي.",
                "Outcome": "تكبيد العدو خسائر فادحة (حوالي 700 قتيل) واغتنام أسلحة كثيرة."
            },
            "geometry": { "type": "Point", "coordinates": [7.28, 34.88] }
        },
        {
            "type": "Feature",
            "properties": {
                "Name": "مركز قيادة جبل شلية",
                "Type": "center",
                "Wilaya": "الولاية الأولى",
                "Date": "1954-1956",
                "Leader": "مصطفى بن بولعيد",
                "Description": "أعلى قمة في الأوراس، كانت مقراً لاجتماعات قادة الأوراس والتخطيط للهجمات الأولى.",
                "Importance": "موقع حصين يصعب اختراقه من قبل قوات الاحتلال."
            },
            "geometry": { "type": "Point", "coordinates": [6.63, 35.32] }
        },

        // --- الولاية الثانية (الشمال القسنطيني) ---
        {
            "type": "Feature",
            "properties": {
                "Name": "هجومات 20 أوت 1955",
                "Type": "battle",
                "Wilaya": "الولاية الثانية (قسنطينة/سكيكدة)",
                "Date": "20 أوت 1955",
                "Leader": "زيغود يوسف",
                "Description": "نقطة تحول كبرى شملت هجمات منسقة على مراكز العدو في 26 مدينة وقرية.",
                "Outcome": "فك الحصار عن الأوراس ونقل الثورة إلى المدن الكبرى."
            },
            "geometry": { "type": "Point", "coordinates": [6.93, 36.72] }
        },
        {
            "type": "Feature",
            "properties": {
                "Name": "مركز وادي بوكركر",
                "Type": "center",
                "Wilaya": "الولاية الثانية",
                "Date": "1955",
                "Leader": "زيغود يوسف",
                "Description": "المكان الذي خطط فيه الشهيد زيغود يوسف لهجمات 20 أوت التاريخية.",
                "Importance": "مركز إدارة العمليات في الشمال القسنطيني."
            },
            "geometry": { "type": "Point", "coordinates": [6.65, 36.50] }
        },

        // --- الولاية الثالثة (القبائل) ---
        {
            "type": "Feature",
            "properties": {
                "Name": "مركز قيادة أكفادو (مغارة عميروش)",
                "Type": "center",
                "Wilaya": "الولاية الثالثة",
                "Date": "1956-1959",
                "Leader": "العقيد عميروش",
                "Description": "المقر الحصين في غابة أكفادو ببيجاية، كان يضم أجهزة لاسلكي ومستشفى عسكري.",
                "Importance": "تنسيق العمليات بين الولايات وضمان الاتصال مع القيادة في تونس."
            },
            "geometry": { "type": "Point", "coordinates": [4.58, 36.68] }
        },
        {
            "type": "Feature",
            "properties": {
                "Name": "معركة إيفري",
                "Type": "battle",
                "Wilaya": "الولاية الثالثة",
                "Date": "أوت 1956",
                "Leader": "عبان رمضان / العربي بن مهيدي",
                "Description": "وقعت في قرية إيفري أوزلاقن تزامناً مع انعقاد مؤتمر الصومام التاريخي.",
                "Outcome": "تأمين نجاح المؤتمر الذي وضع الهياكل التنظيمية للثورة."
            },
            "geometry": { "type": "Point", "coordinates": [4.54, 36.52] }
        },

        // --- الولاية الرابعة (الجزائر/البليدة) ---
        {
            "type": "Feature",
            "properties": {
                "Name": "مركز قيادة جبل الونشريس",
                "Type": "center",
                "Wilaya": "الولاية الرابعة",
                "Date": "1957",
                "Leader": "سي امحمد بوقرة",
                "Description": "مقر قيادة الولاية الرابعة في منطقة جبلية وعرة بين تيسمسيلت والمدية.",
                "Importance": "قاعدة انطلاق العمليات نحو قلب العاصمة والمدن المجاورة."
            },
            "geometry": { "type": "Point", "coordinates": [1.95, 35.88] }
        },
        {
            "type": "Feature",
            "properties": {
                "Name": "معركة جبل بوزقزة",
                "Type": "battle",
                "Wilaya": "الولاية الرابعة",
                "Date": "أوت 1957",
                "Leader": "سي لخضر بوشمع",
                "Description": "معركة بطولية قرب العاصمة واجه فيها المجاهدون فيلقاً كاملاً من المظليين الفرنسيين.",
                "Outcome": "سحق قوات النخبة الفرنسية (بيجار) وإسقاط طائرات مروحية."
            },
            "geometry": { "type": "Point", "coordinates": [3.45, 36.62] }
        },

        // --- الولاية الخامسة (الوهراني) ---
        {
            "type": "Feature",
            "properties": {
                "Name": "معركة جبل جحفة",
                "Type": "battle",
                "Wilaya": "الولاية الخامسة",
                "Date": "1956",
                "Leader": "قادة الغرب الجزائري",
                "Description": "معركة طاحنة وقعت في تلمسان ضد قوات الاحتلال المتمركزة قرب الحدود.",
                "Outcome": "تأمين خطوط الإمداد بالسلاح من المغرب نحو الداخل."
            },
            "geometry": { "type": "Point", "coordinates": [-1.32, 34.88] }
        },

        // --- الولاية السادسة (الصحراء) ---
        {
            "type": "Feature",
            "properties": {
                "Name": "معركة جبل ثامر",
                "Type": "battle",
                "Wilaya": "الولاية السادسة",
                "Date": "28 مارس 1959",
                "Leader": "العقيد عميروش وسي الحواس",
                "Description": "معركة غير متكافئة استبسل فيها القائدان ضد آلاف الجنود المدعومين بالطيران.",
                "Outcome": "استشهاد العقيدين عميروش وسي الحواس في ملحمة خالدة."
            },
            "geometry": { "type": "Point", "coordinates": [3.95, 35.15] }
        },
          // --- الولاية الخامسة (وهران، تلمسان، سيدي بلعباس، عين تموشنت، مستغانم) ---
        {
            "type": "Feature",
            "properties": {
                "Name": "معركة فلاوسن",
                "Type": "battle",
                "Wilaya": "الولاية الخامسة",
                "Date": "1957-04-20", // تنسيق YYYY-MM-DD لتسهيل عمل الشريط الزمني
                "Leader": "قادة المنطقة الثانية (تلمسان)",
                "Description": "من أضخم معارك الغرب الجزائري بجبال فلاوسن، شاركت فيها قوات فرنسية ضخمة مدعومة بالطيران.",
                "Outcome": "تكبيد الاحتلال أكثر من 500 قتيل واعتراف العدو بشراسة المقاومة."
            },
            "geometry": { "type": "Point", "coordinates": [-1.65, 35.05] }
        },
        {
            "type": "Feature",
            "properties": {
                "Name": "مركز قيادة غار بوجليدة",
                "Type": "center",
                "Wilaya": "الولاية الخامسة",
                "Date": "1956-01-01",
                "Leader": "سي لوتفي / هواري بومدين",
                "Description": "مغارة استراتيجية في جبال تلمسان كانت مقراً لإدارة العمليات بالغرب والاتصال بالقاعدة الخلفية.",
                "Importance": "نقطة استلام وتوزيع السلاح القادم من وراء الحدود."
            },
            "geometry": { "type": "Point", "coordinates": [-1.35, 34.85] }
        },
        {
            "type": "Feature",
            "properties": {
                "Name": "معركة جبل بيض",
                "Type": "battle",
                "Wilaya": "الولاية الخامسة",
                "Date": "1956-05-18",
                "Leader": "أحمد مدغري",
                "Description": "معركة استهدفت قوافل الإمداد الفرنسية بمنطقة سعيدة.",
                "Outcome": "غنم كميات معتبرة من الذخيرة ورفع الروح المعنوية بالغرب."
            },
            "geometry": { "type": "Point", "coordinates": [0.15, 34.83] }
        },

        // --- الولاية السادسة (الصحراء، بسكرة، المسيلة، الجلفة، الأغواط) ---
        {
            "type": "Feature",
            "properties": {
                "Name": "معركة جبل ثامر",
                "Type": "battle",
                "Wilaya": "الولاية السادسة",
                "Date": "1959-03-28",
                "Leader": "العقيد عميروش وسي الحواس",
                "Description": "الملحمة التي استشهد فيها قائد الولاية الثالثة والسادسة بعد وشاية كشفت موقعهما.",
                "Outcome": "استشهاد القادة وتحول المكان إلى مزار وطني يرمز للوحدة بين الولايات."
            },
            "geometry": { "type": "Point", "coordinates": [3.95, 35.15] }
        },
        {
            "type": "Feature",
            "properties": {
                "Name": "مركز قيادة القعدة (الجلفة)",
                "Type": "center",
                "Wilaya": "الولاية السادسة",
                "Date": "1958-01-01",
                "Leader": "سي الحواس",
                "Description": "موقع حصين في جبال القعدة الوعرة، اتخذه سي الحواس مركزاً لإعادة تنظيم الولاية السادسة.",
                "Importance": "تأمين الطرق الصحراوية وربط الشمال بالجنوب."
            },
            "geometry": { "type": "Point", "coordinates": [3.05, 34.15] }
        },
        {
            "type": "Feature",
            "properties": {
                "Name": "معركة جبل قعيقع",
                "Type": "battle",
                "Wilaya": "الولاية السادسة",
                "Date": "1956-12-05",
                "Leader": "عمر إدريس",
                "Description": "مواجهة كبرى ضد قوات الجنرال 'بلون' الموالي لفرنسا.",
                "Outcome": "تطهير المنطقة من الطابور الخامس وتثبيت سلطة جيش التحرير في الصحراء."
            },
            "geometry": { "type": "Point", "coordinates": [3.50, 35.30] }
        },
        {
            "type": "Feature",
            "properties": {
                "Name": "مركز جبل بوكحيل",
                "Type": "center",
                "Wilaya": "الولاية السادسة",
                "Date": "1961-01-01",
                "Leader": "شعباني محمد",
                "Description": "معقل الولاية السادسة المنيع، شهد معارك طاحنة في أواخر الثورة.",
                "Importance": "أفشل مخططات فرنسا لفصل الصحراء عن بقية الجزائر."
            },
            "geometry": { "type": "Point", "coordinates": [4.15, 34.60] }
        },
        {

            "type": "Feature",
            "properties": {
                "Name": "معركة جبل بوكحيل",
                "Type": "battle",
                "Wilaya": "الولاية السادسة",
                "Date": "1961-09-17",
                "Leader": "العقيد شعباني",
                "Description": "من أشرس معارك الصحراء، واجه فيها المجاهدون قوات النخبة الفرنسية في تضاريس وعرة.",
                "Outcome": "فشل فرنسا في تطويق الولاية السادسة وإثبات قوة الثورة في العمق الصحراوي."
            },
            "geometry": { "type": "Point", "coordinates": [4.12, 34.58] }
        },
        {
            "type": "Feature",
            "properties": {
                "Name": "معركة حاسي ساخي (عين صالح)",
                "Type": "battle",
                "Wilaya": "الجنوب الكبير",
                "Date": "1958-11-20",
                "Leader": "قوات المنطقة الصحراوية",
                "Description": "هجوم جريء على قافلة عسكرية فرنسية لتأمين طريق الإمداد الجنوبي.",
                "Outcome": "زعزعة أمن الاحتلال في المناطق النفطية الاستراتيجية."
            },
            "geometry": { "type": "Point", "coordinates": [2.48, 27.20] }
        },
        {
            "type": "Feature",
            "properties": {
                "Name": "مركز قيادة القعدة (أفلو)",
                "Type": "center",
                "Wilaya": "الولاية السادسة",
                "Date": "1957-06-15",
                "Leader": "سي الحواس",
                "Description": "مقر حصين وسط سلسلة جبال القعدة، كان نقطة ربط بين التل والجنوب.",
                "Importance": "إدارة العمليات العسكرية في الهضاب العليا والصحراء."
            },
            "geometry": { "type": "Point", "coordinates": [2.12, 34.11] }
        },

        // --- الولاية الخامسة (الغرب والحدود الغربية) ---
        {
            "type": "Feature",
            "properties": {
                "Name": "معركة جبل عصفور (الحدود)",
                "Type": "battle",
                "Wilaya": "الولاية الخامسة",
                "Date": "1956-10-12",
                "Leader": "سي لوتفي",
                "Description": "مواجهة كبرى لتأمين عبور قوافل السلاح عبر خط موريس بالغرب.",
                "Outcome": "اختراق ناجح لخطوط العدو وإيصال السلاح للداخل."
            },
            "geometry": { "type": "Point", "coordinates": [-1.78, 34.75] }
        },
        // --- القاعدة الخلفية (تصحيح خطأ وجدة) ---
        {
            "type": "Feature",
            "properties": {
                "Name": "مركز قيادة وجدة (المالك)",
                "Type": "center",
                "Wilaya": "القاعدة الخلفية (الغرب)",
                "Date": "1956-01-01",
                "Leader": "عبد الحفيظ بوصوف",
                "Description": "مركز 'المالك' الشهير؛ مهد المخابرات الجزائرية والاتصالات اللاسلكية وتدريب التقنيين.",
                "Importance": "تأمين الاتصالات المشفرة بين قيادة الثورة والولايات الداخليه."
            },
            "geometry": { "type": "Point", "coordinates": [-1.911, 34.842] }
        },

        // --- أقصى الجنوب (إبراز البعد الجغرافي) ---
        {
            "type": "Feature",
            "properties": {
                "Name": "معركة 'تيمياوين' (أقصى الجنوب)",
                "Type": "battle",
                "Wilaya": "الولاية السادسة",
                "Date": "1960-10-15",
                "Leader": "فصيلة من المنطقة السادسة",
                "Description": "معركة جرت في أقصى الحدود الجنوبية لمواجهة محاولات الاحتلال مراقبة طرق القوافل.",
                "Outcome": "تأكيد امتداد الثورة إلى عمق الصحراء الكبرى."
            },
            "geometry": { "type": "Point", "coordinates": [1.812, 20.441] }
        },

        // --- الحدود الشرقية (تأمين العبور) ---
        {
            "type": "Feature",
            "properties": {
                "Name": "معركة جبل الكويف",
                "Type": "battle",
                "Wilaya": "القاعدة الشرقية (تبسة)",
                "Date": "1955-06-21",
                "Leader": "لغرور عباس",
                "Description": "مواجهة طاحنة لتأمين عبور السلاح من تونس نحو منطقة الأوراس.",
                "Outcome": "إلحاق خسائر كبيرة بجيش الاحتلال وكسر حصار خط موريس المبكر."
            },
            "geometry": { "type": "Point", "coordinates": [8.315, 35.412] }
        },

        // --- الولاية الخامسة (معارك الحدود) ---
        {
            "type": "Feature",
            "properties": {
                "Name": "معركة 'بني سنوس'",
                "Type": "battle",
                "Wilaya": "الولاية الخامسة",
                "Date": "1957-08-10",
                "Leader": "سي لوتفي",
                "Description": "واحدة من معارك الاستنزاف الكبرى في جبال تلمسان الحدودية.",
                "Outcome": "إرباك المخططات الفرنسية الرامية لعزل الداخل عن المدد المغربي."
            },
            "geometry": { "type": "Point", "coordinates": [-1.458, 34.641] }
        },

        // --- مركز قيادة جبل بومطماط (الصحراء) ---
        {
            "type": "Feature",
            "properties": {
                "Name": "مركز قيادة جبل بومطماط",
                "Type": "center",
                "Wilaya": "الولاية السادسة",
                "Date": "1959-05-12",
                "Leader": "العقيد سي الحواس",
                "Description": "موقع حصين استخدم لإدارة شؤون المجاهدين في مناطق المسيلة وبوسعادة.",
                "Importance": "تنسيق التحركات العسكرية في منطقة الهضاب والجنوب."
            },
            "geometry": { "type": "Point", "coordinates": [4.215, 35.084] }
        },

        // --- الولاية الثانية (أقصى الشرق والحدود) ---
        {
            "type": "Feature",
            "properties": {
                "Name": "معركة سوق أهراس الكبرى",
                "Type": "battle",
                "Wilaya": "الولاية الثانية/القاعدة الشرقية",
                "Date": "1958-04-26",
                "Leader": "محمد لعموري",
                "Description": "أكبر مواجهة مباشرة (وجهاً لوجه) في تاريخ الثورة، استمرت أسبوعاً كاملاً.",
                "Outcome": "استشهاد 639 مجاهداً وقتل أكثر من 300 جندي فرنسي؛ ملحمة خط موريس."
            },
            "geometry": { "type": "Point", "coordinates": [7.95, 36.28] }
        },
        {
            "type": "Feature",
            "properties": {
                "Name": "مركز قيادة غار الدماء",
                "Type": "center",
                "Wilaya": "قاعدة الشرق",
                "Date": "1957-01-01",
                "Leader": "قيادة الأركان العامة",
                "Description": "مقر الأركان العامة لجيش التحرير بالحدود الشرقية.",
                "Importance": "تنظيم دخول الفيالق العسكرية الجزائرية نحو الداخل."
            },
            "geometry": { "type": "Point", "coordinates": [8.30, 36.45] }
        },

        // --- الولاية الرابعة (الوسط والونشريس) ---
        {
            "type": "Feature",
            "properties": {
                "Name": "معركة جبل باب البكوش",
                "Type": "battle",
                "Wilaya": "الولاية الرابعة",
                "Date": "1958-05-20",
                "Leader": "سي محمد بوقرة",
                "Description": "مواجهة استراتيجية في قلب جبال الونشريس لإفشال مخططات التمشيط الفرنسية.",
                "Outcome": "هزيمة قوات الكوماندوس الفرنسية والاستيلاء على تجهيزات لاسلكية."
            },
            "geometry": { "type": "Point", "coordinates": [1.72, 35.95] }

       }
    ]
};


    // 3. الدوال الأساسية
    function resetSidebar() {
        document.getElementById('welcome-msg').style.display = 'none';
        document.getElementById('details-content').style.display = 'block';
        document.getElementById('chart-container').style.display = 'none';
        if(myChart) myChart.destroy();
    }

    function closeSidebar() {
        document.getElementById('details-content').style.display = 'none';
        document.getElementById('welcome-msg').style.display = 'block';
    }

   // دالة عرض الولايات (مساحات) - نسخة موثقة تاريخياً
function populateWilaya(props) {
    resetSidebar();
    
    // تحديث العناوين
    document.getElementById('label-name').innerText = "قائد الولاية المؤسس:";
    
    let name = props.Wilaya || props.WILAYA || "ولاية تاريخية";
    let leader = props.leader || props.Leader || props.LEADER || "غير معروف";
    let bio = props.bio || props.Description || "وصف الولاية التاريخي.";
    
    // معالجة عدد المناطق
    let zonesCount = props.Nb_Zon || props.NB_ZONES || props.zones || props.Zones_Count || 4;

    document.getElementById('p-wilaya').innerText = name;
    document.getElementById('p-leader').innerText = leader;
    document.getElementById('p-years').innerText = props.years || "1954 - 1962";
    document.getElementById('p-bio').innerText = bio;
    document.getElementById('p-zones').innerText = zonesCount + " مناطق عسكرية عظمى";
    
    // عرض العناصر
    document.getElementById('row-zones').style.display = 'flex';
    document.getElementById('stat-btn').style.display = 'block';

    // --- تحميل الصورة ---
    let imageID = props.OBJECTID || props.id || 1;
    const container = document.getElementById('leader-img-container');
    container.innerHTML = ""; // تفريغ الحاوية أولاً

    let imgElement = document.createElement('img');
    // إزالة أي نمط مباشر (inline style) للسماح لملف الـ CSS بالتحكم
    imgElement.style = ""; 
    imgElement.src = "/static/images/" + imageID + ".jpg";

    // منطق الـ Error Handling المتسلسل
    imgElement.onerror = function() {
        if (this.src.endsWith(".jpg")) {
            this.src = "/static/images/" + imageID + ".jfif";
        } else {
            this.src = "/static/images/default.jpg";
            this.onerror = null;
        }
    };
    
    container.appendChild(imgElement);
    prepareChart(name, zonesCount);
}



    // دالة عرض المعارك والمراكز (نقاط)
    function showHistoricalDetails(props) {
        resetSidebar();
        const typeColor = props.Type === 'battle' ? '#cc0000' : '#006633';
        document.getElementById('label-name').innerText = props.Type === 'battle' ? "اسم المعركة:" : "المركز الاستراتيجي:";
        document.getElementById('p-wilaya').innerText = props.Wilaya;
        document.getElementById('p-leader').innerText = props.Name;
        document.getElementById('p-years').innerText = props.Date;
        document.getElementById('row-zones').style.display = 'none';
        document.getElementById('stat-btn').style.display = 'none';

        document.getElementById('p-bio').innerHTML = `
            <div style="border-right: 4px solid ${typeColor}; padding-right: 10px;">
                <p><strong>المسؤول:</strong> ${props.Leader}</p>
                <p><strong>الوصف:</strong> ${props.Description}</p>
                <p style="background:#f4f4f4; padding:8px; border-radius:5px;">
                    <strong>الأهمية:</strong> ${props.Outcome || props.Importance}
                </p>
            </div>`;
        
        const icon = props.Type === 'battle' ? '⚔️' : '🚩';
        document.getElementById('leader-img-container').innerHTML = `<div style="font-size: 50px; text-align: center; padding: 15px; background: #f4f4f4; border-radius: 10px;">${icon}</div>`;
    }

    // 4. تحميل الطبقات
    // طبقة الولايات (المساحات)
    if (typeof json_wilayas_1 !== 'undefined') {
        L.geoJson(json_wilayas_1, {
            style: { color: '#006633', weight: 2, fillOpacity: 0.2 },
            onEachFeature: function(f, l) {
                l.on('click', (e) => { populateWilaya(f.properties); map.fitBounds(l.getBounds()); L.DomEvent.stopPropagation(e); });
            }
        }).addTo(map);
    }

    // طبقة المعارك (النقاط)
    L.geoJson(battleDataLibrary, {
        pointToLayer: function (feature, latlng) {
            let color = feature.properties.Type === 'battle' ? '#cc0000' : '#006633';
            return L.marker(latlng, {
                icon: L.divIcon({
                    className: 'custom-marker',
                    html: `<div style="background-color: ${color}; width: 15px; height: 15px; border-radius: 50%; border: 2px solid white; box-shadow: 0 0 8px rgba(0,0,0,0.4);"></div>`,
                    iconSize: [15, 15]
                })
            });
        },
        onEachFeature: function (feature, layer) {
            layer.on('click', function (e) {
                showHistoricalDetails(feature.properties);
                map.setView(e.latlng, 10);
                L.DomEvent.stopPropagation(e);
            });
            layer.bindTooltip(feature.properties.Name);
        }
    }).addTo(map);

    // 5. وظائف إضافية
    function prepareChart(name, zones) {
        const ctx = document.getElementById('martyrsChart').getContext('2d');
        let data = Array.from({length: zones}, () => Math.floor(Math.random() * 2000) + 500);
        myChart = new Chart(ctx, {
            type: 'bar',
            data: { labels: data.map((_, i) => "منطقة " + (i+1)), datasets: [{ label: 'إحصاء تقديري للشهداء', data: data, backgroundColor: '#cc0000' }] }
        });
    }

    function toggleStats() {
        let c = document.getElementById('chart-container');
        c.style.display = c.style.display === 'none' ? 'block' : 'none';
    }

// 1. الإحداثيات التاريخية الموثقة
const easternLineCoords = [[36.9, 7.7], [36.2, 7.9], [35.4, 8.1], [34.4, 7.5]];
const westernLineCoords = [[35.0, -2.2], [34.8, -1.3], [33.5, -2.1], [31.6, -2.2]];

// 2. دالة إضافة الخطوط المكهربة للخريطة
function addElectricBarriers() {
    if (typeof map !== 'undefined') {
        var eastLine = L.polyline(easternLineCoords, {
            color: '#ffff00', 
            weight: 5, 
            className: 'electric-line line-glow'
        }).addTo(map);

        var westLine = L.polyline(westernLineCoords, {
            color: '#ffff00', 
            weight: 5, 
            className: 'electric-line line-glow'
        }).addTo(map);

        // ربط الأحداث
        eastLine.on('click', function(e) {
            showBarrierPopup('الشرقي');
            L.DomEvent.stopPropagation(e);
        });

        westLine.on('click', function(e) {
            showBarrierPopup('الغربي');
            L.DomEvent.stopPropagation(e);
        });
    }
}


function showBarrierPopup(type) {
    const modal = document.getElementById('barrier-popup');
    const audio = document.getElementById('explosion-sound');
    
    if (audio) {
        audio.currentTime = 0;
        audio.play().catch(e => console.log("الصوت محجوب من المتصفح"));
    }
    
    document.body.classList.add('shake');
    setTimeout(() => document.body.classList.remove('shake'), 500);

    if (type === 'الشرقي') {
        document.getElementById('popup-header').innerText = "خط موريس وشال (الشرقي)";
        document.getElementById('m-length').innerText = "460 كلم";
        document.getElementById('m-bombs').innerText = "6 ملايين لغم";
        document.getElementById('m-wilayas').innerText = "عنابة، الطارف، سوق أهراس، تبسة، الوادي.";
        document.getElementById('m-desc').innerText = "سد مكهرب بجهد 30 ألف فولت...";
    } else {
        document.getElementById('popup-header').innerText = "خط موريس وشال (الغربي)";
        document.getElementById('m-length').innerText = "700 كلم";
        document.getElementById('m-bombs').innerText = "5 ملايين لغم";
        document.getElementById('m-wilayas').innerText = "تلمسان، سيدي بلعباس، النعامة، بشار.";
        document.getElementById('m-desc').innerText = "نظام دفاعي يعتمد على الأسلاك الشائكة...";
    }
    modal.style.display = 'block';
}

// 4. دالة إغلاق النافذة
function closeBarrierPopup() {
    document.getElementById('barrier-popup').style.display = 'none';
}

// 5. دالة عداد الألغام (تأثير تصاعدي)
function startMinesCounter() {
    const target = 11000000; 
    const duration = 3000; 
    const stepTime = 30; 
    const increment = target / (duration / stepTime);
    
    let current = 0;
    const counterDisplay = document.getElementById('mines-number');

    if (counterDisplay) {
        const timer = setInterval(() => {
            current += increment;
            if (current >= target) {
                counterDisplay.innerText = "11,000,000";
                clearInterval(timer);
            } else {
                counterDisplay.innerText = Math.floor(current).toLocaleString();
            }
        }, stepTime);
    }
}

// 6. تشغيل الوظائف عند تحميل الصفحة
window.addEventListener('load', function() {
    addElectricBarriers();
    startMinesCounter();
});   


let algeriaBoundary; // متغير عالمي لتخزين الطبقة

function startRevolutionSymphony() {
    const btn = document.getElementById('revolution-trigger');
    btn.style.display = 'none';

    // 1. الوضع الداكن
    document.getElementById('map').classList.add('dark-map');

    // 2. الصوت
    const gunshot = document.getElementById('gunshot-sound');
    const ululation = document.getElementById('ululation-sound');
    if(gunshot) gunshot.play();

    // 3. الموجات المتوازية (شمال، وسط، جنوب)
    const waves = [
        // الموجة الأولى: الشمال (الأوراس، القبائل، قسنطينة، تلمسان)
        [[35.48, 6.62], [36.75, 5.08], [36.36, 6.61], [35.18, -1.31], [36.75, 3.05]],
        // الموجة الثانية: الهضاب والجلفة والنعامة
        [[34.67, 3.25], [33.59, 2.73], [33.27, 0.31], [34.33, 5.06]],
        // الموجة الثالثة: الواحات والجنوب الكبير
        [[31.94, 5.32], [30.03, 2.45], [28.03, 1.66], [22.79, 5.52]]
    ];

    waves.forEach((wavePoints, waveIndex) => {
        setTimeout(() => {
            wavePoints.forEach(pos => {
                const circle = L.circle(pos, {
                    radius: 100,
                    className: 'expansion-circle'
                }).addTo(map);

                // توسيع الدائرة ببطء شديد
                let currentR = 100;
                const expand = setInterval(() => {
                    currentR += 4000;
                    circle.setRadius(currentR);
                    if (currentR > 450000) clearInterval(expand);
                }, 100);
            });

            // في الموجة الأخيرة، انتظر قليلاً ثم أظهر الرسالة
            if (waveIndex === waves.length - 1) {
                setTimeout(() => {
                    if(ululation) ululation.play();
                    showFinalMessage();
                }, 6000);
            }
        }, waveIndex * 2500); // تأخير بين كل موجة وأخرى (ثانيتين ونصف)
    });
}

function showFinalMessage() {
    const msg = document.getElementById('independence-message');
    msg.style.display = 'flex';
}
function startMinesCounter() {
    const target = 11000000; 
    const duration = 3000; // مدة العد (3 ثواني)
    const stepTime = 30; 
    const increment = target / (duration / stepTime);
    
    let current = 0;
    const counterDisplay = document.getElementById('mines-number');

    if (counterDisplay) {
        const timer = setInterval(() => {
            current += increment;
            if (current >= target) {
                counterDisplay.innerText = "11,000,000";
                clearInterval(timer);
            } else {
                counterDisplay.innerText = Math.floor(current).toLocaleString();
            }
        }, stepTime);
    }
}



// --- دالة إضافة الحدود السياسية أو الإدارية المطلوبة ---
function addPoliticalBorder() {
    if (typeof map !== 'undefined') {
        // الإحداثيات التي تريد رسم الخط بناءً عليها
        var politicalBorderCoords = [
            [27.668, -13.16], 
            [27.66, -11.5],
            [27.65, -8.66]   
        ];

        var politicalLine = L.polyline(politicalBorderCoords, {
            color: '#ff3300',      // لون أحمر فاقع وواضح
            weight: 6,             // سُمك كبير للخط لضمان رؤيته بوضوح
            dashArray: '10, 10',   // خط مقطع احترافي
            opacity: 1             // شفافية كاملة
        }).addTo(map);

        politicalLine.bindPopup("<strong>الحد الجغرافي بين المملكة المغربية وجمهورية الصحراء الغربية </strong><br>الحد السياسي .");
    }
}


window.addEventListener('load', function() {
    addElectricBarriers();    // خطوط موريس وشال
    addPoliticalBorder();    // الحدود السياسية الجديدة (ستعمل فوراً بعد إضافة الدالة في الأعلى)
    startMinesCounter();      // عداد الألغام
});