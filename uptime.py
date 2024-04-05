import csv
import ssl, socket
import requests
from datetime import datetime

sites_to_check = ['https://wgxls.site', 'https://1881997.xyz']

def save_to_csv(data):
    with open('uptime_data.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow(data)
        
def check_uptime(url):
    try:
        r = requests.get(url)
        if r.status_code == 200:
            return True
        else:
            return False
    except requests.exceptions.RequestException as err:
        print ("ERROR: ", err)
        return False
        
def check_ssl_expiry(url):
    port = '443'

    cert=ssl.get_server_certificate((url, port))
    x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert)
    date_format = r'%b %d %H:%M:%S %Y %Z'

    not_after = datetime.strptime(x509.get_notAfter().decode('ascii'), date_format)
    
    remaining = not_after - datetime.utcnow()

    return remaining.days

for site in sites_to_check:
    uptime_status = check_uptime(site)
    ssl_expiry = check_ssl_expiry(site)
    result = [site, uptime_status, ssl_expiry]
    save_to_csv(result)
