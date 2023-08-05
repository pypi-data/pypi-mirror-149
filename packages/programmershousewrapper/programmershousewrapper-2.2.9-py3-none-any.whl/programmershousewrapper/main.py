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
        raise TypeError("Вкажи запитання!")
    if question == empty:  
        raise TypeError("Вкажи запитання!")
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
        raise TypeError("Вкажи Заголовок!")
    elif(title == empty):
        raise TypeError("Вкажи Заголовок!")
    elif description == None:
        raise TypeError("Вкажи Опис!")
    elif(description == empty):
        raise TypeError("Вкажи Опис!")
    else:
        url = "https://www.programmershouse-api.ga/reddit?title=" + title + "description=" + description
        response = requests.get(url)
        data = response.text
        parse_json = json.loads(data)
        input = parse_json['ukraine']
        return input

def ukrmemes()->str:
    url = "https://www.programmershouse-api.ga/ukrmemes" 
    response = requests.get(url)
    data = response.text
    parse_json = json.loads(data)
    input = parse_json
    return input

def reversetext(text:str,property=None)->str:
    empty = ""
    if text == None:
        raise TypeError("Вкажи текст!")
    elif(text == empty):
        raise TypeError("Вкажи текст!")
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
        raise TypeError("Вкажи текст!")
    elif(text == empty):
        raise TypeError("Вкажи текст!")
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
        raise TypeError("Вкажи число!")
    elif(str(number) == empty):
        raise TypeError("Вкажи число!")
    else:
        url = "https://www.programmershouse-api.ga/numberfact?number=" + str(number) 
        response = requests.get(url)
        data = response.text
        parse_json = json.loads(data)
        input = parse_json['ukraine']
        return input

def qrcode(text:str,property=None)->str:
    empty = ""
    if text == None:
        raise TypeError("Вкажи текст!")
    elif(text == empty):
        raise TypeError("Вкажи текст!")
    else:
        url = "https://www.programmershouse-api.ga/qrcode?text=" + text 
        return url

def randomtext(text1,text2, property=None)->str:
    empty = ""
    if str(text1) == None:
        raise TypeError("Вкажи текст!")
    elif str(text1) == empty:
        raise TypeError("Вкажи текст!")
    elif str(text2) == None:
        raise TypeError("Вкажи текст!")
    elif str(text2) == empty:
        raise TypeError("Вкажи текст!")
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
        raise TypeError("Вкажи ip!")
    elif ip == empty:
        raise TypeError("Вкажи ip!")
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
        raise TypeError("Вкажи  код запрошення!")
    elif code == empty:
        raise TypeError("Вкажи код запрошення!")
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
        raise TypeError("Вкажи нік!")
    elif username == empty:
        raise TypeError("Вкажи нік!")
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
        raise TypeError("Вкажи через r/ !")
    if redditname == None:
        raise TypeError("Вкажи нік!")
    elif redditname == empty:
        raise TypeError("Вкажи нік!")
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
    if (key.find('key') < 0):
        raise TypeError("Вкажи ключ! Щоб отримати ключ зайди на наш сервер https://discord.gg/caPZmZY9KF, створи білет та попроси у власників")
    else:
         if key == None:
            raise TypeError("Вкажи ключ!")
         elif key == empty:
            raise TypeError("Вкажи ключ!")
         else:
            url = "https://www.programmershouse-api.ga/hentai?key=" + key
            response = requests.get(url)
            data = response.text
            parse_json = json.loads(data)
            input = parse_json['ukraine']
            return input