import csv
import ssl
import socket
from urllib.parse import urlparse
from datetime import  datetime, timedelta
from requests import Session, exceptions
import requests
from collections import deque
import json

g_config = {
    "https://wgxls.site": 
    {
        "status": "STATUS_WGXLS_SITE='",
        "uptime7d": "WGXLS_SITE_UP_7='",
        "uptime24h": "WGXLS_SITE_UP_24='",
        "ssl": "WGXLS_SITE_SSL='"
    },
    "https://1881997.xyz":
    {
        "status": "STATUS_1881997_XYZ='",
        "uptime7d": "X1881997_XYZ_UP_7='",
        "uptime24h": "X1881997_XYZ_UP_24='",
        "ssl": "X1881997_XYZ_SSL='"
    },
    "https://blog.wgxls.eu.org:8443":
    {
        "status": "STATUS_BLOG_WGXLS_EU_ORG='",
        "uptime7d": "BLOG_WGXLS_EU_ORG_UP_7='",
        "uptime24h": "BLOG_WGXLS_EU_ORG_UP_24='",
        "ssl": "BLOG_WGXLS_EU_ORG_SSL='"
    },
    "https://opengrok.dijk.eu.org":
    {
        "status": "STATUS_OPENGROK_DIJK_EU_ORG='",
        "uptime7d": "OPENGROK_DIJK_EU_ORG_UP_7='",
        "uptime24h": "OPENGROK_DIJK_EU_ORG_UP_24='",
        "ssl": "OPENGROK_DIJK_EU_ORG_SSL='"
    },
    "https://423.1881997.xyz":
    {
        "status": "STATUS_423_1881997_XYZ='",
        "uptime7d": "X423_1881997_XYZ_UP_7='",
        "uptime24h": "X423_1881997_XYZ_UP_24='",
        "ssl": "X423_1881997_XYZ_SSL='"
    },
    "https://opengrok.wgxls.eu.org:8443":
    {
        "status": "STATUS_OPENGROK_WGXLS_EU_ORG='",
        "uptime7d": "OPENGROK_WGXLS_EU_ORG_UP_7='",
        "uptime24h": "OPENGROK_WGXLS_EU_ORG_UP_24='",
        "ssl": "OPENGROK_WGXLS_EU_ORG_SSL='"
    },
    "https://pdf.dijk.eu.org":
    {
        "status": "STATUS_PDF_DIJK_EU_ORG='",
        "uptime7d": "PDF_DIJK_EU_ORG_UP_7='",
        "uptime24h": "PDF_DIJK_EU_ORG_UP_24='",
        "ssl": "PDF_DIJK_EU_ORG_SSL='"
    },
    "https://725.1881997.xyz":
    {
        "status": "STATUS_725_1881997_XYZ='",
        "uptime7d": "X725_1881997_XYZ_UP_7='",
        "uptime24h": "X725_1881997_XYZ_UP_24='",
        "ssl": "X725_1881997_XYZ_SSL='"
    },
    "https://pdf.wgxls.eu.org:8443":
    {
        "status": "STATUS_PDF_WGXLS_EU_ORG='",
        "uptime7d": "PDF_WGXLS_EU_ORG_UP_7='",
        "uptime24h": "PDF_WGXLS_EU_ORG_UP_24='",
        "ssl": "PDF_WGXLS_EU_ORG_SSL='"
    },
    "https://image-host-wgx.pages.dev":
    {
        "status": "STATUS_IMAGE_HOST_PAGES='",
        "uptime7d": "IMAGE_HOST_PAGES_UP_7='",
        "uptime24h": "IMAGE_HOST_PAGES_UP_24='",
        "ssl": "IMAGE_HOST_PAGES_SSL='"
    },
    "https://lsky.wgxls.eu.org:8443":
    {
        "status": "STATUS_LSKY_WGXLS_EU_ORG='",
        "uptime7d": "LSKY_WGXLS_EU_ORG_UP_7='",
        "uptime24h": "LSKY_WGXLS_EU_ORG_UP_24='",
        "ssl": "LSKY_WGXLS_EU_ORG_SSL='"
    }    
}

g_data_file = 'data.csv'
g_data_list = []
g_data_list.append([])

