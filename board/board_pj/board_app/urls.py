from django.urls import path
from .views import *

urlpatterns = [
   path('', NoticeList.as_view()),
   path('my/', MyNoticeList.as_view()),
   path('<int:pk>', NoticeDetail.as_view()),
   path('create/', NoticeCreate.as_view(), name='notice_create'),
   path('update/<int:pk>', NoticeUpdate.as_view(), name='notice_update'),
   path('feedbacks/feedback/<int:pk>', FeedbackDetail.as_view()),
   path('feedback/create', FeedbackCreate.as_view(), name='feedback_create'),
   path('feedbacks/feedback/<int:pk>/delete', FeedbackDelete.as_view(), name='feedback_delete'),
   path('feedbacks/', FeedbackList.as_view(), name='my_notice_feedbacks'),
   path('feedback/accept/<int:pk>', accept_feedback, name='accept_feedback'),
]
