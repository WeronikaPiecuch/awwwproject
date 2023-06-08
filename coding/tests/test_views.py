import json
from django.test import RequestFactory, TestCase, Client
from django.urls import reverse
from django.contrib.sessions.middleware import SessionMiddleware
from coding.models import Folder, File, Section_type, File_section, Section_status
from coding.views import *
from django.contrib.auth.models import User
import json
from django.http import JsonResponse

class ViewsTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.folder = Folder.objects.create(name='Test Folder')
        file = open('./test_error.c', 'r')
        self.file_error = file.read()
        file.close()
        file = open('./test_error.c', 'r')
        self.file_compile = file.read()
        file.close()
        self.file = File.objects.create(name='Test File', parent=self.folder, content=self.file_compile)
        self.file_error = File.objects.create(name='Test File', parent=self.folder, content=self.file_error)
        self.client = Client()
        self.user = User.objects.create_user(username='your_username', password='your_password')
        Section_type.objects.create(name='procedury')
        Section_type.objects.create(name='dyrektywy')
        Section_type.objects.create(name='deklaracja zmiennych')
        Section_type.objects.create(name='wstawka asemblerowa')
        Section_type.objects.create(name='komentarz')
        Section_status.objects.create(name = 'nie kompiluje się')
        Section_status.objects.create(name = 'kompiluje się z ostrzeżeniami')
        Section_status.objects.create(name = 'kompiluje się bez ostrzeżeń')

    def test_login(self):
        response = self.client.post("/login/", {"username": "john", "password": "smith"})
        self.assertEqual(response.status_code, 200)
        
    def test_index_authenticated_user(self):
        self.client.login(username='your_username', password='your_password')
        response = self.client.get(reverse('coding:index'))
        self.assertEqual(response.status_code, 200)

    def test_index_unauthenticated_user(self):
        response = self.client.get(reverse('coding:index'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('coding:login'))

    def test_add_folder_view(self):
        url = reverse('coding:add/folder')
        data = {'parent_id': self.folder.id, 'name': 'New Folder'}
        request = self.factory.post(url, data=json.dumps(data), content_type='application/json')
        request.user = self.user
        response = add_folder(request)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, JsonResponse)

    def test_add_file_view(self):
        url = reverse('coding:add/file')
        data = {'parent_id': self.folder.id, 'file': 'Test file content', 'name': 'New File'}
        request = self.factory.post(url, json.dumps(data), content_type='application/json')
        request.user = self.user
        response = add_file(request)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, JsonResponse)

    def test_add_section_view(self):
        url = reverse('coding:add/section', args=[self.file.id])
        data = {'first_line': 1, 'last_line': 3, 'name': 'New Section', 'type': 'Section Type'}
        request = self.factory.post(url, json.dumps(data), content_type='application/json')
        response = add_section(request, self.file.id)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, JsonResponse)

    def test_delete_folder_view(self):
        url = reverse('coding:delete/folder', args=[self.folder.id])
        request = self.factory.post(url)
        response = delete_folder(request, self.folder.id)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, JsonResponse)

    def test_delete_file_view(self):
        url = reverse('coding:delete/file', args=[self.file.id])
        request = self.factory.post(url)
        response = delete_file(request, self.file.id)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, JsonResponse)

    def test_delete_section_view(self):
        section = File_section.objects.create(name='Test Section', file=self.file, begin=1, end=1, content = self.file_compile.splitlines()[0])
        url = reverse('coding:delete/section', args=[self.file.id, section.id])
        request = self.factory.post(url)
        response = delete_section(request, self.file.id, section.id)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, JsonResponse)

    def test_compile_error_view(self):
        url = reverse('coding:compile', args=[self.file_error.id])
        request = self.factory.post(url)
        request.user = self.user
        middleware = SessionMiddleware(lambda request: None)
        middleware.process_request(request) 
        request.session.save()
        request.session['standard']= 'C11'
        request.session['procesor']='MCS51'
        request.session['optymalizacje'] = []
        request.session['mcs51'] = '--model-small'
        request.session['z80']= '--asm=z80asm'
        request.session['stm8'] = '--opt-code-size'
        response = compile(request, self.file.id)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, JsonResponse)

    def test_compile_view(self):
        url = reverse('coding:compile', args=[self.file.id])
        request = self.factory.post(url)
        request.user = self.user
        middleware = SessionMiddleware(lambda request: None)
        middleware.process_request(request) 
        request.session.save()
        request.session['standard']= 'C11'
        request.session['procesor']='MCS51'
        request.session['optymalizacje'] = []
        request.session['mcs51'] = '--model-small'
        request.session['z80']= '--asm=z80asm'
        request.session['stm8'] = '--opt-code-size'
        response = compile(request, self.file.id)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, JsonResponse)

    def test_download(self):
        file_id = 3
        file = File.objects.create(pk=file_id, name="example.c")  # Create a File object
        url = reverse('coding:download', args=[file_id])
        request = self.factory.get(url)
        response = download(request, file_id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get('Content-Type'), 'application/octet-stream')
        self.assertEqual(response.get('Content-Disposition'), 'attachment; filename="example.asm"')

    def test_standard(self):
        url = reverse('coding:standard')
        data = {'standard': 'C11'}
        request = self.factory.post(url, json.dumps(data), content_type='application/json')
        middleware = SessionMiddleware(lambda request: None)
        middleware.process_request(request)
        request.session.save()
        response = standard(request)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, JsonResponse)

    def test_optymalizacje(self):
        url = reverse('coding:optymalizacje')
        data = {'optymalizacje': ['--noinvariant', '--noinduction']}
        request = self.factory.post(url, json.dumps(data), content_type='application/json')
        middleware = SessionMiddleware(lambda request: None)
        middleware.process_request(request)
        request.session.save()
        request.session['optymalizacje'] = []
        response = optymalizacje(request)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, JsonResponse)

    def test_procesor(self):
        url = reverse('coding:procesor')
        data = {'procesor': 'mcs51'}
        request = self.factory.post(url, json.dumps(data), content_type='application/json')
        middleware = SessionMiddleware(lambda request: None)
        middleware.process_request(request)
        request.session.save()
        response = procesor(request)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, JsonResponse)

    def test_zalezne(self):
        url = reverse('coding:zalezne')
        data = {'procesor': 'mcs51', 'opcje': '--model-small'}
        request = self.factory.post(url, json.dumps(data), content_type='application/json')
        middleware = SessionMiddleware(lambda request: None)
        middleware.process_request(request) 
        request.session.save() 
        response = zalezne(request)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, JsonResponse)

    def test_asm_split(self):
        # Test case 1: No sections
        content = "This is a test.\nNo sections in this content."
        expected_output = "This is a test.\nNo sections in this content.\n"
        assert asm_split(content) == expected_output
    
        # Test case 2: Single section
        content = ";--------------------------------------------------------\nHeader1\n;--------------------------------------------------------\nSection 1\n"
        expected_output = "<pre class='asm_section'>\n<pre class='asm_section_header' id='asm_header_0'>\n;--------------------------------------------------------\nHeader1\n;--------------------------------------------------------\n</pre><pre class='asm_section_content show' id='asm_content_0'>\nSection 1\n</pre></pre>\n"
        self.assertEqual(asm_split(content), expected_output)
    
        # Test case 3: Multiple sections
        content = ";--------------------------------------------------------\nHeader1\n;--------------------------------------------------------\nSection 1\n"
        content += ";--------------------------------------------------------\nHeader2\n;--------------------------------------------------------\nSection 2\n"
        expected_output = "<pre class='asm_section'>\n<pre class='asm_section_header' id='asm_header_0'>\n;--------------------------------------------------------\nHeader1\n;--------------------------------------------------------\n</pre><pre class='asm_section_content show' id='asm_content_0'>\nSection 1\n</pre></pre>"
        expected_output += "<pre class='asm_section'>\n<pre class='asm_section_header' id='asm_header_1'>\n;--------------------------------------------------------\nHeader2\n;--------------------------------------------------------\n</pre><pre class='asm_section_content show' id='asm_content_1'>\nSection 2\n</pre></pre>\n"
        self.assertEqual(asm_split(content),expected_output)
    
        # Test case 4: Empty content
        content = ""
        expected_output = ""
        self.assertEqual(asm_split(content), expected_output)
    
        # Test case 5: Content with only section headers
        content = ";--------------------------------------------------------\nHeader1\n;--------------------------------------------------------\n;--------------------------------------------------------\nHeader2\n;--------------------------------------------------------\n"
        expected_output = "<pre class='asm_section'>\n<pre class='asm_section_header' id='asm_header_0'>\n;--------------------------------------------------------\nHeader1\n;--------------------------------------------------------\n</pre><pre class='asm_section_content show' id='asm_content_0'>\n</pre></pre>"
        expected_output += "<pre class='asm_section'>\n<pre class='asm_section_header' id='asm_header_1'>\n;--------------------------------------------------------\nHeader2\n;--------------------------------------------------------\n</pre><pre class='asm_section_content show' id='asm_content_1'>\n</pre></pre>\n"
        self.assertEqual(asm_split(content),expected_output)

    def test_line_type(self):
        # Test case 1: Line with '__asm'
        line = "Some code __asm more code"
        self.assertEqual(line_type(line).name, "wstawka asemblerowa")

        # Test case 2: Line starting with '/*'
        line = "/* This is a comment"
        self.assertEqual(line_type(line).name , "komentarz")

        # Test case 3: Line starting with '#'
        line = "#pragma once"
        self.assertEqual(line_type(line).name, "dyrektywy")

        # Test case 4: Line with variable declaration
        line = "int x = 10;"
        self.assertEqual(line_type(line).name,"deklaracja zmiennych")

        # Test case 5: Line with no specific pattern
        line = "Some code"
        self.assertEqual(line_type(line).name,"procedury")

    def test_divide_into_sections(self):
        # Test case 1: No sections in the file
        content = "This is a test.\nNo sections in this file."
        file = File(content=content, name="test_file")
        file.save()
        divide_into_sections(file)
        file_sections = File_section.objects.filter(file=file)
        self.assertEqual(len(file_sections),1)
        self.assertEqual(file_sections[0].begin,1)
        self.assertEqual(file_sections[0].end,2)
        self.assertEqual(file_sections[0].type.name,"procedury")
        self.assertEqual(file_sections[0].content,"This is a test.\nNo sections in this file.\n")

        # Test case 2: Multiple sections in the file
        content = "int x = 10;\n/* Comment 1 */\nvoid foo() {\n/* Comment 2 */\n}\n/* Comment 3\n Comment 3 */\n  __asm\n  {\n    nop\n  }\n __endasm;\n void bar() {\n   \n}\n"
        file = File(content=content, name="test_file")
        file.save()
        divide_into_sections(file)
        file_sections = File_section.objects.filter(file=file)
        self.assertEqual(len(file_sections),8)

        self.assertEqual(file_sections[0].begin,1)
        self.assertEqual(file_sections[0].end,1)
        self.assertEqual(file_sections[0].type.name,"deklaracja zmiennych")
        self.assertEqual(file_sections[0].content,"int x = 10;\n")

        self.assertEqual(file_sections[1].begin,2)
        self.assertEqual(file_sections[1].end,2)
        self.assertEqual(file_sections[1].type.name,"komentarz")
        self.assertEqual(file_sections[1].content,"/* Comment 1 */\n")

        self.assertEqual(file_sections[2].begin, 3)
        self.assertEqual(file_sections[2].end, 3)
        self.assertEqual(file_sections[2].type.name,"procedury")
        self.assertEqual(file_sections[2].content,"void foo() {\n")

        self.assertEqual(file_sections[3].begin,4)
        self.assertEqual(file_sections[3].end, 4)
        self.assertEqual(file_sections[3].type.name,"komentarz")
        self.assertEqual(file_sections[3].content,"/* Comment 2 */\n")

        self.assertEqual(file_sections[4].begin,5)
        self.assertEqual(file_sections[4].end, 5)
        self.assertEqual(file_sections[4].type.name,"procedury")
        self.assertEqual(file_sections[4].content,"}\n")

        self.assertEqual(file_sections[5].begin, 6)
        self.assertEqual(file_sections[5].end,7)
        self.assertEqual(file_sections[5].type.name,"komentarz")
        self.assertEqual(file_sections[5].content,"/* Comment 3\n Comment 3 */\n")

        self.assertEqual(file_sections[6].begin,8)
        self.assertEqual(file_sections[6].end,12)
        self.assertEqual(file_sections[6].type.name,"wstawka asemblerowa")
        self.assertEqual(file_sections[6].content,"  __asm\n  {\n    nop\n  }\n __endasm;\n")

        self.assertEqual(file_sections[7].begin, 13)
        self.assertEqual(file_sections[7].end,15)
        self.assertEqual(file_sections[7].type.name, "procedury")
        self.assertEqual(file_sections[7].content," void bar() {\n\n}\n")

        


