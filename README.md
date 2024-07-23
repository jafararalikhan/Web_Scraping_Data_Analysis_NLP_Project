# Web Scraping and Text Analysis Project

## Overview
This project is designed to scrape article content from websites and perform text analysis, including sentiment analysis, readability metrics, and text complexity calculations. The results are saved into an Excel file for easy reporting and further analysis.

## Features
- **Web Scraping:** Extracts titles and content from web pages using BeautifulSoup.
- **Text Cleaning:** Removes stop words and unwanted characters from the text.
- **Sentiment Analysis:** Calculates positive and negative scores, polarity, and subjectivity using TextBlob.
- **Readability Metrics:** Computes average sentence length, FOG index, complex word percentage, and other readability metrics.
- **Data Management:** Uses Pandas to process and store results in an Excel file.

## Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/jafararalikhan/Web_Scraping_Data_Analysis_NLP_Project.git
    ```
2. Navigate to the project directory:
    ```bash
    cd Web_Scraping_Data_Analysis_NLP_Project
    ```
3. Install the required libraries:
    ```bash
    pip install -r requirements.txt
    ```

## Usage
1. Prepare your input data in an Excel file named `Input.xlsx` with columns `URL` and `URL_ID`.
2. Place any additional stop words in the `StopWords` folder.
3. Run the main script:
    ```bash
    python app.py
    ```
4. The results will be saved in the `Output` folder and the `Output.xlsx` file.

## File Structure
- `app.py`: Main script for web scraping and text analysis.
- `requirements.txt`: List of required Python libraries.
- `StopWords/`: Folder containing custom stop words.
- `MasterDictionary/`: Folder containing positive and negative word lists.
- `Input.xlsx`: Input file with URLs to be scraped.
- `Output/`: Folder to save scraped articles and analysis results.
- `Output.xlsx`: Output file containing the analysis results.

## Contributions
Contributions are welcome. Please fork the repository and submit a pull request with your changes.
