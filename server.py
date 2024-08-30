import os
from dotenv import load_dotenv
load_dotenv()
if os.getenv('USE_MLX', 'false').lower() == 'true':
    from packages.MLX.server import app
else:
    from packages.pytorch.server import app

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5555)
