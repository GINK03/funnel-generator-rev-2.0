import os

import glob

try:
  os.mkdir('models')
except OSError as e:
  ...
for name in glob.glob('transformed/*.txt'):
  save_name = 'models/' + name.split('/').pop()
  os.system('./fasttext skipgram -dim 512 -minn 0 -maxn 0 -input {name} -output {save_name} '.format(name=name, save_name=save_name))
