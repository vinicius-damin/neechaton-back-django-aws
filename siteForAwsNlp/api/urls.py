from django.urls import path
from .views import CommentList, CommentDetail, AnalysisList, AnalysisDetail

urlpatterns = [
    path('comment/<int:pk>/', CommentDetail.as_view()),
    path('comment/', CommentList.as_view()),
    path('analysis/<int:pk>/', AnalysisDetail.as_view()),
    path('analysis/', AnalysisList.as_view()),
]