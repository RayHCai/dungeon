import os
import subprocess

subprocess.run(f'pip install -e {os.path.dirname(__file__)}/_app')
