import json
from PIL import Image

from rest_framework import serializers
from student.api.serializers import StudentMiniSerializer
from society.models import JoinSocietyRequest, ActivityRequest, Society
from society_manage.models import CreditDistribution
from society.constants import AVATAR_MAX_SIZE


class JoinSocietyRequestSerializer(serializers.ModelSerializer):
    member = StudentMiniSerializer()

    class Meta:
        model = JoinSocietyRequest
        fields = ('id', 'member', 'status')


class ReviewJoinSocietyRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = JoinSocietyRequest
        fields = ('status',)


class KickMemberSerializer(serializers.Serializer):
    member_id = serializers.IntegerField()

    class Meta:
        fields = ('member_id',)


class ActivityRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityRequest
        fields = '__all__'
        read_only_fields = ('status',)


class ActivityRequestMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityRequest
        fields = ('title', 'status', 'place', 'start_time')
        read_only_fields = ('status',)


class CreditDistributionSerializer(serializers.ModelSerializer):
    available_receivers = StudentMiniSerializer(many=True, source='get_available_receivers')
    receivers = serializers.SerializerMethodField()

    class Meta:
        model = CreditDistribution
        fields = ('credit', 'id', 'year', 'semester', 'receivers', 'available_receivers', 'open')

    def get_receivers(self, obj):
        return [receiver.id for receiver in obj.receivers.all()]


class SocietyProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Society
        fields = '__all__'
        read_only_fields = (
            'id',
            'user',
            'society_id',
            'type',
            'status',
            'avatar',
            'established_time',
            'password_changed',
            'assistant'
        )


class UploadAvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Society
        fields = ('id', 'avatar',)
        read_only_fields = ('id',)

    def validate(self, data):
        avatar = data['avatar']
        # sometimes frontend will send 'undefined'
        try:
            # crop is represented in percentage (%)
            crop = json.loads(self.context['request'].data.get('crop', None))
        except Exception as e:
            raise serializers.ValidationError("invalid crop object format")

        if avatar is None or avatar.size > AVATAR_MAX_SIZE:
            raise serializers.ValidationError("image file size too large")
        if crop is None:
            raise serializers.ValidationError("no crop object provided")

        try:
            image = Image.open(avatar)
            region = image.crop((
                crop['x'] * image.width / 100,
                crop['y'] * image.height / 100,
                (crop['x'] + crop['width']) * image.width / 100,
                (crop['y'] + crop['height']) * image.height / 100
            ))
            data['avatar'].seek(0, 0)
            region.save(data['avatar'])
        except Exception as e:
            raise serializers.ValidationError("cannot crop image")

        return data
