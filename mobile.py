import requests, json, time, re

class Supreme():
	def __init__(self):
		self.headers = {'user-agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 6_1_4 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10B350 Safari/8536.25'}
		self.mobileStockURL='http://www.supremenewyork.com/mobile_stock.json'

	def mobileReq(self):
		resp = requests.get(self.mobileStockURL,headers=self.headers)
		print(resp.status_code)
		data = json.loads(resp.text)
		#print (data)

		print ("\nCategories:\n")

		count = 0
		for item in data[u'products_and_categories']:
			print(str(count)+' '+str(item))
			count+=1
		choice = raw_input('What Catagory? (1-10)')

		for i in data[u'products_and_categories'][u'T-Shirts']:
			name = i[u'name']
			a = i[u'image_url']
			b = str(i)
			c = re.search('............jpg',b).group()
			d = str(c).split('.jpg')[0]
			e = 'https://supremenewyork.com/shop/t-shirts/%s'%d
			print '{0} {1}'.format(name,e)

instance = Supreme()
instance.mobileReq()