def write_list_to_csv():
    global g_data_list
    with open(g_data_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(g_data_list)

def read_csv_to_list():
    global g_data_list  
    with open(g_data_file, 'r') as file:
        reader = csv.reader(file)
        g_data_list = list(reader)

def remove_data_before_seven_days():
    global g_data_list  
    seven_days_ago = datetime.now() - timedelta(days=7)
    g_data_list = [data for data in g_data_list if len(data) > 0 and datetime.strptime(data[0], "%Y-%m-%d %H:%M:%S") >= seven_days_ago]

def get_current_time():
    now = datetime.now()
    return now.strftime('%Y-%m-%d %H:%M:%S')

def check_uptime(url):
    try:
        r = requests.get(url)
        return r.status_code == 200
    except exceptions.RequestException:
        return False


def check_ssl_expiry(url):
    try:
        parsed_url = urlparse(url)
        domain = parsed_url.hostname
        port = parsed_url.port if parsed_url.port else 443
        ssl_date_fmt = r'%b %d %H:%M:%S %Y %Z'
        context = ssl.create_default_context()

        conn = context.wrap_socket(
            socket.socket(socket.AF_INET),
            server_hostname=domain,
        )
        conn.settimeout(3.0)

        conn.connect((domain, port))
        
        ssl_info = conn.getpeercert()
        return (datetime.strptime(ssl_info['notAfter'], ssl_date_fmt) - datetime.utcnow()).days

    except Exception as e:
        print(f"An error occurred when checking SSL expiry for {url}: {e}")
        return -1

def to_bool(s):
    if isinstance(s, bool):
        return s
    else:
        return s == "True"

def check_url(url):
    global g_data_list
    result = []
    result.append(get_current_time())
    result.append(url)
    status = check_uptime(url)
    result.append(status)
    ssl_day = check_ssl_expiry(url)
    result.append(ssl_day)
    g_data_list.append(result)
    if status:
        g_config[url]['status'] += "Status-Up-green.svg'"
    else:
        g_config[url]['status'] += "Status-Down-red.svg'"
    
    ssl_msg = ''
    if int(ssl_day) <= 0:
        ssl_msg = f"""<span style="color: red;">{ssl_day} Days</span>'"""
    elif int(ssl_day) <= 15:
        ssl_msg = f"""<span style="color: orange;">{ssl_day} Days</span>'"""
    elif int(ssl_day) >= 60:
        ssl_msg = f"""<span style="color: green;">{ssl_day} Days</span>'"""
    else:
        ssl_msg = f"""<span style="color: blue;">{ssl_day} Days</span>'"""
    g_config[url]['ssl'] += ssl_msg

def get_uptime_msg(uptime):
    msg = ''
    if uptime >= 90.0:
        msg = f"""<span style="color: green;">{uptime:.2f}%</span>'"""
    elif uptime >= 70.0:
        msg = f"""<span style="color: blue;">{uptime:.2f}%</span>'"""
    elif uptime >= 50.0:
        msg = f"""<span style="color: orange;">{uptime:.2f}%</span>'"""
    else:
        msg = f"""<span style="color: red;">{uptime:.2f}%</span>'"""
    return msg

def calc_uptime():
    temp = {}
    for key,value in g_config.items():
        temp[key] = {}
        temp[key]['S7'] = 0
        temp[key]['S24'] = 0
        temp[key]['u7d'] = 0
        temp[key]['u24h'] = 0
        
    one_days_ago = datetime.now() - timedelta(days=1)
    for data in g_data_list:
        temp[data[1]]['S7'] += 1
        if to_bool(data[2]):
            temp[data[1]]['u7d'] += 1
        if datetime.strptime(data[0], "%Y-%m-%d %H:%M:%S") >= one_days_ago:
            temp[data[1]]['S24'] += 1
            if to_bool(data[2]):
                temp[data[1]]['u24h'] += 1
    print(temp)
    for key, value in temp.items():
        u7d = temp[key]['u7d'] / temp[key]['S7'] * 100.0
        u24h = temp[key]['u24h'] / temp[key]['S24'] * 100.0
        u7d_msg = get_uptime_msg(u7d)
        u24h_msg = get_uptime_msg(u24h)
        g_config[key]['uptime7d'] += u7d_msg
        g_config[key]['uptime24h'] += u24h_msg

def write_env():
    env = f"export CURRENT_TIME='{get_current_time()}'\n"
    for key, value in g_config.items():
        for k,v in value.items():
            env += f"export {v}\n"
    
    with open('./siteenv','w') as f:
        f.write(env)

def main():
    read_csv_to_list()
    remove_data_before_seven_days()
    for key, value in g_config.items():
        check_url(key)
    calc_uptime()
    write_list_to_csv()
    write_env()

if __name__ == '__main__':
    main()

