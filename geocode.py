import xlrd, xlwt
from xlutils.copy import copy
import requests
import sys

if len(sys.argv) < 2:
  print 'specify file'
  exit(1)

file = sys.argv[1]

rb = xlrd.open_workbook(file)
rs = rb.sheet_by_index(0)
wb = copy(rb)
ws = wb.get_sheet(0)

print 'Loaded ' + file

headers = []
for c in range(rs.ncols):
  key = rs.cell(0, c).value
  headers.append(key)

geocodes = 0
failures = 0

cache = {}

cache_hits = 0

try:
  lat_c = headers.index("Latitude")
  lng_c = headers.index("Longitude")
except:
  lat_c = rs.ncols + 1
  lng_c = rs.ncols + 2
  headers.append('Latitude')
  headers.append('Longitude')
  ws.write(0,lat_c,'Latitude')
  ws.write(0,lng_c,'Longitude')

locality = 'Locality'
try:
  headers.index("Locality")
except:
  locality = 'locality'

for r in range(1, rs.nrows):
  row = {}
  for c in range(len(headers)):
    try:
      row[headers[c]] = rs.cell(r,c).value
    except:
      row[headers[c]] = ''
  if not row['Latitude'] or not row['Longitude']:
    if row[locality] in cache:
      cache_hits += 1
      latlng = cache[row[locality]]
    else:
      params = {'query': row[locality]}
      print 'geocoding ' + row[locality]
      geo = requests.get('http://localhost:8081/', params=params).json()
      if geo['interpretations']:
        latlng = geo['interpretations'][0]['feature']['geometry']['center']
        cache[row[locality]] = latlng
        geocodes += 1
      else:
        print 'no result for ' + row[locality]
        cache[row[locality]] = {'lat':'','lng':''}
        failures += 1
        continue
    ws.write(r,lat_c,latlng['lat'])
    ws.write(r,lng_c,latlng['lng'])

wb.save(file + '_geocoded.xls')
print 'geocodes: {}. failures: {}. cache hits: {}'.format(geocodes, failures, cache_hits)