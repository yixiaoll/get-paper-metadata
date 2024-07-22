import requests
import pandas as pd


search_terms = [
"search phrase 1",
"search phrase 2"
]

def fetch_all_papers():
    dfs = []
    for term in search_terms:
        print(f"Fetching papers for: {term}")
        dfs.append(fetch_from_semantic_scholar(term))
    combined_df = pd.concat(dfs, ignore_index=True)
    combined_df['Record Order'] = combined_df.groupby(['Source', 'Search Phrase']).cumcount() + 1
    combined_df.to_csv('ieee.csv', index=False)

def fetch_from_semantic_scholar(query):
    url = "https://api.semanticscholar.org/graph/v1/paper/search"
    headers = {
        'x-api-key': 'API key',         # Replace with your API key
        'Content-Type': 'application/json'
    }
    params = {'query': query, 'limit': 50, 'fields': 'paperId,externalIds,url,title,venue,year,authors,abstract'}
    response = requests.get(url, headers=headers, params=params)
    results = []
    if response.status_code == 200:
        data = response.json()['data']
        for item in data:
            results.append({
                'DOI': item['externalIds'].get('DOI', 'N/A'),
                'Source': 'Semantic Scholar',
                'Search Phrase': query,
                'Title': item['title'],
                'Year Published': item['year'],
                'Venue': item['venue'],
                'Authors': ', '.join(author['name'] for author in item['authors']),
                'Abstract': item['abstract'],
                'URL': item['url']
            })
    return pd.DataFrame(results)

# Run the script
fetch_all_papers()
