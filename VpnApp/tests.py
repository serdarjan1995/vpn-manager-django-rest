from django.test import TestCase
from VpnApp.models import VpnServer, VpnInstance


IP_ADDR_IN_US = "103.192.45.92"
IP_ADDR_IN_DE = "75.23.178.11"


class VpnServerTestCase(TestCase):
    def setUp(self):
        server_in_us = VpnServer.objects.create(ip=IP_ADDR_IN_US, country="US")
        VpnInstance.objects.create(server=server_in_us, port=1194, auth=False)
        VpnInstance.objects.create(server=server_in_us, port=443, auth=True)

        server_in_de = VpnServer.objects.create(ip=IP_ADDR_IN_DE, country="DE")
        VpnInstance.objects.create(server=server_in_de, port=8888, auth=False)
        VpnInstance.objects.create(server=server_in_de, port=443, auth=False)
        VpnInstance.objects.create(server=server_in_de, port=5000, auth=True)

    def test_vpn_server_instances(self):
        """Vpn Servers with instances"""
        server_in_us = VpnServer.objects.get(ip=IP_ADDR_IN_US)
        print(server_in_us)
        self.assertEqual(server_in_us.__str__(), f'VpnServer {IP_ADDR_IN_US} in US')
        instances = VpnInstance.objects.filter(server=server_in_us)
        for instance in instances:
            print(instance)
            if instance.port == 1194 or instance.port == 443:
                self.assertEqual(instance.__str__(),  f'VpnInstance of server {IP_ADDR_IN_US} '
                                                      f'in running on port {instance.port}/{instance.protocol}')
            else:
                self.fail(f'VpnServer {IP_ADDR_IN_US} failed test')

        server_in_de = VpnServer.objects.get(ip=IP_ADDR_IN_DE)
        print(server_in_de)
        self.assertEqual(server_in_de.__str__(), f'VpnServer {IP_ADDR_IN_DE} in DE')
        instances = VpnInstance.objects.filter(server=server_in_de)
        for instance in instances:
            print(instance)
            if instance.port == 8888 or instance.port == 443 or instance.port == 5000:
                self.assertEqual(instance.__str__(), f'VpnInstance of server {IP_ADDR_IN_DE} '
                                                     f'in running on port {instance.port}/{instance.protocol}')
            else:
                self.fail(f'VpnServer {IP_ADDR_IN_DE} failed test')
