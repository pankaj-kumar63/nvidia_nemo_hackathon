import sys 
import os 
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'/hackathon_teams/hack_team_11/workspace')))
from base.t2 import chat       

# Main loop to interact with the chatbot
async def main(question, flag):
    print("Welcome to the NEET Exam Analysis Chatbot!")
    # question = input("Enter your question (or type 'exit' to quit): ")
    if question.lower() == "exit":
        print("Goodbye!")
    res = await chat(question, flag)
    print("Response:\n", res)
    # while True:
    #     question = input("Enter your question (or type 'exit' to quit): ")
    #     if question.lower() == "exit":
    #         print("Goodbye!")
    #         break
    #     await chat(question)
        
# Run the main loop
# if __name__ == "__main__":
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(main())
#     loop.close()
