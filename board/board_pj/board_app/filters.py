from django_filters import FilterSet, ModelChoiceFilter
from .models import *

class NoticeFilter(FilterSet):
    class Meta:
        model = Feedback
        fields = [
            'notice_fb',
        ]
    def __init__(self,*args, **kwargs):
        super(NoticeFilter, self).__init__(*args, **kwargs)
        self.filters['notice_fb'].queryset = Notice.objects.filter(author_nc_id=kwargs['request'])
