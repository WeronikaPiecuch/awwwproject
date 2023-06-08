from django.shortcuts import render
from .models import Folder, File, File_section, Section_type
from django.http import HttpResponseRedirect, FileResponse
from django.urls import reverse
from django.utils import timezone
from .forms import *
from .sdcc_options import *
import re
import os
from django.http import JsonResponse
import json

def create_structure():
    folder_list = Folder.objects.filter(parent = None).filter(available=True)
    file_list = File.objects.filter(parent = None).filter(available=True)
    result = '<ul>'
    for folder in folder_list:
        result += folder.structure()
    for file in file_list:
        result += file.structure()
    result += '</ul>'
    return result

def line_type(line):
    match = re.fullmatch(".*__asm.*", line)
    if match != None :
        return Section_type.objects.get(name = "wstawka asemblerowa")
    match = re.fullmatch("\s*\/\*.*", line)
    if match != None :
        return Section_type.objects.get(name = "komentarz")
    match = re.fullmatch("\s*#.*", line)
    if match != None :
        return Section_type.objects.get(name = "dyrektywy")
    match = re.fullmatch("\s*(int|double|float|char).*\;", line)
    if match != None :
        return Section_type.objects.get(name = "deklaracja zmiennych")
    return Section_type.objects.get(name = "procedury")

def divide_into_sections(file):
    lines = file.content.splitlines()
    section_content = ""
    counter = 1
    section_type = None
    first_line = 1
    for line in lines :
        if section_type != None:
            if section_type.name == "komentarz" and re.fullmatch(".*\*\/\s*", line) == None:
                section_content += line + '\n'
                counter = counter + 1
                continue
            if section_type.name == "komentarz" and re.fullmatch(".*\*\/\s*", line) != None:
                section_content += line + '\n'
                counter = counter + 1
                new_section = File_section(begin = first_line, end = counter - 1, type = section_type,  file = file, content=section_content)
                new_section.name = 'File id: '+ str(file.id) + ' lines: '+str(first_line)+'-'+str(counter-1)
                new_section.save()
                section_type = None
                section_content = ""
                continue
            if section_type.name == "wstawka asemblerowa" and re.fullmatch(".*__endasm;.*", line) == None:
                section_content += line + '\n'
                counter = counter + 1
                continue
            if section_type.name == "wstawka asemblerowa" and re.fullmatch(".*__endasm;.*", line) != None:
                section_content += line + '\n'
                counter = counter + 1
                new_section = File_section(begin = first_line, end = counter - 1, type = section_type,  file = file, content=section_content)
                new_section.name = 'File id: '+ str(file.id) + ' lines: '+str(first_line)+'-'+str(counter-1)
                new_section.save()
                section_type = None
                section_content = ""
                continue
        if re.fullmatch("\s*", line) != None:
            counter = counter + 1
            section_content += '\n'
            continue
        actual_line_type = line_type(line)
        if actual_line_type.name == "komentarz" and re.fullmatch(".*\*\/\s*", line):
            if section_type != None :
                new_section = File_section(begin = first_line, end = counter - 1, type = section_type,  file = file, content=section_content)
                new_section.name = 'File id: '+ str(file.id) + ' lines: '+str(first_line)+'-'+str(counter-1)
                new_section.save()
            section_type = actual_line_type
            section_content = line + '\n'
            first_line = counter
            counter = counter + 1
            new_section = File_section(begin = first_line, end = counter - 1, type = section_type,  file = file, content=section_content)
            new_section.name = 'File id: '+ str(file.id) + ' lines: '+str(first_line)+'-'+str(counter-1)
            new_section.save()
            first_line = counter
            section_type = None
            section_content = ""
            continue
        if actual_line_type == section_type :
            section_content += line + '\n'
        else :
            if section_type != None :
                new_section = File_section(begin = first_line, end = counter - 1, type = section_type,  file = file, content=section_content)
                new_section.name = 'File id: '+ str(file.id) + ' lines: '+str(first_line)+'-'+str(counter-1)
                new_section.save()
            section_type = actual_line_type
            section_content = line + '\n'
            first_line = counter
        counter = counter + 1
    new_section = File_section(begin = first_line, end = counter - 1, type = section_type,  file = file, content=section_content)
    new_section.name = 'File id: '+ str(file.id) + ' lines: '+str(first_line)+'-'+str(counter-1)
    new_section.save()

def asm_split(content) :
    first_line = 1
    content = content.splitlines()
    compile = ""
    index = 0
    for line in content:
        if line == ";--------------------------------------------------------":
            if first_line:
                if compile != "":
                    compile += "</pre></pre>"
                    index += 1
                compile += "<pre class='asm_section'>\n"
                compile += "<pre class='asm_section_header' id='asm_header_"+str(index)+"'>\n"
                compile += line + '\n'
                first_line = 0
            else:
                compile += line + '\n'
                compile += "</pre><pre class='asm_section_content show' id='asm_content_"+str(index)+"'>\n"
                first_line = 1
        else:
            if (".c:" in line):
                id = line.split(':')[1]
                compile += "<pre class='asm_line' id='asm_line_"+id+"'>" + line + '\n' + "</pre>"
            else:
                compile += line + '\n'
    if "<pre" in compile:
        return compile + "</pre></pre>\n"
    else:
        return compile

