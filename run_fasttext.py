import os

import glob

for name in glob.glob('trains/*.txt'):
  save_name = 'models/' + name.split('/').pop()
  os.system('./fasttext skipgram -dim 512 -maxn 0 -input {name} -output {save_name} '.format(name=name, save_name=save_name))
