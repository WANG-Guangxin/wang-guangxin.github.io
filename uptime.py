import csv
import ssl
import socket
from urllib.parse import urlparse
from datetime import  datetime, timedelta
import pytz
from requests import Session, exceptions
import requests
from collections import deque
import json
import os
from email.mime.text import MIMEText
from email.header import Header
from smtplib import SMTP_SSL

g_config = {
    "https://wgxls.site": 
    {
        "status": "STATUS_WGXLS_SITE='",
        "uptime7d": "WGXLS_SITE_UP_7='",
        "uptime24h": "WGXLS_SITE_UP_24='",
        "ssl": "WGXLS_SITE_SSL='",
    },
    "https://opengrok.dijk.eu.org":
    {
        "status": "STATUS_OPENGROK_DIJK_EU_ORG='",
        "uptime7d": "OPENGROK_DIJK_EU_ORG_UP_7='",
        "uptime24h": "OPENGROK_DIJK_EU_ORG_UP_24='",
        "ssl": "OPENGROK_DIJK_EU_ORG_SSL='"
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
    "https://alist.wgxls.eu.org:8443":
    {
        "status": "STATUS_ALIST_WGXLS_EU_ORG='",
        "uptime7d": "ALIST_WGXLS_EU_ORG_UP_7='",
        "uptime24h": "ALIST_WGXLS_EU_ORG_UP_24='",
        "ssl": "ALIST_WGXLS_EU_ORG_SSL='"
    },
    "https://pma.wgxls.eu.org:8443":
    {
        "status": "STATUS_PHPMYADMIN_WGXLS_EU_ORG='",
        "uptime7d": "PHPMYADMIN_WGXLS_EU_ORG_UP_7='",
        "uptime24h": "PHPMYADMIN_WGXLS_EU_ORG_UP_24='",
        "ssl": "PHPMYADMIN_WGXLS_EU_ORG_SSL='"
    },
    "https://web.dijk.eu.org":
    {
        "status": "STATUS_WEB_DIJK_EU_ORG='",
        "uptime7d": "WEB_DIJK_EU_ORG_UP_7='",
        "uptime24h": "WEB_DIJK_EU_ORG_UP_24='",
        "ssl": "WEB_DIJK_EU_ORG_SSL='"
    }
}

g_data_file = 'data.csv'
g_data_list = []
g_data_list.append([])
g_notice_enable = True

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
    # Also remove itmes which are not in g_config
    g_data_list = [data for data in g_data_list if data[1] in g_config]

def get_current_time():
    now = datetime.now()
    return now.strftime('%Y-%m-%d %H:%M:%S')

def get_current_time_cst():
    now = datetime.now(pytz.timezone('Asia/Shanghai'))
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
    env += f"export CURRENT_TIME_CST='{get_current_time_cst()}'\n"
    for key, value in g_config.items():
        for k,v in value.items():
            env += f"export {v}\n"
    
    with open('./siteenv','w') as f:
        f.write(env)

def send_mail(notice_title, notice_message):
    notice_host_server = os.environ.get("notice_host_server")
    notice_user = os.environ.get("notice_user")
    notice_pwd = os.environ.get("notice_pwd")
    notice_mail = os.environ.get("notice_mail")
    notice_receiver = os.environ.get("notice_receiver")

    #ssl登录
    smtp = SMTP_SSL(notice_host_server)
    #set_debuglevel()是用来调试的。参数值为1表示开启调试模式，参数值为0关闭调试模式
    smtp.set_debuglevel(1)
    smtp.ehlo(notice_host_server)
    smtp.login(notice_user, notice_pwd)

    msg = MIMEText(notice_message, "html", 'utf-8')
    msg["Subject"] = Header(notice_title, 'utf-8')
    msg["From"] = notice_mail
    msg["To"] = notice_receiver
    smtp.sendmail(notice_mail, notice_receiver, msg.as_string())
    smtp.quit()

def do_notice():
    notice_title = f"Uptime Report {get_current_time()}"
    notice_message_pre = f"""<html>
    <head></head>
    <body>
    <h2>Status Changed: </h2>
    """
    ssl_warning = f""" 
    <h2>SSL Warning: </h2>
    """
    notice_message_post = f"""
    <p>点击查看全部网站：<a href='https://wang-guangxin.github.op/sites'>https://wang-guangxin.github.op/sites</p> 
    </body>
    </html>"""

    notice_message = notice_message_pre 
    message_body = ''
    send_status_change = False
    send_ssl_warning = False

    # 根据 g_config 初始化一个 notice_dict
    notice_dict = {}
    for key, value in g_config.items():
        notice_dict[key] = {}
        notice_dict[key]['status'] = None
        notice_dict[key]['ssl'] = None
        notice_dict[key]['ssl_warning'] = False
        notice_dict[key]['seen'] = 0
    
    
    # 逆序遍历 g_data_list
    for data in reversed(g_data_list):
        brk = True
        if len(data) == 0:
            continue
        url = data[1]
        print("Checking: ", data)
        if notice_dict[url]['seen'] == 0:
            notice_dict[url]['status'] = data[2]
            notice_dict[url]['ssl'] = data[3]
            if notice_dict[url]['ssl'] <= 15:
                ssl_warning += f"""<p>{url} Remaining {notice_dict[url]['ssl']} Days</p>"""
                notice_dict[url]['ssl_warning'] = True
            notice_dict[url]['seen'] = 1
        elif notice_dict[url]['seen'] == 1:
            if str(notice_dict[url]['status']) != str(data[2]):
                print(f"Status Changed: {url} From {data[2]} to {notice_dict[url]['status']}")
                message_body += f"""<p><a href='{url}'>{url}</a> From {data[2]} to {notice_dict[url]['status']}</p>"""
                send_status_change = True
            if int(data[3]) == int(notice_dict[url]['ssl']):
                print(f"SSL Warning: {url} From {notice_dict[url]['ssl']} to {data[3]}")
                notice_dict[url]['ssl_warning'] = False
            notice_dict[url]['seen'] = 2
        
        for key, value in notice_dict.items():
            if value['seen'] == 1:
                brk = False
                break
        if brk:
            break
    
    for key, value in notice_dict.items():
        if value['ssl_warning']:
            send_ssl_warning = True
            break
    
    notice_message += message_body
    notice_message += ssl_warning
    notice_message += notice_message_post

    notice_message = notice_message.replace("From True to False", "From <strong>Up</strong> to 🔴<strong><span style='color: red;'>Down</span></strong>")
    notice_message = notice_message.replace("From False to True", "From <strong>Down</strong> to 🟢<strong><span style='color: green;'>Up</span></strong>")

    if send_status_change: # or send_ssl_warning:
        send_mail(notice_title, notice_message)

def main():
    read_csv_to_list()
    remove_data_before_seven_days()
    for key, value in g_config.items():
        check_url(key)
    calc_uptime()
    write_list_to_csv()
    write_env()
    if g_notice_enable:
        do_notice()

if __name__ == '__main__':
    main()

