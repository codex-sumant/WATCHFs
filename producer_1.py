from confluent_kafka import Producer , Consumer
from confluent_kafka.admin import AdminClient, NewTopic
import json , csv

csvFilePath="/home/sumant/ELF-Predictor/system/final.csv"




a = AdminClient({'bootstrap.servers': 'localhost:9092'})

p = Producer({'bootstrap.servers': 'localhost:9092'})
count=0
with open(csvFilePath) as csvFile:
	csvReader=csv.DictReader(csvFile)
	for row in csvReader:
		p.poll(0)
		p.produce('request',json.dumps(row).encode('utf-8'))
		count+=1

exit={'type':'exit'}
p.poll(0)
p.produce('request', json.dumps(exit).encode('utf-8'),"message",0)
p.produce('request', json.dumps(exit).encode('utf-8'),"message",1)
p.flush()

c = Consumer({
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'mygroup2',
		'enable.auto.commit':'false',
    'auto.offset.reset': 'earliest'
})

c.subscribe(['response'])

count1=0
while count1<count:
	msg = c.poll(1.0)
	c.commit()
	if msg is None:
		continue
	if msg.error():
		print("Consumer error: {}".format(msg.error()))
		continue
	msg = json.loads(msg.value().decode('utf-8'))
	try:
		if(msg['type']=="exit"):
			continue;
	except:
		print('Received message: {}'.format(msg['Identification']))
	count1+=1
	p.poll(0)
c.close()
a.delete_topics(["request","response"])
