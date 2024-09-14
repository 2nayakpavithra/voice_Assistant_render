import requests
def joke():
    url = "https://official-joke-api.appspot.com/random_joke"
    json_data = requests.get(url).json()

    setup = json_data["setup"]
    punchline = json_data["punchline"]

    return setup, punchline
