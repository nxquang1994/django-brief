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

    # def __init__(self, id, category, title, link, published_date, created_at, deleted_flag, updated_at):
    #     self.category = category
    #     self.title = title
    #     self.linl = link
    #     self.published_date = published_date

    
    @classmethod
    def from_all_prop(cls, data):
        return cls(
            # category=data['category'],
            # title=data['title'],
            # link=data['link'],
            # published_date=data['published_date']
        )

