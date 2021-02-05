from bs4 import BeautifulSoup
import requests

print("Enter the job title or programming language you are looking for: ")
search_position = input()
print("Enter the city you are looking for: ")
search_city = input()
print(f'Looking for {search_position} in {search_city}')
print()


def scrape_for_jobs():
    with open('jobs.txt', 'w') as jobsFile:
        # moj-posao.net
        page_text = requests.get('https://www.moj-posao.net/Pretraga-Poslova/?searchWord=&keyword=&job_title'
                                 '=&job_title_id=&area=&category=11').text
        soup = BeautifulSoup(page_text, 'lxml')
        jobs = soup.find_all('div', class_='job-data')
        for job in jobs:
            job_position = job.find('span', class_='job-position')
            if job_position is not None:
                job_position = job_position.text.strip()
                job_city = job.find('span', class_='job-location').text.strip()
                if search_position.lower() in job_position.lower() and search_city.lower() in job_city.lower():
                    jobsFile.write(job_position + '\n')
                    jobsFile.write(job_city + '\n')
                    jobsFile.write(job.a['href'] + '\n')
                    jobsFile.write('\n')

        # careerjet.com.hr
        request_url = 'https://www.careerjet.com.hr/trazi/poslovi?s=' + search_position + '&l=Hrvatska'
        page_text = requests.get(request_url).text
        soup = BeautifulSoup(page_text, 'lxml')
        jobs = soup.find_all('article', class_='job clicky')
        for job in jobs:
            job_position = job.find('h2')
            if job_position is not None:
                job_position = job_position.text.strip()
                job_city = job.find('ul', class_='details').li.text.strip()
                if search_position.lower() in job_position.lower() and search_city.lower() in job_city.lower():
                    jobsFile.write(job_position + '\n')
                    jobsFile.write(job_city + '\n')
                    jobsFile.write("https://www.careerjet.com.hr" + job.a['href'] + '\n')
                    jobsFile.write('\n')

    jobsFile.close()
    print("You can find selected jobs in jobs.txt file!")


if __name__ == '__main__':
    scrape_for_jobs()
    end = input()