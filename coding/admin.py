from django.contrib import admin
from .models import Folder, File, File_section, Section_type, Section_status, Status_data, User

admin.site.register(Folder)
admin.site.register(File)
admin.site.register(File_section)
admin.site.register(Section_type)
admin.site.register(Section_status)
admin.site.register(Status_data)


# Register your models here.
