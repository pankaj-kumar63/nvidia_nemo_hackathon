import os
import json
import asyncio
import pandas as pd
import re
import seaborn as sns
import matplotlib.pyplot as plt 
import re
import pandas as pd
import plotly.express as px



import sqlite3

def retrieve_data(Email_Id: str) -> str:
    """
    Retrieves the last progress report of a student from the SQLite database using Email_Id.

    This function connects to the 'student_report.db' SQLite database and queries the 
    'new_Student_Progress_report' table for the report associated with the provided Email_Id. 
    If a report is found, the last one is returned as a string; otherwise, the function returns None.

    Args:
        Email_Id (str): The unique email identifier for the student whose report is to be retrieved.

    Returns:
        str or None: The student's last progress report as a string if found, otherwise None.
    """
    path = "/hackathon_teams/hack_team_11/workspace/Nvidia_nim_hackathon/backend/base/student_report.db"
    my_connection = sqlite3.connect(path)
    my_cursor = my_connection.cursor()
    
    # Retrieve reports based on Email_Id
    my_cursor.execute('SELECT Timestamp,Report FROM new_Student_Progress_report WHERE Email_Id = ?', (Email_Id,))
    results = my_cursor.fetchall()
    
    my_connection.close()
    
    # Check if any results were found
    if results:
        # Return the last report as a string
        return results  # Access the last element and the first item in the tuple
    else:
        return None


def overall_accuracy_test():

    with open("/hackathon_teams/hack_team_11/workspace/Nvidia_nim_hackathon/backend/base/file.txt", 'r') as file:
        Email_Id = file.read()
        print(Email_Id )
        
    report=retrieve_data(Email_Id)
    # Define the regular expression pattern to extract data
    pattern = re.compile(
        r"\*\*Overall Score Summary\*\*\n\n"
        r"\* Total Questions Answered: (\d+)\n"
        r"\* Total Correct Answers: (\d+)\n"
        r"\* Total Incorrect Answers: (\d+)\n"
        r"\* Overall Accuracy Percentage: ([\d.]+)%"
    )
    
    # Initialize an empty list to store extracted data
    records = []
    
    # Iterate over each tuple in the report list
    for timestamp, single_report in report:
        match = pattern.search(single_report)
        if match:
            total_answered = int(match.group(1))
            correct_answers = int(match.group(2))
            incorrect_answers = int(match.group(3))
            accuracy_percentage = float(match.group(4))
            
            # Append data to the records list
            records.append({
                "Timestamp": timestamp,  # Use timestamp instead of attempt
                "Total Questions Answered": total_answered,
                "Total Correct Answers": correct_answers,
                "Total Incorrect Answers": incorrect_answers,
                "Overall Accuracy Percentage": accuracy_percentage})
     # Convert the list of records to a DataFrame
    df = pd.DataFrame(records)

    return df

    


# Define the function to extract chapter data
def extract_chapter_data(text):
    chapter_pattern = re.compile(
        r"\*\*\s*([^*]+)\s*\*\*:\s*"
        r"\* Total Questions Answered:\s*(\d+)\s*"
        r"\* Correct Answers:\s*(\d+)\s*"
        r"\* Incorrect Answers:\s*(\d+)\s*"
        r"\* Accuracy Percentage:\s*([\d.]+)%", re.MULTILINE
    )
    
    chapters = []
    
    for match in chapter_pattern.finditer(text):
        chapter_name = match.group(1).strip()
        total_questions = int(match.group(2))
        correct_answers = int(match.group(3))
        incorrect_answers = int(match.group(4))
        accuracy_percentage = float(match.group(5))
        
        chapters.append({
            "Chapter": chapter_name,
            "Total Questions": total_questions,
            "Correct Answers": correct_answers,
            "Incorrect Answers": incorrect_answers,
            "Accuracy Percentage": accuracy_percentage
        })
    
    
    return chapters


# Function to extract overall score summary data
def extract_overall_score_summary(text):
    # Regex pattern to match each line in the Overall Score Summary
    summary_pattern = re.search(
        r"\* Total Questions Answered:\s*(\d+)\s*"
        r"\* Total Correct Answers:\s*(\d+)\s*"
        r"\* Total Incorrect Answers:\s*(\d+)\s*"
        r"\* Overall Accuracy Percentage:\s*([\d.]+)%", text
    )

    # Check if match is found and extract data
    if summary_pattern:
        total_questions = int(summary_pattern.group(1))
        correct_answers = int(summary_pattern.group(2))
        incorrect_answers = int(summary_pattern.group(3))
        accuracy_percentage = float(summary_pattern.group(4))
        
        # Return the data as a dictionary
        return {
            "Total Questions Answered": total_questions,
            "Total Correct Answers": correct_answers,
            "Total Incorrect Answers": incorrect_answers,
            "Overall Accuracy Percentage": accuracy_percentage
        }
    
    return None



