import xlrd
import json
import codecs
import requests
import sys

if len(sys.argv) < 2:
  print 'specify file'
  exit(1)

file = sys.argv[1]

sheet = xlrd.open_workbook(file).sheet_by_index(0)
data = []

print 'Loaded ' + file
headers = []
for c in range(sheet.ncols):
  key = sheet.cell(0, c).value
  headers.append(str(key))

rows_with_lat = 0
missing_year = 0

for r in range(2, sheet.nrows):
  row = {}
  for c in range(sheet.ncols):
    row[headers[c]] = sheet.cell(r,c).value
  if row['Latitude'] and row['Longitude']:
    lat = float(row['Latitude'])
    lng = float(row['Longitude'])
    rows_with_lat +=1 
    if 'Authority' in row:
      row['Authority'] = row['Authority'].strip('()')
      year = row['Authority'].split(',')[-1].strip()[:4]
      if not year or not year.isdigit():
        missing_year += 1
        continue
      year = int(year)
      name = row['ScientificName'] + ' (' + row['Authority'] + ')'
      info = u'<b>{}</b><br>'.format(name)
      if row['Source']:
        info += u'Source: {}<br>'.format(row['Source'])
      if row['Locality']:
        info += u'Locality: {}<br>'.format(row['Locality'])
      if row['MinDepth']:
        info += 'Depth: {} - {}<br>'.format(row['MinDepth'], row['MaxDepth'])
      if row['BeginYear']:
        info += 'Collection Start: {}-{}-{}<br>'.format(row['BeginYear'], row['BeginMonth'], row['BeginDay'])
      if row['EndYear']:
        info += 'Collection End: {}-{}-{}<br>'.format(row['EndYear'], row['EndMonth'], row['EndDay'])
      
      kingdom = row['Kingdom']
      phylum = row['Phylum']
      class_ = row['Class']
      order = row['Order']
      family = row['Family']
      genus = row['Genus']
      species = row['Species']
      sciname = row['ScientificName']
      info += u'Kingdom: {}, Phylum: {}, Class: {}, Order: {}, Family: {}, Genus: {}, Species: {}<br>'.format(kingdom, phylum, class_, order, family, genus, species)
    elif 'recordedby' in row:
      #class family genus eventdate kingdom locality order_ phylum scientificname year elevation depth Latitude Longitude recordedby
      year = row['year']
      if not year:
        missing_year += 1
        continue
      name = row['scientificname']
      sciname = row['species']
      info = u'<b>{}</b><br>'.format(name)
      if row['locality']:
        info += u'Locality: {}<br>'.format(row['locality'])
      order = row['order_']
    else:
      print 'unable to parse'
      continue

    stripped_row = {
      'year': year,
      'latlng': {'lat': lat, 'lng': lng},
      'name': name,
      'sciname': sciname,
      'order': order,
      #'taxonomy': {'kingdom': kingdom, 'phylum': phylum, 'class': class_, 'order': order, 'family': family, 'genus': genus, 'species': species},
      'info': info
    }
    data.append(stripped_row)

print 'Total rows: {}. Rows with lat: {}. Missing year: {}'.format(sheet.nrows - 1, rows_with_lat, missing_year)

with codecs.open(file + '.json', 'w', 'utf8') as f:
  s = json.dumps(data, ensure_ascii=False)
  f.write(s)