# File: generic_course_parser.py

import requests
from bs4 import BeautifulSoup
import json
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def fetch_page_content(url):
    """
    Fetch HTML content of a given URL.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None



def fetch_dynamic_content(url):
    options = Options()
    options.add_argument("--headless")  # Run in headless mode
    # options.add_argument("--no-sandbox")
    # options.add_argument("--disable-dev-shm-usage")
    service = Service("/usr/bin/chromedriver")  # Replace with the path to your chromedriver
    driver = webdriver.Chrome(executable_path="/usr/bin/chromedriver", options=options)
    
    try:
        driver.get(url)
        # Wait for the mat-sidenav-container to be present
        WebDriverWait(driver, 100).until(
            EC.presence_of_element_located((By.TAG_NAME, "app-review-detail"))
        )
        return driver.page_source
    finally:
        driver.quit()


def extract_generic_text(soup:BeautifulSoup, tag="p", class_substring=None):
    """
    Extract text content from specified tags, optionally filtering by a class substring.
    """
    results = []
    elements = soup.find_all( attrs={'class': "mat-mdc-card-content"})
    
    for element in elements:
        # Filter by class substring, if specified
        if class_substring:
            classes = element.get("class", [])
            if not any(class_substring in cls for cls in classes):
                continue
        
        text = element.get_text(strip=True)
        if text:
            results.append(text)
    
    return results


def parse_course(html_content):
    """
    Parse the HTML content to extract generic course details.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Extract key information based on `<p>` tags and `_ngcontent` pattern
    paragraphs = extract_generic_text(soup, tag="p")
    
    # Extract title and other details explicitly
    title = soup.find("h1", {"class": "white"}).get_text(strip=True) if soup.find("h1", {"class": "white"}) else "N/A"
    subtitle = soup.find("h2", {"class": "white"}).get_text(strip=True) if soup.find("h2", {"class": "white"}) else "N/A"
    
    return {
        "course_title": title,
        "course_name": subtitle,
        "details": paragraphs
    }


def scrape_courses_from_file(file_path):
    """
    Scrape course details from a list of URLs in a file.
    """
    all_courses = []
    if not os.path.exists(file_path):
        print(f"Error: File {file_path} does not exist.")
        return all_courses
    
    with open(file_path, 'r', encoding='utf-8') as file:
        urls = [line.strip() for line in file.readlines()]
    
    for url in urls:
        print(f"Scraping course from {url}...")
        html_content = fetch_dynamic_content(url)
        # print(html_content)
        if html_content:
            course_data = parse_course(html_content)
            all_courses.append(course_data)
        else:
            print(f"Skipping {url} due to fetch error.")
    
    return all_courses


def save_to_jsonlines(data, output_path):
    """
    Save data to a JSONLines file.
    """
    with open(output_path, 'w', encoding='utf-8') as f:
        for entry in data:
            f.write(json.dumps(entry) + '\n')


def main():
    # Input file containing course paths (one URL per line)
    input_file = "course_paths.txt"
    
    # Output file path
    output_dir = "documents"
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, "courses.jsonl")
    
    print(f"Reading course URLs from {input_file}...")
    all_courses = scrape_courses_from_file(input_file)
    
    if all_courses:
        print(f"Scraped {len(all_courses)} courses.")
        save_to_jsonlines(all_courses, output_file)
        print(f"Data saved to {output_file}")
    else:
        print("No courses scraped.")
    

if __name__ == "__main__":
    main()
