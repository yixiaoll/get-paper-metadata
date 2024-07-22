from scholarly import scholarly
import pandas as pd


search_terms = [
"search phrase 1",
"search phrase 2"
]

def fetch_all_papers():
    dfs = []
    for term in search_terms:
        print(f"Fetching papers for: {term}")
        dfs.append(fetch_from_google_scholar(term))
    combined_df = pd.concat(dfs, ignore_index=True)
    combined_df['Record Order'] = combined_df.groupby(['Source', 'Search Phrase']).cumcount() + 1
    combined_df.to_csv('google_scholar.csv', index=False)

def fetch_from_google_scholar(query):
    search_query = scholarly.search_pubs(query)
    results = []
    try:
        for _ in range(50):
            paper = next(search_query)
            results.append({
                'DOI': 'N/A',
                'Source': 'Google Scholar',
                'Search Phrase': query,
                'Title': paper['bib'].get('title', 'No title available'),
                'Year Published': paper['bib'].get('pub_year', 'No year available'),
                'Venue': paper['bib'].get('venue', 'No venue available'),
                'Authors': ', '.join(paper['bib'].get('author', [])),
                # No abstract available
                'Abstract': paper['bib'].get('abstract', 'No abstract available'),
                'URL': paper.get('pub_url', 'No URL available')
            })
    except StopIteration:
        pass
    return pd.DataFrame(results)

# Run the script
fetch_all_papers()
