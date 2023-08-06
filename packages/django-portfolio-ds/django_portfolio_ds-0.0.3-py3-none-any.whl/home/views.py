from django.shortcuts import render


def home(request):
    context = {
        "theme": "medilab_ds",
        'color': "default",
        "portfolio": {
            'title': "케이스",
            'subtitle': '주목할 만한 치과 케이스 모음',
        }
    }
    return render(request, f"home.html", context)
