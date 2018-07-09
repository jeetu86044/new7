from django.shortcuts import render
from django.http import  HttpResponse
import  requests
# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin
def index(request):
    if(request.POST):
        res = {}
        api_id = 'e6897aa7'
        api_key = '5f5095c3d2794fc1caa3f4ba24935a31'
        name = request.POST['name']
        url = 'https://od-api.oxforddictionaries.com:443/api/v1/search/en?q='+name.lower()+'&prefix=false'
        response = requests.get(url, headers={'app_id': api_id, 'app_key': api_key})
        #return HttpResponse(response.text)
        try:
            if response.status_code == 200:
                res = response.json()
                name = res['results'][0]['word']
                #print(name)
                url = 'https://od-api.oxforddictionaries.com:443/api/v1/entries/en/' + name.lower()
                response = requests.get(url,headers = {'app_id': api_id, 'app_key': api_key})
                if response.status_code == 200:
                    res = response.json()
                    audio_url = res['results'][0]['lexicalEntries'][0]['pronunciations'][0]['audioFile']
                    context = {
                    'res':res,
                    'valid':False,
                    'audio':audio_url,
                    }
                    return render(request,'words/index.html', context)

        except:
            return HttpResponse("<h2>Please enter valid english word</h2>")
        return HttpResponse("<h2>Please enter valid english word</h2>")

    else:
        context = {
            'valid': True,

        }
        return render(request,'words/index.html',context)