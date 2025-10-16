import requests
from bs4 import BeautifulSoup

# Function to get film details from a single page
def get_films_from_page(page_url):
    films = []
    response = requests.get(page_url)
    print(f"Fetching URL: {page_url}")
    print(f"Response Status Code: {response.status_code}")
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        # film_items = soup.find_all('li', class_='poster-container film-watched')
        film_items = soup.select('li.poster-container film-watched')
        print(f"Found {len(film_items)} film items on the page.")
        
        # Extracting film names
        for film in film_items:
            film_div = film.find('div', class_=['react-component', 'poster'])
            if film_div:
                film_name = film_div.get('data-film-name')
                films.append(film_name)
    else:
        print("Failed to retrieve the page.")
    return films

# Function to handle pagination and gather films from multiple pages
def get_all_films(base_url, pages=5):
    all_films = []
    for page_num in range(1, pages + 1):
        page_url = f'{base_url}/page/{page_num}'
        films = get_films_from_page(page_url)
        if films:
            all_films.extend(films)
        else:
            break  # If a page has no films, stop scraping
    return all_films

# Main execution
if __name__ == "__main__":
    user_profile_url = 'https://letterboxd.com/mxc48/films'
    all_watched_films = get_all_films(user_profile_url, pages=5)  # Set pages as needed
    print("Films I've watched:")
    for film in all_watched_films:
        print(film)