def errors_split(errors, file_name):
    result = ""
    for error in errors:
        match = re.fullmatch(".*\.c:[0-9]*:.*", error)
        if match != None:
            line_str = error.split(':')[1]
            line = int(line_str)
            if result != "":
                result += "</pre>"
            result += "<pre class='error_section' id='error_"+line_str+"'>"
            result += file_name
            splits = error.split(':')
            for i in range(1, len(splits)):
                result += ':' + splits[i]
            result += '\n'
        else:
            result += error + "\n"
    if "<pre" in result:
        result += "</pre>\n"
    return result

def index(request):
    if request.user.is_authenticated == False:
        return HttpResponseRedirect(reverse("coding:login"))
    structure = create_structure()
    context = {
        'structure': structure,
        'standard_form': StandardForm(initial={'standard': request.session['standard']}),
        'optymalizacje_form': OptymalizacjeForm(initial={'optymalizacje': request.session['optymalizacje']}),
        'procesor_form': ProcesorForm(initial={'procesor': request.session['procesor']}),
        'z80_form': Z80Form(initial={'z80': request.session['z80']}),
        'stm8_form': STM8Form(initial={'stm8': request.session['stm8']}),
        'mcs51_form': MCS51Form(initial={'mcs51': request.session['mcs51']}),
        'file_form': FileUploadForm(),
        'folder_form': FolderUploadForm(),
        'section_form': SectionUploadForm(),
    }
    return render(request, "coding/index.html", context)

def file(request, file_id):
    file = File.objects.get(pk=file_id)
    context = {
        # 'content': file.write_sections(),
        'content': file.content,
    }
    return JsonResponse(context)

def save_file(request, file_id):
    data = json.loads(request.body)
    file = File.objects.get(pk=file_id)
    file.content = data['content']
    file.modification_date = timezone.now()
    file.save()
    # divide_into_sections(file)
    context = {}
    return JsonResponse(context)

def add_folder(request):
    data = json.loads(request.body)
    parent_id = data['parent_id']
    if parent_id == 0:
        parent_folder = None
    else:
        parent_folder = Folder.objects.get(pk=parent_id)
    if request.user.is_authenticated:
        current_user = request.user
    else:
        current_user = None
    name = data['name']
    new_folder = Folder(name=name, parent=parent_folder, user=current_user)
    new_folder.save()
    structure = create_structure()
    context = {
        'structure': structure,
        'folder_id': new_folder.id,
    }
    return JsonResponse(context)

def add_file(request):
    data = json.loads(request.body)
    parent_id = data['parent_id']
    if parent_id == 0:
        parent_folder = None
    else:
        parent_folder = Folder.objects.get(pk=parent_id)
    if request.user.is_authenticated:
        current_user = request.user
    else:
        current_user = None
    file = data['file']
    name = data['name']
    new_file = File(name=name, parent=parent_folder, content=file, user = current_user)
    new_file.save()
    # divide_into_sections(new_file)
    structure = create_structure()
    context = {
        'structure': structure,
        'file_id': new_file.id,
        'content': new_file.content,
        # 'file_content': new_file.write_sections(),
    }
    return JsonResponse(context)

def add_section(request, file_id):
    data = json.loads(request.body)
    first_line = data['first_line']
    last_line = data['last_line']
    name = data['name']
    type = data['type']
    error = 0
    file = File.objects.get(pk=file_id)
    if (File_section.objects.filter(file = file, begin__lt = first_line, end__lt=last_line, end__gte = first_line).count() > 0):
        error = 1
    if (File_section.objects.filter(file = file, begin__gt = first_line, end__gt=last_line, begin__lte=last_line).count() > 0):
        error = 1
    if (error == 0):
        section_types = Section_type.objects.filter(name=type)
        section_type = None
        if (len(section_types) == 0) :
            section_type = Section_type(name=type)
            section_type.save()
        else :
            section_type = section_types[0]
        lines = file.content.splitlines()
        content = ''
        for i in range(first_line - 1, last_line):
            content += lines[i] +'\n'

        parents = File_section.objects.filter(file = file, begin__lte = first_line, end__gte=last_line)
        new_section = File_section(name=name, type = section_type, begin = first_line, end = last_line, content = content, file = file)
        parent = None
        difference = len(lines)
        for item in parents:
            if difference > item.end - item.begin + 1:
                difference = item.end - item.begin + 1
                parent = item
        if (parent != None):
            new_section.parent = parent
        new_section.save()
        children = File_section.objects.filter(file = file, begin__gte = first_line, end__lte=last_line, parent = parent)
        for child in children:
            if child != new_section and (child.begin != first_line or child.end != last_line):
                child.parent = new_section
                child.save()
    content = file.write_sections()
    context = {
        'content': content,
        'error': error,
    }
    return JsonResponse(context)

