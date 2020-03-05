from django.contrib import admin
from .models import *


class ImagesInline (admin.TabularInline):
    model = TechniqueItemImage
    readonly_fields = ('image_tag', )
    exclude = ('image_small',)
    extra = 0

class DocsInline (admin.TabularInline):
    model = TechniqueItemDoc
    readonly_fields = ('image_tag', )
    exclude = ('image_small',)
    extra = 0

class TechniqueItemAdmin(admin.ModelAdmin):
    list_display = ['image_tag','name','rent_price']

    inlines = [ImagesInline,DocsInline]
    search_fields = ('name_lower',)
    list_filter = ('sub_section', 'is_free', 'is_moderated',)

    class Meta:
        model = TechniqueItem

admin.site.register(TechniqueType)
admin.site.register(TechniqueSection)
admin.site.register(TechniqueSubSection)
admin.site.register(TechniqueItem,TechniqueItemAdmin)

