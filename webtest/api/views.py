from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from django.http import HttpResponse
import requests as req
import collections
import json as j


def get_questions_id(chat_data):
    qids = {}
    for question in chat_data.get('questions'):
        qids[question['order']] = question.get('qid')

    oqids = collections.OrderedDict(sorted(qids.items()))
    ids = []
    for qid in oqids.values():
        ids.append(qid)
    return ids


def get_question_data(qids):
    question_url = "http://ec2-54-175-34-191.compute-1.amazonaws.com:8000/conversation_builder/question/"
    question_data = []
    for qid in qids:
        temp_url = question_url + str(qid)
        try:
            qdata = req.get(temp_url).json()
        except Exception as e:
            return e
        question_data.append(qdata)

    return question_data


def get_answer_data(qids):
    answer_url = "http://ec2-54-175-34-191.compute-1.amazonaws.com:8000/conversation_builder/answer"
    try:
        data = req.get(answer_url).json()
    except Exception as e:
        return e
    answer_data = {}
    for qid in qids:
        for answer in data:
            if qid in answer.get("qids"):
                if answer.get("text") is not None:
                    if answer_data.get(qid):
                        answer_data.get(qid).append(answer.get("text"))
                    else:
                        answer_data[qid] = [answer.get("text")]
                elif answer.get("range") is not None:
                    answer_data[qid] = answer.get("range")
                    break

    return answer_data


def main(request, chat_id):
    chat_url = "http://ec2-54-175-34-191.compute-1.amazonaws.com:8000/conversation_builder/chat/"
    chat_url += chat_id

    try:
        chat_data = req.get(chat_url).json()
    except Exception as e:
        return e

    qids = get_questions_id(chat_data)
    # it two functions for async ...
    questions_data = get_question_data(qids)
    answer_data = get_answer_data(qids)

    for question in questions_data:
        question["answer"] = answer_data.get(question.get("id"))
        del question["id"]

    return HttpResponse(f"chat_id: {chat_id}, \n details: \n   {questions_data}")
