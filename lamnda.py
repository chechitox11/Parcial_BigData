import json
import boto3
from datetime import datetime
import requests
#recibe num de registros a obtener
def traer(cantidad):
  url = 'https://api.fincaraiz.com.co/document/api/1.0/listing/search'
  data = {"filter":{"offer":{"slug":["sell"]},"path":"zona-chapinero bogota"},"fields":{"exclude":[],"facets":[],"include":["area","baths.id","baths.name","baths.slug","client.client_type","client.company_name","client.first_name","client.fr_client_id","client.last_name","client.logo.full_size","garages.name","is_new","locations.cities.fr_place_id","locations.cities.name","locations.cities.slug","locations.countries.fr_place_id","locations.countries.name","locations.countries.slug","locations.groups.name","locations.groups.slug","locations.groups.subgroups.name","locations.groups.subgroups.slug","locations.neighbourhoods.fr_place_id","locations.neighbourhoods.name","locations.neighbourhoods.slug","locations.states.fr_place_id","locations.states.name","locations.states.slug","locations.location_point","max_area","max_price","media.photos.list.image.full_size","media.photos.list.is_main","media.videos.list.is_main","media.videos.list.video","media.logo.full_size","min_area","min_price","offer.name","price","products.configuration.tag_id","products.configuration.tag_name","products.label","products.name","products.slug","property_id","property_type.name","fr_property_id","fr_parent_property_id","rooms.id","rooms.name","rooms.slug","stratum.name","title"],"limit":25,"offset":0,"ordering":[],"platform":41,"with_algorithm":True}}
  headers = {
      'Content-Type': 'application/json',
      'Connection': 'keep-alive',
  }
  response = requests.post(url, json=data, headers=headers)
  return response.json()

#columnas area, num habitacion, nueva, foto, titulo publicacion, id propiedad, estrato, # garages, # banos, precio, cliente, tipo propiedad, barrio, ciudad, pais, id_fr
def estructure(dic):
  todos = []
  interes = [['area'], ['rooms', 'name'], ['is_new'], ['media', 'photos', 'list', 'image', 'full_size'],['title'], ['property_id'], ['stratum', 'name'], ['garages', 'name'],
            ['baths', 'name'], ['price'], ['client', 'company_name'], ['property_type', 'name'], ['locations', 'neighbourhoods', 'name'],
            ['locations', 'cities', 'name'], ['locations', 'countries', 'name'], ['fr_property_id']]
  tam = len(dic['hits']['hits'])
  for k in range(tam):
    ims = dic['hits']['hits'][k]['_source']['listing']
    datos = []
    for i in interes:
      for j in range(len(i)):
        sel = [[ims[i[j]][0] if type(ims.get(i[j])) == list else ims.get(i[j], ims)][0] if j ==0 else [sel[i[j]][0] if type(sel.get(i[j])) == list else sel.get(i[j], sel)][0]][0]
      datos.append(sel)
    todos.append(datos)
  return todos

def f():
    # TODO implement
    client = boto3.client('s3')
    datos = traer(50)
    body = estructure(datos)
    body[:15]
    client.put_object(Body=body,Bucket='raaaw',Key='dollar.txt')
    print('s3')