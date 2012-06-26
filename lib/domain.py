class Domain(object):
    '''store domain parameters'''
    def __init__(self, name, hosts, password, ip):
        self.name = name
        self.hosts = self._massage_hosts(hosts)
        self.password = password
        self.ip = ip

    def _massage_hosts(self, hosts):
        if type(hosts) is str:
            return map(lambda s: s.strip(), hosts.split(','))
        elif type(hosts) is list:
            return map(lambda s: s.strip(), hosts)
