from rest_framework import serializers
from appForNlp.models import Comment, Analysis


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'comment_text', 'person_id', 'comment_day', 'comment_month', 'comment_year']

class AnalysisSerializer(serializers.ModelSerializer):
    person_id = serializers.CharField(source='comment.person_id')
    comment_text = serializers.CharField(source='comment.comment_text')
    day = serializers.CharField(source='comment.comment_day')
    month = serializers.CharField(source='comment.comment_month')
    year = serializers.CharField(source='comment.comment_year')
    class Meta:
        model = Analysis
        fields = ['id', 'comment_absa_result', 'comment_sa_result', 'person_id', 'comment_text', 'day', 'month', 'year']