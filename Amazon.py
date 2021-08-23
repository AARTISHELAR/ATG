
from bs4 import BeautifulSoup
from requests import get
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
from pandas import DataFrame
from webdriver_manager.chrome import ChromeDriverManager


def load_full_javascript_page(browser):
    #Simulate scrolling to capture all posts
    SCROLL_PAUSE_TIME = 1.5

    # Get scroll height
    last_height = browser.execute_script("return document.body.scrollHeight")

    while True:

        # Scroll down to bottom
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = browser.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    return browser




def get_product_data():
    data = {'product':[],'price':[],'discount':[],'image':[],'rating':[],'global rating':[]}
    options = webdriver.ChromeOptions()
    options.headless = True
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_experimental_option('useAutomationExtension', False)
    browser = webdriver.Chrome(ChromeDriverManager().install(),options=options)
    browser.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    browser.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36'})
    browser.get('https://www.amazon.in/s?bbn=976419031&rh=n%3A976419031%2Cp_89%3Arealme&dc&qid=1624216249&rnid=3837712031&ref=lp_976420031_nr_p_89_3')
    for i in range(1,10):
        browser = load_full_javascript_page(browser)
        markup = browser.page_source
        browser.implicitly_wait(10)
        soup = BeautifulSoup(markup,'lxml')
        product = soup.find('div',class_='s-main-slot s-result-list s-search-results sg-row').find_all('div',class_='s-result-item')
        #product = soup.find('div',class_='sg-col-inner').find('span',class_='s-latency-cf-section').contents[1].find_all('div',class_='s-result-item')
        for p in product:
            #half = p.find('div',class_="a-section a-spacing-medium").find('div',class_='a-section a-spacing-none').find('a',class_="a-link-normal a-text-normal")
            try:
                name =  p.find('h2').text.strip() #half.text.strip(),class_="a-size-mini a-spacing-none a-color-base s-line-clamp-4"
                print(name)
                if name == 'Need help?':
                    continue
                else:
                    data['product'].append(name)
            except:
                continue
            try:
                rating = float(p.find('span',class_='a-icon-alt').text.split()[0])
                print(rating)
                data['rating'].append(rating)
            except:
                data['rating'].append(None)
            try:
                global_rating = int(p.find('span',class_='a-size-base').text.replace('\"','').replace(',','').strip())
                print(global_rating)
                data['global rating'].append(global_rating)
            except:
                data['global rating'].append(None)
            try:
                image = p.find('img')['src']
                data['image'].append(image)
            except:
                data['image'].append(None)
            try:
                price = float(p.find('span',class_='a-price-whole').text.strip().replace(',',''))
                print(price)
                data['price'].append(price)
            except:
                data['price'].append(None)
            try:
                discount = p.find('span',class_='a-letter-space').next.text.replace('₹','').strip()
                print(discount)
                data['discount'].append(discount)
            except:
                data['discount'].append(None)
        try:
            link = f'https://www.amazon.in/s?i=electronics&bbn=976419031&rh=n%3A976419031%2Cp_89%3Arealme&dc&page={i}&qid=1629447300&rnid=3837712031&ref=sr_pg_{i}'
            browser.get(link)
            browser.implicitly_wait(5)
            print(f'let\'s turn out {i} page')
        except:
            return data
    return data

def save_data(data):
    df = DataFrame(data)
    df = df.drop_duplicates()
    df = df.dropna(how = 'all')
    df.to_csv('amazon_product.csv')
    print('save')

if __name__ == "__main__":
    print('let\'s open browser! ')
    data = get_product_data()
    save_data(data)

