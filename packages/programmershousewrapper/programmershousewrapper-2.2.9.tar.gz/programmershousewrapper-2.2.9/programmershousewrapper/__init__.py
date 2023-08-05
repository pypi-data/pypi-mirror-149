import requests
import json

def joke():
  url = "https://www.programmershouse-api.ga/joke"
  response = requests.get(url)
  data = response.text
  parse_json = json.loads(data)
  input = parse_json['ukraine']
  return input
  
def eightball(question:str ,property=None)->str:
    empty = ""
    if question ==None:
        raise TypeError("Give a question!")
    if question == empty:  
        raise TypeError("Give a question!")
    else:
        url = "https://www.programmershouse-api.ga/8ball?question="+question
        response = requests.get(url)
        data = response.text
        parse_json = json.loads(data)
        input = parse_json['ukraine']
        return input
   

def cats():
    url = "https://www.programmershouse-api.ga/cats"
    response = requests.get(url)
    data = response.text
    parse_json = json.loads(data)
    input = parse_json['ukraine']
    return input

def ukraine(avatar:str)->str:
    url = "https://www.programmershouse-api.ga/ukraine?avatar=" + avatar
    return url

def wanted(avatar:str)->str:
    url = "https://www.programmershouse-api.ga/wanted?avatar=" + avatar
    return url

def wasted(avatar:str)->str:
    url = "https://www.programmershouse-api.ga/wasted?avatar=" + avatar
    return url

def reddit(title:str,description:str,property=None)->str:
    empty = ""
    if title == None:
        raise TypeError("Give a title!")
    elif(title == empty):
        raise TypeError("Give a title!")
    elif description == None:
        raise TypeError("Give a description!")
    elif(description == empty):
        raise TypeError("Give a description!")
    else:
        url = "https://www.programmershouse-api.ga/reddit?title=" + title.replace(" ",'+') + "&description=" + description.replace(" ",'+')
        return url

def ukrmemes()->str:
    url = "https://www.programmershouse-api.ga/ukrmemes" 
    response = requests.get(url)
    data = response.json()
    return data

def reversetext(text:str,property=None)->str:
    empty = ""
    if text == None:
        raise TypeError("Give a text!")
    elif(text == empty):
        raise TypeError("Give a text!")
    else:
        url = "https://www.programmershouse-api.ga/reversetext?text=" + text 
        response = requests.get(url)
        data = response.text
        parse_json = json.loads(data)
        input = parse_json['ukraine']
        return input

def emojify(text:str,property=None)->str:
    empty = ""
    if text == None:
        raise TypeError("Give a text!")
    elif(text == empty):
        raise TypeError("Give a text!")
    else:
        url = "https://www.programmershouse-api.ga/emojify?text=" + text 
        response = requests.get(url)
        data = response.text
        parse_json = json.loads(data)
        input = parse_json['ukraine']
        return input

def shotoniphone()->str:
    url = "https://www.programmershouse-api.ga/shotoniphone"
    response = requests.get(url)
    data = response.text
    parse_json = json.loads(data)
    input = parse_json['ukraine']
    return input

def numberfact(number,property=None)->str:
    empty = ""
    if number == None:
        raise TypeError("Give a number!")
    elif(str(number) == empty):
        raise TypeError("Give a number!")
    else:
        url = "https://www.programmershouse-api.ga/numberfact?number=" + str(number) 
        response = requests.get(url)
        data = response.text
        parse_json = json.loads(data)
        input = parse_json['ukraine']
        return input

def yearsfact()->str:
    url = "https://www.programmershouse-api.ga/yearsfact"
    response = requests.get(url)
    data = response.text
    parse_json = json.loads(data)
    input = parse_json['ukraine']
    return input

def qrcode(text:str,property=None)->str:
    empty = ""
    if text == None:
        raise TypeError("Give a text!")
    elif(text == empty):
        raise TypeError("Give a text!")
    else:
        url = "https://www.programmershouse-api.ga/qrcode?text=" + text.replace(" ",'+')
        return url

def randomtext(text1,text2, property=None)->str:
    empty = ""
    if str(text1) == None:
        raise TypeError("Give a text!")
    elif str(text1) == empty:
        raise TypeError("Give a text!")
    elif str(text2) == None:
        raise TypeError("Give a text 2!")
    elif str(text2) == empty:
        raise TypeError("Give a text 2!")
    else:
        url = "https://www.programmershouse-api.ga/randomtext?text1="+ str(text1) +"&text2=" + str(text2) 
        response = requests.get(url)
        data = response.text
        parse_json = json.loads(data)
        input = parse_json['ukraine']
        return input

def currentday()->str:
    url = "https://www.programmershouse-api.ga/currentday"
    response = requests.get(url)
    data = response.text
    parse_json = json.loads(data)
    input = parse_json['ukraine']
    return input

