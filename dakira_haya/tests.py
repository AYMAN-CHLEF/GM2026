from django.test import TestCase
from django.urls import reverse

from .models import Flag


class DakiraHayaTests(TestCase):
    def setUp(self):
        self.flag = Flag.objects.create(
            full_name='عبد الحميد بن باديس',
            biography='رائد النهضة الجزائرية',
            latitude=36.3676,
            longitude=6.6118,
            slug='bin-badis',
        )

    def test_library_page_status_code(self):
        response = self.client.get(reverse('dakira_haya:flags_list'))
        self.assertEqual(response.status_code, 200)

    def test_flag_detail_view(self):
        response = self.client.get(reverse('dakira_haya:flag_detail', args=[self.flag.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.flag.full_name)

    def test_map_page_without_figure_returns_to_library(self):
        response = self.client.get(reverse('dakira_haya:map_page'))
        self.assertRedirects(response, reverse('dakira_haya:flags_list'))

    def test_unready_figure_cannot_open_interactive_map(self):
        response = self.client.get(reverse('dakira_haya:map_page'), {'figure': self.flag.slug})
        self.assertRedirects(response, reverse('dakira_haya:flags_list'))

    def test_ready_figure_loads_its_interactive_map(self):
        self.flag.is_ready = True
        self.flag.save(update_fields=['is_ready'])
        response = self.client.get(reverse('dakira_haya:map_page'), {'figure': self.flag.slug})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['flag'], self.flag)
        self.assertIn('science_data_json', response.context)
