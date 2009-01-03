from django.db import models

class PublicManager (models.Manager):
    def get_query_set (self):
        return super(PublicManager, self).get_query_set().filter(status='pbl')

class CategorizedManager (models.Manager):
    def get_query_set (self):
        return super(CategorizedManager, self
            ).get_query_set().order_by('category', 'pub_date',)

class PublicCategorizedManager (models.Manager):
    def get_query_set (self):
        return super(PublicCategorizedManager,
            self).get_query_set().filter(status='pbl'
                ).order_by('category', 'pub_date',)


