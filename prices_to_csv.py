#!/usr/bin/env python

import csv
import datetime
from pymongo import MongoClient
from collector.settings import MONGO_URL
from pprint import pprint

db = MongoClient(MONGO_URL)['bm']
i_year = datetime.datetime.now().year
year = str(i_year)
first_day = datetime.datetime(i_year, 1, 1)

general_fieldnames=['key', 'updated_at', 'scraped_at', 'name', 'address', 'company']

query = {}
projection = {
    '_id': 0,
    "loc.coordinates": 1,
    ("prices_yearly."+year+".bencin-95"): 1,
    ("prices_yearly."+year+".diesel"): 1,
    ("prices_yearly."+year+".bencin-100" ): 1,
}
projection.update({k: 1 for k in general_fieldnames})

with open('stations.csv', 'w') as csvfile:
    fieldnames = general_fieldnames + ['date', 'fuel', 'price', 'lon', 'lat']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for station in db['stations'].find({}, projection):
        for fuel in station['prices_yearly'][year]:
            for raw_day in station['prices_yearly'][year][fuel]:
                row = {f: station[f] for f in general_fieldnames}
                row['fuel'] = fuel
                row['date'] = (first_day + datetime.timedelta(days=int(raw_day)-1)).isoformat()
                row['fuel'] = fuel
                row['price'] = station['prices_yearly'][year][fuel][raw_day]
                row['lon'], row['lat'] = station['loc']['coordinates']
                row['scraped_at'] = row['scraped_at'].isoformat()
                row['updated_at'] = row['updated_at'].isoformat()
                writer.writerow(row)
