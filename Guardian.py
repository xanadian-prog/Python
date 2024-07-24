import requests
from bs4 import BeautifulSoup

def get_guardian_headlines():
    url = "https://www.theguardian.com/uk"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        
        soup = BeautifulSoup(response.content, 'html.parser')
        headlines = soup.find_all('h3')
        
        if headlines:
            for i, headline in enumerate(headlines, start=1):
                print(f"{i}. {headline.get_text()}")
        else:
            print("No headlines found.")
    
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    get_guardian_headlines()
