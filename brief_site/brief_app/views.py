from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse


# Create your views here.
def index(request):
    return render(request, 'brief_app/index.html')

def response_site_data(request):
    data_site = {
        'data': [
            {
                'Id': 1,
                'Name': 'Quang',
                'Category': 'K01',
                'Note': 'Happy National day'
            },
            {
                'Id': 2,
                'Name': 'Phuong',
                'Category': 'K02',
                'Note': 'Try hard to be the best of me'
            }
        ]
    }
    print('HERE')
    return JsonResponse(data_site)

