import requests
import operator

from lib import piclient_object

from datetime import datetime

class pihole_obj():

	def __init__(self, webpassword, server_ip):			

		self.webpassword = webpassword
		self.server_ip = server_ip
		self.data = None
		
		self.domains_being_blocked = None
		self.dns_queries_today = None
		self.ads_blocked_today = None
		self.ads_percentage_today = None
		self.unique_domains = None
		self.clients_ever_seen = None
		self.unique_clients = None

		self.top_sources = None

		self.top_items = None

		self.clients_list = {}
		self.ignore_list = []
		self.get_ignore_list()


	def get_ignore_list(self):
		with open('ignore_list.txt', 'r') as ignore_file:
			for line in ignore_file:
				if '###' in line:
					pass
				else:
					self.ignore_list.append(line.strip())

	def update(self):
		self.clients_list = {}
		
		# Update summary data
		r = requests.get('http://{}/admin/api.php?summary&auth={}'.format(self.server_ip, self.webpassword))
		self.data = r.json()
		self.update_summary()

		# Update query_sources data

		try:
			r = requests.get('http://{}/admin/api.php?getQuerySources&auth={}'.format(self.server_ip, self.webpassword))
			self.top_sources = r.json()
			self.top_sources = self.top_sources['top_sources']
			self.translate_query_sources()
		except:
			print('\nError fetching API data, maybe a wrong WEBPASSWORD ?\n')
			raise SystemExit(0)

		# Update topItems
		r = requests.get('http://{}/admin/api.php?topItems=25&auth={}'.format(self.server_ip, self.webpassword))
		self.top_queries = r.json()
		self.top_queries = self.top_queries['top_queries']
		self.update_top_queries()


		# Recent Blocked
		r = requests.get('http://{}/admin/api.php?recentBlocked&auth={}'.format(self.server_ip, self.webpassword))
		self.recentBlocked = r.text



	def update_summary(self):
		self.domains_being_blocked = self.data['domains_being_blocked']
		self.dns_queries_today = self.data['dns_queries_today']
		self.ads_blocked_today = self.data['ads_blocked_today']
		self.ads_percentage_today = self.data['ads_percentage_today']
		self.unique_domains = self.data['unique_domains']
		self.clients_ever_seen = self.data['clients_ever_seen']
		self.unique_clients = self.data['unique_clients']

	def translate_query_sources(self):
		for key, value in self.top_sources.items():
			if '|' in key:
				ip = key.split('|')[1]
			else:
				ip = key

			piclient = piclient_object.piclient_obj(ip, value)
			if piclient.ip not in self.clients_list:
				self.clients_list[piclient.ip] = piclient


	def update_top_queries(self):
		for key in self.top_queries.copy():
			if key in self.ignore_list:
				self.top_queries.pop(key)
		self.top_queries = sorted(self.top_queries.items(), key=operator.itemgetter(1), reverse=True)




	def print_stats(self):
		print('\n' * 200)
		print(' ########################################## {}'.format(datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')))
		# print(' Domains being blocked: {}'.format(self.domains_being_blocked))
		print('\tDNS queries today: {}'.format(self.dns_queries_today))
		print('\tAds blocked today: {}'.format(self.ads_blocked_today))
		print('\tClients ever seen: {}'.format(self.clients_ever_seen))
		print('\tUnique clients: {: <10} Most recent blocked: {}\n'.format(self.unique_clients, self.recentBlocked))
		print('################################################################')

		print('\tClientsQueries:\t\t\tTopDomains:\n')
		i = 0
		for entry in sorted(self.clients_list.values(), key=operator.attrgetter('hits'), reverse=True):
			if i < 8:

				if entry.ip.strip() not in self.ignore_list:
					print('\t{: <25.20}{: <20}{: <40}{}'.format(entry.hostname, entry.hits, self.top_queries[i][0], str(self.top_queries[i][1])))
					i+=1
		print('\n################################################################')


