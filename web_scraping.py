# Import Python Libraries :
import requests
from bs4 import BeautifulSoup 
import csv
from itertools import zip_longest
# Lists to store the extracted information
job_title = []
company_name = []
location_name = []
job_skill = []
links = []
date = []
page_number = 0

# Base URL
base_url = "https://wuzzuf.net"

# Loop to go through each page
while True:
    url = f"{base_url}/search/jobs/?a=hpb%7Cspbg&q=python&start={page_number}"
    result = requests.get(url)
    src = result.content
    
    # Parse content using BeautifulSoup
    soup = BeautifulSoup(src, 'lxml')

    # Find the page limit
    page_limit_elem = soup.find("strong")
    if page_limit_elem:
        page_limit = int(page_limit_elem.text)
    else:
        print("Could not find the page limit element. Exiting loop.")
        break
    
    if page_number > page_limit // 15:
        print("Page end reached, terminating.")
        break
    
    # Find elements containing the required information
    job_titles = soup.find_all("h2", {"class": "css-m604qf"})
    company_names = soup.find_all("a", {"class": "css-17s97q8"})
    locations_names = soup.find_all("span", {"class": "css-5wys0k"})
    job_skills = soup.find_all("div", {"class": "css-y4udm8"})
    posted_new = soup.find_all("div", {"class": "css-4c4ojb"})
    posted_old = soup.find_all("div", {"class": "css-do6t5g"})
    posted = posted_new + posted_old

    # Extract and store the data
    for i in range(len(job_titles)):
        job_title.append(job_titles[i].text.strip())
        job_link = job_titles[i].find("a").attrs["href"]
        links.append(base_url + job_link)
        company_name.append(company_names[i].text.strip())
        location_name.append(locations_names[i].text.strip())
        job_skill.append(job_skills[i].text.strip())
        date_text = posted[i].text.replace("-", "").strip()
        date.append(date_text)
    
    page_number += 1
    print(f"Page {page_number} processed.")

# Save data to CSV (without salary and responsibilities)
file_list = [job_title, company_name, date, location_name, job_skill, links]
exported = zip_longest(*file_list)

with open("D:\\AI\\Machine Learning\\spyder\\z\\1\\web_scraping.csv", "w", encoding="utf-8", newline='') as myfile:
    wr = csv.writer(myfile)
    wr.writerow(['Job Title', 'Company Name', 'Date', 'Location Name', 'Job Skills', "Links"])
    wr.writerows(exported)

print("Data saved successfully!")