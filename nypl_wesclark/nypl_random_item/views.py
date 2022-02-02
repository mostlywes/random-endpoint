from django.http import HttpResponseBadRequest, JsonResponse, HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import View
import requests
import json
import random

# Create your views here.


def index(request):
    type_of_resource_options = ["still image", "text", "cartographic",
                                "moving image", "notated music", "sound recording", "three dimensional object",
                                "sound recording-musical", "sound recording-nonmusical"]
    context = {'type_of_resource_options': type_of_resource_options}
    return render(request, 'nypl_random_item/index.html', context)


class RandomItemView(View):

    def get(self, request):
        # returns most recent 500 captures added
        url = 'http://api.repo.nypl.org/api/v1/items/recent?per_page=500&page=1'
        # print(request.headers.get('Authorization'))
        headers = {'Authorization': request.headers.get('Authorization')}
        # get resource type url parameter or return 400 error
        if request.GET.get('type_of_resource', ''):
            parameter_value = str(request.GET.get('type_of_resource'))
        else:
            return HttpResponseBadRequest("You didn't select a valid resource type option.")
        captures = requests.get(url, headers=headers)
        data = captures.json()
        # drill down into the returned data to isolate capture properties
        result = data['nyplAPI']['response']['capture']
        # loop through result and build list with typeOfResource key with value that matches the resource type parameter
        possible_matches_to_parameter = []
        for r in result:
            if r['typeOfResource']['$'] == parameter_value:
                possible_matches_to_parameter.append(r)
        # if we found a typeOfResource key that matched the parameter, choose one at random and get its properties
        if possible_matches_to_parameter:
            randomNumber = random.randint(
                0, len(possible_matches_to_parameter) - 1)
            randomCaptureUuid = possible_matches_to_parameter[randomNumber]['uuid']['$']
            randomCaptureType_of_resource = possible_matches_to_parameter[
                randomNumber]['typeOfResource']['$']
            randomCaptureItemLink = possible_matches_to_parameter[randomNumber]['itemLink']['$']

            random_item_data = {
                'uuid': randomCaptureUuid,
                'type_of_resource': randomCaptureType_of_resource,
                'item_link': randomCaptureItemLink,
            }

            return HttpResponse(json.dumps(random_item_data), content_type='application/json')
        # if we didn't find a typeOfResource key that matched, let the user know
        else:
            return HttpResponse("Looks like we haven't added anything recent of that type!")