def extract_topic_data(text):
    # Regex pattern to capture chapter and subtopic details
    topic_pattern = re.compile(
        r"\*\*\s*([^*]+)\s*\*\*:\n\s*(.*?)\s*(?=\*\*|\Z)", re.DOTALL
    )
    
    topics = []

    for match in topic_pattern.finditer(text):
        chapter_name = match.group(1).strip()
        subtopics_data = match.group(2).strip()
        
        # Extract subtopics using another regex
        subtopic_pattern = re.compile(
            r"\*\s*Subtopic:\s*([^\n]+)\n\s*"
            r"- Questions Attempted:\s*(\d+)\n\s*"
            r"\*\s*Correct Answers:\s*(\d+)\n\s*"
            r"\*\s*Incorrect Answers:\s*(\d+)\n\s*"
            r"\*\s*Accuracy Percentage:\s*([\d.]+)%"
        )
        
        for submatch in subtopic_pattern.finditer(subtopics_data):
            subtopic_name = submatch.group(1).strip()
            questions_attempted = int(submatch.group(2))
            correct_answers = int(submatch.group(3))
            incorrect_answers = int(submatch.group(4))
            accuracy_percentage = float(submatch.group(5))
            
            topics.append({
                "Chapter": chapter_name,
                "Subtopic": subtopic_name,
                "Questions Attempted": questions_attempted,
                "Correct Answers": correct_answers,
                "Incorrect Answers": incorrect_answers,
                "Accuracy Percentage": accuracy_percentage
            })

    return pd.DataFrame(topics)





def progress_compare(report):
    # Updated regex pattern to match the progress comparison section
    pattern = r"\*\*Overall Accuracy\*\*:\n\s+\*\s+Previous:\s+([\d.]+)%\n\s+\*\s+Current:\s+([\d.]+)%\n\s+\*\s+Change:\s+([-+]?\d+\.?\d*)%\s+\((\w+)\)"
    
    match = re.search(pattern, report)
    
    if match:
        # Extract the matched groups
        previous_accuracy = match.group(1)
        current_accuracy = match.group(2)
        change_percentage = match.group(3)
        change_description = match.group(4)
        
        # Create a DataFrame
        data = {
            'Previous Accuracy': [previous_accuracy],
            'Current Accuracy': [current_accuracy],
            'Change (%)': [change_percentage],
            'Description': [change_description]
        }
        df = pd.DataFrame(data)
        return df
    else:
        print("No match found.")
        return pd.DataFrame()  # Return an empty DataFrame if no match is found


    return df 





def plot_graph_chapter_wise(report):

    path = "/hackathon_teams/hack_team_11/workspace/Nvidia_nim_hackathon/frontend/myapp/src/graphs"
    
    # Extract chapter data from the report
    chapter_data = extract_chapter_data(report)
    
    # Convert the chapter data into a DataFrame
    df_chapter_wise = pd.DataFrame(chapter_data)
    # Reshape the DataFrame for Plotly
    df_long = df_chapter_wise.melt(
        id_vars='Chapter', 
        value_vars=['Total Questions', 'Correct Answers', 'Incorrect Answers'], 
        var_name='Answer Type', 
        value_name='Count')
    
    # Create a bar plot using Plotly
    fig = px.bar(
        df_long, 
        x='Chapter', 
        y='Count', 
        color='Answer Type', 
        barmode='group',  # Side-by-side bars for each "Answer Type"
        title='Chapter-wise Question Analysis',
        color_discrete_sequence=px.colors.sequential.Viridis)
    
    # Customize the plot (add labels, rotate x-axis for readability)
    fig.update_layout(
        xaxis_title='Chapter', 
        yaxis_title='Number of Questions',
        title_font_size=16,
        xaxis_tickangle=-90  )
    
    # Define the file path for saving the bar plot
    chapter_wise_plot_path = os.path.join(path, "chapter_wise_analysis.png")
    
    # Save the bar plot as an image
    fig.write_image(chapter_wise_plot_path)
    

    

