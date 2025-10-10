import urllib.request

def isConnected():
    try:
        urllib.request.urlopen('https://www.google.com', timeout=3)
        return True
    except:
        return False