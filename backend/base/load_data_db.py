import pandas as pd
from models import Question

# Load the Excel file
df = pd.read_excel(r'C:\One-Drive\OneDrive - Tredence\Desktop\AICademy\final_excel.xlsx')

# Iterate through the DataFrame and save data to the database
for idx, row in df.iterrows():
    question = Question(
        _id = row['_id'],
        question=row['question'],
        option_1=row['option_1'],
        option_2=row['option_2'],
        option_3=row['option_3'],
        option_4=row['option_4'],
        correct_option_number=row['correct_option_number'],
        correct_answer=row['correct_answer'],
        solution=row['solution']
    )
    question.save()
