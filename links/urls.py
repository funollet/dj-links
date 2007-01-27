from django.conf.urls.defaults import *
from links.models import Link

link_dict = { 'queryset': Link.public_categorized.all() }
#link_dict_permalink = dict(link_dict, slug_field='permalink')
#categ_dict = {'queryset': LinkCategory.objects.all() }
#categ_dict_slug = dict(categ_dict, slug_field='permalink')

urlpatterns = patterns('django.views.generic.list_detail',
    (r'^$', 'object_list', link_dict),
    #(r'^(?P<slug>[\-\w]+)/$', 'object_detail', categ_dict_slug),
    #(r'^[\w-]+/(?P<slug>[\-\w]+)/$', 'object_detail', link_dict_slug),
)

