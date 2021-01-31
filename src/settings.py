'''Settings file for ChombyBot'''

import os

DEBUG = True

if DEBUG:
    from dotenv import load_dotenv
    load_dotenv()
    
    TOKEN = os.getenv('DEV_TOKEN')
else:
    TOKEN = os.getenv('TOKEN')
