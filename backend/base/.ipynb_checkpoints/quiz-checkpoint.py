import streamlit as st
from questions import questions
import json

# Define the quiz questions and options


def run_quiz():
    st.title("MCQ Quiz")

    # Initialize score
    score = 0
    user_answers = []
    quiz_result=[]

    # Loop through each question
    for idx, q in enumerate(questions):
        st.write(f"Q{idx+1}. {q['question']}")
        
        # Prepend an empty option for 'not selected' state
        answer_given = st.radio(
            f"Choose your answer for question {idx+1}",
            q['options'],  # Add an empty option at the beginning
            key=f"question_{idx}",
            index=None
        )
        
        # Add the user's answer for review later
        user_answers.append(answer_given)

        # Only update score if the user selected a valid option (not the empty string)
        if answer_given == q["answer"]:
            score += 1
        

    # Submit button
    if st.button("Submit"):
        # Check if all questions are answered
        if "" in user_answers:
            st.error("Please answer all questions before submitting!")
        else:
            # Display the score
            st.write(f"Your score is {score} out of {len(questions)}")

            # Provide feedback
            for idx, q in enumerate(questions):
                st.write(f"Q{idx+1}. {q['question']}")
                st.write(f"Your answer: {user_answers[idx]}")
                st.write(f"Correct answer: {q['answer']}")
                st.write("---")

                quiz_result.append({
                            'question':q['question'],
                            'chapter':q['chapter'],
                            'user_answer':user_answers[idx],
                            'correct_answer':q["answer"]})
            json_object = json.dumps(quiz_result, indent=4)
            with open("sample.json", "w") as outfile:
                  outfile.write(json_object)

if __name__ == "__main__":
   run_quiz()
