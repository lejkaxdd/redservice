import logging as log
import json 


# pip install python-json-logger

log.basicConfig(filename='./log/app.log', level=log.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
# insert 2024_08_04 

# Event Code 
# 1000 - Get Request. 
# 1001 - Post Request.
# 1002 - DB not initialized. Try delete file db/data.db or restart service 
# 1003 - XXE file:///
# 1004 - XXE .dtd
# 1005 - Post Request error

global loga
loga = """{{
    "event_code" : "{event}",
    "agent" : {{
        "ip" : "10.61.10.11",     
        "name": "wazuh-agent",    
        "id" : ""                
        }},
    "manager": {{
      "name": "SiemN"
      }},
    "data": {{
      "tx_id": "0",
      "app_proto": "http",
      "in_iface": "ens33",           
      "src_ip": "{ip}",             
      "src_port": "{port}", 
      "dest_port": "5000",          
      "event_type": "alert",
      "alert": {{
        "severity": "1",
        "rev": "5",
        "metadata": {{
          "created_at": [
            "{time}"                  
            ]
          }}
        }}
      }},
      "http": {{
        "hostname": "{hostname}",                         
        "protocol": "{protocol}",             
        "http_method": "{http_method}",             
        "payload" : [
          "{payload}"
          ],             
        "url": "{url}",
        "http_user_agent": "{http_user_agent}",      
        "status": "{status}"                
      }},
      "error" : "{error}"
    }}"""

def start_page(flag, params):
    output = loga.format(event=params[0], ip=params[1], port=params[2], time=params[3], hostname=params[4], protocol=params[5],
                           http_method=params[6], payload=params[8], url=params[7], http_user_agent=params[9], status=params[10], error=params[11])
    if flag:
        log.info(json.loads(output))
    else:
        log.error(json.loads(output))

def receive_payload(flag, params):
    output = loga.format(event=params[0], ip=params[1], port=params[2], time=params[3], hostname=params[4], protocol=params[5],
                           http_method=params[6], payload=params[8], url=params[7], http_user_agent=params[9], status=params[10], error=params[11])
    
    # print(output)
    if flag:
        log.info(json.loads(output))
    else:
        log.error(json.loads(output))