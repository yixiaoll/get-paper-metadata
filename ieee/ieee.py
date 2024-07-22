import json
import xploreapi
import pandas as pd


search_terms = [
"search phrase 1",
"search phrase 2"
]

def fetch_all_papers():
    dfs = []
    for term in search_terms:
        print(f"Fetching papers for: {term}")
        dfs.append(fetch_from_ieee(term))
    combined_df = pd.concat(dfs, ignore_index=True)
    combined_df['Record Order'] = combined_df.groupby(['Source', 'Search Phrase']).cumcount() + 1
    combined_df.to_csv('ieee.csv', index=False)

def fetch_from_ieee(query):
    api_key = 'API KEY'             # Replace with your IEEE API key
    xplore = xploreapi.XPLORE(api_key)
    xplore.dataType('json')
    xplore.maximumResults(50)
    xplore.queryText(query)
    results = xplore.callAPI()
    papers = []
    if results:
        data = json.loads(results)
        for item in data.get('articles', []):
            authors_data = item.get('authors', {}).get('authors', [])
            authors = [author.get('full_name', 'Unknown') for author in authors_data if isinstance(author, dict)]
            papers.append({
                'DOI': item.get('doi', 'N/A'),
                'Source': 'IEEE',
                'Search Phrase': query,
                'Title': item['title'],
                'Year Published': item.get('publication_year', 'N/A'),
                'Venue': item.get('publication_title', 'N/A'),
                'Authors': ', '.join(authors),
                # No abstract available
                'Abstract': item.get('abstract', 'No abstract available'),
                'URL': item.get('html_url', 'No URL available')
            })
    return pd.DataFrame(papers)

# Run the script
fetch_all_papers()
