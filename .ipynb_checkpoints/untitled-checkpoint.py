import sys 
import os 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'/hackathon_teams/hack_team_11/workspace')))
from t import *       

def get_report():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(chat())
    loop.close()