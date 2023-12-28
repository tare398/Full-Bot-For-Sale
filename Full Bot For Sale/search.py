import requests, urllib, time
from googlesearch import search
from telebot.apihelper import ApiTelegramException
from bs4 import BeautifulSoup


wait_time = 60

def detect_captcha_type(url):
    response = requests.get(url)
    if "Just a moment..." in response.text and response.status_code == 403:
        cloud_flare = "True ❌"
    else:
        cloud_flare = "False ✅"
    soup = BeautifulSoup(response.content, 'html.parser')

    captcha_types = [
"re-captcha", "re_captcha", "recaptcha",
"captcha-v2", "captcha_v2", "captchav2",
"captcha-v3", "captcha_v3", "captchav3",
"h-captcha", "h_captcha", "hcaptcha",
"Captcha", "captcha"
    ]

    for captcha_type in captcha_types:
        if captcha_type in str(soup):
            return captcha_type, cloud_flare

    return "Clear ✅", cloud_flare


def read_urls_from_file():
    try:
        with open('gates.txt', 'r') as file:
            urls = file.read().splitlines()
        return urls
    except FileNotFoundError:
        return []

def save_url_to_file(url):
    with open('gates.txt', 'a') as file:
        file.write(url + '\n')

def perform_search(v1, v2, v3):
    sites_to_exclude = [
    "support.stripe.com",
    "stripe.com",
    "youtube.com",
    "kinsta.com",
    "ve.wordpress.org",
    "wordpress.org",
    "wordpress.com",
    "stackoverflow.com",
    "jotform.com",
    "pcogiving.zendesk.com",
    "givewp.com",
    "quora.com",
    "formidableforms.com",
    "github.com",
    "sisterschiropractor.com",
    "s-plugins.com",
    "support.kindful.com",
    "support.raisely.com",
    "support.donorfy.com",
    "discourse.webflow.com",
    "donorbox.org"
]
    prefix = f"{v2} site:.{v3} intext:{v1} -intext:captcha"
    queries = [f"-site:{site}" for site in sites_to_exclude]
    query = prefix + ' '.join(queries)
    

    try:
        urls = read_urls_from_file()
        num = len(urls) + 1

        search_results = list(search(query, num_results=num,sleep_interval=2))
        
        new_urls = [url for url in search_results if url not in urls]
        
        if new_urls:
            url_to_send = new_urls[0]
            save_url_to_file(url_to_send)
            captcha_type = detect_captcha_type(url_to_send)
            result_message = f"Site URL: {url_to_send}\nDomain: {url_to_send.split('/')[2]}\nCaptcha: {captcha_type[0]}\nCloud Flare: {captcha_type[1]}\n\n"
            return result_message
        else:
            return "No new results found."
    except (requests.exceptions.ConnectionError, urllib.error.HTTPError):
        return "Network issue or too many requests. need to wait for some time and try again..."
    except ApiTelegramException:
        time.sleep(wait_time)
        return "Too Many Requests Error. You need to wait for some time and try again..."
    except Exception as e:
        return f"An error occurred while searching. {e}"
