from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.exceptions import NotFound
from .models import CustomUser
from .permissions import IsOwnerUserOrReadOnly
from .serializers import UserSerializer


class UserListCreateView(ListCreateAPIView):
	queryset = CustomUser.objects.all()
	serializer_class = UserSerializer
	# permission_classes = [IsAuthenticated]

	def perform_create(self, serializer):
		user = self.request.user
		serializer.save(user=user)


class UserDetailView(RetrieveUpdateDestroyAPIView, ListAPIView):
	queryset = CustomUser.objects.all()
	serializer_class = UserSerializer
	# permission_classes = [IsOwnerUserOrReadOnly, IsAuthenticated]
	# permission_classes = [IsAdminUser, IsOwnerUserOrReadOnly, IsAuthenticated]

	def get_queryset(self):
		pk = self.kwargs.get('pk', None)
		if not pk:
			raise NotFound(detail=None, code=None)
		return CustomUser.objects.filter(pk=pk)