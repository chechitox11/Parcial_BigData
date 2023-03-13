import requests
from bs4 import BeautifulSoup
import boto3
import datetime
import json
import csv
import os


def f():

    s3 = boto3.client('s3')
    dt = datetime.date.today()
    
    source_file_name = dt.strftime("%Y-%m-%d")+".html"
    csv_file_name ='{dt}.csv'
    
    try:
        s3.download_file('casachechitox', source_file_name, source_file_name)
        
        html_doc = read_file(source_file_name)
        
        div_tag_script = BeautifulSoup.find('script', type='application/ld+json')
        json_text = div_tag_script.string.strip()
        json_file = json.loads(json_text)
        
        create_csv(csv_file_name, json_file)

        with open(csv_file_name, 'rb') as csvfile:
            s3.upload_fileobj(csvfile, 'casafinal', '{dt}.csv')

        os.remove(source_file_name)
        os.remove('/tmp/' + csv_file_name)

    except Exception as e:
        # Handle the exception
        print('error:{e}')
    
    
    return {
        'statusCode': 200 
    }  
      
      
      
def create_csv(csv_name, data):

    fields = ["date", "@type", "name", 
              "numberOfBedrooms","numberOfBathroomsTotal",
              "address.addressRegion", "address.addressLocality",
              "address.addressCountry.name","floorSize.value","floorSize.unitCode"]

    header_row = dict((field, field) for field in fields)

    with open('/tmp/' + csv_name, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        writer.writerow(header_row)

        for item in data['about']:
            row = {
                "date":
                    datetime.date.today().strftime("%Y-%m-%d"),
                "@type":
                    item.get('@type', ''),
                "name":
                    item.get('name', ''),
                "numberOfBedrooms":
                    item.get('numberOfBedrooms', ''),
                "numberOfBathroomsTotal":
                    item.get('numberOfBathroomsTotal', ''),
                "address.addressRegion":
                    item.get('address', {}).get('addressRegion', ''),
                "address.addressLocality":
                    item.get('address', {}).get('addressLocality', ''),
                "address.addressCountry.name":
                    item.get('address', {}).get('addressCountry', {}).get('name', ''),
                "floorSize.value":
                    item.get('floorSize', {}).get('value', {}),
                "floorSize.unitCode":
                    item.get('floorSize', {}).get('unitCode', {})
                  }
            writer.writerow(row)


def read_file(source_file_name):

    with open(source_file_name, 'r') as f:
        html_doc = f.read()
    return html_doc
