# this file reads data from DB and writes it to a live plot.ly graph
# this file is intended to be used as a standalone model
# watching for DB updates from mongo is crucial
import time, re, sys, arrow

import plotly.plotly as ply # plotly lib
from plotly.graph_objs import Scatter, Layout, Figure, Data, Stream, YAxis

# plotly config
username = "plotly_arc"
api_key = "x0c1fu75vc"
shares_stream_token = "icf8tcvpfn"
hashrate_stream_token = "qoej2vrvoe"

ply.sign_in(username, api_key)


from pymongo import MongoClient
client = MongoClient()
db = client['etherPool_log']
collection = db['pre_thaw']

def convertStamp(timestamp):
	meta = arrow.get(timestamp)
	local_conv = meta.to('US/Eastern')
	time = local_conv.format('YYYY-MM-DD HH:mm:ss')
	return(time)

# config for actual streaming plot

trace_shares = Scatter(
	x=[],
	y=[],
	stream=Stream(
		token=shares_stream_token
		),
	yaxis='y'
	)

trace_hashrate = Scatter(
	x=[],
	y=[],
	stream=Stream(
		token=hashrate_stream_token
		),
	yaxis='y2'
	)

layout = Layout(
	title='Ether Pool Hashrate & Mined Shares',
	yaxis=YAxis(
		title='Ether'
		),
	yaxis2=YAxis(
		title='MH/s',
		side='right',
		overlaying="y"
		)
	)

data = Data([trace_shares, trace_hashrate])
fig = Figure(data=data, layout=layout)

print ply.plot(fig, filename = 'Ether Pool Stats')

stream_shares = ply.Stream(shares_stream_token)
stream_shares.open()

stream_hashrate = ply.Stream(hashrate_stream_token)
stream_hashrate.open()


print 'init db len set'
lastUpdate = db.pre_thaw.count()

while(True):
	check = db.pre_thaw.count()
	if (check > lastUpdate):
		print 'Update detected'
		lastUpdate = check
		
		#figure out what to push to live graph
		metric_obj = collection.find().sort("_id", -1)[0]
		now = convertStamp(metric_obj["timestamp"])

		if(metric_obj["shares_change"] and not(metric_obj["hashrate_change"])):
			# do stuff
			print '- shares update -'
			shares = metric_obj["shares"]
			stream_shares.write({'x': now, 'y': shares })

		if(metric_obj["hashrate_change"] and not(metric_obj["shares_change"])):
			# do stuff
			print '- hashrate update -'
			hashrate = metric_obj["hashrate"]
			stream_hashrate.write({'x': now, 'y': hashrate })

		if(metric_obj["shares_change"] and metric_obj["hashrate_change"]):
			# do stuff
			print '- shares and hasrate update -'
			shares = metric_obj["shares"]
			hashrate = metric_obj["hashrate"]
			stream_shares.write({'x': now, 'y': shares })
			stream_hashrate.write({'x': now, 'y': hashrate })

	time.sleep(1)

stream_shares.close()
stream_hashrate.close()




