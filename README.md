# DynHost / DynDNS Updater Component for Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/hacs/integration)

To use the integration in your installation, add the following to your `configuration.yaml` file:

#### Configuration variables:
| Variable |  Required  |  Type  | Description |
| -------- | ---------- | ----------- | ----------- |
| `server` | yes | string | The DynDNS server your domain is configured |
| `domain` | yes | string |  The subdomain you are modifying the DNS configuration for |
| `username` | yes | string | The DynHost username |
| `password` | yes | string | Password for the DynHost username |
| `scan_interval` | no |  time | How often to call the update service. (default: 10 minutes) |

#### Basic Example:

```yaml
ovh:
  server: dyndns.org
  domain: subdomain.domain.com
  username: YOUR_USERNAME
  password: YOUR_PASSWORD
```
Based on the official [hassio-ovh](https://github.com/GuilleGF/hassio-ovh),  [No-IP.com](https://github.com/home-assistant/core/tree/dev/homeassistant/components/no_ip) and [Mythic Beasts](https://github.com/home-assistant/core/blob/dev/homeassistant/components/mythicbeastsdns) integrations. Thanks to the creators!
