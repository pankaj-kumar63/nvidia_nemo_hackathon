from base.plot import *


def generate_graph():
    with open("/hackathon_teams/hack_team_11/workspace/Nvidia_nim_hackathon/backend/base/report.txt","r") as f:
        report=f.read()
    plot_graph_chapter_wise(report)
    overall_accuracy(report)
    topic_wise(report)
    plot_compare_report(report)
    NEET_Biology_Exam_Accuracy()

