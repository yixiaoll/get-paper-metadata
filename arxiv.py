import requests
import pandas as pd
import xml.etree.ElementTree as ET


search_terms = [
"search phrase 1",
"search phrase 2"
]


def fetch_all_papers():
    dfs = []
    for term in search_terms:
        print(f"Fetching papers for: {term}")
        dfs.append(fetch_from_arxiv(term))
    combined_df = pd.concat(dfs, ignore_index=True)
    combined_df['Record Order'] = combined_df.groupby(['Source', 'Search Phrase']).cumcount() + 1
    combined_df.to_csv('arxiv.csv', index=False)

def fetch_from_arxiv(query):
    base_url = 'http://export.arxiv.org/api/query?'
    params = {
        'search_query': query,
        'start': 0,
        'max_results': 50
    }
    response = requests.get(base_url, params=params)
    papers = []
    if response.status_code == 200:
        root = ET.fromstring(response.text)
        for i, entry in enumerate(root.findall('{http://www.w3.org/2005/Atom}entry')):
            journal_ref = entry.find('{http://arxiv.org/schemas/atom}journal_ref')
            doi = entry.find('{http://arxiv.org/schemas/atom}doi')
            papers.append({
                'DOI': doi.text.strip() if doi is not None else 'N/A',
                'Source': 'ArXiv',
                'Search Phrase': query,
                'Title': entry.find('{http://www.w3.org/2005/Atom}title').text.strip(),
                'Year Published': entry.find('{http://www.w3.org/2005/Atom}published').text[:4],
                'Venue': journal_ref.text.strip() if journal_ref is not None else 'arXiv',
                'Authors': ', '.join([author.find('{http://www.w3.org/2005/Atom}name').text for author in entry.findall('{http://www.w3.org/2005/Atom}author')]),
                'Abstract': entry.find('{http://www.w3.org/2005/Atom}summary').text.strip(),
                'URL': entry.find('{http://www.w3.org/2005/Atom}link[@rel="alternate"]').attrib['href']
            })
    return pd.DataFrame(papers)

# Run the script
fetch_all_papers()
