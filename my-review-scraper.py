import requests
from bs4 import BeautifulSoup

# Base URL and target output file
base_url = "https://letterboxd.com/mxc48/films/reviews/page/"
output_file = "my_letterboxd_reviews.txt"

# Initialize the page number
page_num = 1
reviews_exist = True

# Open the output file
with open(output_file, "w", encoding="utf-8") as file:
    while reviews_exist:
        # Construct URL for each paginated page
        url = f"{base_url}{page_num}"
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Failed to retrieve page {page_num}")
            break

        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        reviews = soup.select('li.film-detail')

        # Stop if there are no reviews on this page
        if not reviews:
            reviews_exist = False
            continue

        # Extract reviews and write to file
        for review in reviews:
            # Extract film title, year, rating, and review text
            title = review.select_one('h2.headline-2 a').text
            year = review.select_one('small.metadata a').text
            rating = review.select_one('span.rating').text.strip() if review.select_one('span.rating') else "No rating"
            review_text = review.select_one('div.body-text').text.strip()

            # Write formatted data to file
            file.write(f"Title: {title} ({year})\n")
            file.write(f"Rating: {rating}\n")
            file.write(f"Review: {review_text}\n")
            file.write("\n" + "="*40 + "\n\n")

        print(f"Page {page_num} processed.")
        page_num += 1

print("All reviews fetched and saved.")
