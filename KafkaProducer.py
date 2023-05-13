import requests
import json
from json import dumps
from time import sleep
from kafka import KafkaProducer
from datetime import datetime
import pandas as pd

def main():

    df = pd.read_csv('temperature.csv')
    df.dropna(inplace=True)
    df.iloc[:,1:] = df.iloc[:,1:].apply(convert_K_to_F)
    public_ip = '18.224.5.231'
    producer = KafkaProducer(bootstrap_servers=[f'{public_ip}:9092'],
                             value_serializer=lambda x: dumps(x).encode('utf-8'))
    while True:
        for n in range(len(df)):
            sample = df.iloc[n].to_dict()
            producer.send('demo_test', value=sample)

def convert_K_to_F(K):
    return (K - 273.15) * 1.8 + 32

if __name__ == '__main__':
    main()