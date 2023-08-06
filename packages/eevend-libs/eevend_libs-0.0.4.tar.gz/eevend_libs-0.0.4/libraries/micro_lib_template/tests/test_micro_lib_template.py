from unittest import TestCase

from eevend_libs.micro_lib_template.micro_lib_template import MicroLibTemplate


class MicroLibTemplateTests(TestCase):

    def setUp(self):
        self.micro_lib_template = MicroLibTemplate()

    def test_greeting(self):
        name = 'Bob'
        result = self.micro_lib_template.greeting(name)
        self.assertEqual(result, 'Hello %s' % name)
