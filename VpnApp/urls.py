from django.urls import path, include, register_converter
from VpnApp.views import (vpn_server_list,
                          vpn_server_detail,
                          vpn_instance_list,
                          vpn_instance_detail,
                          vpn_config,
                          ApiRoot)
from VpnApp import converters


register_converter(converters.IpV4Converter, 'ip')
urlpatterns = [
    path('', ApiRoot.as_view(), name='api-root'),
    path('api-auth/', include('rest_framework.urls')),
    path('servers/', vpn_server_list, name='server-list'),
    path('servers/<ip:pk>/', vpn_server_detail, name='server-detail'),
    path('servers/<ip:server>/instances', vpn_instance_list, name='instance-list'),
    path('servers/<ip:server>/instances/<int:port>', vpn_instance_detail, name='instance-detail'),
    path('servers/<ip:server>/instances/<int:port>/config', vpn_config, name='instance-config'),
]