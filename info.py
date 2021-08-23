import json

train_info_file = open('train_info.json', 'r')
output = json.load(train_info_file)
algorithm = output['algorithm']
time = output['train_time']
t = time.split('time: ')[1]
print(f'Algorithm : {algorithm}\nTrain time: {t}')
train_info_file.close()
