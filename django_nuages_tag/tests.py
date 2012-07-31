from django.utils import unittest
from django.template import Template, Context, TemplateSyntaxError

class TemplateTagsTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def test_compute_tag_cloud_requires_arguments(self):
        with self.assertRaises(TemplateSyntaxError):
            t = Template('{% load django_nuages_tag %}'
                         '{% compute_tag_cloud %}')
            c = Context({})
            t.render(c)             
        