(() => {
  const lang = (document.documentElement.lang || 'ar').slice(0, 2);
  const copy = {
    'الرئيسية':['Accueil','Home','Ana sayfa'], 'من نحن':['À propos','About us','Hakkımızda'],
    'المكتبة التاريخية':['Bibliothèque historique','History library','Tarih kütüphanesi'],
    'المتحف الرقمي':['Musée numérique','Digital museum','Dijital müze'],
    'الابتكار والأثر الاقتصادي':['Innovation et impact économique','Innovation and economic impact','Yenilik ve ekonomik etki'],
    'المستودع الرقمي':['Dépôt numérique','Digital repository','Dijital arşiv'],
    'العودة للرئيسية':['Retour à l’accueil','Back to home','Ana sayfaya dön'],
    'العودة إلى الرئيسية':['Retour à l’accueil','Back to home','Ana sayfaya dön'],
    'تسجيل الدخول':['Connexion','Sign in','Giriş yap'], 'تسجيل الدخول الموحد':['Connexion unifiée','Unified sign in','Birleşik giriş'],
    'إنشاء حساب':['Créer un compte','Create account','Hesap oluştur'], 'إنشاء حساب موحد':['Créer un compte unifié','Create a unified account','Birleşik hesap oluştur'],
    'اسم المستخدم أو البريد الإلكتروني':['Nom d’utilisateur ou adresse e-mail','Username or email','Kullanıcı adı veya e-posta'],
    'كلمة المرور':['Mot de passe','Password','Şifre'], 'تذكرني':['Se souvenir de moi','Remember me','Beni hatırla'],
    'مرحباً بك مجدداً، اختر وجهتك وسجل دخولك للمنصة':['Ravi de vous revoir. Choisissez votre espace et connectez-vous.','Welcome back. Choose your workspace and sign in.','Tekrar hoş geldiniz. Alanınızı seçip giriş yapın.'],
    'أنشئ حسابك الجديد واختر المسار المفضل لديك لبدء الرحلة':['Créez un compte et choisissez votre parcours.','Create an account and choose your learning path.','Hesap oluşturun ve öğrenme yolunuzu seçin.'],
    'تأكيد عملية الدفع':['Confirmer le paiement','Confirm payment','Ödemeyi onayla'], 'تأكيد الدفع':['Confirmation du paiement','Payment confirmation','Ödeme onayı'],
    'ارفع صورة وصل الدفع (CCP):':['Téléversez le reçu de paiement (CCP) :','Upload your payment receipt (CCP):','Ödeme makbuzunu yükleyin (CCP):'],
    'سيقوم فريقنا بالتحقق من الحوالة وتفعيل الأطلس خلال 24 ساعة.':['Notre équipe vérifiera le paiement et activera l’atlas sous 24 heures.','Our team will verify the payment and activate the atlas within 24 hours.','Ekibimiz ödemeyi doğrulayıp atlası 24 saat içinde etkinleştirir.'],
    'تم استلام طلبك بنجاح!':['Votre demande a bien été reçue !','Your request was received successfully!','Talebiniz başarıyla alındı!'],
    'أطلس الثورة التحريرية الكبرى':['Atlas de la guerre de libération','Atlas of the Liberation Revolution','Kurtuluş Devrimi Atlası'],
    'أطلس المقاومات الشعبية':['Atlas des résistances populaires','Atlas of popular resistance','Halk direnişleri atlası'],
    'فتح الخريطة':['Ouvrir la carte','Open map','Haritayı aç'], 'كل الحقبات':['Toutes les périodes','All periods','Tüm dönemler'],
    'الحقبة القديمة':['Antiquité','Ancient period','Antik dönem'], 'الحقبة الإسلامية':['Période islamique','Islamic period','İslam dönemi'],
    'الاستعمار والمقاومة':['Colonisation et résistance','Colonialism and resistance','Sömürgecilik ve direniş'],
    'الثورة التحريرية':['Révolution de libération','Liberation Revolution','Kurtuluş Devrimi'],
    'الخريطة الحية':['Carte vivante','Live map','Canlı harita'], 'المستودع الذكي':['Dépôt intelligent','Smart repository','Akıllı arşiv'],
    'عرض الوثيقة':['Afficher le document','View document','Belgeyi görüntüle'], 'محتوى الدرس:':['Contenu du cours :','Lesson content:','Ders içeriği:'],
    'الوحدة:':['Module :','Unit:','Ünite:'], 'مشاهدة فيديو الدرس':['Voir la vidéo du cours','Watch lesson video','Ders videosunu izle'],
    'لا توجد وحدات بعد.':['Aucun module pour le moment.','No modules have been added yet.','Henüz modül eklenmedi.'],
    'خدمات رقمية':'Services numériques', 'فضاءات العمل والتكوين':'Espaces de travail et de formation',
    'المستكشف:':['Explorateur :','Explorer:','Kaşif:'], 'النقاط:':['Points :','Score:','Puan:'],
    'الوقت:':['Temps :','Time:','Süre:'], 'الطاقة:':['Énergie :','Energy:','Enerji:'],
    'إعادة المغامرة':['Recommencer l’aventure','Restart adventure','Macerayı yeniden başlat'],
    'تفعيل رحلة المستكشف':['Activer le parcours de l’explorateur','Activate explorer journey','Kaşif yolculuğunu etkinleştir'],
    'أدخل الرمز المخطوط الموجود على بطاقتك لفك أسرار الخريطة.':['Saisissez le code inscrit sur votre carte pour découvrir les secrets de la carte.','Enter the code printed on your card to unlock the map’s secrets.','Haritanın sırlarını açmak için kartınızdaki kodu girin.'],
    'لوحة التحكم | المنصة التعليمية | Geo-Memory':['Tableau de bord | Plateforme éducative | Geo-Memory','Dashboard | Learning platform | Geo-Memory','Kontrol paneli | Eğitim platformu | Geo-Memory'],
    'محرك الذاكرة الوطنية التفاعلي':['Moteur interactif de mémoire nationale','Interactive national memory engine','Etkileşimli ulusal hafıza motoru'],
    'مستودع الأطالس':['Bibliothèque des atlas','Atlas collection','Atlas arşivi'],
    'التاريخ ليس ماضياً، التاريخ مكان.':['L’histoire n’est pas le passé : elle est un lieu.','History is not the past; history is a place.','Tarih geçmiş değildir; tarih bir mekândır.'],
    'استخدم خريطتنا التفاعلية لاسترجاع تفاصيل الثورة في موقعك الجغرافي الحالي.':['Utilisez notre carte interactive pour découvrir l’histoire de la révolution à votre emplacement.','Use our interactive map to explore the revolution’s history at your location.','Konumunuzdaki devrim tarihini keşfetmek için etkileşimli haritamızı kullanın.'],
    'بوابة الخريطة التفاعلية':['Portail de la carte interactive','Interactive map portal','Etkileşimli harita portalı'],
    'أرشيف معاهدة التافنة':['Archives du traité de la Tafna','Tafna Treaty archive','Tafna Antlaşması arşivi'],
    'نسخة رقمية فائقة الدقة. استخدم خاصية المطابقة الجغرافية.':['Copie numérique haute résolution. Utilisez la fonction de comparaison géographique.','High-resolution digital copy. Use the geospatial comparison feature.','Yüksek çözünürlüklü dijital kopya. Coğrafi eşleştirme özelliğini kullanın.'],
    'جولة داخل قاعة المتحف الرقمي الافتراضي':['Visite de la salle du musée numérique virtuel','Tour inside the virtual digital museum','Sanal dijital müze salonunu gezin'],
    'ابدأ جولة الـ VR للمتحف':['Commencer la visite VR du musée','Start the museum VR tour','Müze VR turunu başlat'],
    'الواقع الافتراضي 360 درجة':['Réalité virtuelle à 360°','360-degree virtual reality','360 derece sanal gerçeklik'],
    'جميع الحقوق محفوظة لمؤسسة Geo-Memory.':['Tous droits réservés à Geo-Memory.','All rights reserved by Geo-Memory.','Geo-Memory tarafından tüm hakları saklıdır.']
    ,'بواباتنا ومنتجاتنا':['Nos portails et produits','Our portals and products','Portallarımız ve ürünlerimiz']
    ,'فضاءات العمل والتكوين':['Espaces de travail et de formation','Work and training spaces','Çalışma ve eğitim alanları']
    ,'💻 بوابة التكوين والاشتراكات (GIS)':['💻 Portail de formation et abonnements (SIG)','💻 Training and subscriptions portal (GIS)','💻 Eğitim ve abonelik portalı (CBS)']
    ,'🎓 المنصة التعليمية للناشئة':['🎓 Plateforme éducative pour les jeunes','🎓 Learning platform for young learners','🎓 Gençler için eğitim platformu']
    ,'🎓 المنصة التعليمية (تسجيل دخول)':['🎓 Plateforme éducative (connexion)','🎓 Learning platform (sign in)','🎓 Eğitim platformu (giriş)']
    ,'المنتجات الخرائطية والتراثية':['Produits cartographiques et patrimoniaux','Mapping and heritage products','Harita ve miras ürünleri']
    ,'🗺️ مستودع الأطالس الرقمية':['🗺️ Bibliothèque des atlas numériques','🗺️ Digital atlas collection','🗺️ Dijital atlas arşivi']
    ,'🏛️  الخدمات الرقمية والتوأمة':['🏛️ Services numériques et jumeaux digitaux','🏛️ Digital services and digital twins','🏛️ Dijital hizmetler ve dijital ikizler']
    ,'📚 المكتبة التاريخية والمخطوطات':['📚 Bibliothèque historique et manuscrits','📚 History library and manuscripts','📚 Tarih kütüphanesi ve el yazmaları']
    ,'خدماتنا':['Nos services','Our services','Hizmetlerimiz']
    ,'لوحة التحكم المركزية':['Tableau de bord central','Central dashboard','Merkezi kontrol paneli']
    ,'مرحباً،':['Bienvenue,','Welcome,','Hoş geldiniz,']
    ,'تسجيل الدخول الموحد':['Connexion unifiée','Unified sign in','Birleşik giriş']
    ,'إنشاء حساب جديد':['Créer un nouveau compte','Create a new account','Yeni hesap oluştur']
    ,'التاريخ في خريطة رقمية':['L’histoire sur une carte numérique','History on a digital map','Dijital haritada tarih']
    ,'حيث تنبض':['Où la','Where','Tarihin']
    ,'الجغرافيا':['géographie fait vivre','geography brings','coğrafyanın canlandığı']
    ,'بأمجاد':['les gloires de','the glories of','ve şanlı']
    ,'التاريخ':['l’histoire','history','tarihin']
    ,'أول بيئة رقمية وهندسية متكاملة لرقمنة وتوثيق التراث والتاريخ باستخدام نظم المعلومات الجغرافية المتطورة والأطالس الذكية.':['Un environnement numérique et géospatial intégré pour numériser et documenter le patrimoine et l’histoire grâce aux SIG avancés et aux atlas intelligents.','An integrated digital and geospatial environment for digitizing and documenting heritage and history with advanced GIS and smart atlases.','Gelişmiş CBS ve akıllı atlaslarla miras ve tarihi dijitalleştiren, belgeleyen bütünleşik dijital ve coğrafi ortam.']
    ,'ولوج فضاء التكوين والاشتراكات':['Accéder à la formation et aux abonnements','Enter training and subscriptions','Eğitim ve aboneliklere git']
    ,'تصفح تقنية AR/VR':['Découvrir la réalité augmentée et virtuelle','Explore AR/VR','AR/VR teknolojisini keşfet']
    ,'رؤيتنا في مؤسسة Geo-Memory':['Notre vision chez Geo-Memory','Our vision at Geo-Memory','Geo-Memory vizyonumuz']
    ,'نحن شركة ناشئة جزائرية طموحة وهندسية، نسعى لحماية الذاكرة من خلال إسقاط المحتوى التاريخي جغرافياً ورقمياً. نربط المعالم، المعارك، والمسارات بمواقعها الحقيقية عبر برمجيات الـ GIS الاحترافية، ونوفر بيئة تدريبية للأكاديميين لبناء قواعد بيانات جغرافية تاريخية آمنة وموثقة.':['Nous sommes une jeune entreprise algérienne qui protège la mémoire en reliant numériquement les récits historiques aux lieux. Nos outils SIG relient monuments, batailles et itinéraires à leurs emplacements et forment les spécialistes à créer des bases géohistoriques fiables.','We are an ambitious Algerian geospatial startup preserving memory by connecting historical content to real places. Our professional GIS tools map monuments, battles, and routes, while training specialists to build trusted historical geographic databases.','Tarihi içeriği gerçek konumlarla ilişkilendirerek hafızayı koruyan yenilikçi bir Cezayir coğrafi teknoloji girişimiyiz. CBS araçlarımız anıtları, savaşları ve rotaları haritalar; uzmanları güvenilir tarihî coğrafi veritabanları oluşturmaları için eğitir.']
    ,'مرحباً بك مجدداً، اختر وجهتك وسجل دخولك للمنصة':['Ravi de vous revoir. Choisissez votre espace et connectez-vous.','Welcome back. Choose your workspace and sign in.','Tekrar hoş geldiniz. Alanınızı seçip giriş yapın.']
    ,'بيانات الدخول غير صحيحة، يرجى المحاولة مجدداً.':['Identifiants incorrects. Veuillez réessayer.','Incorrect sign-in details. Please try again.','Giriş bilgileri hatalı. Lütfen tekrar deneyin.']
    ,'اختر مساحة العمل المطلوبة:':['Choisissez votre espace de travail :','Choose your workspace:','Çalışma alanınızı seçin:']
    ,'📖 مساحة التعليم':['📖 Espace éducatif','📖 Learning space','📖 Eğitim alanı']
    ,'🛠️ تدريب GIS':['🛠️ Formation SIG','🛠️ GIS training','🛠️ CBS eğitimi']
    ,'دخول إلى الحساب':['Se connecter','Sign in','Giriş yap']
    ,'ليس لديك حساب بعد؟':['Vous n’avez pas encore de compte ?','Don’t have an account yet?','Henüz hesabınız yok mu?']
    ,'أنشئ حساباً جديداً الآن':['Créez un compte maintenant','Create a new account now','Şimdi yeni hesap oluşturun']
    ,'يرجى تصحيح الأخطاء التالية:':['Veuillez corriger les erreurs suivantes :','Please correct the following errors:','Lütfen aşağıdaki hataları düzeltin:']
    ,'اختر نوع الحساب والمسار العملي:':['Choisissez votre type de compte et votre parcours :','Choose your account type and learning path:','Hesap türünüzü ve öğrenme yolunuzu seçin:']
    ,'📖 مسار التعليم':['📖 Parcours éducatif','📖 Learning path','📖 Eğitim yolu']
    ,'الدروس والمحتوى التاريخي الجغرافي':['Cours et contenu géohistorique','Lessons and geo-historical content','Dersler ve tarihî coğrafi içerik']
    ,'🛠️ تدريب GIS المتقدم':['🛠️ Formation SIG avancée','🛠️ Advanced GIS training','🛠️ İleri CBS eğitimi']
    ,'ورشات وخرائط هندسية تفاعلية':['Ateliers et cartes géospatiales interactives','Workshops and interactive geospatial maps','Atölyeler ve etkileşimli coğrafi haritalar']
    ,'إنشاء الحساب وبدء الرحلة 🎓':['Créer le compte et commencer 🎓','Create account and begin 🎓','Hesap oluştur ve başla 🎓']
    ,'لديك حساب بالفعل؟ سجل دخولك من هنا':['Vous avez déjà un compte ? Connectez-vous ici','Already have an account? Sign in here','Zaten hesabınız var mı? Buradan giriş yapın']
    ,'📚 طالب في المنصة التعليمية':['📚 Élève de la plateforme éducative','📚 Learning platform student','📚 Eğitim platformu öğrencisi']
    ,'غير مفعل':['Non activé','Inactive','Etkin değil']
    ,'معلومات الحساب الشخصي':['Informations du compte','Account information','Hesap bilgileri']
    ,'💳 تفعيل بطاقة الاشتراك':['💳 Activer la carte d’abonnement','💳 Activate subscription card','💳 Abonelik kartını etkinleştir']
    ,'أدخل الكود السري':['Saisissez le code secret','Enter the secret code','Gizli kodu girin']
    ,'تفعيل':['Activer','Activate','Etkinleştir']
    ,'🌐 منصة التعليم':['🌐 Plateforme éducative','🌐 Learning platform','🌐 Eğitim platformu']
    ,'⚙️ إعدادات الحساب':['⚙️ Paramètres du compte','⚙️ Account settings','⚙️ Hesap ayarları']
    ,'🏆 أوسمتي':['🏆 Mes distinctions','🏆 My awards','🏆 Ödüllerim']
    ,'🚪 تسجيل الخروج':['🚪 Déconnexion','🚪 Sign out','🚪 Çıkış yap']
    ,'حفظ التعديلات':['Enregistrer les modifications','Save changes','Değişiklikleri kaydet']
    ,'تعليم متوسط':['Enseignement moyen','Middle school','Ortaokul']
    ,'التعليم الابتدائي':['Enseignement primaire','Primary education','İlköğretim']
    ,'التعليم المتوسط':['Enseignement moyen','Middle school','Ortaokul']
    ,'التعليم الثانوي':['Enseignement secondaire','Secondary education','Lise']
    ,'إرسال الطلب للمراجعة':['Envoyer la demande pour examen','Submit request for review','İnceleme için gönder']
    ,'العودة للوحة التحكم':['Retour au tableau de bord','Back to dashboard','Kontrol paneline dön']
    ,'🤖 المرشد الذكي AI':['🤖 Guide intelligent IA','🤖 AI smart guide','🤖 Yapay zekâ akıllı rehberi']
    ,'تنشيط السياحة والتوأمة الرقمية 2026':['Tourisme et jumelage numérique 2026','Tourism and digital twinning 2026','Turizm ve dijital ikiz 2026']
    ,'Geo-Memory  من ذاكرة المكان إلى السياحة الذكية':['Geo-Memory : de la mémoire des lieux au tourisme intelligent','Geo-Memory: from place memory to smart tourism','Geo-Memory: mekân hafızasından akıllı turizme']
    ,'اكتشف الوجهة بذكاء':['Découvrez la destination intelligemment','Explore the destination intelligently','Destinasyonu akıllıca keşfedin']
    ,'استعرض البيئة الداخلية للمتحف المستوحاة من البرومت التفاعلي. انقر على الزر أدناه لبدء جولة افتراضية حقيقية بالـ VR تمكنك من الاستدارة واستكشاف أروقة المتحف وعناصر الهولوجرام بـ 360 درجة.':['Explorez l’intérieur du musée et lancez une visite virtuelle à 360° pour découvrir ses salles et hologrammes.','Explore the museum interior with an immersive 360° VR tour of its galleries and holograms.','Müzenin iç mekânını keşfedin; salonları ve hologramları 360° sanal gerçeklik turuyla gezin.']
    ,'ولاية وهران':['Wilaya d’Oran','Oran Province','Oran ili']
    ,'المعالم التذكارية والتاريخية':['Monuments commémoratifs et historiques','Memorial and historic landmarks','Anıtlar ve tarihî yapılar']
    ,'استعراض هندسي وتاريخي شامل للمعلم، يشمل تفاصيل التوأمة مع المواقع الأثرية الأخرى.':['Présentation historique et géospatiale du site, avec ses liens vers d’autres lieux archéologiques.','A historical and geospatial overview of the landmark, including links to other archaeological sites.','Yapının tarihî ve coğrafi incelemesi ile diğer arkeolojik alanlarla bağlantıları.']
    ,'🌐 مجهز بـ VR/AR':['🌐 Compatible VR/AR','🌐 VR/AR enabled','🌐 VR/AR destekli']
    ,'جولة VR':['Visite VR','VR tour','VR turu']
    ,'معاينة':['Aperçu','Preview','Önizleme']
    ,'توأمة ذكية':['Jumeau intelligent','Smart twin','Akıllı ikiz']
    ,'منصة التوأمة الرقمية التفاعلية':['Plateforme interactive de jumeaux numériques','Interactive digital twin platform','Etkileşimli dijital ikiz platformu']
    ,'مركز التوأمة الرقمية التفاعلية':['Centre de jumeaux numériques interactifs','Interactive digital twinning center','Etkileşimli dijital ikiz merkezi']
    ,'مركز التوأمة الرقمية التفاعلية\nبيئة رقمية موحّدة تربط التوائم الرقمية للمواقع والمعالم التراثية، لتقديم تمثيل تفاعلي للوجهة السياحية وإتاحة استكشافها وإدارتها بذكاء':['Centre numérique unifié reliant les jumeaux des sites patrimoniaux pour explorer et gérer les destinations.','A unified digital center connecting heritage-site twins for exploring and managing destinations.','Miras alanlarının dijital ikizlerini destinasyon keşfi ve yönetimi için birleştiren merkez.']
    ,'إدارة مركزية':['Gestion centralisée','Central management','Merkezi yönetim']
    ,'فتح لوحة التوأمة':['Ouvrir le tableau de jumelage','Open digital twin dashboard','Dijital ikiz panelini aç']
    ,'تسيير رموز الـ QR للبطاقات التقنية':['Gestion des QR des fiches techniques','Manage QR codes for technical cards','Teknik kartların QR kodlarını yönet']
    ,'لوحة تسيير وتوليد رموز المعالم':['Gestion et génération des QR des monuments','Landmark QR management and generation','Yapı QR kodu yönetimi ve üretimi']
    ,'ربط وتكامل وطني':['Connexion et intégration nationale','National connection and integration','Ulusal bağlantı ve entegrasyon']
    ,'مشروع التوأمة الرقمية بين المعالم السياحية':['Projet de jumeaux numériques des sites touristiques','Digital twin project for tourist landmarks','Turistik yapılar için dijital ikiz projesi']
    ,'🌐 تكنولوجيا الذاكرة':['🌐 Technologie de la mémoire','🌐 Memory technology','🌐 Hafıza teknolojisi']
    ,'ابدأ الاستكشاف الميداني ➔':['Commencer l’exploration sur le terrain ➔','Start field exploration ➔','Saha keşfine başla ➔']
    ,'المسارات الرقمية التفاعلية للأعلام التاريخية.':['Parcours numériques interactifs consacrés aux figures historiques.','Interactive digital journeys featuring historic figures.','Tarihî şahsiyetlere yönelik etkileşimli dijital rotalar.']
    ,'ساهم بذاكرتك الوطنية':['Contribuez à la mémoire nationale','Contribute to national memory','Ulusal hafızaya katkı sağlayın']
    ,'هل تملك وثائق تاريخية أو صوراً نادرة؟ انضم لمجتمع الموثقين وشارك في بناء الخريطة.':['Possédez-vous des documents historiques ou des photos rares ? Rejoignez la communauté et contribuez à la carte.','Have historical documents or rare photos? Join our community and help build the map.','Tarihî belgeleriniz veya nadir fotoğraflarınız mı var? Topluluğa katılıp haritaya katkıda bulunun.']
    ,'سجل كباحث الآن':['S’inscrire comme chercheur','Register as a researcher','Araştırmacı olarak kaydol']
    ,'أدخل الرمز التسلسلي...':['Saisissez le code de série...','Enter the serial code...','Seri kodunu girin...']
    ,'ابدأ الاستكشاف':['Commencer l’exploration','Start exploring','Keşfetmeye başla']
    ,'جارٍ التحميل...':['Chargement...','Loading...','Yükleniyor...']
    ,'مخطوطة اللغز التاريخي':['Manuscrit de l’énigme historique','Historical puzzle manuscript','Tarihî bilmece el yazması']
    ,'تسجيل باحث':['Inscription chercheur','Researcher registration','Araştırmacı kaydı']
    ,'تاريخ الجزائر':['Histoire de l’Algérie','Algerian history','Cezayir tarihi']
    ,'جغرافيا الجزائر':['Géographie de l’Algérie','Algerian geography','Cezayir coğrafyası']
    ,'اختر الطور الدراسي لعرض المراحل والسنوات المتاحة':['Choisissez le niveau scolaire pour afficher les étapes et années disponibles','Choose a school level to view available grades and years','Mevcut sınıf ve yılları görmek için eğitim düzeyini seçin']
    ,'المستكشف:':['Explorateur :','Explorer:','Kaşif:']
    ,'النقاط:':['Points :','Score:','Puan:']
    ,'⏱️ الوقت:':['⏱️ Temps :','⏱️ Time:','⏱️ Süre:']
    ,'⚡ الطاقة:':['⚡ Énergie :','⚡ Energy:','⚡ Enerji:']
    ,'إتمام الدرس والانتقال للتالي ➔':['Terminer le cours et continuer ➔','Complete lesson and continue ➔','Dersi tamamla ve devam et ➔']
    ,'الأنشطة التفاعلية':['Activités interactives','Interactive activities','Etkileşimli etkinlikler']
    ,'ابدأ الاختبار القصير 📝':['Commencer le quiz 📝','Start the short quiz 📝','Kısa sınavı başlat 📝']
    ,'استكشف خريطة التفاعلية':['Explorer la carte interactive','Explore the interactive map','Etkileşimli haritayı keşfet']
    ,'أدخل الرمز التسلسلي...':['Saisissez le code de série...','Enter the serial code...','Seri kodunu girin...']
    ,'ابدأ الاستكشاف':['Commencer l’exploration','Start exploring','Keşfetmeye başla']
    ,'إدخال الرمز المخطوط الموجود على بطاقتك لفك أسرار الخريطة.':['Saisissez le code inscrit sur votre carte pour découvrir ses secrets.','Enter the code printed on your card to unlock its secrets.','Sırlarını açmak için kartınızdaki kodu girin.']
    ,'الحقبة القديمة':['Antiquité','Ancient period','Antik dönem']
    ,'أطلس الحركة الوطنية':['Atlas du mouvement national','National Movement Atlas','Ulusal Hareket Atlası']
    ,'أطلس المعارك الكبرى':['Atlas des grandes batailles','Atlas of major battles','Büyük Savaşlar Atlası']
    ,'أطلس الخطوط المكهربة':['Atlas des lignes électrifiées','Atlas of electrified lines','Elektrikli Hatlar Atlası']
    ,'أطلس القيادة والتنظيم':['Atlas du commandement et de l’organisation','Atlas of leadership and organization','Liderlik ve örgütlenme atlası']
    ,'أطلس الدول والكيانات القديمة':['Atlas des États et entités anciennes','Atlas of ancient states and entities','Antik devletler ve varlıklar atlası']
    ,'أطلس الممالك الإسلامية':['Atlas des royaumes islamiques','Atlas of Islamic kingdoms','İslam krallıkları atlası']
    ,'أطلس إيالة الجزائر':['Atlas de la Régence d’Alger','Atlas of the Regency of Algiers','Cezayir Eyaleti Atlası']
    ,'سيظهر المجسم ثلاثي الأبعاد هنا':['Le modèle 3D apparaîtra ici','The 3D model will appear here','3B model burada görünecek']
    ,'أضف ملف المجسم من لوحة إدارة الأصول لتفعيل المعاينة والواقع المعزز.':['Ajoutez un modèle dans la gestion des ressources pour activer l’aperçu et la réalité augmentée.','Add a model file in asset management to enable previews and augmented reality.','Önizleme ve artırılmış gerçekliği etkinleştirmek için varlık yönetimine bir model dosyası ekleyin.']
    ,'الخدمة في طور الإنجاز':['Service en cours de développement','Service in development','Hizmet geliştirme aşamasında']
    ,'نعمل حالياً على تطوير وتفعيل بوابة الدفع والاشتراك الآلي لتقديم أفضل تجربة تكوينية. ترقبوا الإطلاق الرسمي قريباً!':['Nous développons le paiement et l’abonnement automatiques pour améliorer la formation. Le lancement officiel approche !','We are developing automated payments and subscriptions to improve the learning experience. Official launch coming soon!','Eğitim deneyimini geliştirmek için otomatik ödeme ve abonelik üzerinde çalışıyoruz. Resmî açılış yakında!']
    ,'إعدادات الملف التقني والحساب':['Paramètres du profil technique et du compte','Technical profile and account settings','Teknik profil ve hesap ayarları']
    ,'تحديث الصورة الشخصية للحساب':['Mettre à jour la photo de profil','Update account profile photo','Hesap profil fotoğrafını güncelle']
    ,'الاسم':['Prénom','First name','Ad']
    ,'اللقب':['Nom','Last name','Soyad']
    ,'البريد الإلكتروني التقني':['Adresse e-mail professionnelle','Technical email','Teknik e-posta']
    ,'لا توجد محاور مضافة لهذه الدورة بعد.':['Aucun module n’a encore été ajouté à ce cours.','No modules have been added to this course yet.','Bu kursa henüz modül eklenmedi.']
    ,'تحديث بياناتك الشخصية، معلومات الاتصال، وصورة الملف الشخصي':['Mettez à jour vos informations personnelles, coordonnées et photo de profil','Update your personal details, contact information, and profile photo','Kişisel bilgilerinizi, iletişim bilgilerinizi ve profil fotoğrafınızı güncelleyin']
    ,'← عودة للمنصة':['← Retour à la plateforme','← Back to platform','← Platforma dön']
    ,'الاسم الأول (بالعربية)':['Prénom (en arabe)','First name (Arabic)','Ad (Arapça)']
    ,'اسم العائلة (بالعربية)':['Nom de famille (en arabe)','Last name (Arabic)','Soyadı (Arapça)']
    ,'رقم الهاتف':['Numéro de téléphone','Phone number','Telefon numarası']
    ,'صورة الملف الشخصي':['Photo de profil','Profile photo','Profil fotoğrafı']
    ,'تاريخ الجزائر':['Histoire de l’Algérie','Algerian history','Cezayir tarihi']
    ,'تأكيد عملية الدفع':['Confirmer le paiement','Confirm payment','Ödemeyi onayla']
    ,'بريد الجزائر (CCP)':['Algérie Poste (CCP)','Algeria Post (CCP)','Cezayir Postası (CCP)']
    ,'الأطلس المختار':['Atlas sélectionné','Selected atlas','Seçilen atlas']
    ,'اطلب صورة وصل الدفع (CCP):':['Téléversez le reçu de paiement (CCP) :','Upload your payment receipt (CCP):','Ödeme makbuzunu yükleyin (CCP):']
    ,'تم استلام طلبك بنجاح!':['Votre demande a bien été reçue !','Your request was received successfully!','Talebiniz başarıyla alındı!']
    ,'مستودع الأطالس الخرائطية المفتوحة - Geo-Memory © 2026':['Collection d’atlas cartographiques ouverts - Geo-Memory © 2026','Open cartographic atlas collection - Geo-Memory © 2026','Açık kartografik atlas koleksiyonu - Geo-Memory © 2026']
    ,'🏛️ الرواق الرقمي والمتحف الافتراضي':['🏛️ Galerie numérique et musée virtuel','🏛️ Digital gallery and virtual museum','🏛️ Dijital galeri ve sanal müze']
    ,'🏛️ الرواق الرقمي ومنصة التوأمة السياحية':['🏛️ Galerie numérique et plateforme de jumelage touristique','🏛️ Digital gallery and tourism twin platform','🏛️ Dijital galeri ve turizm ikiz platformu']
    ,'💳 دفع 500 دج':['💳 Payer 500 DZD','💳 Pay 500 DZD','💳 500 DZD öde']
    ,'💳 دفع 600 دج':['💳 Payer 600 DZD','💳 Pay 600 DZD','💳 600 DZD öde']
    ,'💳 دفع 700 دج':['💳 Payer 700 DZD','💳 Pay 700 DZD','💳 700 DZD öde']
    ,'💳 دفع 800 دج':['💳 Payer 800 DZD','💳 Pay 800 DZD','💳 800 DZD öde']
    ,'💳 دفع 900 دج':['💳 Payer 900 DZD','💳 Pay 900 DZD','💳 900 DZD öde']
    ,'💳 دفع 1000 دج':['💳 Payer 1 000 DZD','💳 Pay 1,000 DZD','💳 1.000 DZD öde']
    ,'بواباتنا ومنتجاتنا':['Nos portails et produits','Our portals and products','Portallarımız ve ürünlerimiz']
    ,'المستودع التاريخي العام':['Dépôt historique public','Public history repository','Kamu tarih arşivi']
    ,'أحدث المحطات والخرائط المبتكرة':['Derniers contenus et cartes innovantes','Latest stories and innovative maps','En yeni içerikler ve yenilikçi haritalar']
    ,'هل أنت مستعد لاختبار ذكائك التاريخي؟':['Prêt à tester vos connaissances historiques ?','Ready to test your historical knowledge?','Tarih bilginizi sınamaya hazır mısınız?']
    ,'المنطقة الجغرافية قيد الاستكشاف! بينما نعمل على إضافة معالم جديدة، يمكنك تجربة التحديات المتاحة.':['Cette zone est en cours d’exploration ! En attendant de nouveaux sites, essayez les défis disponibles.','This area is being explored! Try the available challenges while we add new landmarks.','Bu bölge keşfediliyor! Yeni yerler eklenirken mevcut görevleri deneyin.']
    ,'ابدأ تحدي "المسار المحرر"':['Lancer le défi « parcours de libération »','Start the “liberation route” challenge','“Kurtuluş rotası” görevini başlat']
    ,'منصاتنا وأنظمتنا الفرعية':['Nos plateformes et systèmes','Our platforms and systems','Platformlarımız ve sistemlerimiz']
    ,'اختر البوابة الرقمية المناسبة لبدء العمل والبحث الميداني':['Choisissez le portail adapté à vos recherches et activités de terrain','Choose the right portal for your work and field research','Çalışma ve saha araştırmanız için uygun portalı seçin']
    ,'الأطالس الرقمية التفاعلية':['Atlas numériques interactifs','Interactive digital atlases','Etkileşimli dijital atlaslar']
    ,'خرائط جغرافية تفاعلية دقيقة مبنية بإحداثيات GIS لتتبع مسارات المقاومات الشعبية الكبرى ومعارك الثورة التحريرية المظفرة.':['Des cartes géographiques interactives fondées sur des coordonnées SIG pour suivre les résistances populaires et les batailles de la révolution.','Precise GIS-based interactive maps tracing major popular resistance routes and battles of the liberation revolution.','Büyük halk direnişlerinin ve kurtuluş devrimi savaşlarının rotalarını izleyen, CBS koordinatlarına dayalı etkileşimli haritalar.']
    ,'ولوج مستودع الخرائط':['Accéder aux cartes','Browse the map collection','Harita arşivine git']
    ,'منصة التكوين الهندسي (GIS)':['Plateforme de formation géospatiale (SIG)','Geospatial training platform (GIS)','Coğrafi eğitim platformu (CBS)']
    ,'بيئة تدريبية واحترافية مستقلة مخصصة للأكاديميين والباحثين لإنشاء وتسيير قواعد البيانات الجغرافية بنظام اشتراك سنوي.':['Un environnement professionnel pour aider les chercheurs à créer et gérer des bases de données géographiques avec un abonnement annuel.','A professional environment where researchers can build and manage geographic databases through an annual subscription.','Araştırmacıların yıllık abonelikle coğrafi veritabanları oluşturup yönetebileceği profesyonel ortam.']
    ,'بوابة التكوين والاشتراكات':['Portail de formation et abonnements','Training and subscriptions portal','Eğitim ve abonelik portalı']
    ,'الخدمات الرقمية والتوأمة':['Services numériques et jumeaux numériques','Digital services and digital twins','Dijital hizmetler ve dijital ikizler']
    ,'معرض رقمي مفتوح لعرض مجسمات المواقع والمعالم التاريخية الوطنية الموثقة، ويدعم السياحة الثقافية عبر الـ QR Code.':['Un espace numérique pour présenter des modèles de sites et monuments documentés, et soutenir le tourisme culturel avec des QR codes.','An open digital gallery of documented national heritage sites and landmarks, supporting cultural tourism with QR codes.','Belgelenmiş ulusal miras alanlarını sergileyen ve QR kodlarıyla kültür turizmini destekleyen dijital galeri.']
    ,'استكشف .... بتقنية AR/VR':['Explorer en réalité augmentée et virtuelle','Explore with AR/VR','AR/VR ile keşfet']
    ,'خطط الاشتراك الرقمية':['Offres d’abonnement numérique','Digital subscription plans','Dijital abonelik planları']
    ,'اختر الخطة التي تناسب احتياجاتك البحثية أو المؤسساتية':['Choisissez l’offre adaptée à vos besoins de recherche ou à votre institution','Choose a plan for your research or organization','Araştırma veya kurum ihtiyaçlarınıza uygun planı seçin']
    ,'طالب':['Étudiant','Student','Öğrenci']
    ,'مجاني/مدعوم':['Gratuit / subventionné','Free / supported','Ücretsiz / destekli']
    ,'✓ الوصول للمتحف الرقمي':['✓ Accès au musée numérique','✓ Digital museum access','✓ Dijital müzeye erişim']
    ,'✓ تصفح الأطالس العامة':['✓ Consultation des atlas publics','✓ Browse public atlases','✓ Genel atlaslara göz atın']
    ,'✓ موارد تعليمية محدودة':['✓ Ressources éducatives limitées','✓ Limited learning resources','✓ Sınırlı eğitim kaynakları']
    ,'التفاصيل والتسجيل':['Détails et inscription','Details and registration','Ayrıntılar ve kayıt']
    ,'أستاذ / باحث':['Enseignant / chercheur','Teacher / researcher','Öğretmen / araştırmacı']
    ,'خاص':['Sur mesure','Custom','Özel']
    ,'✓ أدوات GIS المتقدمة':['✓ Outils SIG avancés','✓ Advanced GIS tools','✓ Gelişmiş CBS araçları']
    ,'✓ بناء قواعد بيانات جغرافية':['✓ Création de bases de données géographiques','✓ Build geographic databases','✓ Coğrafi veritabanları oluşturun']
    ,'✓ دعم تقني مخصص':['✓ Assistance technique dédiée','✓ Dedicated technical support','✓ Özel teknik destek']
    ,'طلب اشتراك تكويني':['Demander un abonnement de formation','Request a training subscription','Eğitim aboneliği iste']
    ,'مؤسسة':['Institution','Organization','Kurum']
    ,'مخصص':['Personnalisé','Custom','Özel']
    ,'✓ حسابات متعددة للمستخدمين':['✓ Comptes multi-utilisateurs','✓ Multiple user accounts','✓ Çoklu kullanıcı hesabı']
    ,'✓ تقارير GIS تحليلية':['✓ Rapports SIG analytiques','✓ GIS analytics reports','✓ CBS analiz raporları']
    ,'✓ لوحة تحكم إدارية كاملة':['✓ Tableau de bord administratif complet','✓ Full administrative dashboard','✓ Tam yönetim paneli']
    ,'تواصل معنا':['Nous contacter','Contact us','Bize ulaşın']
    ,'Geo-Memory ، منصة رقمية متكاملة للتراث والسياحة، تبني ذاكرة جغرافية للوجهة وتطوّر توأمها الرقمي من خلال دمج المعطيات المكانية والزمانية والسياقية وتوظيف الذكاء الاصطناعي، لتقديم تجارب سياحية ذكية، ورقمنة التراث وتثمينه، ودعم إدارة الوجهة وصناعة القرار.':['Geo-Memory est une plateforme numérique du patrimoine et du tourisme. Elle construit la mémoire géographique des destinations et leur jumeau numérique grâce aux données spatio-temporelles et à l’intelligence artificielle.','Geo-Memory is a digital heritage and tourism platform that builds geographic destination memory and digital twins using spatial and temporal data and AI.','Geo-Memory, miras ve turizm için dijital bir platformdur. Mekânsal ve zamansal veriler ile yapay zekâ kullanarak destinasyonların coğrafi belleğini ve dijital ikizini oluşturur.']
    ,'🥽 ابدأ جولة الـ VR للمتحف':['🥽 Commencer la visite VR du musée','🥽 Start the museum VR tour','🥽 Müze VR turunu başlat']
    ,'انقر لدخول جولة الـ VR':['Cliquez pour entrer dans la visite VR','Click to enter the VR tour','VR turuna girmek için tıklayın']
    ,'معلم مصنف':['Site classé','Classified heritage site','Tescilli miras alanı']
    ,'مركز التوأمة الرقمية التفاعلية بيئة رقمية موحّدة تربط التوائم الرقمية للمواقع والمعالم التراثية، لتقديم تمثيل تفاعلي للوجهة السياحية وإتاحة استكشافها وإدارتها بذكاء':['Le centre de jumelage numérique relie les jumeaux des sites patrimoniaux dans un espace interactif pour explorer et gérer les destinations.','The digital twinning center connects heritage-site twins in one interactive space for exploring and managing destinations.','Dijital ikiz merkezi, miras alanlarının ikizlerini etkileşimli bir ortamda birleştirerek destinasyonların keşfedilmesini ve yönetilmesini sağlar.']
    ,'مركز التوأمة الرقمية التفاعلية':['Centre de jumelage numérique','Digital Twinning Center','Dijital İkiz Merkezi']
    ,'بيئة رقمية موحّدة تربط التوائم الرقمية للمواقع والمعالم التراثية، لتقديم تمثيل تفاعلي للوجهة السياحية وإتاحة استكشافها وإدارتها بذكاء':['Un espace numérique unifié pour explorer et gérer les jumeaux des sites patrimoniaux.','A unified digital space for exploring and managing heritage-site digital twins.','Miras alanlarının dijital ikizlerini keşfetmek ve yönetmek için birleşik dijital ortam.']
    ,'مخصصة لإنشاء وربط رموز استجابة سريعة ميدانية تعرض البطاقة التقنية للموقع الأثري بلغات متعددة حسب لغة السائح.':['Conçue pour créer des QR codes sur site et afficher la fiche technique du lieu dans la langue du visiteur.','Creates on-site QR codes that show a heritage site’s technical profile in the visitor’s language.','Sahada QR kodları oluşturur ve miras alanının teknik kartını ziyaretçinin dilinde gösterir.']
    ,'يتيح هذا النظام ربط شبكة المتاحف والمعالم الأثرية بين مختلف الولايات، مما يوفر للمؤسسات السياحية رؤية موحدة للزوار والباحثين مدعومة ببيانات تفاعلية دقيقة.':['Ce système relie musées et sites archéologiques entre les wilayas et fournit aux institutions touristiques une vue unifiée, fondée sur des données interactives.','This system connects museums and archaeological sites across wilayas, giving tourism institutions a unified view supported by interactive data.','Bu sistem müzeleri ve arkeolojik alanları vilayetler arasında bağlar; turizm kurumlarına etkileşimli verilerle desteklenen ortak bir görünüm sunar.']
    ,'لوحة التحكم الرقمي (Digital Twin)':['Tableau de bord du jumeau numérique','Digital Twin dashboard','Dijital İkiz paneli']
    ,'انضم إلى شبكة التوأمة السياحية':['Rejoindre le réseau de jumelage touristique','Join the tourism twinning network','Turizm ikiz ağına katılın']
    ,'تجربة الذاكرة عبر الأجيال':['Une mémoire partagée entre les générations','A memory experience across generations','Nesiller arası hafıza deneyimi']
    ,'مع نظارات Geo-Memory للواقع المعزز، قمنا بدمج التكنولوجيا مع التاريخ. الآن، يمكن لمختلف الأجيال أن يقفوا في نفس المكان، لكن كل منهم يرى طبقة مختلفة من التاريخ تتفاعل أمام أعينهم في وقت واحد.':['Avec les lunettes de réalité augmentée Geo-Memory, la technologie rencontre l’histoire. Plusieurs générations peuvent se tenir au même endroit et voir simultanément différentes couches historiques.','Geo-Memory AR glasses bring technology and history together. Different generations can stand in the same place and see distinct layers of history at once.','Geo-Memory artırılmış gerçeklik gözlükleri teknolojiyle tarihi birleştirir. Farklı nesiller aynı yerde durup tarihin ayrı katmanlarını eş zamanlı görebilir.']
    ,'للواقع المعزز، قمنا بدمج التكنولوجيا مع التاريخ. الآن، يمكن لمختلف الأجيال أن يقفوا في نفس المكان، لكن كل منهم يرى طبقة مختلفة من التاريخ تتفاعل أمام أعينهم في وقت واحد.':['pour la réalité augmentée, nous avons réuni technologie et histoire. Plusieurs générations peuvent partager un lieu et voir différentes couches historiques.','for augmented reality, we bring technology and history together. Different generations can share a place and see distinct layers of history.','artırılmış gerçeklikle teknoloji ve tarihi buluşturuyoruz. Farklı nesiller aynı yerde durup tarihin ayrı katmanlarını görebilir.']
    ,'الماضي':['Passé','Past','Geçmiş'],'الحاضر':['Présent','Present','Şimdi'],'المستقبل':['Futur','Future','Gelecek']
    ,'نظارات الواقع المعزز للتراث':['Lunettes de réalité augmentée pour le patrimoine','AR glasses for heritage','Miras için artırılmış gerçeklik gözlükleri']
    ,'استكشف قصر بشار العتيق بالواقع المعزز (AR)':['Découvrez l’ancien palais de Béchar en réalité augmentée','Explore the old Béchar palace in AR','Eski Beşar Sarayı’nı artırılmış gerçeklikle keşfedin']
    ,'قم بتوجيه كاميرا هاتفك نحو سطح مستوٍ لتجربة المجسم ثلاثي الأبعاد في بيئتك الحقيقية.':['Pointez l’appareil photo vers une surface plane pour voir le modèle 3D dans votre environnement.','Point your camera at a flat surface to view the 3D model in your surroundings.','3B modeli gerçek ortamınızda görmek için kameranızı düz bir yüzeye doğrultun.']
    ,'مع نظارات':['Avec les lunettes','With the glasses','Gözlüklerle']
    ,'تتيح لك هذه اللوحة ربط الرمز الميداني لكل معلم أثري مضاف في تطبيق (Monuments)؛ حيث يتم عرض كود الـ QR الخاص به فوراً.':['Ce tableau relie le code de chaque site ajouté dans Monuments et affiche immédiatement son QR code.','This dashboard links each site added in Monuments to its field code and displays its QR code instantly.','Bu panel, Monuments uygulamasına eklenen alanları saha kodlarına bağlar ve QR kodlarını anında gösterir.']
    ,'⚠️ هذه الخدمة متوفرة ضمن الباقة المدفوعة':['⚠️ Ce service est inclus dans l’offre payante','⚠️ This service is included in the paid plan','⚠️ Bu hizmet ücretli pakete dahildir']
    ,'توليد وطباعة رموز الـ QR اللامحدودة لكافة المعالم يتطلب ترقية الحساب.':['La génération et l’impression illimitées de QR codes nécessitent une mise à niveau du compte.','Unlimited QR code generation and printing requires an account upgrade.','Sınırsız QR kodu üretimi ve yazdırma için hesap yükseltmesi gerekir.']
    ,'انقر واسحب بالماوس أو الإصبع لاستكشاف المكان في جميع الاتجاهات (360 درجة).':['Cliquez et faites glisser pour explorer les lieux à 360° avec la souris ou le doigt.','Click and drag with a mouse or finger to explore the site in 360 degrees.','360 derece keşif için fareyle veya parmağınızla tıklayıp sürükleyin.']
    ,'تكنولوجيا الذاكرة':['Technologies de la mémoire','Memory technology','Hafıza teknolojisi'],'أعلام وسير':['Personnalités et biographies','Figures and biographies','Önemli kişiler ve biyografiler'],'عرض المسارات':['Afficher les itinéraires','Show routes','Rotaları göster']
  };
  const spanishCopy = {
    'الرئيسية':'Inicio','من نحن':'Sobre nosotros','المكتبة التاريخية':'Biblioteca histórica','المتحف الرقمي':'Museo digital','الابتكار والأثر الاقتصادي':'Innovación e impacto económico','الأطالس':'Atlas',
    'المستودع الرقمي':'Repositorio digital','العودة للرئيسية':'Volver al inicio','العودة إلى الرئيسية':'Volver al inicio','تسجيل الدخول':'Iniciar sesión','تسجيل الدخول الموحد':'Inicio de sesión unificado','إنشاء حساب':'Crear cuenta','إنشاء حساب موحد':'Crear cuenta unificada','لوحة التحكم':'Panel de control',
    'اسم المستخدم أو البريد الإلكتروني':'Nombre de usuario o correo electrónico','كلمة المرور':'Contraseña','تذكرني':'Recordarme','Language':'Idioma','اختيار اللغة':'Seleccionar idioma','منصة Geo-Memory':'Plataforma Geo-Memory',
    'مرحباً بك مجدداً، اختر وجهتك وسجل دخولك للمنصة':'Te damos la bienvenida. Elige tu espacio e inicia sesión.','أنشئ حسابك الجديد واختر المسار المفضل لديك لبدء الرحلة':'Crea tu cuenta y elige tu itinerario para comenzar.','بيانات الدخول غير صحيحة، يرجى المحاولة مجدداً.':'Los datos de acceso no son correctos. Inténtalo de nuevo.','اختر مساحة العمل المطلوبة:':'Elige el espacio de trabajo:','دخول إلى الحساب':'Iniciar sesión','ليس لديك حساب بعد؟':'¿Aún no tienes una cuenta?','أنشئ حساباً جديداً الآن':'Crea una cuenta ahora',
    'بواباتنا ومنتجاتنا':'Nuestros portales y productos','فضاءات العمل والتكوين':'Espacios de trabajo y formación','خدماتنا':'Nuestros servicios','لوحة التحكم المركزية':'Panel de control central','تواصل معنا':'Contáctanos',
    'التاريخ في خريطة رقمية':'La historia en un mapa digital','حيث تنبض':'Donde','الجغرافيا':'la geografía cobra vida','بأمجاد':'con las glorias de','التاريخ':'la historia','أول بيئة رقمية وهندسية متكاملة لرقمنة وتوثيق التراث والتاريخ باستخدام نظم المعلومات الجغرافية المتطورة والأطالس الذكية.':'Un entorno digital y geoespacial integrado para digitalizar y documentar el patrimonio y la historia con SIG avanzados y atlas inteligentes.','ولوج فضاء التكوين والاشتراكات':'Acceder a formación y suscripciones','تصفح تقنية AR/VR':'Explorar AR/VR','رؤيتنا في مؤسسة Geo-Memory':'Nuestra visión en Geo-Memory',
    'المستودع التاريخي العام':'Repositorio público de historia','أحدث المحطات والخرائط المبتكرة':'Últimos relatos y mapas innovadores','هل أنت مستعد لاختبار ذكائك التاريخي؟':'¿Listo para poner a prueba tus conocimientos históricos?','ابدأ تحدي "المسار المحرر"':'Iniciar el reto «ruta de liberación»','منصاتنا وأنظمتنا الفرعية':'Nuestras plataformas y sistemas','اختر البوابة الرقمية المناسبة لبدء العمل والبحث الميداني':'Elige el portal digital adecuado para trabajar e investigar sobre el terreno','الأطالس الرقمية التفاعلية':'Atlas digitales interactivos','ولوج مستودع الخرائط':'Explorar la colección de mapas','منصة التكوين الهندسي (GIS)':'Plataforma de formación geoespacial (SIG)','الخدمات الرقمية والتوأمة':'Servicios digitales y gemelos digitales','خطط الاشتراك الرقمية':'Planes de suscripción digital','اختر الخطة التي تناسب احتياجاتك البحثية أو المؤسساتية':'Elige el plan que se adapte a tus necesidades de investigación o institución','طالب':'Estudiante','أستاذ / باحث':'Docente / investigador','مؤسسة':'Institución','التفاصيل والتسجيل':'Detalles e inscripción',
    'تحميل الشهادة كصورة':'Descargar certificado como imagen','عودة لوحة التحكم':'Volver al panel de control','معرف التحقق الرسمي':'Identificador oficial de verificación','شهادة إتمام ونجاح رسمية':'Certificado oficial de finalización','شهادة إتمام المسار التعليمي':'Certificado de finalización del itinerario educativo','تاريخ الإصدار الرسمي':'Fecha oficial de emisión','امسح للتحقق من صحة الشهادة':'Escanea para verificar el certificado','Geo-Memory | الذاكرة عبر الجغرافيا الرقمية':'Geo-Memory | La memoria a través de la geografía digital',
    'Innovation et impact économique':'Innovación e impacto económico','Innovation géospatiale au service de la mémoire.':'Innovación geoespacial para preservar la memoria.','© 2026 Tous droits réservés à Geo-Memory.':'© 2026 Geo-Memory. Todos los derechos reservados.','مجاني/مدعوم':'Gratis / con apoyo','مهارات ووظائف رقمية':'Competencias y empleos digitales','فرص للفاعلين المحليين':'Oportunidades para profesionales locales','تثمين التراث':'Puesta en valor del patrimonio','الابتكار والاقتصاد المحلي':'Innovación y economía local',
    'Geo-Memory ، منصة رقمية متكاملة للتراث والسياحة، تبني ذاكرة جغرافية للوجهة وتطوّر توأمها الرقمي من خلال دمج المعطيات المكانية والزمانية والسياقية وتوظيف الذكاء الاصطناعي، لتقديم تجارب سياحية ذكية، ورقمنة التراث وتثمينه، ودعم إدارة الوجهة وصناعة القرار.':'Geo-Memory es una plataforma digital de patrimonio y turismo que crea memoria geográfica y gemelos digitales con datos espaciales y temporales e inteligencia artificial.','مركز التوأمة الرقمية التفاعلية':'Centro de gemelos digitales','مركز التوأمة الرقمية التفاعلية\nبيئة رقمية موحّدة تربط التوائم الرقمية للمواقع والمعالم التراثية، لتقديم تمثيل تفاعلي للوجهة السياحية وإتاحة استكشافها وإدارتها بذكاء':'Centro digital unificado para conectar, explorar y gestionar gemelos digitales del patrimonio.','بيئة رقمية موحّدة تربط التوائم الرقمية للمواقع والمعالم التراثية، لتقديم تمثيل تفاعلي للوجهة السياحية وإتاحة استكشافها وإدارتها بذكاء':'Un espacio digital unificado para explorar y gestionar los gemelos digitales de sitios patrimoniales.',
    '🥽 ابدأ جولة الـ VR للمتحف':'🥽 Iniciar visita VR del museo','انقر لدخول جولة الـ VR':'Haz clic para iniciar la visita VR','معلم مصنف':'Sitio patrimonial protegido','مركز التوأمة الرقمية التفاعلية بيئة رقمية موحّدة تربط التوائم الرقمية للمواقع والمعالم التراثية، لتقديم تمثيل تفاعلي للوجهة السياحية وإتاحة استكشافها وإدارتها بذكاء':'Centro de gemelos digitales que conecta sitios patrimoniales en un entorno interactivo para explorar y gestionar destinos.',
    'مخصصة لإنشاء وربط رموز استجابة سريعة ميدانية تعرض البطاقة التقنية للموقع الأثري بلغات متعددة حسب لغة السائح.':'Crea códigos QR en los sitios para mostrar la ficha técnica del lugar en el idioma del visitante.','يتيح هذا النظام ربط شبكة المتاحف والمعالم الأثرية بين مختلف الولايات، مما يوفر للمؤسسات السياحية رؤية موحدة للزوار والباحثين مدعومة ببيانات تفاعلية دقيقة.':'Conecta museos y sitios arqueológicos de distintas provincias y ofrece a las instituciones turísticas una visión unificada basada en datos interactivos.',
    'لوحة التحكم الرقمي (Digital Twin)':'Panel del gemelo digital','انضم إلى شبكة التوأمة السياحية':'Únete a la red de gemelos turísticos','تجربة الذاكرة عبر الأجيال':'Una experiencia de memoria entre generaciones','مع نظارات Geo-Memory للواقع المعزز، قمنا بدمج التكنولوجيا مع التاريخ. الآن، يمكن لمختلف الأجيال أن يقفوا في نفس المكان، لكن كل منهم يرى طبقة مختلفة من التاريخ تتفاعل أمام أعينهم في وقت واحد.':'Las gafas de realidad aumentada Geo-Memory unen tecnología e historia: varias generaciones pueden compartir un lugar y ver distintas capas históricas a la vez.','للواقع المعزز، قمنا بدمج التكنولوجيا مع التاريخ. الآن، يمكن لمختلف الأجيال أن يقفوا في نفس المكان، لكن كل منهم يرى طبقة مختلفة من التاريخ تتفاعل أمام أعينهم في وقت واحد.':'con realidad aumentada, unimos tecnología e historia: varias generaciones pueden compartir un lugar y ver distintas capas históricas.',
    'الماضي':'Pasado','الحاضر':'Presente','المستقبل':'Futuro','نظارات الواقع المعزز للتراث':'Gafas de realidad aumentada para el patrimonio','استكشف قصر بشار العتيق بالواقع المعزز (AR)':'Explora el antiguo palacio de Béchar con realidad aumentada','قم بتوجيه كاميرا هاتفك نحو سطح مستوٍ لتجربة المجسم ثلاثي الأبعاد في بيئتك الحقيقية.':'Apunta la cámara del móvil a una superficie plana para ver el modelo 3D en tu entorno real.','تكنولوجيا الذاكرة':'Tecnología de la memoria','أعلام وسير':'Figuras y biografías','عرض المسارات':'Mostrar rutas','مع نظارات':'Con las gafas','تتيح لك هذه اللوحة ربط الرمز الميداني لكل معلم أثري مضاف في تطبيق (Monuments)؛ حيث يتم عرض كود الـ QR الخاص به فوراً.':'Este panel enlaza cada sitio añadido en Monuments con su código de campo y muestra su QR al instante.','⚠️ هذه الخدمة متوفرة ضمن الباقة المدفوعة':'⚠️ Servicio incluido en el plan de pago','توليد وطباعة رموز الـ QR اللامحدودة لكافة المعالم يتطلب ترقية الحساب.':'La generación e impresión ilimitadas de códigos QR requiere actualizar la cuenta.','انقر واسحب بالماوس أو الإصبع لاستكشاف المكان في جميع الاتجاهات (360 درجة).':'Haz clic y arrastra con el ratón o el dedo para explorar el lugar en 360 grados.',
    'نحن شركة ناشئة جزائرية طموحة وهندسية، نسعى لحماية الذاكرة من خلال إسقاط المحتوى التاريخي جغرافياً ورقمياً. نربط المعالم، المعارك، والمسارات بمواقعها الحقيقية عبر برمجيات الـ GIS الاحترافية، ونوفر بيئة تدريبية للأكاديميين لبناء قواعد بيانات جغرافية تاريخية آمنة وموثقة.':'Somos una empresa emergente geoespacial argelina que preserva la memoria al vincular los relatos históricos con lugares reales. Nuestras herramientas SIG conectan monumentos, batallas y rutas con sus ubicaciones, y formamos a especialistas para crear bases de datos geohistóricas fiables.',
    'المنطقة الجغرافية قيد الاستكشاف! بينما نعمل على إضافة معالم جديدة، يمكنك تجربة التحديات المتاحة.':'Esta zona está en exploración. Mientras añadimos nuevos lugares, puedes probar los retos disponibles.',
    'خرائط جغرافية تفاعلية دقيقة مبنية بإحداثيات GIS لتتبع مسارات المقاومات الشعبية الكبرى ومعارك الثورة التحريرية المظفرة.':'Mapas geográficos interactivos y precisos, basados en coordenadas SIG, para seguir las rutas de las grandes resistencias populares y las batallas de la revolución de liberación.',
    'بيئة تدريبية واحترافية مستقلة مخصصة للأكاديميين والباحثين لإنشاء وتسيير قواعد البيانات الجغرافية بنظام اشتراك سنوي.':'Entorno profesional de formación para que investigadores y académicos creen y gestionen bases de datos geográficas mediante una suscripción anual.',
    'معرض رقمي مفتوح لعرض مجسمات المواقع والمعالم التاريخية الوطنية الموثقة، ويدعم السياحة الثقافية عبر الـ QR Code.':'Galería digital abierta de modelos 3D de sitios y monumentos históricos nacionales documentados, con códigos QR para apoyar el turismo cultural.',
    '✓ الوصول للمتحف الرقمي':'✓ Acceso al museo digital','✓ تصفح الأطالس العامة':'✓ Consulta de atlas públicos','✓ موارد تعليمية محدودة':'✓ Recursos educativos limitados','✓ أدوات GIS المتقدمة':'✓ Herramientas SIG avanzadas','✓ بناء قواعد بيانات جغرافية':'✓ Creación de bases de datos geográficas','✓ دعم تقني مخصص':'✓ Asistencia técnica especializada','✓ حسابات متعددة للمستخدمين':'✓ Cuentas para varios usuarios','✓ تقارير GIS تحليلية':'✓ Informes de análisis SIG','✓ لوحة تحكم إدارية كاملة':'✓ Panel de administración completo',
    'خاص':'Personalizado','مخصص':'Personalizado','تواصل معنا':'Contáctanos','طلب اشتراك تكويني':'Solicitar suscripción de formación','Professional Academy':'Academia profesional'
  };
  const index = {fr:0,en:1,tr:2,es:3}[lang];
  if (index === undefined) return;
  const translate = (value) => {
    const key = value.trim();
    if (!copy[key] && !spanishCopy[key]) return value;
    const translated = lang === 'es' ? (spanishCopy[key] || (copy[key] && copy[key][1])) : (copy[key] && copy[key][index]);
    return translated ? value.replace(key, translated) : value;
  };
  const nodes = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  const textNodes = [];
  while (nodes.nextNode()) textNodes.push(nodes.currentNode);
  for (const node of textNodes) {
    if (!node.parentElement.closest('script,style,textarea,code,pre,[data-no-translate]')) node.nodeValue = translate(node.nodeValue);
  }
  document.querySelectorAll('.lang-text[data-en],.lang-text[data-ar]').forEach(el => {
    const value = lang === 'ar' ? el.getAttribute('data-ar') : (el.getAttribute(`data-${lang}`) || el.getAttribute('data-en'));
    if (value) el.textContent = value;
  });
  for (const el of document.querySelectorAll('[placeholder],[title],[aria-label]')) {
    for (const attr of ['placeholder','title','aria-label']) if (el.hasAttribute(attr)) el.setAttribute(attr, translate(el.getAttribute(attr)));
  }
  const localized = (ar, values, es) => lang === 'es' ? es : values[index];
  const labels = {home:localized('home',['Accueil','Home','Ana sayfa'],'Inicio'),library:localized('library',['Bibliothèque historique','History library','Tarih kütüphanesi'],'Biblioteca histórica'),museum:localized('museum',['Musée numérique','Digital museum','Dijital müze'],'Museo digital'),innovation:localized('innovation',['Innovation et impact économique','Innovation and economic impact','Yenilik ve ekonomik etki'],'Innovación e impacto económico'),about:localized('about',['À propos','About us','Hakkımızda'],'Sobre nosotros'),atlases:localized('atlases',['Atlas','Atlases','Atlaslar'],'Atlas'),login:localized('login',['Connexion','Sign in','Giriş yap'],'Iniciar sesión'),register:localized('register',['Créer un compte','Create account','Hesap oluştur'],'Crear cuenta'),dashboard:localized('dashboard',['Tableau de bord','Dashboard','Kontrol paneli'],'Panel de control'),'footer-summary':localized('footer-summary',['Innovation géospatiale au service de la mémoire.','Geospatial innovation for preserving memory.','Hafızayı korumak için coğrafi yenilik.'],'Innovación geoespacial para preservar la memoria.'),copyright:localized('copyright',['© 2026 Tous droits réservés à Geo-Memory.','© 2026 All rights reserved by Geo-Memory.','© 2026 Geo-Memory tarafından tüm hakları saklıdır.'],'© 2026 Geo-Memory. Todos los derechos reservados.'),'student-role':localized('student-role',['📚 Élève de la plateforme éducative','📚 Learning platform student','📚 Eğitim platformu öğrencisi'],'📚 Estudiante de la plataforma educativa'),'ai-guide':localized('ai-guide',['🤖 Guide intelligent IA','🤖 AI smart guide','🤖 Yapay zekâ akıllı rehberi'],'🤖 Guía inteligente de IA'),'sovereign-status':localized('sovereign-status',['Conteneur souverain local (Docker) - sécurisé','Local sovereign container (Docker) - secure','Yerel egemen konteyner (Docker) - güvenli'],'Contenedor local soberano (Docker) - seguro')};
  document.querySelectorAll('[data-gm-i18n]').forEach(el => { const key=el.dataset.gmI18n; if(labels[key]) el.textContent=labels[key]; });
  if (document.title) document.title = translate(document.title);
  document.documentElement.dir = lang === 'ar' ? 'rtl' : 'ltr';
  const observer = new MutationObserver(records => {
    for (const record of records) {
      for (const node of record.addedNodes) {
        if (node.nodeType === Node.TEXT_NODE) {
          if (!node.parentElement.closest('script,style,textarea,code,pre,[data-no-translate]')) node.nodeValue = translate(node.nodeValue);
        } else if (node.nodeType === Node.ELEMENT_NODE && !node.matches('script,style,textarea,code,pre,[data-no-translate]')) {
          const walker = document.createTreeWalker(node, NodeFilter.SHOW_TEXT);
          while (walker.nextNode()) if (!walker.currentNode.parentElement.closest('script,style,textarea,code,pre,[data-no-translate]')) walker.currentNode.nodeValue = translate(walker.currentNode.nodeValue);
        }
      }
    }
  });
  observer.observe(document.body, {childList:true,subtree:true});
})();
