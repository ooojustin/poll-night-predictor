# Poll Night Predictor

### USA 2024 Presdential Election

A quick script to extract county-level election data from current data for a specified state and extrapolate results based on the current vote distribution between primary candidates.

> **Note:** This tool is based solely on statistical extrapolation and will not be fully accurate. It is intended for informational purposes only and does not reflect any opinions or biases.

## Instructions

1. **Expand All Counties**: Open the state results page and expand to view all counties. [Example screenshot](https://i.imgur.com/5fgQU8S.png).
2. **Locate Data Node**: Use the DOM query `div#president-results-table` to find the HTML element which encapsulates all county nodes.
3. **Copy and Share**: Copy the outer HTML of this element, then upload it to a remote URL (e.g., Pastebin).
4. **Update and Run**: Replace the state URL in the script and execute.

## Example State URL

- Pennsylvania: `https://www.nbcnews.com/politics/2024-elections/pennsylvania-president-results`
