from proxy import GetIp

ips = GetIp().get_ips()
for ip in ips['http']:
    print(ip)

