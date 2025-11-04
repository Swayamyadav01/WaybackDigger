# WaybackDigger

**WaybackDigger** is a Python-based tool designed to extract and filter URLs from the Wayback Machine archive based on specific file extensions like `.pdf`, `.zip`, `.sql`, `.xls`, `.txt`, and many others. It checks each URL’s availability and saves only the ones returning a **200 OK** response to an output file. This makes it ideal for research, web scraping, or collecting archived resources from historical domains.

---

## Features

- Fetch URLs from the Wayback Machine for any target domain.  
- Filter URLs by file types such as `.pdf`, `.zip`, `.xls`, `.sql`, `.txt`, etc.  
- Validate URLs and store only those with a **200 OK** response.  
- Process multiple domains by providing a file containing a list of domains.  
- Save all valid URLs into a text file automatically.  
- Display progress during URL checking using a progress bar.  
- Clean, formatted, and color-highlighted output in the terminal for better readability.

---

## Requirements

- Python 3.6+  
- `requests`  
- `pyfiglet`  
- `colorama`  
- `tqdm`

---

## Installation

1. Clone the repository to your local system:

```
git clone https://github.com/Swayamyadav01/WaybackDigger.git
cd WaybackDigger
```

## Install dependencies  
1. Install the required dependencies using pip:

```
pip install -r requirements.txt
```

---

## Input Options

You can use **WaybackDigger** in two different modes:

1. **Single Domain**:  
   - When prompted, enter a single domain (e.g., `example.com`).  
   - The tool will extract archived URLs associated with that domain.  

2. **Multiple Domains from a File**:  
   - Press Enter to load domains from a text file instead.  
   - Provide the name of the file containing one domain per line.  
   - Example input file:  
     ```
     example1.com
     example2.com
     example3.com
     ```
