
class Scanner:
    _most_used_ports = {
        '21': 'FTP',
        '22': 'SSH',
        '23': 'TELNET',
        '25': 'SMTP',
        '53': 'DNS',
        '69': 'TFTP',
        '80': 'HTTP',
        '109': 'POP2',
        '110': 'POP3',
        '123': 'NTP',
        '137': 'NETBIOS-NS',
        '138': 'NETBIOS-DGM',
        '139': 'NETBIOS-SSN',
        '143': 'IMAP',
        '156': 'SQL-SERVER',
        '389': 'LDAP',
        '443': 'HTTPS',
        '546': 'DHCP-CLIENT',
        '547': 'DHCP-SERVER',
        '995': 'POP3-SSL',
        '993': 'IMAP-SSL',
        '2086': 'WHM/CPANEL',
        '2087': 'WHM/CPANEL',
        '2082': 'CPANEL',
        '2083': 'CPANEL',
        '3306': 'MYSQL',
        '8443': 'PLESK',
        '10000': 'VIRTUALMIN/WEBMIN'
    }

    def __init__(self, hosts=[], ports=[]):
        self.hosts = hosts
        self.ports = ports

    @classmethod
    def most_used_ports(cls):
        return ','.join(Scanner._most_used_ports.keys())

    def getinfo(self, host):
        import nmap
        result = {}
        try:
            sc = nmap.PortScanner()
            result = sc.scan(host, self.ports)
        finally:
            return result
    def getportstatus(self,host,port):
        import socket
        try:
           s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
           s.settimeout(0.5)
           code = s.connect_ex((host, int(port)))
        finally:
                s.close()
                return (code==0)

    def getinfobyip(self,host):
        result={}
        for port in self.ports.split(","):
            result[port]=self.getportstatus(host,port)
        return result

    def getstatusbyhost(self):
        results = {}
        for host in self.hosts:
            payload=self.getinfo(host)
            if payload=={}:
                  payload=self.getinfobyip(host)
            results[host] = payload
        return results


if __name__ == '__main__':
    x = Scanner(['www.nmap.org'], Scanner.most_used_ports())
    print(x.getstatusbyhost())



