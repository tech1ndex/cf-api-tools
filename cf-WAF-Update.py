import requests
import json
zone_id=""
ruleset=""
token=""
my_ip=requests.get("http://ifconfig.me")

#Get Rules
url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/rulesets/{ruleset}"
headers={"Authorization": f"Bearer {token}" ,"Content-Type":"application/json"}
r = requests.get(url, headers=headers)


#Patch Rule 1 - Whitelist single IP
rule_id=""
description="Block Access to Uptime Kuma Login"
url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/rulesets/{ruleset}/rules/{rule_id}"
headers={"Authorization": f"Bearer {token}"}
data={"action": "block","description": f"{description}","expression": f"(http.request.uri.path contains \"/dashboard\" and ip.src ne {my_ip.text})"}
r1 = requests.patch(url, json.dumps(data), headers=headers)