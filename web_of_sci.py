import requests
import csv

def retrieve_wos_data(api_key, search_phrases, count=50):
    url = "https://wos-api.clarivate.com/api/wos"
    headers = {
        'X-ApiKey': api_key,
        'Accept': 'application/json'
    }
    all_papers = []
    for search_phrase in search_phrases:
        params = {
            'databaseId': 'WOS',
            'usrQuery': f"ts=({search_phrase})",
            'count': count,
            'firstRecord': 1
        }

        print("Fetching data for:", search_phrase)
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            result = response.json()
            if result.get('Data') and result['Data'].get('Records') and result['Data']['Records'].get('records') and result['Data']['Records']['records'].get('REC'):
                papers = extract_paper_details(result, search_phrase)
                all_papers.extend(papers)
            else:
                print(f"No records found for: {search_phrase}")
        else:
            print('Failed to retrieve data:', response.text)
    return all_papers

def extract_paper_details(data, search_phrase):
    papers = []
    records = data['Data']['Records']['records']['REC']
    for index, record in enumerate(records, start=1):
        try:
            identifiers = record['dynamic_data']['cluster_related']['identifiers']['identifier']
            doi = next((identifier['value'] for identifier in identifiers if identifier['type'] == 'doi'), "No DOI found")
        except (KeyError, TypeError):
            print(f"Error processing identifiers for record {index}: Expected list of dictionaries but got something else.")
            doi = "No DOI found"
        author_entries = record['static_data']['summary']['names']['name']
        authors = ', '.join(f"{name.get('first_name', '')} {name.get('last_name', '')}".strip() for name in author_entries if isinstance(name, dict))
        wos_link = f"https://www.webofscience.com/wos/woscc/full-record/{record['UID']}"

        paper_info = {
            'DOI': doi,
            'Source': 'Web of Science',
            'Search Phrase': search_phrase,
            'Title': next((title['content'] for title in record['static_data']['summary']['titles']['title'] if title['type'] == 'item'), None),
            'Year Published': record['static_data']['summary']['pub_info']['pubyear'],
            'Venue': next((title['content'] for title in record['static_data']['summary']['titles']['title'] if title['type'] == 'source'), None),
            'Authors': authors,
            'Abstract': record['static_data']['fullrecord_metadata']['abstracts']['abstract']['abstract_text']['p'] if 'abstracts' in record['static_data']['fullrecord_metadata'] else 'No abstract',
            'URL': wos_link,
            'Record Order': index
        }
        papers.append(paper_info)
    return papers

def save_to_csv(papers, filename="wos.csv"):
    keys = papers[0].keys()
    with open(filename, 'w', newline='', encoding='utf-8') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(papers)

# Example usage
api_key = 'API KEY'  # Replace 'API KEY' with your actual Web of Science API key(Web of Science API Expanded)

search_terms = [
"search phrase 1",
"search phrase 2"
]

papers = retrieve_wos_data(api_key, search_terms)
if papers:
    save_to_csv(papers)



