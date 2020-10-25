class IpV4Converter:
    regex = r'(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)'

    def to_python(self, value):
        return str(value)

    def to_url(self, value):
        return '%s' % value
