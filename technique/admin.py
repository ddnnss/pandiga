from django.contrib import admin
from .models import *

class SectionInline(admin.TabularInline):
    model = TechniqueSection
    extra = 0

class TechniqueTypeAdmin(admin.ModelAdmin):
    list_display = ['name']
    inlines = [SectionInline]
    class Meta:
        model = TechniqueType


class SubSectionInline(admin.TabularInline):
    model = TechniqueSubSection
    extra = 0

class TechniqueSectionAdmin(admin.ModelAdmin):
    list_display = ['name']
    inlines = [SubSectionInline]
    class Meta:
        model = TechniqueSection

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

admin.site.register(TechniqueType,TechniqueTypeAdmin)
admin.site.register(TechniqueSection,TechniqueSectionAdmin)
admin.site.register(TechniqueSubSection)
admin.site.register(TechniqueItem,TechniqueItemAdmin)

