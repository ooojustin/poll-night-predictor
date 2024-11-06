from bs4 import BeautifulSoup
import requests
import logging

logging.basicConfig(level=logging.ERROR,
                    format="%(asctime)s - %(levelname)s - %(message)s")

# Data stored in this URL should be manually projected from an individual state.
# Example URLL: https://www.nbcnews.com/politics/2024-elections/pennsylvania-president-results
# 1.) Open the page for the selected state and expand the content to show all counties. (https://i.imgur.com/5fgQU8S.png)
# 2.) Locate the HTML node that contains all county data by using this DOM query: 'div#president-results-table'
# 3.) Copy the entire outer HTML of this element and make the raw content accessible via a remote URL (e.g., using Pastebin).
# 4.) Replace the following state name/URL (or modify the script to support multiple states - this was written last minute) and execute the script.
STATE, URL = "Pennsylvania", "https://pastebin.com/raw/YY0nhtQ9"


def fetch_and_project_votes(state_name, url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        html = response.text
        soup = BeautifulSoup(html, "html.parser")
        projected_trump_votes_total = 0
        projected_harris_votes_total = 0

        county_rows = soup.find_all("div", {"data-testid": "county-row"})

        for county in county_rows:
            county_name = "Unknown"
            try:
                county_name = county.get("data-monitoring", county_name)
                percent_in_element = county.find("span", class_="percent-in")
                if percent_in_element:
                    percent_in_text = percent_in_element.text.strip("% in")
                    percent_in = float(percent_in_text) / 100
                else:
                    logging.error(
                        f"Missing percent-in element for county {county_name}")
                    continue

                total_votes_element = county.find(
                    "span", {"data-testid": "state-results-table-area-votes"})
                if total_votes_element:
                    total_votes_text = total_votes_element.text
                    total_votes = int(total_votes_text.replace(
                        "votes", "").strip().replace(",", ""))
                else:
                    logging.error(
                        f"Missing total votes element for county {county_name}")
                    continue

                trump_votes = 0
                harris_votes = 0
                rows = county.find_all("tr")

                for row in rows:
                    candidate_cell = row.find("td", {"data-type": "candidate"})
                    votes_cell = row.find("td", {"data-type": "votes"})

                    if candidate_cell and votes_cell:
                        candidate_name_full = candidate_cell.find(
                            "span", {"data-testid": "text--m"})
                        if candidate_name_full:
                            candidate_name = candidate_name_full.get_text(
                                strip=True)

                            if "Trump" in candidate_name:
                                votes_text = votes_cell.get_text(
                                    strip=True).replace(",", "")
                                trump_votes = int(
                                    votes_text) if votes_text.isdigit() else 0
                            elif "Harris" in candidate_name:
                                votes_text = votes_cell.get_text(
                                    strip=True).replace(",", "")
                                harris_votes = int(
                                    votes_text) if votes_text.isdigit() else 0

                trump_ratio = trump_votes / total_votes if total_votes else 0
                harris_ratio = harris_votes / total_votes if total_votes else 0
                projected_votes = total_votes / percent_in if percent_in else total_votes

                projected_trump_votes = projected_votes * trump_ratio
                projected_harris_votes = projected_votes * harris_ratio

                projected_trump_votes_total += projected_trump_votes
                projected_harris_votes_total += projected_harris_votes

                print(f"County: {county_name}")
                print(f" - % In: {percent_in * 100:.2f}%")
                print(f" - Current Trump Votes: {trump_votes}")
                print(f" - Current Harris Votes: {harris_votes}")
                print(
                    f" - Projected Trump Votes: {int(projected_trump_votes)}")
                print(
                    f" - Projected Harris Votes: {int(projected_harris_votes)}\n")

            except Exception as e:
                logging.error(f"Error processing county {county_name}: {e}")

        total_votes_projected = projected_trump_votes_total + projected_harris_votes_total

        trump_projected_percentage = (
            projected_trump_votes_total / total_votes_projected) * 100 if total_votes_projected else 0
        harris_projected_percentage = (
            projected_harris_votes_total / total_votes_projected) * 100 if total_votes_projected else 0

        # calculate estimated error margin based on remaining votes
        total_percent_in = sum(float(county.find("span", class_="percent-in").text.strip("% in")) / 100
                               for county in county_rows if county.find("span", class_="percent-in"))
        average_percent_in = total_percent_in / \
            len(county_rows) if county_rows else 1
        error_margin = (1 - average_percent_in) * 100

        winner = "Trump" if projected_trump_votes_total > projected_harris_votes_total else "Harris"

        print(f"State: {state_name}")
        print(f"Max Est. Error Margin: ±{error_margin:.2f}%\n")

        print(f"Projected Winner: {winner}")
        print(
            f"Total Projected Trump Votes: {int(projected_trump_votes_total)} ({trump_projected_percentage:.2f}%)")
        print(
            f"Total Projected Harris Votes: {int(projected_harris_votes_total)} ({harris_projected_percentage:.2f}%)")

    except Exception as e:
        logging.error(f"Error fetching and parsing data: {e}")


fetch_and_project_votes(STATE, URL)
