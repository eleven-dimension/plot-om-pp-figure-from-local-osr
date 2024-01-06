import requests

def make_api_request(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print(f"error code: {response.status_code}")
    except requests.RequestException as e:
        print(f"error: {e}")


api_url = "https://osu.ppy.sh/api/get_beatmaps?k=b03936ca56264f6a08f27637229aa18ef04fa707&h=00cb6228a2af3a8f6b7b25b386a13a8e"
response_data = make_api_request(api_url)

if response_data:
    print(response_data)
