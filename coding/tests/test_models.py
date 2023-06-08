from django.test import TestCase
from django.contrib.auth.models import User
from coding.models import *

class ModelsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.section_type = Section_type.objects.create(name='Test Type')
        self.section_status = Section_status.objects.create(name='Test Status')
        self.status_data = Status_data.objects.create(name='Test Data')
        self.folder = Folder.objects.create(name='Test Folder', user=self.user)
        self.file = File.objects.create(name='Test File', user=self.user, parent=self.folder)
        self.file_section = File_section.objects.create(file = self.file, begin = 1, end = 1)

    def test_section_type_str(self):
        self.assertEqual(str(self.section_type), 'Test Type')

    def test_file_section_str(self):
        self.assertEqual(str(self.file_section), '')

    def test_section_status_str(self):
        self.assertEqual(str(self.section_status), 'Test Status')

    def test_status_data_str(self):
        self.assertEqual(str(self.status_data), 'Test Data')

    def test_folder_structure(self):
        self.assertTrue('<li class="folder"><button onClick="folder('+str(self.folder.id)+')" id="folder_'+str(self.folder.id)+'">Test Folder</button><ul>' in self.folder.structure())

    def test_file_structure(self):
        self.assertEqual('<li class="file"><button onClick="file('+str(self.file.id)+')" id="file_'+str(self.file.id)+'">Test File</button></li>',self.file.structure())
    
    def test_file_section_write(self):
        file_section = File_section.objects.create(name='Test Section', type=self.section_type, status=self.section_status, status_data=self.status_data, file=self.file, begin=1, end=1)
        self.assertEqual(file_section.write(''), '// Sekcja: Test Section\n// Rodzaj sekcji: Test Type, zakres: od 1 do 1 linii\n// Status: Test Status\n// Dane statusu: Test Data')

    def test_file_section_write_content(self):
        file_section = File_section.objects.create(name='Test Section', type=self.section_type, status=self.section_status, status_data=self.status_data, file=self.file, begin=1, end=1, content = 'Test Content')
        self.assertEqual(file_section.write_content('', '', ['    Test Content']), '<button id="section_'+str(file_section.id)+'" class="section_header"><pre>// Sekcja: Test Section\n// Rodzaj sekcji: Test Type, zakres: od 1 do 1 linii\n// Status: Test Status\n// Dane statusu: Test Data</pre></button><br><pre class="line" id="line_1">    Test Content</pre>')


    def tearDown(self):
        self.user.delete()
        self.section_type.delete()
        self.section_status.delete()
        self.status_data.delete()
        self.folder.delete()
        self.file.delete()

