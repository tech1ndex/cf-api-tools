import requests
import json
from settings import Settings
import logging

settings = Settings(_env_file=".env")

my_ip=requests.get("http://ifconfig.me").text # Get your public IP address or set it manually in .env

def get_cf_waf_rules(cf_api_url, token, zone_id, ruleset):
    api_url = f"{cf_api_url}/zones/{zone_id}/rulesets/{ruleset}"
    request_headers={"Authorization": f"Bearer {token}" ,"Content-Type":"application/json"}

    return requests.get(api_url, headers=request_headers).json()


def update_ip_cf_waf_rule(cf_api_url, token, zone_id, ruleset, rule_id, description):
    api_url = f"{cf_api_url}/zones/{zone_id}/rulesets/{ruleset}/rules/{rule_id}"
    request_headers={"Authorization": f"Bearer {token}" ,"Content-Type":"application/json"}
    data = {"action": "block", "description": f"{description}",
            "expression": f"ip.src ne {my_ip}"}

    return requests.patch(api_url, headers=request_headers, data=json.dumps(data)).json()


rules = get_cf_waf_rules(cf_api_url=settings.cf_api_url,
                     token=settings.token.get_secret_value(),
                     zone_id=settings.zone_id,
                     ruleset=settings.ruleset)


for x in rules['result']['rules']:
    update_ip_cf_waf_rule(cf_api_url=settings.cf_api_url,
                        token=settings.token,
                        zone_id=settings.zone_id,
                        ruleset=settings.ruleset,
                        rule_id=x['id'],
                        description=x['description'])

    logging.info(f"IP Address for Rule: {x['description']} updated")

