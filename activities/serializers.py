from dataclasses import fields
from rest_framework import serializers

from activities.models import ActivityItem, ActivityList


class ActivityListSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField()
    status = serializers.ReadOnlyField()
    item_count = serializers.ReadOnlyField()

    class Meta:
        model = ActivityList
        fields = '__all__'

    def to_representation(self, instance):
        representation = super(ActivityListSerializer, self).to_representation(instance)
        representation['date_created'] = instance.date_created.astimezone().strftime("%Y-%m-%d %H:%M")
        return representation


class ActivityItemSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField()

    class Meta:
        model = ActivityItem
        fields = '__all__'

    def to_representation(self, instance):
        representation = super(ActivityItemSerializer, self).to_representation(instance)
        representation['status'] = instance.get_status_display()
        return representation

    def _validate_user(self, validated_data):
        auth_user = self.context['request'].user
        list_id = validated_data.get('list_id')
        activity_list = ActivityList.objects.get(pk=list_id.id)
        if activity_list.owner != auth_user:
            raise serializers.ValidationError('No se encontro una lista', code='authorization')
        
    def create(self, validated_data):
        self._validate_user(validated_data)
        return ActivityItem.objects.create(**validated_data)

    def update(self, instance, validated_data):
        list_id = validated_data.get('list_id', None)
        if list_id:
            self._validate_user(validated_data)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class ActivityListDetailSerializer(serializers.ModelSerializer):
    items = ActivityItemSerializer(many=True, read_only=True)
    status = serializers.ReadOnlyField()
    item_count = serializers.ReadOnlyField()

    class Meta:
        model = ActivityList
        fields = ['id', 'name', 'status', 'item_count', 'items']
