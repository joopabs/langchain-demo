import os

import requests
from dotenv import load_dotenv
from rich.console import Console

load_dotenv()


def scrape_linkedin_profile(linkedin_profile_url: str, mock: bool = False):
    """Scrapes information from LinkedIn profiles.
    Manually scrape the information or fetch it using an API."""

    if mock:
        linkedin_profile_url = "https://gist.githubusercontent.com/joopabs/5ef140c680643f48acaeab276fca2176/raw/7844dd6615351d94e2f4988b70123d5978b5ab8d/jpabular-linkedin-scrapin.json"
        response = requests.get(linkedin_profile_url, timeout=10)
    else:
        api_endpoint = "https://api.scrapin.io/enrichment/profile"
        params = {
            "apikey": os.getenv("SCRAPIN_API_KEY"),
            "linkedInUrl": linkedin_profile_url,
        }
        response = requests.get(api_endpoint, params=params)

    data = response.json().get("person")
    # Filter out empty dictionaries and lists
    data = {k: v for k, v in data.items() if v not in (None, "", [], {})}

    return data


if __name__ == "__main__":
    data = scrape_linkedin_profile(
        linkedin_profile_url="https://www.linkedin.com/in/julius-p-0052794/",
        mock=True,
    )

    console = Console()
    # Display formatted JSON using Rich's built-in method
    console.print_json(data=data)
