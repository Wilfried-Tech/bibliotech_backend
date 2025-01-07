from rest_framework import viewsets


class MultipleSerializerMixin(viewsets.ViewSetMixin):
    serializer_class = None
    detail_serializer_class = None

    def get_serializer_class(self):
        if self.action == 'retrieve' or self.action == 'update' or self.action == 'partial_update':
            return self.detail_serializer_class
        return self.serializer_class
