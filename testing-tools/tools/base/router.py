import requests
import colorama
from requests.adapters import HTTPAdapter
from tools.base import config
from tools.base import matcher
from tools.base import util

LOG = util.get_logger('router')


def get_lobby_route(feature=None, insecure=False):
    payload = {'appId': config.APP_ID}
    if config.FEATURE is not None:
        payload['feature'] = config.FEATURE
    if insecure or config.FORCE_USE_INSECURE_ADDR:
        payload['insecure'] = True

    auth_url = "%s/route" % config.ROUTER_URL
    LOG.info(colorama.Fore.YELLOW + "request game router at %s" % auth_url)

    if not auth_url.startswith("http"):
        auth_url = "https://" + auth_url

    with requests.Session() as session:
        session.mount(auth_url, HTTPAdapter(max_retries=3))
        resp = session.get(auth_url, params=payload, timeout=5)
        LOG.info(colorama.Fore.YELLOW +
                 "get router link got response %s" % resp.json())
        return resp.json()


if __name__ == "__main__":
    config.init_config('q0')
    print(get_lobby_route())
