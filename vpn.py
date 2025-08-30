import requests
import random
import urllib3
import gzip
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.proxy import *
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

def get_free_proxies():
    url = "https://free-proxy-list.net/"
    # получаем ответ HTTP и создаем объект soup
    soup = bs(requests.get(url).content, "html.parser")
    proxies = []
    for row in soup.find("table", attrs={"class": "table-striped"}).find_all("tr")[1:]:
        tds = row.find_all("td")
        try:
            ip = tds[0].text.strip()
            port = tds[1].text.strip()
            host = f"{ip}:{port}"
            proxies.append(host)
        except IndexError:
            continue
    return proxies

free_proxies = get_free_proxies()


print(f'Обнаружено бесплатных прокси - {len(free_proxies)}:')

proxies = {
    'https': "104.238.30.12:63232",
    'https': "104.238.30.12:63232",
}

for i in range(len(free_proxies)):

    print(proxies)
    # site = 'https://ficbook.net/'
    # site = 'https://ficbook.net/readfic/0196e531-947f-774c-b879-d5f16dbc0b5d'
    site = 'https://author.today/work/480172'
    # site = 'https://author.today'

    try:

        PROXY = proxies['https']

        proxy = Proxy({
            'proxyType': ProxyType.MANUAL,
            'httpProxy': PROXY,
            'sslProxy': PROXY,
            'noProxy': ''
        })

        options = Options()
        # options.proxy = proxy
        driver = webdriver.Firefox(options=options)

        wait = WebDriverWait(driver, 10)
        driver.get(site)

        # resp = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@class="description"] a'))).text
        resp = wait.until(EC.element_to_be_clickable((BY.XPATH, '//div[@class="book-title"]'))).text

        # resp = driver.find_element('XPATH', '//[@class="description word-break"]')

        print(resp)
        if resp.text:

            print(resp, resp.text)
            break


    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе: {e}")

    proxies = {
        'https': f"{free_proxies[i]}",
        'https': f"{free_proxies[i]}",
    }

driver.quit()



    # Черновичное

    # headers = {
    #     'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Mobile Safari/537.36',
    #     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    #     'Accept-Encoding': 'gzip, deflate, br, zstd',
    #     'Accept-Language': 'ru,en;q=0.9',
    #     'Content-Type': 'text/html; charset=utf-8',
    #     'cookie': 'adrcid=AsO8yjmgOfrvtvJWXsUOKVw; _ym_uid=1756041010655022292; _ym_d=1756041918; _ym_isad=2; cf_clearance=DOzMmm3cE4pFb9Kkz.C64LtAnEXN0I1hXQFp4VNNuJ4-1756041918-1.2.1.1-99KWMFd2fnOwDsUAvsfsUYU8vJKi1u4TVRVWi2hPChFscwOylbB6TcSBMfjz5ytj9.Nr1H0RlB3oM41SFpv1yKTIC.mJH9Vts_OfVuJ2cNJ4jvREbdrsZnyTmhkWjuxP23VuNkif9452fJLUnXoYPgnFgVn5OeauixM08L7W4x5pwGTsxsSybSJYc_ReZoyMJkuf44N27DlKawUKwH8ENBeAM_POM615Bb3ReJji2nE; _ym_visorc=b',
    #     'refere': 'https://ficbook.net/readfic/0196e531-947f-774c-b879-d5f16dbc0b5d',
    #     'sec-ch-ua-platform-version': '6.0',
    #     'cache-control': 'no-cache',
    #     'pragma': 'no-cache',
    #     'priority': 'u=0, i',
    #     'upgrade-insecure-requests': '1',
    #     'sec-fetch-user': '?1',
    #     'sec-fetch-dest': 'document',
    #     'sec-ch-ua-mobile': '?1',
    #     'sec-fetch-mode': 'navigate',
    #     'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "YaBrowser";v="25.8", "Yowser";v="2.5"',
    # }

    # session = requests.Session()
    # resp = session.get(site, proxies=proxies, headers=headers, timeout=3)

    # resp = bs(requests.get(site, proxies=proxies, headers=headers).content, "html.parser", from_encoding="UTF-8")
    # resp = bs(requests.get(site, proxies=proxies, headers=headers, timeout=3).content, "html.parser")