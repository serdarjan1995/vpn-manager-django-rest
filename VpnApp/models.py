from django.db import models

PROTOCOLS = [
    ('udp', 'udp'),
    ('tcp', 'tcp')
]


def config_default():
    return {}


class VpnServer(models.Model):
    ip = models.GenericIPAddressField(protocol='IPv4', primary_key=True)
    country = models.CharField(max_length=5)
    city = models.CharField(max_length=30, null=True, blank=True)
    free = models.BooleanField(default=True)

    class Meta:
        ordering = ['country']

    def __str__(self):
        return "VpnServer %s in %s" % (self.ip, self.country)


class VpnInstance(models.Model):
    server = models.ForeignKey(VpnServer, related_name='instances', on_delete=models.CASCADE)
    port = models.IntegerField(default=1194)
    protocol = models.CharField(choices=PROTOCOLS, default='udp', max_length=5)
    auth = models.BooleanField(default=False)

    class Meta:
        ordering = ['port']

    def __str__(self):
        return "VpnInstance of server %s in running on port %d/%s" % (self.server.ip, self.port, self.protocol)


class VpnConfig(models.Model):
    instance = models.OneToOneField(VpnInstance, related_name='config', on_delete=models.CASCADE)
    client = models.BooleanField(default=True)
    dev = models.CharField(choices=[('tun', 'tun'), ('tap', 'tap')], default='tun', max_length=5)
    proto = models.CharField(choices=PROTOCOLS, default='udp', max_length=5)
    remote = models.CharField(max_length=30)
    remote_random = models.BooleanField(default=True)
    resolv_retry = models.CharField(max_length=30, default="infinite")
    nobind = models.BooleanField(default=True)
    user = models.CharField(max_length=30, default="nobody")
    group = models.CharField(max_length=30, default="nogroup")
    persist_key = models.BooleanField(default=True)
    persist_tun = models.BooleanField(default=True)
    remote_cert_tls = models.CharField(max_length=30, default="server")
    cipher = models.CharField(max_length=30, default="AES-256-CBC")
    auth = models.CharField(max_length=30, default="SHA256")
    comp_lzo = models.BooleanField(default=True)
    verb = models.IntegerField(default=3)
    auth_user_pass = models.BooleanField(default=True)
    key_direction = models.IntegerField(default=1)
    ca = models.TextField(null=True, blank=True)
    cert = models.TextField(null=True, blank=True)
    key = models.TextField(null=True, blank=True)
    tls_auth = models.TextField(null=True, blank=True)

    def __str__(self):
        return "VpnConfig of server %s" % self.instance.server.ip
