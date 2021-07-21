# clico

###### The library implements create short links via [cli.com](https://cli.com) (Ex. cli.co) service.
###### [cli.com documentation](https://cli.com/docs/)

### Installation

```sh
$ pip install clico
```

### Settings

Optional environment variables:

CLICO_API_KEY - Your [API key](https://my.cli.com/dashboard/account)

### Using

```sh
from clico import Clico
from clico.models import Link, Domain, Integration

clico = Clico(api_key='YOUR_API_KEY')

or

clico = Clico() # If `CLICO_API_KEY` environment variable exists

single_link = clico.single_link(Link(**{
    'domain': Domain.CLI_CO,
    'target_url': 'https://google.com',
    'callback_url': 'https://my-api.com/callback',
    'is_deep': False,
    'id_campaign': 'my-campaign',
    'utm_phone': 'XXXXXXXXXXX',
    'utm_source': 'twitter',
    'utm_medium': 'banner',
    'utm_campaign': '2019',
    'utm_content': 'my ad',
    'utm_term': 'term'
}))

multiple_links = clico.multiple_links([
    Link(**{
        'domain': Domain.CLI_CO,
        'target_url': 'https://google.com',
        'callback_url': 'https://my-api.com/callback'
    }),
    Link(**{
        'domain': Domain.IN_SV,
        'target_url': 'https://google.com',
        'callback_url': 'https://my-api.com/callback',
        'utm_phone': 'XXXXXXXXXXX',
        'utm_term': 'term'
    })
])

integration = clico.integration(Integration(**{
    'callback_uri': 'https://my-api.com/callback',
    'redirect_uri': 'https://google.com',
    'user_data': {
        'key': 'value'
    }
}))
```