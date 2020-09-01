from django.db import models

# Create your models here.
class RssFeedItem(models.Model):
    category = models.CharField(max_length=50, null=True, blank=True)
    title = models.TextField()
    link = models.TextField(null=True, blank=True)
    published_date = models.DateTimeField(null=True, blank=True)
    deleted_flag = models.BooleanField(null=False, default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'rss_feed_items'

    def __str__(self):
        return self.title

    def delete(self):
        self.deleted_flag = True
        self.save()