def overall_accuracy(report):
    # Extract overall score summary
    overall_score_data = extract_overall_score_summary(report)
    path="/hackathon_teams/hack_team_11/workspace/Nvidia_nim_hackathon/frontend/myapp/src/graphs"
    pie_data = pd.DataFrame({
        "Answer Type": ["Correct Answers", "Incorrect Answers"],
        "Count": [overall_score_data["Total Correct Answers"], overall_score_data["Total Incorrect Answers"]]})
    pie_data
    fig = px.pie(pie_data, values='Count', names='Answer Type', title='Overall Score Distribution for Current Exam',
                 color_discrete_sequence=px.colors.qualitative.Plotly)
    # Display the pie chart
    overall_score_pie_path = os.path.join(path, "overall_score_distribution.png")
    fig.write_image(overall_score_pie_path)
    
    
def topic_wise(report):
    # Extract topic data
    topic_df = extract_topic_data(report)
    path="/hackathon_teams/hack_team_11/workspace/Nvidia_nim_hackathon/frontend/myapp/src/graphs"
    # Reshape the DataFrame for plotting
    df_long = topic_df.melt(id_vars=["Chapter", "Subtopic"], 
                      value_vars=["Questions Attempted", "Correct Answers", "Incorrect Answers"],
                      var_name="Answer Type", value_name="Count")
    
    # Create a grouped bar plot
    fig = px.bar(df_long, x="Subtopic", y="Count", color="Answer Type", 
                 barmode="group", 
                 title="Topic-wise Breakdown of Questions",
                 labels={"Count": "Number of Questions"},
                 height=600)
    
    # Update layout for better visualization
    fig.update_layout(
        xaxis_title="Subtopic-wise analysis",
        yaxis_title="Number of Questions",
        xaxis_tickangle=90,
        )
    
    # Display the plot
    topic_wise_plot_path = os.path.join(path, "topic_wise_breakdown.png")
    fig.write_image(topic_wise_plot_path)
    # fig.show()


def plot_compare_report(report):
    df = progress_compare(report)

    # Convert the accuracy values to float for plotting
    df['Previous Accuracy'] = df['Previous Accuracy'].astype(float)
    df['Current Accuracy'] = df['Current Accuracy'].astype(float)
    
    # Reshape the DataFrame for plotting
    df_long = df.melt(value_vars=["Previous Accuracy", "Current Accuracy"],
                      var_name="Accuracy Type", value_name="Percentage")
    
    # Define the path for saving the plot
    path = "/hackathon_teams/hack_team_11/workspace/Nvidia_nim_hackathon/frontend/myapp/src/graphs"
    
    # Create a grouped bar plot with text values displayed
    fig = px.bar(df_long, x="Accuracy Type", y="Percentage", color="Accuracy Type", 
                 title="Accuracy Comparison with Respect to Last Exam",
                 labels={"Percentage": "Accuracy (%)"},
                 text='Percentage',  # Display values on the bars
                 height=600)
    
    # Update layout for better visualization
    fig.update_layout(
        yaxis_title="Accuracy (%)",
        xaxis_title="Accuracy Type",
        yaxis=dict(range=[0, 100])
    )
    
    # Display the plot
    progress_compare_plot_path = os.path.join(path, "progress_compare.png")
    fig.write_image(progress_compare_plot_path)
    # fig.show()


def NEET_Biology_Exam_Accuracy():
    # Convert 'Timestamp' to datetime
    path = "/hackathon_teams/hack_team_11/workspace/Nvidia_nim_hackathon/frontend/myapp/src/graphs"
    df=overall_accuracy_test()
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    
    # Create a line plot using Plotly
    fig = px.line(df, x='Timestamp', y='Overall Accuracy Percentage', 
                  title='NEET Biology Exam Accuracy Over Time',
                  labels={'Overall Accuracy Percentage': 'Accuracy (%)'},
                  markers=True)
    
    # Update the x-axis to show both date and time consistently and rotate labels
    fig.update_xaxes(tickformat="%Y-%m-%d %H:%M", 
                     tickangle=90,  # Transparent background
                    )  # Set the format to show date and time and rotate labels

    
    
    # Show the plot
    NEET_Biology_Exam_Accuracy = os.path.join(path, "NEET_Biology_Exam_Accuracy_Over_Time.png")
    fig.write_image(NEET_Biology_Exam_Accuracy)
    # fig.show()


    

