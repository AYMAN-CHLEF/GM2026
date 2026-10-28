from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [('core', '0004_prepaidcard_target_cycle_prepaidcard_target_year_and_more')]
    operations = [
        migrations.AddField(
            model_name='course',
            name='course_type',
            field=models.CharField(choices=[('coding', 'برمجة'), ('specialized', 'نظم معلومات جغرافية GIS')], db_index=True, default='specialized', max_length=20, verbose_name='نوع الدورة'),
        ),
    ]
