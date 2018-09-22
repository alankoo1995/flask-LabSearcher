import json
from datetime import datetime
import requests
import re
import os,time

import pandas as pd
from flask import Flask,request,render_template
from flask_restplus import Resource, Api
from flask_sqlalchemy import SQLAlchemy

class get_time():
	def __init__(self):
		self.time = self._get_time()

	def _get_time(self):
		os.environ['TZ'] = 'AEST-10AEDT-11,M10.5.0,M3.5.0'
		creation_time = time.strftime("%H:%M")
		hour_and_minute = creation_time.split(':')

		if int(hour_and_minute[1]) > 0 and int(hour_and_minute[1]) < 30:
			hour_and_minute[1] = '00'
		if int(hour_and_minute[1]) > 30 and int(hour_and_minute[1]) < 59:
			hour_and_minute[1] = '30'

		return hour_and_minute[0] + ":" + hour_and_minute[1]

def read_csv(csv_file):
	return pd.read_csv(csv_file)

def print_dataframe(dataframe):
	for index,row in dataframe.iterrows():
		print(",".join([str(row[column]) for column in dataframe]))

app = Flask(__name__)

@app.route('/',methods=['POST','GET'])
@app.route('/index')
def index():
	df = pd.read_csv('data.csv')
	datum = []
	# if request.method == 'POST':
	# 	start_time,end_time = request.form['start_time'], request.form['end_time']
	# 	times = ['9:00','9:30','10:00','10:30','11:00']
	# 	df.set_index('Time', inplace=True)
	# 	headers = list(df.dtypes.index)
	# 	free_labs = {}
	# 	for t in times:
	# 		temp_list = []
	# 		a = list(df.loc[t])
	# 		for key in range(len(a)):
	# 			if a[key] == 'FREE':
	# 				temp_list.append(headers[key])
	# 		free_labs[t] = temp_list
	# 	print(free_labs)
	# 	return render_template('index.html',labs=free_labs,times=times)
	# datum = [e for e in row if e =='FREE']
	now = get_time().time
	# print(df.filter(items=['{}'.format(now)]))
	df.set_index('Time', inplace=True)
	headers = list(df.dtypes.index)
	free_labs = []
	a = list(df.loc[now])
	for key in range(len(a)):
		if a[key] == 'FREE':
			free_labs.append(headers[key])
	# times = list(df.index.values)
	times = [now]
	return render_template('index.html',labs=free_labs,times=times)


if __name__ == '__main__':
	app.run(debug=True)