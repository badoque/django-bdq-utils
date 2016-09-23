from rest_framework import generics, mixins

class CustomReturnSerializerGenericAPIView(generics.GenericAPIView):

    def get_return_serializer(self, *args, **kwargs):
        """
        Return the serializer instance that should be used for validating and
        deserializing input, and for serializing output.
        """
        serializer_class = self.get_return_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)

    def get_return_serializer_class(self):
        """
        Return the class to use for the serializer.
        Defaults to using `self.serializer_class`.

        You may want to override this if you need to provide different
        serializations depending on the incoming request.

        (Eg. admins get full serialization, others get basic serialization)
        """
        return self.return_serializer_class


class CustomReturnSerializerUpdateModelMixin(mixins.UpdateModelMixin):

    def update(self, request, *args, **kwargs):
        original_response = super(CustomReturnSerializerUpdateModelMixin, self).update(request, *args, **kwargs)

        instance = self.get_object()
        return_serializer = self.get_return_serializer(instance)
        
        if (return_serializer != None):
            return Response(return_serializer.data)
        else:
            return original_response

    def perform_update(self, serializer):
        return serializer.save()
