# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['trado']
install_requires = \
['PyYAML>=6.0,<7.0']

entry_points = \
{'console_scripts': ['trado = trado:main']}

setup_kwargs = {
    'name': 'trado',
    'version': '0.4.2',
    'description': 'Dumb and dirty docker-compose files generator for traefik exposing',
    'long_description': '# trado\n\nTODO: FIX IT\n\nDumb and dirty docker-compose files generator for traefik exposing\n\nAll services described in one services.toml file and converted to more or less docker-compose compatible blocks. \nTop-level keys is services name, images, environment, volumes, ports is mirrored to docker-compose.\n\n## Services exposure to traefik\n\nThe most complicated part is `public` key, which is used to generate traefik labels.\n`public` signature is:\n```yaml\npublic: <host>[/<path>][@port]\n```\n\n- `host` directly used as hostname in traefik labels. TLS with letsencrypt is enabled by default.\n- `path` is optional and used as path in traefik. New service will be exposed with `https://host/path` but after proxing the path will be truncated.\n   Be careful, `host` without path must be configured in a diffrenent service at least once.\n- `port`: it\'s a hint for traefik to find a proper port for proxying\n\nNotice, that default `networks` for all services with `public` defined is `traefik`.\n\n## Options\n\n- `image`: docker image name\n- `envs`: list of environment variables\n  - `doppler`: extract list of variables from [doppler](doppler.com/)\n- `volumes`: list of volumes\n- `ports`: list of ports\n- `restart`: restart policy, default is `always`\n- `networks`: list of networks. Default is `traefik` for every service with `public` defined but can be extended.\n- `labels`: list of labels. For every `public` service it\'s filled with traefik-specific labels.\n  - `watchtower`: add label to enable and disable autoupdate of service with [watchtower](https://github.com/containrrr/watchtower)\n## Example\n\n```toml\n[gitea]\nimage = "gitea/gitea:latest"\npublic = "git.rubedo.cloud @ 3000"\ndoppler = true\nwathctower = true\nvolumes = ["./data:/data"]\n\nports = ["3000:3000", "2222:22"]\n    [gitea.envs]\n    USER_UID = 1000\n    USER_GID = 1000\n    TEST = "test"\n\n[asdf]\nimage = "containous/whoami"\npublic = "asdf.rubedo.cloud"\nrestart = "unless-stopped"\n\n[whoami2]\nimage = "containous/whoami"\npublic = "git.rubedo.cloud /test"\nrestart = "unless-stopped"\nlabels = "testlabel=true"\n\n[blah]\nimage = "containous/whoami" # not exposed to traefik at all\n```\n',
    'author': 'Grigory Bakunov',
    'author_email': 'thebobuk@ya.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
