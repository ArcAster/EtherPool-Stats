#just tracks a given user's share value on EtherPool

import arrow, lxml.html, time, sys
import re
import cfscrape # to circumvent cloudflare anti DDOS 

scraper = cfscrape.create_scraper()

from decimal import Decimal as D
from blessed import Terminal
t = Terminal()

from pymongo import MongoClient
client = MongoClient()
db = client['etherPool_log']
collection = db['pre_thaw']

user_url = 'http://ethpool.org/balance/e35c3cda59d0e88e0d76f72ea199f224c7d499ad'


print '- Init. done ~ starting now -'

def BalanceUnit(raw_shares, shares_str):
	#print 'starting balanceUnit()'
	unit = shares_str.split()[2]
	#print ('UNIT IS - %s') % unit
	value = re.compile("([0-9]*\.[0-9]*)", 0).search(shares_str).group(1)
	#print ('VALUE IS - %s') % value
	if(unit == 'Finney'):
		print 'unit is Finney\nAdjusting to Ether...'
		outValue = value*(0.001)
	else:
		outValue = value

	return outValue


def getMetrics(user_url):
	reg = "([0-9]*\.[0-9]*)"
	page_source = scraper.get(user_url).content

	tree = lxml.html.document_fromstring(page_source)
	raw_shares = tree.xpath(".//div[@id='home' and @class='container']//ul[1]/li[2]/text()")
	raw_hashRate = tree.xpath(".//div[@id='home' and @class='container']//ul[1]/li[1]/text()")

	try:
		shares_str = str(raw_shares[0])
		print ('SHARES STR - %s') % shares_str
		shares = BalanceUnit(raw_shares, shares_str)
	except:
		print "parse error @ shares!"
		pass

	try:
		hashRate_str = str(raw_hashRate[0])
		hashRate = re.compile(reg, 0).search(hashRate_str).group(1)
	except:
		print "parse error @ hashRate"
		pass
	try:	
		# note this time is in UTC (time-zone agnostic!)
		utc = arrow.utcnow()
		timestamp = utc.timestamp

		metrics = {
			"shares": shares,
			"hashrate": hashRate,
			"timestamp": timestamp
		}
	
		return metrics
	except:
		print 'Skipping...'

while(True):
	
	metrics_A = getMetrics(user_url)
	#print '%s -- %s' % (metrics[0], metrics[1])
	time.sleep(5)
	metrics_B = getMetrics(user_url)

	#if(metrics_A["shares"] == metrics_B["shares"] and metrics_A["hash-rate"] == metrics_B["hash-rate"]):
	#	pass
		
	if((metrics_A and metrics_B) and not(metrics_A["shares"] == metrics_B["shares"] and metrics_A["hashrate"] == metrics_B["hashrate"])):
		shares_change = ""
		shares_diff = ""
		shares_marker = ""

		hashrate_change = ""
		hashrate_diff = ""
		hashrate_marker = ""

		shares_A = D(metrics_A["shares"])
		shares_B = D(metrics_B["shares"])
		
		hashrate_A = D(metrics_A["hashrate"])
		hashrate_B = D(metrics_B["hashrate"])
		
		if(shares_A < shares_B):
			shares_change = "UP"
			shares_diff = shares_B - shares_A
			shares_marker = t.bold(t.green('UP')) 
		
		if(shares_B < shares_A):
			shares_change = "DOWN"
			shares_diff = abs(shares_A - shares_B)
			shares_marker = t.bold(t.red('DOWN'))

		if(hashrate_A < hashrate_B):
			hashrate_change = "UP"
			hashrate_diff = hashrate_B - hashrate_A
			hashrate_marker = t.bold(t.green('UP'))

		if(hashrate_A > hashrate_B):
			hashrate_change = "DOWN"
			hashrate_diff = abs(hashrate_A - hashrate_B)
			hashrate_marker = t.bold(t.red('DOWN'))			

		output = {
			"shares":metrics_B["shares"],
			"hashrate":metrics_B["hashrate"],
			"timestamp":metrics_B["timestamp"],
			"shares_change":shares_change,
			"shares_diff":str(shares_diff),
			"hashrate_change":hashrate_change,
			"hashrate_diff":str(hashrate_diff)
			}

		print '%s %s -- %s %s @ %s' % (output["shares"], shares_marker, output["hashrate"],hashrate_marker, output["timestamp"])
		db.pre_thaw.insert(output)

	else:
		pass

# page_source = driver.page_source
# tree = lxml.html.document_fromstring(page_source)
# members = tree.xpath(".//div[@class='fbProfileBrowserList fbProfileBrowserListContainer']//li")
# initLen = len(members)


