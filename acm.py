import requests
from bs4 import BeautifulSoup
import random
import pandas as pd


# Define User-Agents for ACM scraping
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.4 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; AS; rv:11.0) like Gecko",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
]

search_terms = [
"search phrase 1",
"search phrase 2"
]

def get_random_headers():
    return {'User-Agent': random.choice(USER_AGENTS)}

def fetch_all_papers():
    dfs = []
    for term in search_terms:
        print(f"Fetching papers for: {term}")
        dfs.append(fetch_from_acm(term))
    combined_df = pd.concat(dfs, ignore_index=True)
    combined_df['Record Order'] = combined_df.groupby(['Source', 'Search Phrase']).cumcount() + 1
    combined_df.to_csv('acm.csv', index=False)

def fetch_from_acm(query):
    search_query = query.replace(' ', '+')
    base_url = "https://dl.acm.org/action/doSearch?AllField="
    results = []
    page = 0
    with requests.Session() as session:
        session.headers.update(get_random_headers())
        while len(results) < 50:
            url = f"{base_url}{search_query}&startPage={page}"
            response = session.get(url)
            if response.status_code != 200:
                break
            soup = BeautifulSoup(response.text, 'html.parser')
            articles = soup.find_all('div', class_='issue-item__content')
            for article in articles:
                if len(results) >= 50:
                    break
                title_element = article.find('h5', class_='issue-item__title')
                link_element = article.find('a')
                venue_element = article.find('span', class_='epub-section__title')
                venue = venue_element.get_text(strip=True) if venue_element else "N/A"
                if title_element and link_element:
                    link = f"https://dl.acm.org{link_element['href']}"
                    details_response = session.get(link)
                    details_soup = BeautifulSoup(details_response.text, 'html.parser')
                    
                    # title
                    title_tag = details_soup.find('h1', {'property': 'name'})
                    title = title_tag.text if title_tag else "N/A"
                    
                    # Extract DOI
                    doi_element = details_soup.find('div', class_='doi')
                    if doi_element:
                        doi_url = doi_element.get_text(strip=True)
                        doi = doi_url.split('https://doi.org/')[1] if 'https://doi.org/' in doi_url else "DOI format error"
                    else:
                        doi = "N/A"

                    # Extract Published Year
                    published_element = details_soup.find('span', class_='core-date-published')
                    published_year = published_element.get_text(strip=True)[-4:] if published_element else "N/A"
    
                    abstract_section = details_soup.find('section', id='abstract')
                    abstract_element = abstract_section.find('div', role='paragraph') if abstract_section else None
                    abstract = abstract_element.text.strip() if abstract_element else "N/A"

                    # Find all spans or divs where the 'role' attribute is 'listitem' and 'typeof' attribute is 'Person'
                    author_elements = details_soup.find_all('span', {'role': 'listitem', 'typeof': 'Person'})

                    # List to hold the names of the authors
                    authors = []

                    # Iterate through each found element and extract names
                    for element in author_elements:
                        given_name = element.find('span', {'property': 'givenName'})
                        family_name = element.find('span', {'property': 'familyName'})
                        
                        # Check if either name part is missing
                        full_name = f"{given_name.text if given_name else 'N/A'} {family_name.text if family_name else 'N/A'}"
                        authors.append(full_name)
                                        
                    results.append({
                        'DOI': doi,
                        'Source': 'ACM',
                        'Search Phrase': query,
                        'Title': title,
                        'Year Published': published_year,
                        'Venue': venue,
                        'Authors': ', '.join(authors) if authors else "N/A",
                        'Abstract': abstract,
                        'URL': link
                    })
            page += 1
    return pd.DataFrame(results)


# Run the script
fetch_all_papers()
