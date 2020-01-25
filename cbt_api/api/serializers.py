from rest_framework import serializers
from .models import Examiner_score


class ScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Examiner_score
        exclude = ["datetime_created"]
