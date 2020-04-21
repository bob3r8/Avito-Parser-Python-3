from selenium import webdriver
from bs4 import BeautifulSoup
from threading import Thread
import time
import csv

URL = 'https://www.avito.ru/'
CITY = 'rossiya'
Q = 'razer'
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36 OPR/67.0.3575.105',
'accept':'*/*'}
TO = 1

def get_html(q, city = 'rossiya', page = 1):
	options = webdriver.ChromeOptions()
	options.add_argument('headless')
	browser = webdriver.Chrome('chromedriver.exe', options=options)
	link = "{0}{1}?cd=1&q={2}&p={3}".format(URL, city, q.replace(' ', '+'), page)
	browser.get(link)
	time.sleep(TO)
	r = browser.page_source
	return r

def get_content(html):
	soup = BeautifulSoup(html, 'html.parser')
	items = soup.find_all('div', class_='item__line')
	goods = []
	for i in items:
		location = i.find('span', class_='item-address-georeferences-item__content')
		if location:
			location = location.get_text(strip = True)
		else:
			location = i.find('span', class_='item-address__string')
			if location:
				location = location.get_text(strip = True)
			else:
				location = 'Не удалось обнаружить'
		try:
			goods.append({
			'name':	i.find('a', class_='snippet-link').get_text(strip = True), 
			'price': i.find('span', class_='snippet-price').get_text(strip = True).replace('\n', ''),
			'location': location,
			'date':	i.find('div', class_='snippet-date-info').get('data-tooltip'),
			'link':	'avito.ru' + i.find('a', class_='snippet-link').get('href')
			})
		except Exception as e:
			pass
	return goods

def get_max_page(html):
	soup = BeautifulSoup(html, 'html.parser')
	button = soup.find('span', {'data-marker':'pagination-button/next'})
	if button:
		max_page = button.find_previous_sibling('span')
		max_page = int(max_page.get_text())
	else:
		max_page = 1
	return max_page

def save_data(goods, path):
	with open(path, 'w', newline='', encoding='utf-8-sig') as file:
		writer = csv.writer(file, delimiter=';')
		writer.writerow(['Название', 'Цена', 'Адрес', 'Дата публикации', 'Ссылка'])
		for i in goods:
			writer.writerow([i['name'], i['price'], i['location'], i['date'], i['link']])


class parsingThread(Thread):
	def __init__(self, page):
		Thread.__init__(self)
		self.page = page
		self.goods = []
	def run(self):
		print("Парсинг страницы номер {} начат".format(self.page))
		self.html = get_html(Q, city = CITY, page = self.page)
		self.goods.extend(get_content(self.html))
		print("Парсинг страницы номер {} завершен".format(self.page))


def parseWithThread():
	html = get_html(Q, city = CITY)
	x = get_max_page(html)
	print("Найдено страниц: {}".format(x))

	thread_list = []
	for i in range(1, x+1):
		thread = parsingThread(i)
		thread.start()
		thread_list.append(thread)

	flag = True
	while flag:
		for i in range(0, x):
			flag = flag and thread_list[i].is_alive()

	goods = []
	for i in range(0, x):
		goods.extend(thread_list[i].goods)
	save_data(goods, "{}.csv".format(Q))



def parse():
	html = get_html(Q, city = CITY)
	x = get_max_page(html)
	goods = []
	for i in range(1, x+1):
		html = get_html(Q, city = CITY, page = i)
		print("Parsing {0} page of {1}".format(i, x))
		goods.extend(get_content(html))
	save_data(goods, "{}.csv".format(Q))

def main():
	parseWithThread()
if __name__ == '__main__':
	main()