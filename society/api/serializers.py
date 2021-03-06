from rest_framework import serializers

from society.models import Society, JoinSocietyRequest, SocietyTag
from student.models import Student

class SocietyTagSerializer(serializers.ModelSerializer):

    class Meta:
        model = SocietyTag
        fields = '__all__'

class SocietySerializer(serializers.ModelSerializer):
    assistant = serializers.StringRelatedField()
    tags = SocietyTagSerializer(many=True)

    class Meta:
        model = Society
        fields = '__all__'


class SocietyMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Society
        fields = (
            'id',
            'society_id',
            'name',
            'status',
            'type',
            'avatar'
        )


class JoinSocietyRequestSerializer(serializers.ModelSerializer):
    society_id = serializers.IntegerField()
    member_id = serializers.IntegerField()

    class Meta:
        model = JoinSocietyRequest
        fields = ('society_id', 'member_id')

    def create(self, validated_data):
        return JoinSocietyRequest.objects.create(
            society=Society.objects.get(id=validated_data['society_id']),
            member=Student.objects.get(id=validated_data['member_id'])
        )
