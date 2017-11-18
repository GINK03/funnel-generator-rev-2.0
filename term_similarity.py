import os

import sys

import glob
import pickle, gzip
import numpy as np
import re
if '--make_vector' in sys.argv:
  for name in glob.glob('models/*.vec'):
    print( name )
    account_name = name.split('/').pop()
    term_vec = {}
    for line in open(name):
      line = line.strip()
      es = line.split()
      term = es.pop(0)
      try:
        vec  = [ float(e) for e in es ]
      except ValueError as e:
        continue
      if len(vec) != 512:
        continue
      term_vec[term] = np.array( vec )
    
    open('vectors/{}.pkl'.format(account_name), 'wb').write( gzip.compress( pickle.dumps(term_vec) ) )

if '--sim' in sys.argv:
  for name in glob.glob('vectors/*.pkl'):
    account_name = name.split('/').pop()
    term_vec = pickle.loads( gzip.decompress( open(name, 'rb').read() ) )
    if term_vec.get('CV') is None:
      continue
    cv = term_vec['CV']
    cv_norm = np.linalg.norm(cv)

    term_sim = {}
    for term, vec in term_vec.items():
      vec_norm = np.linalg.norm(vec)
      print(account_name, term, (vec * cv).sum(axis=0) / (cv_norm * vec_norm) )
      term_sim[ term ] = (vec * cv).sum(axis=0) / (cv_norm * vec_norm)
    
    open('term_sim/{}.pkl'.format(account_name), 'wb').write( gzip.compress( pickle.dumps(term_sim) ) ) 

if '--sort' in sys.argv:
  for name in glob.glob('term_sim/*.pkl'):
    account_name = re.sub(r'\....', '', name.split('/').pop() )
    term_sim = pickle.loads( gzip.decompress( open(name, 'rb').read() ) )
    for term, sim in sorted( term_sim.items(), key=lambda x:x[1]*-1):
      print(account_name, term, sim)
