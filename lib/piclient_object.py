from socket import gethostbyaddr
class piclient_obj():
	def __init__(self, ip, hits):
		self.ip = ip
		self.hits = hits
		self.hostname = 'Unknowed'
		self.get_hostname()
	def get_hostname(self):
		try:
			dns = gethostbyaddr(self.ip.strip())
			self.hostname = dns[0].split('.')[0]
		except:
			self.hostname = self.ip
			pass