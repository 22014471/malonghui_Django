from rest_framework import serializers

from activity.models import Activity


class ActivitySerializer(serializers.ModelSerializer):
    """
    活动首页序列化器
    """

    class Meta:
        model = Activity
        fields = ('id', 'act_name', 'cover', 'start_time', 'city', 'status')


class ActivityDetailSerializer(serializers.ModelSerializer):
    """
    活动详细序列化器
    """

    class Meta:
        model = Activity
        fields = ('id', 'act_name', 'cover', 'start_time', 'start_end', 'act_address', 'sponsor', 'introduce', 'detail', 'deadline', 'status', 'web_sit')