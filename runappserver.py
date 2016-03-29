import sys
from goldensixpacks import app

app_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(app_root)

app.run(host='0.0.0.0')

