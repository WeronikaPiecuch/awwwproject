from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
import subprocess
import os, re
from django.db.models import Q


class Section_type(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Section_status(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Status_data(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class common(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=300, blank=True, default='')
    create_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None, blank = True, null=True)
    available = models.BooleanField(default=True)
    available_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True


class Folder(common):
    parent = models.ForeignKey('self', on_delete=models.CASCADE, default=None, blank=True, null=True)


    def structure(self):
        content_folder = Folder.objects.raw('''SELECT * FROM coding_folder WHERE parent_id = %s AND available = TRUE''', [self.id]) 
        content_file = (File.objects.raw('''SELECT * FROM coding_file WHERE parent_id = %s AND available = TRUE''', [self.id]))
        result = '<li class="folder"><button onClick="folder('+str(self.id)+')" id="folder_'+str(self.id)+'">' + self.name.replace('<', '&lt;').replace('>', '&gt;') + '</button>' 
        if content_folder or content_file:
            result += '<ul>'
            for element in content_folder:
                result += element.structure()
            for element in content_file:
                result += element.structure()
            result += '</ul>'
        result += '</li>'
        return result



class File(common):
    parent = models.ForeignKey(Folder, on_delete=models.CASCADE, default=None, blank=True, null=True)
    content = models.TextField(default='')

    def structure(self):
        return '<li class="file"><button onClick="file('+str(self.id)+')" id="file_'+str(self.id)+'">'  + self.name.replace('<', '&lt;').replace('>', '&gt;') + '</button></li>'
    
    def compile(self, args):
        file = open(str(self.id)+'.c', 'w+')
        file.write(self.content)
        file.close()
        command = ["sdcc", "-S"] + args
        p = subprocess.run(command + [f'{self.id}.c'], capture_output=True)
        errors = p.stderr.decode('utf-8').splitlines()
        sections = None
        section_list = File_section.objects.filter(file=self)
        for section in section_list:
            section.status = None
            section.status_data = None
            section.save()
        for error in errors:
            match = re.fullmatch(".*\.c:[0-9]*:.*", error)
            if match != None:
                line_str = error.split(':')[1]
                line = int(line_str)
                match = re.fullmatch("\s*fatal.*",error.split(':')[2])
                if match != None:
                    fatal = True
                else:
                    fatal = False
                sections = self.set_section_status(line, fatal, error)
        section_list = File_section.objects.filter(file=self)
        for section in section_list:
            if section.status == None:
                section.status = Section_status.objects.get(name = "kompiluje się bez ostrzeżeń")
                section.save()
        os.remove(str(self.id)+'.c')
        if errors != [] and os.path.isfile(str(self.id)+'.asm'):
            os.remove(str(self.id)+'.asm')
        return errors

    def set_section_status(self, number, fatal, error):
        section_list=File_section.objects.filter(file = self, begin__lte= number, end__gte= number)
        if fatal:
            section_status = Section_status.objects.get(name = "nie kompiluje się")
        else:
            section_status = Section_status.objects.get(name = "kompiluje się z ostrzeżeniami")
        splits = error.split(':')
        error = self.name + ':' + splits[1] + ':' + splits[2]
        for section in section_list:
            if section.status_data != None:
                section.status_data.name += '; ' + error + '\n'
            else:
                section.status_data = Status_data(name = error)
            section.status_data.save()
            if section.status == None or section.status.id > section_status.id:
                section.status = section_status
            section.save()
        return section_list
    
    def write_sections(self):
        border = '//----------------------------------------\n'
        result = ''
        section_list = File_section.objects.filter(file=self, parent = None).order_by('begin')
        file_lines = self.content.replace('<', '&lt;').replace('>', '&gt;').splitlines()
        for i in range(len(file_lines)):
            file_lines[i] = '    ' + file_lines[i]
        for section in section_list:
            result += section.write_content('', border, file_lines)
        return result





class File_section(models.Model):
    name = models.CharField(max_length=50, blank=True, default='')
    description = models.CharField(max_length=300, blank=True, default='')
    create_date = models.DateTimeField(auto_now_add=True)
    begin = models.IntegerField(default=0)
    end = models.IntegerField(default=0)
    type = models.ForeignKey(Section_type, on_delete=models.RESTRICT, blank=True, default=None, null=True)
    status = models.ForeignKey(Section_status, on_delete=models.RESTRICT ,blank=True, default=None, null=True)
    status_data = models.ForeignKey(Status_data, on_delete=models.CASCADE, blank=True, default=None, null=True)
    content = models.TextField(default='')
    file = models.ForeignKey(File, on_delete=models.CASCADE, blank=True, default=None, null=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, default=None, null=True)

    def __str__(self):
        return str(self.name)

    def write(self, tabs):
        result = tabs +'// Sekcja: ' + self.name + '\n'
        result += tabs + '// Rodzaj sekcji: ' + self.type.name + ', zakres: od ' + str(self.begin) + ' do ' + str(self.end) + ' linii'
        if self.status != None:
            result += '\n' + tabs + '// Status: ' + self.status.name
        if self.status_data != None:
            result += '\n' + tabs + '// Dane statusu: ' + self.status_data.name
        return result
    
    
    def write_content(self, tabs, border, file_lines):
        result = '<button id="section_'+str(self.id)+'" class="section_header">'+'<pre>' + self.write(tabs) + '</pre></button><br>'
        section_list = File_section.objects.filter(parent = self).order_by('begin')
        current_line = self.begin
        for section in section_list:
            for i in range(current_line, section.begin):
                result += '<pre class="line" id="line_'+ str(i) + '">'  + tabs  + file_lines[i-1] + '</pre>'
            result += section.write_content(tabs + '    ', border, file_lines)
            current_line = section.end + 1
        for i in range(current_line, self.end + 1):
            result += '<pre class="line" id="line_'+ str(i) + '">' + tabs + file_lines[i-1]+ '</pre>'
        return result
     
