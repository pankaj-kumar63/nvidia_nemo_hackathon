import pandas as pd
import random

def get_questions():
    df = pd.read_excel('../backend/final_cleaned.xlsx')
    # print(df.columns)

    all_physics_questions = df[df['subject'] == 'physics'].reset_index(drop=True)
    all_chemistry_questions = df[df['subject'] == 'chemistry'].reset_index(drop=True)
    all_biology_questions = df[df['subject'] == 'biology'].reset_index(drop=True)

    no_of_physics_questions = all_physics_questions.shape[0]
    no_of_chemistry_questions = all_chemistry_questions.shape[0]
    no_of_biology_questions = all_biology_questions.shape[0]
    
    n = 30
    # Correct usage of random.sample() by sampling indices from a range
    # indices_physics = random.sample(range(no_of_physics_questions), n)
    # indices_chemistry = random.sample(range(no_of_chemistry_questions), n)
    indices_biology = random.sample(range(no_of_biology_questions), n)

    # random_30_questions_from_physics = all_physics_questions.iloc[indices_physics]
    # random_30_questions_from_chemistry = all_chemistry_questions.iloc[indices_chemistry]
    random_30_questions_from_biology = all_biology_questions.iloc[indices_biology].reset_index(drop=True)

    # all_quesions = pd.concat([random_30_questions_from_physics, random_30_questions_from_chemistry, random_30_questions_from_biology], axis=0).reset_index(drop=True)

    questions = []
    for idx, row in random_30_questions_from_biology.iterrows():
        cur_row = {
            "_id": idx,
            "text": row['question'],
            "options": [row['option_1'], row['option_2'], row['option_3'], row['option_4']],
            "answer": row['correct_answer'],
            "subject": row['subject'],
            "topic": row['topic'],
            "correct_option":row['correct_option_number']
        }
        questions.append(cur_row)

    return questions


# questions= [
#     {
#       "_id": 1,
#       "text": "What is the chemical symbol for water?",
#       "options": ["O2", "CO2", "H2O", "N2"],
#       "answer": "H2O",
#     },
#     {
#       "_id": 2,
#       "text": "Which planet is known as the Red Planet?",
#       "options": ["Mars", "Venus", "Saturn", "Mercury"],
#       "answer": "Mars",
#     },
#     {
#       "_id": 3,
#       "text": "Who wrote the play 'Romeo and Juliet'?",
#       "options": ["William Shakespeare", "Mark Twain", "Charles Dickens", "J.K. Rowling"],
#       "answer": "William Shakespeare",
#     },
#     {
#       "_id": 4,
#       "text": "Which element has the atomic number 1?",
#       "options": ["Helium", "Hydrogen", "Oxygen", "Carbon"],
#       "answer": "Hydrogen",
#     },
#     {
#       "_id": 5,
#       "text": "What is the largest ocean on Earth?",
#       "options": ["Atlantic Ocean", "Indian Ocean", "Pacific Ocean", "Arctic Ocean"],
#       "answer": "Pacific Ocean",
#     },
#     {
#       "_id": 6,
#       "text": "What is the powerhouse of the cell?",
#       "options": ["Nucleus", "Ribosome", "Mitochondria", "Golgi apparatus"],
#       "answer": "Mitochondria",
#     },
#     {
#       "_id": 7,
#       "text": "Who was the first president of the United States?",
#       "options": ["Abraham Lincoln", "George Washington", "John Adams", "Thomas Jefferson"],
#       "answer": "George Washington",
#     },
#     {
#       "_id": 8,
#       "text": "What is the freezing point of water in Celsius?",
#       "options": ["100°C", "0°C", "-10°C", "32°C"],
#       "answer": "0°C",
#     },
#     {
#       "_id": 9,
#       "text": "Which organ in the human body is primarily responsible for filtering blood?",
#       "options": ["Heart", "Liver", "Kidney", "Lungs"],
#       "answer": "Kidney",
#     },
#     {
#       "_id": 10,
#       "text": "Which gas do plants absorb from the atmosphere for photosynthesis?",
#       "options": ["Oxygen", "Carbon Dioxide", "Nitrogen", "Hydrogen"],
#       "answer": "Carbon Dioxide",
#     }
#   ]

  

