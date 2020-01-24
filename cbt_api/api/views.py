from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from .models import Examiner, Examiner_score
from .forms import ExaminerForm

from datetime import datetime
import hashlib
import json


def create_examiner(request):
    form = ExaminerForm()
    if request.method == "GET":
        return render(request, "api/form.html", {"form": form})
    form = ExaminerForm(request.POST)
    if form.is_valid():
        print("valid form")
        hashed_email = hashlib.md5(form.cleaned_data["email"].encode())
        data = form.cleaned_data
        obj = Examiner(name = data["name"], email = data["email"], exam_id = hashed_email.hexdigest() )
        obj.save()
        return render(request, "api/registered.html", {"id": hashed_email.hexdigest()})
    else:
        print ("Probably CSRF token is missing!")
    return render(request, "api/form.html", {"form": form, "error": "Either CSRF token is missing or email is already registered."})

def save_score(request):
    data = json.loads(request.body)
    try:
        user = Examiner.objects.get(exam_id = data["id"])
    except:
        return JsonResponse({"detail": "invalid id"})
    if user.exam_taken == False:
        user.exam_taken = True
        user.save()
        obj = Examiner_score(user = user, score = data["score"])
        obj.save()
        return JsonResponse({"detail": "saved"})
    else:
        return JsonResponse({"detail": "exam already taken."})

def rank_examiners(request):
    data = json.loads(request.body)
    ranked_objs = Examiner_score.objects.order_by("score")
    for  score_obj in ranked_objs:
        if score_obj.user.exam_id == data["id"]:
            rank = get_rank(ranked_objs, score_obj)
            return JsonResponse({"rank": rank, "name": score_obj.user.name})
    return JsonResponse({"detail": "invalid id"})


def get_rank(score_objs, this_obj):
    score_list = []
    for score in score_objs:
        score_list.append(score.score)
    score_list = list(dict.fromkeys(score_list))
    score_list.sort()
    for index, score in enumerate(score_list):
        if score == this_obj.score:
            return index + 1
