import sqlite3
import asyncio
import os



def create_db():
    """
    Creates a SQLite database and a table for storing student progress reports by Email_Id.
    If the table exists, it is dropped and recreated with the correct schema.
    
    The table 'new_Student_Progress_report' will contain the following columns:
        - Email_Id: A text field representing the unique email identifier for a student.
        - Report_Id: An auto-incremented primary key for each report entry.
        - Report: A text field to store the content of the student's report.
        - Timestamp: A timestamp indicating when the report was created, defaulting to the current time.
    """
    # Define the database file path
    path = "student_report.db"
    # Connect to the SQLite database (creates it if it doesn't exist)
    my_connection = sqlite3.connect(path)
    my_cursor = my_connection.cursor()
    
    
    # Create the table with the correct schema
    my_cursor.execute('''CREATE TABLE IF NOT EXISTS new_Student_Progress_report(
                        Email_Id TEXT,
                        Report_Id INTEGER PRIMARY KEY AUTOINCREMENT,
                        Report TEXT,
                        Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                    )''')
    
    # Commit and close the connection
    my_connection.commit()
    my_connection.close()

def store_report(Email_Id, Report):
    """
    Stores a student's progress report in the database.

    This function connects to the 'student_report.db' SQLite database and inserts a new 
    record into the 'new_Student_Progress_report' table with the provided Email_Id and Report. 
    The function uses parameterized queries to protect against SQL injection.

    Args:
        Email_Id (str): The unique email identifier for the student.
        Report (str): The content of the student's progress report to be stored.

    Returns:
        None
    """
    path="/hackathon_teams/hack_team_11/workspace/Nvidia_nim_hackathon/backend/base/student_report.db"
    my_connection = sqlite3.connect(path)
    my_cursor = my_connection.cursor()

    # Insert the report using the Email_Id as identifier
    my_cursor.execute('''
        INSERT INTO new_Student_Progress_report(Email_Id, Report)
        VALUES (?, ?)
    ''', (Email_Id, Report))  # Pass the values as a tuple
    
    # Commit the transaction
    my_connection.commit()
    
    # Close the connection
    my_connection.close()


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
    my_cursor.execute('SELECT Report FROM new_Student_Progress_report WHERE Email_Id = ?', (Email_Id,))
    results = my_cursor.fetchall()
    
    my_connection.close()
    
    # Check if any results were found
    if results:
        # Return the last report as a string
        return results[-1][0]  # Access the last element and the first item in the tuple
    else:
        return None


