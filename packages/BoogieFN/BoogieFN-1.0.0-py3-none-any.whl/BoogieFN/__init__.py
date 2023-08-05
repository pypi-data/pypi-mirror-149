import requests



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