def delete_folder(request, folder_id):
    folder = Folder.objects.get(pk=folder_id)
    delete_recursive(folder)
    structure = create_structure()
    context = {
        'structure': structure,
    }
    return JsonResponse(context)

def delete_recursive(folder):
    content_folder = Folder.objects.raw('''SELECT * FROM coding_folder WHERE parent_id = %s AND available = TRUE''', [folder.id]) 
    content_file = File.objects.raw('''SELECT * FROM coding_file WHERE parent_id = %s AND available = TRUE''', [folder.id])
    for item in content_folder:
        delete_recursive(item)
    for item in content_file:
        item.available = False
        item.available_date = timezone.now()
        item.save()
        if item.parent != None:
            parent = Folder.objects.get(pk=item.parent.id)
            parent.modification_date = timezone.now()
    folder.available = False
    folder.available_date = timezone.now()
    if folder.parent != None:
        parent = Folder.objects.get(pk=folder.parent.id)
        parent.modification_date = timezone.now()
    folder.save()

def delete_file(request, file_id):
    file = File.objects.get(pk=file_id)
    file.available = False
    file.available_date = timezone.now()
    file.save()
    if file.parent != None:
        parent = Folder.objects.get(pk=file.parent.id)
        parent.modification_date = timezone.now()
        parent.save()
    structure = create_structure()
    context = {
        'structure': structure,
    }
    return JsonResponse(context)

def delete_section(request, file_id, section_id):
    section = File_section.objects.get(pk=section_id)
    first_line = section.begin
    last_line = section.end
    section.delete()
    file = File.objects.get(pk=file_id)
    section_list = File_section.objects.filter(file=file).order_by('begin')
    if section_list != None:
        difference = last_line - first_line + 1
    for section in section_list:
        section.status_data = None
        if section.begin >= last_line and section.end <= last_line:
            section.delete()
            continue
        elif section.begin <= last_line and section.end >= last_line:
            lines = section.content.splitlines()
            section.content = ""
            i = section.begin
            for line in lines:
                if i < first_line:
                    section.content += line + '\n'
                elif i > last_line:
                    section.content += line + '\n'
                i += 1
            section.end -= difference
            section.save()
        elif section.begin > last_line:
            section.begin -= difference
            section.end -= difference
            section.save()
        match = re.fullmatch("File id: [0-9]* lines: [0-9]*-[0-9]*", section.name)
        if match != None:
            section.name = 'File id: '+ str(file.id) + ' lines: '+str(section.begin)+'-'+str(section.end)
        section.save()
    lines = file.content.splitlines()
    content = ""
    i = 1
    for line in lines:
        if i < first_line:
            content += line + '\n'
        elif i > last_line:
            content += line + '\n'
        i += 1
    file.content = content
    file.modification_date = timezone.now()
    file.save()
    context = {
        'content': file.write_sections(),
    }
    return JsonResponse(context)

def compile(request, file_id):
    file = File.objects.get(pk=file_id)
    args = []
    standard = STANDARD.get(request.session['standard'])
    args.append(standard)
    for opt in request.session['optymalizacje']:
        args.append(opt)
    procesor = PROCESOR.get(request.session['procesor'])
    if procesor != '':
        args.append(procesor)
    if procesor == 'Z80':
        args.append(request.session['z80'])
    elif procesor == 'STM8':
        args.append(request.session['stm8'])
    else:
        args.append(request.session['mcs51'])
    errors = file.compile(args)
    if errors == []:
        f = open(str(file_id)+".asm", "r")
        content_compile = f.read()
        f.close()
        os.remove(str(file_id)+".asm")
        f = open("current.asm", "w+")
        f.write(content_compile)
        f.close()
        compile = asm_split(content_compile)
        compiled = 1
    else:
        compiled = 0
        compile = errors_split(errors, file.name)
    context = {
        'compile': compile,
        # 'content': file.write_sections(),
        'compiled': compiled,
    }
    return JsonResponse(context)

def download(request, file_id):
    name = File.objects.get(pk=file_id).name
    if re.fullmatch(".+\.c", name) != None:
        name = name.replace(".c","")
    name += '.asm'
    return FileResponse(open("current.asm", "rb"),as_attachment=True,filename=name)

def standard(request):
    data = json.loads(request.body)
    request.session['standard'] = data['standard']
    request.session.save()
    context = {
        'standard': request.session['standard'],
    }
    return JsonResponse(context)

def optymalizacje(request):
    request.session['optymalizacje'].clear()
    data = json.loads(request.body)
    for id in data['optymalizacje']:
        request.session['optymalizacje'].append(id)
    request.session.save()
    context = {
        'optymalizacje': request.session['optymalizacje'],
    }
    return JsonResponse(context)

def procesor(request):
    data = json.loads(request.body)
    request.session['procesor'] = data['procesor']
    request.session.save()
    context = {
        'procesor': request.session['procesor'],
    }
    return JsonResponse(context)

def zalezne(request):
    data = json.loads(request.body)
    request.session[data['procesor']] = data['opcje']
    request.session.save()
    context = {
        'opcje': request.session[data['procesor']],
    }
    return JsonResponse(context)