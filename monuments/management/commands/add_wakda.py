from django.core.management.base import BaseCommand
from monuments.models import Monument

class Command(BaseCommand):
    help = 'إضافة بيانات قصر واكدة بولاية بشار باستخدام مجلد Static'

    def handle(self, *args, **kwargs):
        slug = 'ksar-wakda-bechar'
        if Monument.objects.filter(slug=slug).exists():
            self.stdout.write(self.style.WARNING('قصر واكدة موجود مسبقاً في القاعدة!'))
            return

        Monument.objects.create(
            slug=slug,
            name_ar="قصر واكدة الأثري",
            name_fr="Ksar Wakda Historique",
            name_en="Historical Ksar Wakda",
            
            description_ar=(
                "يُعد قصر واكدة بولاية بشار واحداً من أهم المعالم العمارية الصحراوية التقليدية "
                "التي تعكس عبقرية الإنسان في التأقلم مع البيئة الواحية القاسية. "
                "يتميز ببناء مدمج من الطين والتراب وأسقف من جذوع النخيل، "
                "ويجسد نموذجاً حياً للقصور العتيقة التي تجمع بين الوظيفة الدفاعية والاجتماعية في منطقة الساورة."
            ),
            description_fr=(
                "Le Ksar Wakda à Béchar est l'un des monuments d'architecture traditionnelle oasienne "
                "les plus remarquables, reflétant l'ingéniosité humaine face aux rudes conditions sahariennes. "
                "Construit en pisé et doté de toits en troncs de palmier, il incarne le modèle typique des ksars anciens."
            ),
            description_en=(
                "Ksar Wakda in Bechar is one of the most remarkable traditional oasis architectural monuments, "
                "reflecting human ingenuity in adapting to harsh Saharan environments. "
                "Built with rammed earth and palm-trunk roofs, it represents a living model of ancient desert ksars."
            ),
            
            location_name="ولاية بشار، الجزائر (Béchar, Algérie)",
            google_maps_url="https://maps.google.com/?q=31.6300,-2.2200", # إحداثيات تقريبية لبشار
            
            # ربط مسارات الملفات من مجلد static مباشرة
            drone_video_path="monuments/videos/wakda_drone.mp4",
            image_path="monuments/images/wakda_cover.png"
        )

        self.stdout.write(self.style.SUCCESS('تمت إضافة "قصر واكدة" مع مسارات Static بنجاح!'))