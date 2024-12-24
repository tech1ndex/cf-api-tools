## cf-waf-ip-update

#### Description:

A simple tool to automatically update a whitelisted IP Address in Cloudflare. Written with love in 🐍.

#### Usage:

A Dockerfile has been provided, there is also a pre-built image available here:

```
docker pull ghcr.io/tech1ndex/cf-waf-ip-update:v0.0.1-amd64
```

Environment Variables required are as follows:

`ZONE_ID` - Unique ID for your Cloudflare Zone, can be obtained from the admin console - https://dash.cloudflare.com/

`RULESET` - Unique ID for your Cloudflare WAF Ruleset. Can be found in Home > Your Zone > Security > WAF.

`TOKEN` - Cloudflare API Token.

`CF_API_URL` - Base API URL for Cloudflare (Default v4 is https://api.cloudflare.com/client/v4)
