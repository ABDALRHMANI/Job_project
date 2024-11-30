import requests
from bs4 import BeautifulSoup 
from selenium import webdriver
from selenium.webdriver.common.by import By
import csv
all_job_details = []

def main_page():
    all_job_details = []  # Initialize the list to store all job details
    for i in range(1, 71):  # Loop through all pages
        driver = webdriver.Chrome()

        # Fetch the main page
        main_page = requests.get(f"https://wuzzuf.net/search/jobs/?filters%5Broles%5D%5B0%5D=IT%2FSoftware%20Development&start={i}")
        main_src = main_page.content
        main_soup = BeautifulSoup(main_src, "lxml")

        # Find all job links
        count=0
        all_links = main_soup.find_all("a", {"class": "css-o171kl"})
        for link in all_links:  # Iterate over all job links

            if link['href'].strip()[0] == 'h':
                print(link['href'])
                driver.get(link['href'])
                details_src = driver.page_source
                details_soup = BeautifulSoup(details_src, "lxml")
                try:
                    all_details = get_details(details_soup,link['href'])  # Get job details
                    all_job_details.append(all_details)  # Add to the list
                except Exception as e:
                    print(f"Error fetching details for link {link['href']}: {e}")
            else:
                continue

        driver.quit()  

    if all_job_details:
        keys = set()  
        for job in all_job_details:
            keys.update(job.keys())
            
        with open("D:\\Jobs_project\\Wuzzaf_jobs_2.csv", "w", newline="", encoding="utf-8") as fi:
            dict_writer = csv.DictWriter(fi, keys)
            dict_writer.writeheader()
            dict_writer.writerows(all_job_details)
        print("File created successfully.")
    else:
        print("No job details found, file not created.")

def get_details(details_soup,link):
    try:
        job_title = details_soup.find("h1", {"class": "css-f9uh36"}).text.strip()
    except Exception as e:
        job_title = None
        print(f"Error fetching job_title: {e}")

    try:
        company_name = details_soup.find("a", {"class": "css-p7pghv"}).text.strip()
    except Exception as e:
        company_name = None
        print(f"Error fetching company_name: {e}")

    try:
        the_place = details_soup.find("strong", {"class": "css-9geu3q"}).text.strip().split('-')[1].strip()
    except Exception as e:
        the_place = None
        print(f"Error fetching the_place: {e}")

    try:
        Work_Status = details_soup.find("span", {"class": "css-ja0r8m eoyjyou0"}).text.strip()
    except Exception as e:
        Work_Status = None
        print(f"Error fetching Work_Status: {e}")

    try:
        Work_Mode = details_soup.find("span", {"class": "css-1yq4msy eoyjyou0"}).text.strip()
    except Exception as e:
        Work_Mode = None
        print(f"Error fetching Work_Mode: {e}")

    try:
        seconed_section = details_soup.find("section", {"class": "css-3kx5e2"})

        headers=seconed_section.find_all("span",{"class":"css-wn0avc"})

        values=seconed_section.find_all("span",{"class":"css-47jx3m"})

        header_value_dict={header.text.strip():value.text.strip() for header,value in zip(headers,values)}

    except Exception as e:
        exp = None
        print(f"Error fetching experience: {e}")

    
    try:
        skills=''
        skills_list = details_soup.find_all('span',{'class','css-158icaa'})
        for sk in skills_list:
            skills += sk.text.strip() + ', '
    except Exception as e:
        skills = None
        print(f"Error fetching skills: {e}")

    try:
        job_desc=''
        job_desc_all = details_soup.find("div", {"class": "css-1uobp1k"})
        try:
            job_desc_list=job_desc_all.find_all(['ul', 'ol'])
            if not job_desc_list:
                for child in job_desc_all.contents:
                    print(f"child: {child}")
                    if child.name:  # If it's a tag, extract text
                        job_desc += child.text.strip() + '! '
                    else:  # If it's a NavigableString, just strip it
                        job_desc += child.strip() + '! '
                print(job_desc)

            else:
                for m_l in job_desc_list:
                    job_desc_l=m_l.find_all(['li'])
                    for l in job_desc_l:
                        job_desc += l.text.strip() + '! '
        except:
            print("no list")

    except Exception as e:
        job_desc = None
        print(f"Error fetching job_description: {e}")

    try:
        job_req=''
        job_req_all = details_soup.find("div", {"class": "css-1t5f0fr"})
        
        try:
            job_req_list=job_req_all.find_all(['ul', 'ol'])
            if not job_req_list:
                for child in job_req_all.contents:
                    print(f"child: {child}")
                    if child.name:  # If it's a tag, extract text
                        job_req += child.text.strip() + '! '
                    else:  # If it's a NavigableString, just strip it
                        job_req += child.strip() + '! '
                print(job_req)

            else:
                for m_l in job_req_list:
                    job_req_l=m_l.find_all(['li'])
                    for l in job_req_l:
                        job_req += l.text.strip() + '! '
        except:
            print("no list")
        
        
    except Exception as e:
        job_req = None
        print(f"Error fetching job_requirements: {e}")

    all_details={
        "job_title": job_title,
        "company_name": company_name,
        "the_place": the_place,
        "Work_Status": Work_Status,
        "Work_Mode": Work_Mode,
        "skills": skills,
        "job_description": job_desc,
        "job_requirements": job_req,
        'url':link
    }

    

    all_details.update(header_value_dict)


    return all_details

main_page()


    
    
