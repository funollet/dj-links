from django.db import models
from misc.markup import markup_help, parse_markup
from tags.models import Tag
from tags import fields
from datetime import datetime


STATUS_CHOICES = (
    ('drf', _('draft')),
    ('rvs', _('revision')),
    ('pbl', _('public')),
    ('hid', _('hidden')),
    )

class LinkCategory (models.Model):

    name = models.CharField (_('name'), maxlength=200, )
    
    description= models.TextField (_('description'), editable=False,)
    description_markup = models.TextField (_('description'), 
        blank=True,
        help_text = markup_help['docutils'],
    )
    
    priority = models.PositiveIntegerField (_('priority'),
        unique = True,
        help_text = _('Categories will be sorted by this field.')
    )
    
    easyname = models.SlugField (_('easyname'),
        unique=True,
        prepopulate_from=('name',),
        help_text = _('Easy-to-link name (good, if short, twice good).'),
    )
    
    pub_date = models.DateTimeField (_('publication date'), default=datetime.now,)
    modif_date = models.DateTimeField (_('modification date'), auto_now=True,)
    crea_date = models.DateTimeField (_('creation date'), auto_now_add=True,)

    icon = models.ImageField (_('icon'),
        upload_to = 'events/category',
        blank = True,
        height_field = 'icon_height', width_field = 'icon_width',
        help_text = _('Optional icon for the category.'),
    )
    # bug#1537  : height and width aren't refreshed on re-save
    icon_height = models.IntegerField(_('icon height'), blank = True, null=True,)
    icon_width = models.IntegerField(_('icon width'), blank = True, null=True, )

    hidden = models.BooleanField(_('hidden category'), default=False,
        help_text = 'Exclude this category from listings.',
    )

    class Meta:
        verbose_name = _('link category')
        verbose_name_plural = _('link categories')
        ordering = ['priority']
    class Admin:
        fields = (
            (None, {'fields': ('name', 'description_markup', 'priority',),}),
            (_('Advanced'), {
                'fields': ('easyname', 'pub_date', 'icon', 'hidden'), 
                'classes': 'collapse',
            } ),
        )
        list_display = ('name', 'priority',)

    
    def __str__ (self):
        return self.name

    def save (self):
        parse_markup (self)
        super(LinkCategory, self).save()

    #def get_absolute_url (self):
        #pass
    
    


class PublicManager (models.Manager):
    def get_query_set (self):
        return super(PublicManager, self).get_query_set().filter(status='pbl')

class CategorizedManager (models.Manager):
    def get_query_set (self):
        return super(CategorizedManager, self).get_query_set().order_by('category', 'pub_date',)

class PublicCategorizedManager (models.Manager):
    def get_query_set (self):
        return super(PublicCategorizedManager,
            self).get_query_set().filter(status='pbl').order_by('category', 'pub_date',)



class Link (models.Model):
    """Link (url, name, description) with metadata: category, tags, and source."""
    name = models.CharField (_('name'), maxlength=200, )
    url = models.URLField (_('url'), verify_exists=False)

    description = models.TextField (_('description'), editable=False,)
    description_markup = models.TextField (_('description'), 
        blank=True,
        help_text = markup_help['docutils']
    )

    status = models.CharField (_('status'), maxlength=3, 
        choices=STATUS_CHOICES,
        default='pbl',
        radio_admin=True,
        )
    
    category = models.ForeignKey ( LinkCategory,
        verbose_name=_('category'),
        blank = True,
    )
    
    via_name = models.CharField ( _('via (name)'), 
        maxlength=200, 
        blank=True,
        help_text = 'Source of the link. Brief description.',
    )
    via_url = models.URLField (_('via (url)'), verify_exists=False,
        blank=True,
        help_text = 'Source of the link. URL.'
    )
    
    pub_date = models.DateTimeField (_('publication date'), default=datetime.now,)
    modif_date = models.DateTimeField (_('modification date'), auto_now=True,)
    crea_date = models.DateTimeField (_('creation date'), auto_now_add=True,)
    easyname = models.SlugField (_('easyname'),
        prepopulate_from = ('name',),
        unique = True,
    )
    tags = fields.TagsField(Tag, blank = True, )

    objects = models.Manager()
    public = PublicManager()
    categorized = CategorizedManager()
    public_categorized = PublicCategorizedManager()

    class Meta:
        verbose_name = _('link')
        verbose_name_plural = _('links')
        order_with_respect_to = 'category'
        ordering = ['pub_date']

    class Admin:
        list_display = ('name', 'url', 'pub_date',)
        list_filter = ('status', 'category',)
        search_fields = ('name',)
        fields = (
            (None, {'fields': ( ('name', 'url'), ('status', 'category',), 
                'description_markup', 'tags',),}),
            (_('Via'), {'fields': ('via_name','via_url',),
                    'classes': 'collapse',}),
            (_('Advanced'), {'fields': ('easyname','pub_date',),
                    'classes': 'collapse',}),
        )

    def __str__ (self):
        return self.name

    def save (self):
        parse_markup (self)
        super(Link, self).save()

    #def get_absolute_url (self):
        #pass

