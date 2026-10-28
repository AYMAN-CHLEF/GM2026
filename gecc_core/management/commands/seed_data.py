from django.core.management.base import BaseCommand
from gecc_core.models import HeritageAsset, TouristService

class Command(BaseCommand):
    help = 'تنظيف وتغذية قاعدة البيانات بمواقع تراثية وخدمات سياحية حقيقية مع توزيع المرشدين حول المعالم'

    def handle(self, *args, **kwargs):
        
        # 0. تنظيف البيانات القديمة أولاً لمنع التكرار
        deleted_h, _ = HeritageAsset.objects.all().delete()
        deleted_s, _ = TouristService.objects.all().delete()
        self.stdout.write(self.style.WARNING(f'تم حذف {deleted_h} معلماً قديماً و {deleted_s} خدمة قديمة بنجاح.'))

        # 1. المواقع التراثية والتاريخية الحقيقية (Heritage Assets) - 20 معلماً
        heritage_data = [
            {
                "name": "قصبة الجزائر - Algiers Casbah | Casbah d'Alger",
                "desc_ar": "حصن عثماني تاريخي وأزقة عريقة مسجلة في قائمة التراث العالمي لليونسكو.",
                "desc_fr": "Citadelle ottomane historique et ruelles classées au patrimoine mondial de l'UNESCO.",
                "desc_en": "Historic Ottoman citadel and winding alleys listed as a UNESCO World Heritage site.",
                "lat": 36.7845, "lon": 3.0560
            },
            {
                "name": "آثار تيمقاد الرومانية - Timgad Ruins | Timgad",
                "desc_ar": "مدينة رومانية أثرية متكاملة بباتنة، تُعرف بلؤلؤة الأوراس التاريخية.",
                "desc_fr": "Cité romaine antique et bien préservée dans les Aurès, perle historique.",
                "desc_en": "Well-preserved ancient Roman city in the Aurès, a historic gem.",
                "lat": 35.4847, "lon": 6.4655
            },
            {
                "name": "آثار جميلة الأثرية - Djemila Ruins | Djemila",
                "desc_ar": "موقع أثري روماني جبلي فريد بولاية سطيف (كويكول التاريخية).",
                "desc_fr": "Site archéologique romain de montagne unique à Sétif (Cuicul antique).",
                "desc_en": "Unique mountain Roman archaeological site in Setif (ancient Cuicul).",
                "lat": 36.3197, "lon": 5.7397
            },
            {
                "name": "قصر المشوار - El Mechouar Palace | Palais du Mechouar",
                "desc_ar": "قصر ملكي تاريخي يعود للدولة الزيانية العريقة بقلب مدينة تلمسان.",
                "desc_fr": "Palais royal historique de la dynastie ziyanide au cœur de Tlemcen.",
                "desc_en": "Historical royal palace of the Ziyanid dynasty in the heart of Tlemcen.",
                "lat": 34.8783, "lon": -1.3150
            },
            {
                "name": "قلعة سانتا كروز - Santa Cruz Fort | Fort de Santa Cruz",
                "desc_ar": "حصن وسور إسباني شامخ يشرف بجمالية على خليج وهران الساحر.",
                "desc_fr": "Fort et rempart espagnol surplombant magnifiquement la baie d'Oran.",
                "desc_en": "Spanish fortress and rampart overlooking the charming bay of Oran.",
                "lat": 35.7314, "lon": -0.6628
            },
            {
                "name": "القصور الطينية بتيميمون - Timimoun Ksour | Ksour de Timimoun",
                "desc_ar": "قصور واحاتية تقليدية فريدة مبنية بالطين في قلب الواحات الصحراوية.",
                "desc_fr": "Ksour oasiens traditionnels uniques construits en pisé au cœur du désert.",
                "desc_en": "Unique traditional mud-brick oasis ksars in the heart of the desert.",
                "lat": 29.2639, "lon": 0.2310
            },
            {
                "name": "حظيرة طاسيلي ناجر - Tassili n'Ajjer | Tassili n'Ajjer",
                "desc_ar": "متحف طبيعي مفتوح للنقوش والرسوم الصخرية التاريخية بجانت.",
                "desc_fr": "Musée à ciel ouvert de gravures et peintures rupestres préhistoriques à Djanet.",
                "desc_en": "Open-air museum of prehistoric rock engravings and paintings in Djanet.",
                "lat": 25.5500, "lon": 9.4833
            },
            {
                "name": "جسر سيدي مسيد المعلق - Sidi M'Cid Bridge | Pont Sidi M'Cid",
                "desc_ar": "أحد أشهر الجسر المعلقة في قسنطينة مدينة الجسر المعلقة فوق الأخدود.",
                "desc_fr": "L'un des ponts suspendus emblématiques de Constantine, la ville des ponts.",
                "desc_en": "One of the iconic suspension bridges in Constantine, the city of bridges.",
                "lat": 36.3650, "lon": 6.6147
            },
            {
                "name": "الموقع الأثري بالشلف (الأصنام) - Chlef Ancient Site",
                "desc_ar": "معالم أثرية رومانية وتاريخية تعكس العمق الحضاري والتاريخي لولاية الشلف.",
                "desc_fr": "Vestiges romains et historiques reflétant la profondeur culturelle de Chlef.",
                "desc_en": "Roman and historical ruins reflecting the cultural depth of Chlef.",
                "lat": 36.1654, "lon": 1.3345
            },
            {
                "name": "الضريح الملكي الموريتاني - Royal Mausoleum of Mauretania",
                "desc_ar": "هرم مدفن أمازيغي ملكي تاريخي شاهق بولاية تيبازة الساحلية.",
                "desc_fr": "Mausolée royal berbère historique situé sur la côte de Tipaza.",
                "desc_en": "Historic royal Berber mausoleum located on the coast of Tipasa.",
                "lat": 36.5583, "lon": 2.5694
            },
            {
                "name": "قلعة بني حماد - Beni Hammad Fort | Al Qal'a",
                "desc_ar": "أول عاصمة للدولة الحمادية الشامخة بولاية المسيلة.",
                "desc_fr": "Première capitale de la prestigieuse dynastie des Hammadides à M'Sila.",
                "desc_en": "First capital of the prestigious Hammadid dynasty in M'Sila.",
                "lat": 35.8183, "lon": 4.7891
            },
            {
                "name": "موقع هيبيوس ريجيوس - Hippo Regius | Annaba",
                "desc_ar": "آثار أثرية رومانية وأسقفية شهيرة بمدينة عنابة الساحلية.",
                "desc_fr": "Site archéologique romain et épiscopal majeur dans la ville côtière d'Annaba.",
                "desc_en": "Major Roman and episcopal archaeological site in the coastal city of Annaba.",
                "lat": 36.8833, "lon": 7.7500
            },
            {
                "name": "قصور وادي مزاب التاريخية - Ghardaïa Ksar | M'Zab Valley",
                "desc_ar": "عمارة واحاتية تقليدية فريدة بوادي مزاب المصنفة ضمن التراث العالمي.",
                "desc_fr": "Architecture oasienne traditionnelle unique de la vallée du M'Zab classée.",
                "desc_en": "Unique traditional oasis architecture of the M'Zab Valley, classed as heritage.",
                "lat": 32.4910, "lon": 3.6730
            },
            {
                "name": "الأسوار التاريخية لبجاية - Bejaïa Historical Walls | Bougie",
                "desc_ar": "الأسوار الحمادية التاريخية الشامخة وبوابة البحر العريقة ببجاية.",
                "desc_fr": "Remparts hammadides historiques imposants et porte de la Mer à Bejaïa.",
                "desc_en": "Imposing historical Hammadid walls and Sea Gate in Bejaia.",
                "lat": 36.7525, "lon": 5.0556
            },
            {
                "name": "حي سيدي الهواري التاريخي - Sidi El Houari | Oran",
                "desc_ar": "حي عريق يضم مساجد عثمانية وكنائس قديمة توثق تاريخ وهران.",
                "desc_fr": "Quartier historique abritant mosquées ottomanes et églises anciennes à Oran.",
                "desc_en": "Historic district featuring Ottoman mosques and old churches documenting Oran's history.",
                "lat": 35.7050, "lon": -0.6500
            },
            {
                "name": "موقع تيارت الأثري - Tiaret Historical Site (Tagdempt)",
                "desc_ar": "آثار ومواقع تاريخية للدولة الرستمية العريقة بتيارت.",
                "desc_fr": "Vestiges et sites historiques de la prestigieuse dynastie rostémide à Tiaret.",
                "desc_en": "Vestiges and historical sites of the prestigious Rustamid dynasty in Tiaret.",
                "lat": 35.3710, "lon": 1.3170
            },
            {
                "name": "الموقع الأثري بسكرة - Biskra Oasis Heritage",
                "desc_ar": "واحات نخيل تاريخية وقصور قديمة تعكس تراث الزيبان بعاصمة الصحراء.",
                "desc_fr": "Oasiens historiques et anciens ksars reflétant le patrimoine des Ziban.",
                "desc_en": "Historical palm oases and old ksars reflecting the Ziban heritage.",
                "lat": 34.8500, "lon": 5.7280
            },
            {
                "name": "قصر الثقافة مفدي زكريا - Palais de la Culture | Algiers",
                "desc_ar": "معلم ثقافي ومعماري حديث بارز بالعاصمة يخلد اسم الشاعر مفدي زكريا.",
                "desc_fr": "Monument culturel et architectural moderne marquant la capitale.",
                "desc_en": "Prominent modern cultural and architectural landmark in the capital.",
                "lat": 36.7510, "lon": 3.0850
            },
            {
                "name": "المتحف الوطني للقرآن - National Museum of Antiquities | Algiers",
                "desc_ar": "أقدم متحف في الجزيرة والمنطقة يضم كنوزاً تاريخية وأثرية نادرة.",
                "desc_fr": "Le plus ancien musée d'Algérie abritant des trésors historiques rares.",
                "desc_en": "The oldest museum in Algeria housing rare historical treasures.",
                "lat": 36.7620, "lon": 3.0540
            },
            {
                "name": "موقع الأقطاب الأثرية بغليزان - Relizane Historical Site",
                "desc_ar": "معالم ومواقع تاريخية تعكس التنوع والثقافة العريقة لولاية غليزان.",
                "desc_fr": "Monuments et sites historiques reflétant la culture de Relizane.",
                "desc_en": "Monuments and historical sites reflecting the heritage of Relizane.",
                "lat": 35.7420, "lon": 0.5550
            }
        ]

        for item in heritage_data:
            full_desc = f"{item['desc_ar']} | {item['desc_fr']} | {item['desc_en']}"
            HeritageAsset.objects.get_or_create(
                name=item['name'],
                defaults={
                    "description": full_desc,
                    "latitude": item['lat'],
                    "longitude": item['lon'],
                }
            )

        # 2. الخدمات السياحية والتشكيلات (Tourist Services)
        services_data = [
            # أ. فنادق حقيقية (Hotels) - 20 فندقاً
            ("فندق الأوراسي - Hotel El Aurassi (الجزائر العاصمة)", "hotel", 36.7681, 3.0614, "+213 21 74 82 52"),
            ("فندق شيراتون نادي الصنوبر - Sheraton Club des Pins (الجزائر)", "hotel", 36.7525, 2.9150, "+213 21 37 77 00"),
            ("فندق ماريوت باب الزوار - Algiers Marriott Bab Ezzouar", "hotel", 36.7167, 3.1833, "+213 21 98 80 00"),
            ("فندق رويال - Royal Hotel Oran - MGallery (وهران)", "hotel", 35.6987, -0.6322, "+213 41 33 33 00"),
            ("فندق فور بونيتس شيراتون - Four Points by Sheraton Oran", "hotel", 35.7056, -0.5894, "+213 41 59 10 00"),
            ("فندق ميريديان وهران - Le Méridien Oran Hotel", "hotel", 35.7119, -0.5956, "+213 41 98 40 00"),
            ("فندق سيراتون عنابة - Sheraton Annaba Hotel", "hotel", 36.9000, 7.7667, "+213 38 45 00 00"),
            ("فندق ماريوت قسنطينة - Constantine Marriott Hotel", "hotel", 36.3556, 6.6111, "+213 31 66 10 00"),
            ("فندق قوس النصر - Arc de Triomphe Hotel (سطيف)", "hotel", 36.1900, 5.4100, "+213 36 74 11 22"),
            ("فندق صبري - Sabri Hotel (عنابة)", "hotel", 36.8350, 7.7400, "+213 38 86 44 44"),
            ("فندق التلمساني - Tlemcen Hotel (تلمسان)", "hotel", 34.8783, -1.3150, "+213 43 26 50 00"),
            ("فندق المهري - El Mehri Hotel (ورقلة)", "hotel", 31.9500, 5.3333, "+213 29 73 11 11"),
            ("فندق تاغيت الواحات - Taghit Oasis Hotel (بشار)", "hotel", 30.9167, -2.0333, "+213 49 81 20 00"),
            ("فندق الهقار - Hoggar Hotel (تمنراست)", "hotel", 22.7850, 5.5228, "+213 29 34 35 36"),
            ("فندق مزاب - M'Zab Hotel (غرداية)", "hotel", 32.4900, 3.6700, "+213 29 88 12 34"),
            ("فندق الساورة - Saoura Hotel (بشار)", "hotel", 31.6300, -2.2200, "+213 49 80 15 15"),
            ("فندق رويال أرجان - Royal Argan (الشلف)", "hotel", 36.1650, 1.3340, "+213 27 77 10 20"),
            ("فندق الشلف الكبير - Grand Chlef Hotel", "hotel", 36.1700, 1.3350, "+213 27 77 40 50"),
            ("فندق سيدي يحيى - Sidi Yahia Hotel (الجزائر العاصمة)", "hotel", 36.7450, 3.0350, "+213 21 60 50 40"),
            ("فندق الأنفال - El Anfal Hotel (تلمسان)", "hotel", 34.8800, -1.3100, "+213 43 21 00 99"),

            # ب. مراقد (Dormitories) - 20 مرقداً
            *[ (f"مرقد الراحة السياحي رقم {i+1} - Al Raha Dormitory", "dormitory", 36.15 + (i*0.01), 1.30 + (i*0.01), f"+213 27 70 00 {10+i}") for i in range(20) ],

            # ج. نزل تراثية (Inns) - 10 نزل
            *[ (f"نزل الواحات التراثي رقم {i+1} - Oasis Heritage Inn", "inn", 32.40 + (i*0.05), 3.60 + (i*0.05), f"+213 29 80 00 {20+i}") for i in range(10) ],

            # د. وكالات سياحية حقيقية (Agencies) - 10 وكالات
            ("وكالة سياحة وأسفار الجزائر - Tours Algiers Agency", "agency", 36.7538, 3.0588, "+213 21 63 35 35"),
            ("وكالة أوراس للأسفار - Auras Travel (باتنة)", "agency", 35.5550, 6.1740, "+213 33 85 12 34"),
            ("وكالة هقار للسياحة - Hoggar Tour (تمنراست)", "agency", 22.7850, 5.5200, "+213 29 34 22 11"),
            ("وكالة مزاب للسفاري - M'Zab Safari (غرداية)", "agency", 32.4900, 3.6800, "+213 29 88 55 66"),
            ("وكالة طاسيلي جانت - Djanet Tassili Travel", "agency", 25.5500, 9.4800, "+213 29 47 11 22"),
            ("وكالة البهجة للسياحة - El Bahdja Travel (وهران)", "agency", 35.6970, -0.6300, "+213 41 33 44 55"),
            ("وكالة سيرتا للسفريات - Cirta Travel (قسنطينة)", "agency", 36.3650, 6.6140, "+213 31 92 33 44"),
            ("وكالة الأرز للأسفار - Cedars Travel (البليدة)", "agency", 36.4700, 2.8200, "+213 25 43 22 11"),
            ("وكالة الشلف للسياحة والأسفار - Chlef Travel Agency", "agency", 36.1650, 1.3340, "+213 27 77 88 99"),
            ("وكالة الساورة للسياحة - Saoura Tour (بشار)", "agency", 31.6300, -2.2200, "+213 49 80 33 44"),

            # و. صناع وبيع تحف تقليدية (Crafts) - 40 صانعاً وحرفة تقليدية
            *[ (f"ورشة الحرف التقليدية وصناعة التحف الفنية رقم {i+1} - Craft Workshop", "craft", 34.8 + (i*0.02), -1.3 + (i*0.02), f"+213 661 00 {50+i}") for i in range(40) ]
        ]

        # 3. توزيع 30 مرشداً سياحياً بشكل ذكي وملتصق بمواقع التراث (Guides distributed near heritage sites)
        for i in range(30):
            # اختيار معلم تراثي بالدور لتوزيع المرشدين حوله مباشرة
            base_site = heritage_data[i % len(heritage_data)]
            # إضافة إزاحة طفيفة جداً (Offset) لتبقى إحداثيات المرشد قريبة جداً من المعلم التراثي
            lat_offset = (i % 3 - 1) * 0.003
            lon_offset = ((i // 3) % 3 - 1) * 0.003
            
            guide_name = f"المرشد السياحي المعتمد: مرافق موقع {base_site['name'].split('-')[0].strip()} (رقم {i+1})"
            services_data.append((
                guide_name,
                "guide",
                base_site['lat'] + lat_offset,
                base_site['lon'] + lon_offset,
                f"+213 550 10 {20+i}"
            ))

        # إدراج جميع الخدمات في قاعدة البيانات
        for name, category, lat, lon, phone in services_data:
            TouristService.objects.get_or_create(
                name=name,
                defaults={
                    "category": category,
                    "latitude": lat,
                    "longitude": lon,
                    "description": f"خدمة سياحية ومرشد معتمد ضمن شبكة منصة Geo-Memory الرقمية. | Service touristique officiel.",
                    "phone": phone
                }
            )

        self.stdout.write(self.style.SUCCESS('تم تنظيف وتعبئة البيانات بنجاح، وتوزيع المرشدين السياحيين بدقة بالقرب من المعالم التراثية باللغات الثلاث!'))