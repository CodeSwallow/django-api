from rest_framework.viewsets import ModelViewSet
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

from activities.models import ActivityList, ActivityItem
from activities.serializers import ActivityListSerializer, ActivityItemSerializer, ActivityListDetailSerializer


class ActivityListViewSet(ModelViewSet):
    queryset = ActivityList.objects.all()
    serializer_class = ActivityListSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(owner=user)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ActivityListDetailSerializer
        
        return self.serializer_class

    @action(detail=True, methods=['get'])
    def finish_list(self, request, pk=None):
        instance = self.get_object()
        items = ActivityItem.objects.filter(list_id=instance)
        for item in items:
            item.status = 'FI'
            item.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class ActivityItemViewSet(ModelViewSet):
    queryset = ActivityItem.objects.all()
    serializer_class = ActivityItemSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(owner=user)

    def get_queryset(self):
        filters = {'owner': self.request.user}
        list_id = self.request.query_params.get('list_id', None)
        if list_id is not None:
            filters['list_id_id'] = list_id
        return self.queryset.filter(**filters)

