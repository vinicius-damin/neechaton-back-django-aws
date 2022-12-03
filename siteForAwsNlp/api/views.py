from django.shortcuts import render
from rest_framework import generics
from appForNlp.models import Comment, Analysis
from .serializers import CommentSerializer, AnalysisSerializer


class CommentList(generics.ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class CommentDetail(generics.RetrieveAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class AnalysisList(generics.ListAPIView):
    queryset = Analysis.objects.all()
    serializer_class = AnalysisSerializer
    
class AnalysisDetail(generics.RetrieveAPIView):
    queryset = Analysis.objects.all()
    serializer_class = AnalysisSerializer
