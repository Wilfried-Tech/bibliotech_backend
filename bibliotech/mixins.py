from rest_framework import viewsets


class MultipleSerializerMixin(viewsets.ViewSetMixin):
    serializer_class = None
    detail_serializer_class = None

    def get_serializer_class(self):
        if self.action != 'list' and self.detail_serializer_class:
            return self.detail_serializer_class
        return self.serializer_class
