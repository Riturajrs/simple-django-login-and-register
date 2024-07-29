import requests
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.core.cache import cache


@api_view(['GET'])
def ping(request):
    if request.user.is_authenticated:
        return Response('Authenticated')
    else:
        return Response('Un-authenticated')

def listAllCoins(request):
    if not request.user.is_authenticated:
        PermissionError("Unauthenticated user!")

    url = "https://api.coingecko.com/api/v3/coins/list"
    cache_key = 'coins_list'
    coins = cache.get(cache_key)

    if not coins:
        try:
            response = requests.get(url)
            response.raise_for_status()
            coins = response.json()
            cache.set(cache_key, coins, 60*60)
        except requests.exceptions.RequestException as error:
            request.error = str(error)
            return render(request, "main/index.html")

    page_number = int(request.GET.get("page_num", 1))
    start_index = (page_number - 1) * 10
    end_index = start_index + 10
    paginated_coins = coins[start_index:end_index]
    
    request.coins = paginated_coins
    request.page_number = page_number
    request.last_page = (end_index >= len(coins))
    
    return render(request, "main/index.html")

def getCoinDetails(request):
    if not request.user.is_authenticated:
        PermissionError("Unauthenticated user!")
    coin_id = request.GET.get("coin_id", "bitcoin")
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}"
    cache_key = {coin_id}
    coin_details = cache.get(cache_key)

    if not coin_details:
        try:
            response = requests.get(url)
            response.raise_for_status()
            coin_details = response.json()
            cache.set(cache_key, coin_details, 60*60)
        except requests.exceptions.RequestException as error:
            request.error = str(error)
            return render(request, "main/index.html")

    request.coin_details = coin_details    
    return render(request, "main/coin-details.html")