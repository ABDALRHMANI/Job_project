from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
from bs4 import BeautifulSoup
import csv
# Initialize Chrome WebDriver options
chrome_options = Options()
chrome_options.add_argument('--disable-blink-features=AutomationControlled')  # Disable Automation Detection
chrome_options.add_argument('--unsafely-treat-insecure-origin-as-secure=https://example.com')  # Replace with your URL

# Path to ChromeDriver (update if necessary)
driver = webdriver.Chrome(options=chrome_options)

def main():
    """Fetch all job links from the main job listing page."""
    all_data = []

    for i in range(1, 100):  # Loop through pages
        try:
            print(f"Processing page {i}...")
            driver.get(f"https://www.naukrigulf.com/it-software-jobs-{i}?country=17,3,14&fa=16&xz=1_20_5")
            time.sleep(5)  # Wait for the page to load completely

            # Parse the page using BeautifulSoup
            page_src = driver.page_source
            soup = BeautifulSoup(page_src, "lxml")

            # Extract job links from the listing page
            job_entries = soup.find_all("div", {"class": "ng-box srp-tuple"})
            job_links = []

            for entry in job_entries:
                try:
                    link_tag = entry.find("a")
                    if link_tag and link_tag.has_attr("href"):
                        job_links.append(link_tag["href"])
                except Exception as e:
                    print(f"Error extracting a link from page {i}: {e}")

            # Visit each job link to extract details
            for l in range(len(job_links)):
                try:
                    print(f"Processing link {l + 1} on page {i}...")
                    driver.get(job_links[l])  # Open the job details page
                    time.sleep(4)  # Allow time for the page to load
                    src = driver.page_source
                    soup_d = BeautifulSoup(src, "lxml")
                    all_data.append(details(soup_d))
                except Exception as e:
                    print(f"Error processing link {l + 1} on page {i}: {e}")

        except Exception as e:
            print(f"Error processing page {i}: {e}")

    # Collect all unique keys for the CSV header
    all_keys = set()
    for data in all_data:
        all_keys.update(data.keys())

    # Save all data to a CSV file
    try:
        with open("D:\\Jobs_project\\naukrigulf_jobs.csv", "w", newline="", encoding="utf-8") as fi:
            writer = csv.DictWriter(fi, fieldnames=all_keys)
            writer.writeheader()
            writer.writerows(all_data)
        print("File created successfully.")
    except Exception as e:
        print(f"Error saving data to CSV: {e}")

    return all_data

def details(soup_d):
    """Visit each job link and extract details."""
    
    # Initialize variables with default values
    job_title = "Not available"
    company_name = "Not available"
    headers_value_dict = {}
    job_desc_text = "No job description available"
    
    # Extract job title
    try:
        all_sec = soup_d.find('h1', {"class": 'info-position'})
        job_title = all_sec.contents[0].strip()
    except Exception as e:
        print(f"Error extracting job title: {e}")
    print("Job Title:", job_title)
    
    # Extract company name
    try:
        company_name_sec = soup_d.find('div', {'class': 'jd-company-desc ng-box'})
        company_name = company_name_sec.find('p', {"class": "heading"}).text.strip()
    except Exception as e:
        print(f"Error extracting company name: {e}")
    print("Company Name:", company_name)
    
    # Extract headers and values
    try:
        all_det = soup_d.find('div', {"class": "candidate-profile"})
        all_headers = all_det.find_all('p', {'class': 'head'})
        all_values = all_det.find_all('p', {'class': 'value'})
        headers_value_dict = {header.text.strip(): value.text.strip() for header, value in zip(all_headers, all_values)}
    except Exception as e:
        print(f"Error extracting headers and values: {e}")
    print("Headers and Values:", headers_value_dict)
    
    # Extract job description
    try:
        job_desc = soup_d.find('article', {'class': 'job-description'})
        job_desc_text = job_desc.text.strip()
    except Exception as e:
        print(f"Error extracting job description: {e}")
    print("Job Description:", job_desc_text)
    
    # Create a dictionary for job details
    job_details = {
        "job_title": job_title,
        "company_name": company_name,
        "job_description": job_desc_text
    }
    
    # Merge headers_value_dict into job_details using update
    job_details.update(headers_value_dict)
    
    time.sleep(2)  # Wait between requests to avoid being flagged
    
    return job_details

# Main execution
try:
    all_data = main()  # Get all job links from the main page
    
     # Visit each job link for details
finally:
    driver.quit()  # Ensure the browser is closed after execution
