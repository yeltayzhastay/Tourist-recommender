from django.shortcuts import render
from django.http import HttpResponse
from .forms import MLForm
from mlrecommend.recommender import TuristRecommender
 
def index(request):
    if request.method == "POST":
        text = request.POST.get("text")
        tr = TuristRecommender()
        results = tr.predict(text)
        mlform = MLForm()
        data = {"form": mlform, 'urls': results}
        return render(request, "index.html", context=data)
    else:
        mlform = MLForm()
        data = {"form": mlform}
        return render(request, "index.html", context=data)

def recommend(request):
    return HttpResponse("Recommend")