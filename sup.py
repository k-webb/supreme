import requests as r
from datetime import datetime
import json, re, socket, time, sys, random
from slackclient import SlackClient

def UTCtoEST():
	current = datetime.now()
	return str(current) + " CST"
socket.setdefaulttimeout(2)

sc = SlackClient("SLACK KEY HERE")


class Supreme:
	def __init__(self):
		self.headers = {'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36'}
		self.totalstock = 0
		self.l1 = []

	def get_stock(self,link,p):

		###USE PROXIES, RANDOM CHOICE
		'''
		with open('proxies.txt','r+') as goodproxies:
			proxies = goodproxies.read().splitlines()
			x = random.choice(proxies)
			bs = {'http': x}
			print (bs)
			#HARD CODE PROXIES
			#proxies = {'http': '69.27.184.131:53281','https': '69.27.184.131:53281'}
			a = r.get(link,headers=self.headers,proxies=bs)
		'''
		##NO PROXIES , DEFAULT
		a = r.get(link,headers=self.headers)

		print (a.status_code)
		#print (a.text)
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
					m =  ('{0} {1} {2} {3} {4}'.format(color, pic, sizelabel, sizeid, stock))
					#print (m)
					if stock != 0:
						self.l1.append(m)
			if p == True:
				print ('\n')
	def monitor(self,link):
		def send_message(team,channel,username, title, link, site, sizes, thumb):
			attachments = [
                    {
                        "color": "#36a64f",
                        "title": title,
                        "title_link": link,
                        "text": "Site: %s"%site,
                        "fields": [
                            {
                                "title": "Sizes Available",
                                "value": sizes,
                                "short": False
                            }
                        ],
                        #"image_url": thumb
                        "thumb_url": thumb,
                        "ts": int(time.time())
                    }
                ]
			try:
				res = team.api_call("chat.postMessage", channel=channel, attachments=attachments, username=username,icon_emoji=':hocho:')
				if not res.get('ok'):
					print('error: {}', res.get('error'))
			except Exception as y:
				print (y)
				print('send_message failed')
		if self.totalstock == 0:
			try:
				self.get_stock(link,p=True)
				if self.totalstock == 0:
					print ('--- CHECK STATUS --- OUT OF STOCK %s'%UTCtoEST())
					time.sleep(int(self.interval))
					self.monitor(link)
				else:
					send_message(sc,'#CHANNEL NAME HERE','BOT USER NAME HERE','titleOfProduct',link[:-5],'<SupremeNY|http://www.supremenewyork.com/shop/all>','strcartlinks','img')
					##INSERT SLACK [X]/ TWITTER [ ]/ CHECKOUT [ ] FUNCTION HERE
					print('--- CHECK STATUS --- RESTOCK\n%s -- %s'%(link,UTCtoEST()))
			except Exception as monitor_error:
				print ('MONITOR ERROR\n%s'%monitor_error)
				pass

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

instance = Supreme()
instance.prompt()
