import requests as r
from datetime import datetime
import json, re, socket, time, sys

def UTCtoEST():
	current = datetime.now()
	return str(current) + " CST"
socket.setdefaulttimeout(2)

class Supreme:
	def __init__(self):
		self.headers = {'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36'}
		self.totalstock = 0

	def get_stock(self,link,p):
		a = r.get(link,headers=self.headers)
		print (a.status_code)
		b = json.loads(a.text)
		info = b[u'styles']
		for value in info:
			pic = value[u'mobile_zoomed_url']
			pic = 'https:'+str(pic)
			color = value[u'name']
			sizes = value[u'sizes']
			if p == True:
				print ('{0} {1}'.format(color,pic))
			for size in sizes:
				sizelabel = size[u'name']
				sizeid = size[u'id']
				stock = size[u'stock_level']
				self.totalstock = self.totalstock + stock
				if p == True:
					print ('{0} {1} {2}'.format(sizelabel,sizeid,stock))
			if p == True:
				print ('\n\n')


	def monitor(self,link):
		while self.totalstock == 0:
			try:
				self.get_stock(link,p=False)
				if self.totalstock == 0:
					print ('--- CHECK STATUS --- OUT OF STOCK %s'%UTCtoEST())
					time.sleep(int(self.interval))
					self.monitor(link)
				else:
					##INSERT SLACK / TWITTER / CHECKOUT FUNCTION HERE
					print('--- RESTOCK --- %s -- %s'%(link,UTCtoEST()))
			except Exception as monitor_error:
				print ('MONITOR ERROR\n%s'%monitor_error)

	def prompt(self):
		link = input('Please Enter A Link To Monitor..\n')
		link = str(link)+'.json'
		self.get_stock(link,p=True)
		print ('{0} {1}'.format('TOTAL STOCK - ',self.totalstock))
		if self.totalstock == 0:
			restock_answer = input('This product is out of stock, start restock mode? Enter - (y/n)\n')
			if restock_answer.lower() == 'y':
				self.interval = input('Please Enter An Interval..\n')
				self.monitor(link)
			else:
				print (restock_answer)
				sys.exit()
def main():
	instance = Supreme()
	try:
		instance.prompt()
	except Exception as mainerror:
		print ('MAIN ERROR')
		print (mainerror)

if __name__ == '__main__':
	main()
