from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from datetime import datetime
from .questions import *
from .models import Student, Question
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .llm_response import main
# from .plot import plot_graph_chapter_wise, overall_accuracy, topic_wise, plot_compare_report, NEET_Biology_Exam_Accuracy
from .t import generate_graph
import asyncio
import os
import sys
import json

def getHome(request):
    return JsonResponse("Hello Home", safe=False)

def getQuestions(request):
    questions = get_questions()
    return JsonResponse(questions, safe=False)

@csrf_exempt
def save_answers(request):
    SAVE_PATH = "/hackathon_teams/hack_team_11/workspace/Nvidia_nim_hackathon/backend/base/quiz_answers"
    with open("/hackathon_teams/hack_team_11/workspace/Nvidia_nim_hackathon/backend/base/report.txt", "w") as f:
        f.close()
    
    if request.method == 'POST':
        try:
            # Load the request body as JSON
            body_unicode = request.body.decode('utf-8')
            body_data = json.loads(body_unicode)

            # Extract answers and questions from the request data
            answers = body_data.get('answers', {})
            questions = body_data.get('questions', [])
            email = body_data.get('email')
            score = body_data.get('score')
            time = body_data.get('timestamp')
            # print(score)
            
            if not email:
                return JsonResponse({"error": "Email not provided"}, status=400)

            # Combine answers with their corresponding questions
            questions_with_answers = []
            for question in questions:
                question_id = question.get('_id')
                user_answer_option = answers.get(str(question_id))  # Match question ID with answer
                question['userAnswer'] = "Not Answered"  # Default to "Not Answered"
                
                # Safely assign user answer from options
                if 'options' in question and user_answer_option is not None:
                    try:
                        question['userAnswer'] = question['options'][int(user_answer_option) - 1]
                    except (IndexError, ValueError):
                        question['userAnswer'] = "Invalid option"
                
                questions_with_answers.append(question)

            # Create a new data structure for saving
            new_questions_with_answers = []
            for obj in questions_with_answers:
                new_obj = {
                    "question": obj['text'],
                    "correct_answer": obj['answer'],  # Ensure this contains the actual correct answer text
                    "user_answer": obj['userAnswer'],
                    "chapter": obj['topic']
                }
                new_questions_with_answers.append(new_obj)

            # Save combined data as JSON in the file
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            file_name = f'{email}_{timestamp}.json'
            save_path_file = os.path.join(SAVE_PATH, file_name)
            with open(save_path_file, 'w', encoding='utf-8') as f:
                json.dump(new_questions_with_answers, f, ensure_ascii=False, indent=4)

            return JsonResponse({"message": "Answers saved successfully"}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Exception as e:
            print(f"Error processing request: {e}")  # Log error for easier debugging
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
def save_student(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            first_name = data.get('firstName')
            last_name = data.get('secondName')
            email = data.get('email')
            password = data.get('password')
            class_name = data.get('className')
            mobile = data.get('mobile')

            # Check if the user with the email already exists
            if User.objects.filter(username=email).exists():
                return JsonResponse({'error': 'Email is already registered'}, status=400)

            # Create a new user using Django's built-in User model
            user = User.objects.create_user(
                username=email, 
                password=password,
                first_name=first_name,
                last_name=last_name,
                email=email,
            )

            user.save()

            # Optionally: create a Student record if needed
            return JsonResponse({"message": "Student created successfully"}, status=201)
        
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    
    return JsonResponse({"error": "Invalid request method"}, status=405)

@csrf_exempt
def get_students(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            password = data.get('password')

            # Authenticate the user
            user = authenticate(request, username=email, password=password)
            
            if user is not None:
                # Login successful, return user data (you can include JWT or session data here)
                with open('/hackathon_teams/hack_team_11/workspace/Nvidia_nim_hackathon/backend/base/file.txt', 'w') as f:
                    f.write(email)
                return JsonResponse({
                    'token': user.password,
                    'user': {
                        'first_name': user.first_name,
                        'email': user.email,
                        # Add more user info as needed
                    }
                }, status=200)
            else:
                return JsonResponse({'error': 'Invalid login credentials'}, status=400)
        
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)

def user_profile(request):
    if request.method == 'GET':
        print(request.body)
        try:
            email = request.GET.get('email')
            obj = User.objects.filter(email=email)  # Ensure you're using the correct field

            if obj.exists():
                user = obj.first()
                print(user.first_name)
                return JsonResponse({
                    'first_name': user.first_name,
                    'email': user.email,
                    'last_name': user.last_name,
                }, status=200)
            else:
                return JsonResponse({'error': 'User not found'}, status=404)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

def user_dashboard(request):
    if request.method == "GET":
        email = request.GET.get('email')
        print(email)
        try:
            report_path = '/hackathon_teams/hack_team_11/workspace/Nvidia_nim_hackathon/backend/base/report.txt'
            
            message = "Generate the detail report of the student exam paper neet ?"
    
            with open(report_path, 'r') as f:
                    response = f.read()
            if len(response.strip()) == 0:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_until_complete(main(message, False))
                loop.close()
                try:
                    generate_graph()
                except Exception as e:
                    print(e)
            print(response)
            return JsonResponse({"Report":response})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)  # Return 500 for general errors
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
        
@csrf_exempt
def getBotResponse(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            message = data.get('userMessage')
            flag = data.get('flag')
            if flag == 1:
                flag = True
            # Process the message (replace with your LLM logic)
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(main(message, flag))
            loop.close()
            with open("/hackathon_teams/hack_team_11/workspace/Nvidia_nim_hackathon/backend/base/response.txt", 'r') as f:
                bot_reply = f.read()
            return JsonResponse({'reply': bot_reply})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
    return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)

        
    
        
        

