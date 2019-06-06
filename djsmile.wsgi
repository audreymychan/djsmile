import sys, os, logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, '/var/www/djsmile')
os.chdir('/var/www/djsmile')
from serve import app
application = app
