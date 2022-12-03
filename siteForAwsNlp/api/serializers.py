from rest_framework import serializers
from appForNlp.models import Comment, Analysis


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'comment_text', 'person_id']

class AnalysisSerializer(serializers.ModelSerializer):
    person_id = serializers.CharField(source='comment.person_id')
    comment_text = serializers.CharField(source='comment.comment_text')
    class Meta:
        model = Analysis
        fields = ['id', 'comment_absa_result', 'comment_sa_result', 'person_id', 'comment_text']