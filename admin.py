from django.utils.translation import ugettext as _
from links.models import Link, LinkCategory
from django.contrib import admin


class LinkCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'easyname': ('name',)}
    
    list_display = ('name', 'priority',)
    fieldsets = (
        (None, {'fields': ('name', 'description',),}),
        (_('Advanced'), {
            'fields': (('easyname', 'priority'), 'pub_date', 'icon', 'hidden'), 
            'classes': ('collapse',),
        } ),
    )
    
admin.site.register(LinkCategory, LinkCategoryAdmin)


class LinkAdmin(admin.ModelAdmin):
    pass
    prepopulated_fields = {'easyname': ('name',)}
    radio_fields = {"status": admin.HORIZONTAL}
    
    list_display = ('name', 'url', 'pub_date',)
    list_filter = ('status', 'category',)
    search_fields = ['name',]
    fieldsets = (
        (None, {'fields': ( ('name', 'url'), ('status', 'category',), 
            'description', 'tags',),}),
        (_('Via'), {'fields': ('via_name','via_url',),
                'classes': ('collapse',),}),
        (_('Advanced'), {'fields': ('easyname','pub_date',),
                'classes': ('collapse',),}),
    )

admin.site.register(Link, LinkAdmin)

