from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Stock
from .serializer import StockSerializer
import requests
from decouple import config
def get_current_price(ticker):
    url = 'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=' + ticker + '&apikey='+config('API_KEY')
    try:
        r = requests.get(url)
        r.raise_for_status()
        apiresponse = r.json()
        return apiresponse['Global Quote']['05. price']
    except (requests.RequestException, KeyError):
        # Return dummy data if the API call fails
        return 100.00  # Mock price value

@api_view(['GET'])
def get_stocks(request):
    stocks=Stock.objects.all()
    serializedData=StockSerializer(stocks, many=True).data
    
    for stock in serializedData:
        stock['currentPrice']=get_current_price(stock['ticker'])
    return Response(serializedData)
    

def get_ticker_name(ticker):
    base_url = "https://www.alphavantage.co/query"
    params = {
        "function": "SYMBOL_SEARCH",
        "keywords": ticker,
        "apikey": config('API_KEY')
    }
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        matches = data.get("bestMatches", [])
        if matches:
            return matches[0]["2. name"]  # Extract the name of the first match
    except (requests.RequestException, KeyError):
        # Return dummy data if the API call fails
        return "Dummy Company Name"
    return False

@api_view(['POST'])
def create_stock(request):
    data = request.data
    try:
        url = 'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=' + data['ticker'] + '&apikey=938T5WL5N9GFPGLV'
        r = requests.get(url)
        r.raise_for_status()
        apiresponse = r.json()
        data['buy_price'] = apiresponse['Global Quote']['05. price']
        data['name'] = get_ticker_name(data['ticker'])
    except (requests.RequestException, KeyError):
        # Use dummy values for development
        data['buy_price'] = 100.00
        data['name'] = "Dummy Company Name"
    
    if not data['name']:
        return Response({'error': 'No match found'}, status=status.HTTP_400_BAD_REQUEST)
    serializer = StockSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def update_stock(request, pk):
    
    try:
        original_stock=Stock.objects.get(pk=pk)
        stock = Stock.objects.filter(pk=pk).values().first()
    except Stock.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    data = request.data
    stock['quantity']=max(0,data['quantity'])
    if not stock['quantity']:
        
        serializer = StockSerializer(original_stock,data=stock)
        original_stock.delete()
        if serializer.is_valid():
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    serializer = StockSerializer(original_stock,data=stock)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_stock(request, pk):
    try:
        stock = Stock.objects.get(pk=pk)
    except Stock.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    stock.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
