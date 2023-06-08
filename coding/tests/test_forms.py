from django.test import TestCase
from coding.forms import StandardForm, OptymalizacjeForm, ProcesorForm, MCS51Form, Z80Form, STM8Form, FileUploadForm, FolderUploadForm, SectionUploadForm
from django.core.files.uploadedfile import SimpleUploadedFile


class FormsTestCase(TestCase):
    def test_standard_form(self):
        form_data = {
            'standard': 'C11',
        }
        form = StandardForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_standard_form_incorrect(self):
        form_data = {
            'standard': 'incorrect_standard',
        }
        form = StandardForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_standard_form_multiple(self):
        form_data = {
            'standard': ['C11', 'C99'],
        }
        form = StandardForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_optymalizacje_form(self):
        form_data = {
            'optymalizacje': ['--nogcse', '--noinvariant', '--noinduction', '--noloopreverse'],
        }
        form = OptymalizacjeForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_optymalizacje_form_empty(self):
        form_data = {
            'optymalizacje': [],
        }
        form = OptymalizacjeForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_optymalizacje_form_incorrect(self):
        form_data = {
            'optymalizacje': ['incorrect_optymalizacje'],
        }
        form = OptymalizacjeForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_procesor_form(self):
        form_data = {
            'procesor': 'MCS51',
        }
        form = ProcesorForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_procesor_form_incorrect(self):
        form_data = {
            'procesor': 'incorrect_procesor',
        }
        form = ProcesorForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_mcs51_form(self):
        form_data = {
            'mcs51': '--model-small',
        }
        form = MCS51Form(data=form_data)
        self.assertTrue(form.is_valid())

    def test_mcs51_form_incorrect(self):
        form_data = {
            'mcs51': 'incorrect_mcs51',
        }
        form = MCS51Form(data=form_data)
        self.assertFalse(form.is_valid())

    def test_z80_form(self):
        form_data = {
            'z80': '--asm=z80asm',
        }
        form = Z80Form(data=form_data)
        self.assertTrue(form.is_valid())

    def test_z80_form_incorrect(self):
        form_data = {
            'z80': 'incorrect_z80',
        }
        form = Z80Form(data=form_data)
        self.assertFalse(form.is_valid())

    def test_stm8_form(self):
        form_data = {
            'stm8': '--opt-code-size',
        }
        form = STM8Form(data=form_data)
        self.assertTrue(form.is_valid())

    def test_stm8_form_incorrect(self):
        form_data = {
            'stm8': 'incorrect_stm8',
        }
        form = STM8Form(data=form_data)
        self.assertFalse(form.is_valid())

    def test_folder_upload_form(self):
        form_data = {
            'folder_name': 'example_folder_name',
        }
        form = FolderUploadForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_folder_upload_form_empty(self):
        form_data = {
            'folder_name': '',
        }
        form = FolderUploadForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_section_upload_form(self):
        form_data = {
            'section_name': 'example_section_name',
            'section_type': 'example_section_type',
        }
        form = SectionUploadForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_section_upload_form_empty_name(self):
        form_data = {
            'section_name': '',
            'section_type': 'example_section_type',
        }
        form = SectionUploadForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_section_upload_form_incorrect(self):
        form_data = {
            'section_name': 'example_section_name',
            'section_type': '',
        }
        form = SectionUploadForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_file_upload_form(self):
        form_data = {
            'file_name': 'example_filename',
        }
        file_content = b'This is a sample file content.'
        file = SimpleUploadedFile('example_file.c', file_content, content_type='text/plain')
        form = FileUploadForm(data=form_data, files={'file': file})
        self.assertTrue(form.is_valid())

    def test_file_upload_form_empty_name(self):
        form_data = {
            'file_name': '',
        }
        file_content = b'This is a sample file content.'
        file = SimpleUploadedFile('example_file.c', file_content, content_type='text/plain')
        form = FileUploadForm(data=form_data, files={'file': file})
        self.assertTrue(form.is_valid())

    def test_file_upload_form_incorrect(self):
        form_data = {
            'file_name': 'example_filename',
        }
        file_content = b'This is a sample file content.'
        file = SimpleUploadedFile('example_file.txt', file_content, content_type='text/plain')
        form = FileUploadForm(data=form_data, files={'file': file})
        self.assertTrue(form.is_valid())

    def test_file_upload_form_empty_file(self):
        form_data = {
            'file_name': 'example_filename',
        }
        form = FileUploadForm(data=form_data, files={})
        self.assertFalse(form.is_valid())

    