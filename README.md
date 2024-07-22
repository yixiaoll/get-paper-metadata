# get-paper-metadata

## Overview
This repository provides tools for acquiring metadata from academic papers across various platforms, including Google Scholar, Semantic Scholar, IEEE, ACM, Web of Science, and Arxiv. It might assist researchers in quickly gathering necessary bibliographic information during literature reviews.

## Supported Platforms and Data Retrieval Methods

### Google Scholar
- **Method**: Combination of the `scholarly` API and custom web scraping.
- **Data Retrieved**:
  - Title
  - Year Published
  - Venue
  - Authors
  - URL
  - Abstract (retrieved individually via web scraping by a separate script)

### Semantic Scholar
- **API Access**: Requires an API key from Semantic Scholar.
- **Data Retrieved**:
  - DOI
  - Title
  - Year Published
  - Venue
  - Authors
  - Abstract
  - URL

### IEEE
- **API Access**: Requires an API key from IEEE.
- **Data Retrieved**:
  - DOI
  - Title
  - Year Published
  - Venue
  - Authors
  - Abstract
  - URL

### ACM
- **Method**: Web scraping.
- **Data Retrieved**:
  - DOI
  - Title
  - Year Published
  - Venue
  - Authors
  - Abstract
  - URL

### Web of Science
- **API Access**: Requires an API key (Web of Science API Expanded).
- **Data Retrieved**:
  - DOI
  - Title
  - Year Published
  - Venue
  - Authors
  - Abstract
  - URL

### Arxiv
- **API Access**: No API key required.
- **Data Retrieved**:
  - DOI
  - Title
  - Year Published
  - Venue
  - Authors
  - Abstract
  - URL

## Usage
Navigate to the script corresponding to the repository you wish to query, and run it as shown below:
```bash
python [script_name].py
```

## Contribution
Contributions are very much welcome. Please open an issue or submit a pull request with your suggested changes.

## License
This project is licensed under the [MIT License](LICENSE).

