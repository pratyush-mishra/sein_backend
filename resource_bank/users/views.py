from rest_framework import generics, permissions
from rest_framework.response import Response
from .models import Member
from .serializers import MemberSerializer

class UserDetail(generics.RetrieveUpdateAPIView):
    serializer_class = MemberSerializer

    def get_object(self):
        if self.kwargs['pk'] == 'me':
            return self.request.user
        return Member.objects.get(pk=self.kwargs['pk'])
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)