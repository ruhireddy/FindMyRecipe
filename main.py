import requests


def search(keyword):
    url = "https://tasty.p.rapidapi.com/recipes/auto-complete"
    querystring = {"prefix": keyword}
    headers = {
        'x-rapidapi-key': "84be2be528msh7d8ed75e3d510f9p11c16ajsn580152d87a12",
        'x-rapidapi-host': "tasty.p.rapidapi.com"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    print(response.text)



def main():
    keyword = input('Enter an ingredient: ')
    search(keyword)

if __name__ == "__main__":
    main()