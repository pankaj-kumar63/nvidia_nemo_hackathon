# import sys
import os
import json
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'/hackathon_teams/hack_team_11/workspace')))
from vector_store import retrive_data

data = retrive_data(1000)
print(data)