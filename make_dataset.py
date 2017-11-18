import glob
import json
import random

cvs = list()
for line in open('conversions.urls'):
  line = line.strip()
  cvs.append( line )
doi_name = {}
for line in open('datasetid.txt'):
  line = line.strip()
  doi, name = line.split(',')
  doi_name[ int(doi) ] = name
  print( doi )

doi_data = {}
doi_fpointer = {}
names = glob.glob('orig_data/part-*')
print(names)
for name in names:
  f = open( name )
  while True:
    try:
      line = f.readline()
    except Exception :
      continue
    if not line:  
      break

    line = line.strip()
    try:
      tuuid, val = line.split('\t')
    except ValueError as e:
      continue
    try:
      obj = json.loads(val)
    except json.decoder.JSONDecodeError as e:
      continue
    
    doi_keywords = {}
    for time, data in sorted(obj.items(), key=lambda x:x[0]):
      data_owner_id = data['data_owner_id']
      doi = doi_name.get( int(data_owner_id) )
      if doi is None:
        continue
      src = data['src']
      keywords = data['keywords']
      if doi_keywords.get( doi ) is None:
        doi_keywords[doi] = []
      #for keyword in keywords:
      if keywords != []:
        keyword = random.choice( keywords )
        doi_keywords[doi].append( keyword )

      iscv = any( [ cv in src for cv in cvs ] )
      if iscv is True:
        doi_keywords[doi].append( 'CV' )
    
    for doi, keywords in doi_keywords.items():
      if doi_fpointer.get(doi) is None:
        doi_fpointer[doi] = open('transformed/{}.txt'.format(doi), 'a')
      doi_fpointer[doi].write( ' '.join(keywords) + '\n' )