def minecraftserver(ip:str, property=None)->str:
    empty = ""
    if ip == None:
        raise TypeError("Give a ip!")
    elif ip == empty:
        raise TypeError("Give a ip!")
    else:
        url = "https://www.programmershouse-api.ga/minecraftserver?ip="+ ip
        response = requests.get(url)
        data = response.text
        parse_json = json.loads(data)
        input = parse_json
        return input

def aboutinvite(code:str, property=None)->str:
    empty = ""
    if code == None:
        raise TypeError("Give a invite code!")
    elif code == empty:
        raise TypeError("Give a invite code!")
    else:
        url = "https://www.programmershouse-api.ga/aboutinvite?code="+ code
        response = requests.get(url)
        data = response.text
        parse_json = json.loads(data)
        input = parse_json
        return input

def mars()->str:
    url = "https://www.programmershouse-api.ga/mars"
    response = requests.get(url)
    data = response.text
    parse_json = json.loads(data)
    input = parse_json["ukraine"]
    return input

def geometrydash(username:str,property=None)->str:
    empty = ""
    if username == None:
        raise TypeError("Give a nickname!")
    elif username == empty:
        raise TypeError("Give a nickname!")
    else:
        url = "https://www.programmershouse-api.ga/geometrydash?username=" + username
        response = requests.get(url)
        data = response.text
        parse_json = json.loads(data)
        input = parse_json
        return input

def cosmosfacts()->str:
    url = "https://www.programmershouse-api.ga/cosmosfacts"
    response = requests.get(url)
    data = response.text
    parse_json = json.loads(data)
    input = parse_json["ukraine"]
    return input
def subreddit(redditname:str,property=None)->str:
    empty = ""
    if (redditname.startswith("r/") == False):
        raise TypeError("Give a name of subreddit, what is starting with r/ !")
    if redditname == None:
        raise TypeError("Give a name of subreddit!")
    elif redditname == empty:
        raise TypeError("Give a name of subreddit!")
    else:
        url = "https://www.programmershouse-api.ga/subreddit?name=" + redditname
        response = requests.get(url)
        data = response.text
        parse_json = json.loads(data)
        input = parse_json
        return input

def randomanime()->str:
    url = "https://www.programmershouse-api.ga/randomanime"
    response = requests.get(url)
    data = response.text
    parse_json = json.loads(data)
    input = parse_json['ukraine']
    return input

def hug()->str:
    url = "https://www.programmershouse-api.ga/hug"
    response = requests.get(url)
    data = response.text
    parse_json = json.loads(data)
    input = parse_json['ukraine']
    return input

def cry()->str:
    url = "https://www.programmershouse-api.ga/cry"
    response = requests.get(url)
    data = response.text
    parse_json = json.loads(data)
    input = parse_json['ukraine']
    return input

def dance()->str:
    url = "https://www.programmershouse-api.ga/dance"
    response = requests.get(url)
    data = response.text
    parse_json = json.loads(data)
    input = parse_json['ukraine']
    return input

def laugh()->str:
    url = "https://www.programmershouse-api.ga/laugh"
    response = requests.get(url)
    data = response.text
    parse_json = json.loads(data)
    input = parse_json['ukraine']
    return input

def kiss()->str:
    url = "https://www.programmershouse-api.ga/kiss"
    response = requests.get(url)
    data = response.text
    parse_json = json.loads(data)
    input = parse_json['ukraine']
    return input

def pat():
    url = "https://www.programmershouse-api.ga/pat"
    response = requests.get(url)
    data = response.text
    parse_json = json.loads(data)
    input = parse_json['ukraine']
    return input

def alerts():
    url = "https://www.programmershouse-api.ga/alerts"
    response = requests.get(url)
    data = response.text
    parse_json = json.loads(data)
    input = parse_json['ukraine']
    return input

def wink()->str:
    url = "https://www.programmershouse-api.ga/wink"
    response = requests.get(url)
    data = response.text
    parse_json = json.loads(data)
    input = parse_json['ukraine']
    return input

def punch()->str:
    url = "https://www.programmershouse-api.ga/punch"
    response = requests.get(url)
    data = response.text
    parse_json = json.loads(data)
    input = parse_json['ukraine']
    return input
def hentai(key:str,property=None)->str:
    empty = ""
    if key == None:
            raise TypeError("Give a key! To get a key, join this server: https://discord.gg/caPZmZY9KF, create ticket and ask owners for key")
    elif key == empty:
            raise TypeError("Give a key! To get a key, join this server: https://discord.gg/caPZmZY9KF, create ticket and ask owners for key")
    else: 
      try:
        url = "https://www.programmershouse-api.ga/hentai?key=" + key
        response = requests.get(url)
        data = response.text
        parse_json = json.loads(data)
        input = parse_json['ukraine']
        return input
      except KeyError:
          raise TypeError("Invalid key!")