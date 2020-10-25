from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from django.urls import path
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework import viewsets, permissions
from VpnApp.models import VpnServer, VpnInstance, VpnConfig
from VpnApp.serializers import (VpnServerListSerializer,
                                VpnServerDetailSerializer,
                                VpnInstanceListSerializer,
                                VpnInstanceDetailSerializer,
                                VpnServerConfigSerializer)


class ApiRoot(APIView):
    """
    List all urls.
    """

    def get(self, request):
        urls = [
            'servers/',
            'servers/<ip>/',
            'servers/<ip>/instances',
            'servers/<ip>/instances/<port>',
            'servers/<ip>/instances/<port>/config'
        ]
        return Response(urls)


class VpnServerListViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions for VpnServer.
    But used only for list action.
    """
    queryset = VpnServer.objects.all()
    serializer_class = VpnServerListSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class VpnServerDetailViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions for VpnServer.
    But used for all actions except list.
    """
    queryset = VpnServer.objects.all()
    serializer_class = VpnServerDetailSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class VpnInstanceListViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions for VpnInstance.
    But used only for list action.
    """
    serializer_class = VpnInstanceListSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        server = self.kwargs['server']
        return VpnInstance.objects.filter(server=server)

    def perform_create(self, serializer):
        server = self.kwargs['server']
        try:
            VpnInstance.objects.get(server=server, port=serializer.validated_data['port'])
            instance_exists = True
        except VpnInstance.DoesNotExist as e:
            instance_exists = False

        if not instance_exists:
            serializer.save(server_id=server)
        else:
            raise ValidationError({"error": "Instance port already defined."
                                            " Cannot create new one on same port"})


class VpnInstanceDetailViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions for VpnInstance.
    But used for all actions except list.
    """
    serializer_class = VpnInstanceDetailSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'port'

    def get_queryset(self):
        server = self.kwargs['server']
        return VpnInstance.objects.filter(server=server)


class VpnConfigViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions for VpnConfig.
    Authenticated users only
    """
    serializer_class = VpnServerConfigSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_vpn_server_instance(self):
        server = self.kwargs['server']
        port = self.kwargs['port']
        try:
            instance = VpnInstance.objects.get(server=server, port=port)
        except VpnInstance.DoesNotExist as e:
            raise NotFound({"error": "Instance Not Found"})
        return instance

    def get_queryset(self):
        try:
            query = VpnConfig.objects.get(instance=self.get_vpn_server_instance())
        except NotFound as e:
            raise e
        except VpnConfig.DoesNotExist as e:
            raise NotFound({"error": "Seems like config not defined yet"})

        return query

    def get_object(self):
        """
        Returns the object the view is displaying.
        Overridden.
        """
        obj = self.get_queryset()
        print(repr(obj))
        self.check_object_permissions(self.request, obj)
        return obj

    def perform_create(self, serializer):
        try:
            self.get_object()
            config_exists = True
        except NotFound as e:
            config_exists = False

        if not config_exists:
            serializer.save(instance=self.get_vpn_server_instance())
        else:
            raise ValidationError({"error": "Config already defined. Cannot create new one"})


vpn_server_list = VpnServerListViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
vpn_server_detail = VpnServerDetailViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy'
})

vpn_instance_list = VpnInstanceListViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
vpn_instance_detail = VpnInstanceDetailViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy'
})

vpn_config = VpnConfigViewSet.as_view({
    'get': 'retrieve',
    'post': 'create',
    'put': 'update',
    'delete': 'destroy'
})
