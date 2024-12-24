import requests
import json
from settings import Settings
import logging
import re

logger = logging.getLogger()
settings = Settings(_env_file=".env")

my_ip=requests.get("http://ifconfig.me").text # Get your public IP address or set it manually in .env

def get_cf_waf_rules(cf_api_url, token, zone_id, ruleset):
    api_url = f"{cf_api_url}/zones/{zone_id}/rulesets/{ruleset}"
    request_headers={"Authorization": f"Bearer {token}" ,"Content-Type":"application/json"}

    return requests.get(api_url, headers=request_headers).json()


def update_ip_cf_waf_rule(cf_api_url, token, zone_id, ruleset, rule_id, description, expression):
    api_url = f"{cf_api_url}/zones/{zone_id}/rulesets/{ruleset}/rules/{rule_id}"
    request_headers={"Authorization": f"Bearer {token}" ,"Content-Type":"application/json"}
    data = {"action": "block", "description": f"{description}",
            "expression": f"{expression}"}

    return requests.patch(api_url, headers=request_headers, data=json.dumps(data)).json()



rules = get_cf_waf_rules(cf_api_url=settings.cf_api_url,
                     token=settings.token.get_secret_value(),
                     zone_id=settings.zone_id,
                     ruleset=settings.ruleset)


for x in rules['result']['rules']:
    try:
        ip = re.findall( r'[0-9]+(?:\.[0-9]+){3}', x['expression'])
        new_ip = x['expression'].replace(ip[0], my_ip)

        update_ip_cf_waf_rule(cf_api_url=settings.cf_api_url,
                        token=settings.token.get_secret_value(),
                        zone_id=settings.zone_id,
                        ruleset=settings.ruleset,
                        rule_id=x['id'],
                        description=x['description'],
                        expression=new_ip)
        logger.info(f"IP Address for Rule: {x['description']} updated from {ip[0]} to {my_ip}")
    except IndexError as e:
        logger.error(f"Rule does not contain IP: {x['description']}")
    except Exception as e:
        logger.error(f"Error updating IP Address for Rule: {x['description']}, {e}")
