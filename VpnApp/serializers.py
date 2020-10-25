from rest_framework import serializers
from VpnApp.models import VpnServer, VpnInstance, VpnConfig


class VpnServerConfigSerializer(serializers.ModelSerializer):

    class Meta:
        model = VpnConfig
        fields = [
            'client',
            'dev',
            'proto',
            'remote',
            'remote_random',
            'resolv_retry',
            'nobind',
            'user',
            'group',
            'persist_key',
            'persist_tun',
            'remote_cert_tls',
            'cipher',
            'auth',
            'comp_lzo',
            'verb',
            'auth_user_pass',
            'key_direction',
            'ca',
            'cert',
            'key',
            'tls_auth'
        ]


class VpnInstanceListSerializer(serializers.ModelSerializer):

    class Meta:
        model = VpnInstance
        fields = ['port', 'protocol', 'auth']


class VpnInstanceDetailSerializer(serializers.ModelSerializer):
    config = VpnServerConfigSerializer(read_only=True)

    class Meta:
        model = VpnInstance
        fields = ['port', 'protocol', 'auth', 'config']


class VpnServerListSerializer(serializers.ModelSerializer):
    class Meta:
        model = VpnServer
        fields = ['ip', 'country', 'city', 'free']


class VpnServerDetailSerializer(serializers.ModelSerializer):
    instances = VpnInstanceListSerializer(many=True, read_only=True)

    class Meta:
        model = VpnServer
        fields = ['ip', 'country', 'instances']


