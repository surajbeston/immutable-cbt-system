from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from .models import Examiner, Examiner_score
from .forms import ExaminerForm

from .serializers import ScoreSerializer

from datetime import datetime
import hashlib
import json

from rest_framework.decorators import api_view


def simple_get(request):
    return HttpResponse('sdjhfkjh')


def create_examiner(request):
    form = ExaminerForm()
    if request.method == "GET":
        return render(request, "api/form.html", {"form": form})
    form = ExaminerForm(request.POST)
    if form.is_valid():
        print("valid form")
        hashed_email = hashlib.md5(form.cleaned_data["email"].encode())
        data = form.cleaned_data
        obj = Examiner( name = data["name"], email = data["email"], exam_id = hashed_email.hexdigest() )
        obj.save()
        return render(request, "api/registered.html", {"id": hashed_email.hexdigest()})
    else:
        print ("Probably CSRF token is missing!")
    return render(request, "api/form.html", {"form": form, "error": "Either CSRF token is missing or email is already registered."})


@api_view(['GET', 'POST'])
def save_score(request):
    data = request.data
    print (request.data)
    print ("This is damn immutable")
    user = Examiner.objects.get(exam_id = data["id"])
    if user.exam_taken == False:
        user.exam_taken = True
        user.save()
        examiners = Examiner_score.objects.all()
        for last_user in examiners:
            pass
        toHash = str(data["score"]) + last_user.hashed
        hash = hashlib.md5(toHash.encode())
        obj = Examiner_score(user = user, score = data["score"], hashed = hash.hexdigest())
        obj.save()
        return JsonResponse({"detail": "saved", "hash": hash.hexdigest()})
    else:
        return JsonResponse({"detail" : "exam already taken."})

def get_user(request):
    data = request.POST
    try:
        user = Examiner.objects.get(exam_id = data["id"])
        return JsonResponse({"detail": "ok", "id": user.exam_id, "name": user.name, "exam_ready": True})
    except:
        return JsonResponse({"detail": "id invalid"})

@api_view(['GET', 'POST'])
def rank_examiners(request):
    data = request.data
    ranked_objs = Examiner_score.objects.order_by("datetime_created")
    for  score_obj in ranked_objs:
        if score_obj.user.exam_id == data["id"]:
            rank = get_rank(ranked_objs, score_obj)
            serializer = ScoreSerializer(ranked_objs, many = True)
            names = []
            for ranked_obj in ranked_objs:
                names.append(ranked_obj.user.name)
            return JsonResponse({"detail": "ok","rank": rank, 'users': serializer.data,"name": score_obj.user.name, "score": score_obj.score, "names": names, "hash": score_obj.hashed})
    return JsonResponse({"detail": "invalid id"})


def get_rank(score_objs, this_obj):
    score_list = []
    for score in score_objs:
        score_list.append(score.score)
    score_list = list(dict.fromkeys(score_list))
    score_list.sort()
    print (score_list)
    for index, score in enumerate(score_list):
        if score == this_obj.score:
            rank = index + 1
            rank = rank - len(score_list)
            if rank < 0:
                rank *= -1
            return rank
