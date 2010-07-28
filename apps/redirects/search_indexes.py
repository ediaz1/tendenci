from haystack import indexes
from haystack import site
from redirects.models import Redirect

class RedirectIndex(indexes.RealTimeSearchIndex):
    text = indexes.CharField(document=True, use_template=True)
    
    from_url = indexes.CharField(model_attr='from_url')
    to_url = indexes.CharField(model_attr='to_url')
    http_status = indexes.IntegerField(model_attr='http_status')
    status =  indexes.IntegerField(model_attr='status')
    uses_regex = indexes.BooleanField(model_attr='uses_regex')
    create_dt = indexes.DateTimeField(model_attr='create_dt')
    update_dt = indexes.DateTimeField(model_attr='update_dt')

site.register(Redirect, RedirectIndex)