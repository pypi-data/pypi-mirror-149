import requests
import hashlib


def generate_game(config):
  emergencynotice = config['emergencynotice']
  background = config['background_image_url']
  r = requests.get("https://fortnitecontent-website-prod07.ol.epicgames.com/content/api/pages/fortnite-game").json()
  r['emergencynoticev2']['emergencynotices']['emergencynotices'] = [{
          "gamemodes": [
            "stw",
            "br"
          ],
          "hidden": False,
          "_type": "CommonUI Emergency Notice Base",
          "title": f"{emergencynotice}",
          "body": f"Backend Made By noteason and Pirxcy\ngithub.com/BoogieFN/BoogieFN-Backend"
        }]
  
  r['dynamicbackgrounds']['backgrounds']['backgrounds'] = {
  "backgroundimage": f"{background}",
  "stage": "season20",
  "_type": "DynamicBackground",
  "key": "lobby"
  },
  {
  "stage": "default",
  "_type": "DynamicBackground",
  "key": "vault"
  }
  return r

def generate_cloudstorage(path):
  DefaultEngine = open(f"{path}/DefaultEngine.ini").read()
  
  DefaultEnginel = len(open(f"{path}/DefaultEngine.ini").readlines())
  
  DefaultGame = open(f"{path}/DefaultGame.ini").read()
  
  DefaultGamel = len(open(f"{path}/DefaultGame.ini").readlines())
  
  DefaultRuntimeOptions = open(f"{path}/DefaultRuntimeOptions.ini").read()
  
  DefaultRuntimeOptionsl= len(open(f"{path}/DefaultRuntimeOptions.ini").readlines())

  
  now = '"'+str(time.time())+'"'

  sha256 = hashlib.sha256()
  sha1 = hashlib.sha1()

  sha1.update(DefaultGame.encode())
  dghash1 = '"'+ sha1.hexdigest() +'"'
  sha1.update(DefaultEngine.encode())
  dehash1 = '"'+ sha1.hexdigest() +'"'
  sha1.update(DefaultRuntimeOptions.encode())
  drohash1 = '"'+ sha1.hexdigest() +'"'
  sha256.update(DefaultGame.encode())
  dghash256 = '"'+ sha256.hexdigest() +'"'
  sha256.update(DefaultEngine.encode())
  dehash256 = '"'+ sha256.hexdigest() +'"'
  sha256.update(DefaultRuntimeOptions.encode())
  drohash256 = '"'+ sha256.hexdigest() +'"'
  cloudstorage = json.loads("""[{"uniqueFilename":"DefaultEngine.ini","filename":"DefaultEngine.ini","hash":""" +dehash1+ ""","hash256":""" +dehash256+ ""","length":"""+str(DefaultEnginel)+""","contentType":"application/octet-stream","uploaded":"someday","storageType":"S3","doNotCache":false},{"uniqueFilename":"DefaultGame.ini","filename":"DefaultGame.ini","hash":""" +dghash1+ ""","hash256":""" +dghash256+ ""","length":"""+str(DefaultGamel)+""","contentType":"application/octet-stream","uploaded":"someday","storageType":"S3","doNotCache":false},{"uniqueFilename":"DefaultRuntimeOptions.ini","filename":"DefaultRuntimeOptions.ini","hash":"""+drohash1+""","hash256":"""+drohash256+""","length":"""+str(DefaultRuntimeOptionsl)+""","contentType":"application/octet-stream","uploaded":"someday","storageType":"S3","doNotCache":false},{"uniqueFilename":"config","filename":"config","hash":"da39a3ee5e6b4b0d3255bfef95601890afd80709","hash256":"e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855","length":0,"contentType":"application/octet-stream","uploaded":"someday","storageType":"S3","doNotCache":false}]""")
  return cloudstorage
