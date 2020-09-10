from apis.models import RssFeedItem

class RssQuery():
    @staticmethod
    def create_new_rss(data):
        try:
            new_item = RssFeedItem.from_all_prop(data)
            new_item.category = data['category']
            new_item.title = data['title']
            new_item.link = data['link']
            new_item.published_date = data['published_date']
            new_item.save()
            return True, new_item.id
        except NameError:
            return False, NameError
    
    @staticmethod
    def edit_rss_item(item_id, data):
        try:
            item = RssFeedItem.objects.get(pk=item_id)
            item.category = data['category']
            item.title = data['title']
            item.link = data['link']
            item.published_date = data['published_date']
            item.save()
            return True
        except NameError:
            return False
