import requests
from bs4 import BeautifulSoup
import random
import pandas as pd
import time

# Define User-Agents
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.4 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; AS; rv:11.0) like Gecko",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
]

# papers.cvs should store the collected papers' titles in the "Title" column.
articles = pd.read_csv('papers.csv')
articles = articles[['Title']][0:30]
p_n = 1
# articles = articles[['Title']][31:62]
# p_n = 2
# articles = articles[['Title']][63:101]
# p_n = 3
# ...

def get_random_headers():
    return {'User-Agent': random.choice(USER_AGENTS)}

def fetch_all_papers():
    batch_size = 4
    num_batches = len(articles) // batch_size + (1 if len(articles) % batch_size > 0 else 0)

    all_results = []
    for i in range(num_batches):
        batch_articles = articles[i*batch_size:(i+1)*batch_size]
        print(f"Processing batch {i+1}/{num_batches}...")
        dfs, success = fetch_from_gs(batch_articles)
        if not dfs.empty:
            all_results.append(dfs)
        else:
            print("No data fetched for this batch.")

        if not success:  # If False is returned, halt further processing
            print("Halting further processing due to an error.")
            break

        if i < num_batches - 1:
            print("Waiting to start next batch...")
            time.sleep(30)  # Waiting

    if all_results:
        combined_df = pd.concat(all_results, ignore_index=True)
        combined_df.to_csv(f'gbatch/papers_{p_n}.csv', index=False)
        print("Data successfully saved.")
    else:
        print("No dataframes to combine.")

def fetch_from_gs(articles):
    results = []
    with requests.Session() as session:
        session.headers.update(get_random_headers())
        for article in articles['Title']:
            retries = 0
            max_retries = 5
            delay = 5  # Initial delay in seconds
            while retries < max_retries:
                search_title = article.replace(' ', '+')
                link = f"https://scholar.google.com/scholar?hl=en&as_sdt=0%2C39&q={search_title}&btnG="
                details_response = session.get(link)
                if details_response.status_code == 429:
                    print(f"Rate limited. Retrying in {delay} seconds...")
                    time.sleep(delay)
                    retries += 1
                    delay *= 2  # Exponential backoff
                    continue
                elif details_response.status_code == 200:
                    details_soup = BeautifulSoup(details_response.text, 'html.parser')
                    try:
                        result = extract_information(details_soup, article)
                        results.append(result)
                    except ValueError as e:
                        print(e)
                        return pd.DataFrame(results), False  # Return results so far and a status
                    break
                else:
                    print(f"Failed to fetch data: {details_response.status_code}")
                    break
            if retries == max_retries:
                print(f"Max retries reached for {article}, skipping...")

    return pd.DataFrame(results), True  # All went well, return True as status


def extract_information(details_soup, article):
    # Extract the abstract
    abstract_div = details_soup.find('div', class_='gs_fma_snp')
    if abstract_div:
        abstract = abstract_div.get_text(strip=True) 
    else:
        gs_rs_div = details_soup.find('div', class_='gs_rs') 
        abstract = gs_rs_div.get_text(separator=' ', strip=True) if gs_rs_div else None

    if abstract is None:
        raise ValueError(f"Cannot get abstract for article: {article}")

    return {
        'Title': article,
        'Abstract': abstract
    }

# Run the script
if __name__ == "__main__":
    fetch_all_papers()


