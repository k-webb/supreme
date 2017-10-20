import requests,re

with open('proxies.txt','r+') as proxy_file:
    p1 = requests.get('https://www.us-proxy.org/')
    found = re.findall('</tr><tr><td>(.*?)</td><td>(.*?)</td><td>', p1.text)
    for f in found:
        format_f = '{0}:{1}\n'.format(f[0],f[1])
        proxy_file.write(format_f)
    proxy_file.close()
