from confluent_kafka import Consumer, KafkaError, Producer
import json
import pandas as pd
import postprocessing
import csv
import subprocess

c = Consumer({
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'mygroup1',
		'enable.auto.commit':'false',
		'partition.assignment.strategy':'roundrobin',
    'auto.offset.reset': 'earliest'
})

p = Producer({'bootstrap.servers': 'localhost:9092'})

c.subscribe(['request'])

while True:
	msg = c.consume()[0]
	c.commit()
	if msg is None:
		continue
	if msg.error():
		print("Consumer error: {}".format(msg.error()))
		continue
	msg = json.loads(msg.value().decode('utf-8'))
	data_file = open('final.csv', 'w') 
	data_file.truncate()		
	# create the csv writer object 
	csv_writer = csv.writer(data_file) 
				
	header = msg.keys() 
	csv_writer.writerow(header) 
	 
	csv_writer.writerow(msg.values()) 
		
	data_file.close() 
	postprocessing.postprocessing()
	x = subprocess.call("java -cp .:./weka.jar evaluate",shell = True)
	reply={"Name":msg["Name"],"Class":x,"type":"response"}	
	p.poll(0)
	p.produce('response', json.dumps(reply).encode('utf-8'))
	p.flush()

p.poll(0)
c.close()

