
### An example of functionality


class NotificationViewSet(SerializerClassMapperViewSetMixin, ...., ....):
    """ViewSet for model Notification"""

    serializer_class_mapper = {
        'list': NotificationListSerializer,
        'read': NotificationReadSerializer,
    }

    @action(methods=['POST'], detail=False)
    def read(self, request, *args, **kwargs):


class GalleryListCreateView(SerializerClassMapperAPIViewMixin, ...., ....):


    serializer_class_mapper = {
        'get': serializers.GalleryRetrieveSerializer,
        'post': serializers.GalleryCreateSerializer,
    }