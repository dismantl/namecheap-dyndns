class Domain(object):
    '''store domain parameters'''
    def __init__(self, name, hosts, password, ip):
        self.name = name
        self.hosts = self._strip_hosts(hosts)
        self.password = password
        self.ip = ip

    def _strip_hosts(self, hosts):
        return map(lambda s: s.strip(), hosts.split(','))
