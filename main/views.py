from django.shortcuts import render
from django.http import HttpResponse
from main.models import joboffer
import requests
from bs4 import BeautifulSoup
import re
import pymysql


# Create your views here.
def get_url(job_type,n):
    html_template = 'https://lebanon.tanqeeb.com/jobs/search?keywords={}&countries[]=199&page_no={}'
    final_html = html_template.format(job_type,n)
    # this method plugs in the 'job position' specified by user input
    return final_html

def main(request):
    
    connection = pymysql.connect(host="localhost", user='root', passwd="", db="capstone")

    dbcursor = connection.cursor()

    if request.method == "POST":
        job_type = request.POST['input_box']
        joboffer.objects.all().delete()
        
        n=1
        while n<=2:

            final_html = get_url(job_type,n)
            n+=1
            html = requests.get(final_html).text
            # now we can extract the 'soup' of the url that is, getting the information we need all at once and put them in a bowl of soup
            soup = BeautifulSoup(html, 'html.parser')
            jobs = soup.find_all('div', class_="card-body")
            job_position = "empty"
            job_url = "empty"
            job_location = "empty"
            company_name = "empty"
            date_posted = "empty"
            for job in jobs:
                try:
                    job_position = job.find('h5').text
                    job_url = "https://lebanon.tanqeeb.com" + job.a['href']
                    span_reach = job.a.div.div.div.p
                    company_unique_id = "<i class=\"fas fa-building mr-2\"></i>"
                    job_location = span_reach.find('span').text
                    company_name = "available in link"
                    if str(span_reach.find('span', class_="pr-2 pb-1 d-block d-lg-inline-block").find_next().find_next().find('i')) in company_unique_id:
                        company_name = span_reach.find('span', class_="pr-2 pb-1 d-block d-lg-inline-block").find_next().find_next().text
                        date_posted = span_reach.find('span', class_="pr-2 pb-1 d-block d-lg-inline-block").find_next().find_next().find_next('span').text

                    else:
                        date_posted = span_reach.find('span', class_="pr-2 pb-1 d-block d-lg-inline-block").find_next().find_next('span').text
                except:
                    continue

                insert = ("INSERT INTO joboffer ( job_position, location, company_name, date_posted, job_link) VALUES (%s,%s,%s,%s,%s)")
                values = (job_position, job_location, company_name, date_posted, job_url)

                ins = joboffer(job_position= job_position, location= job_location, company_name=company_name, date_posted=date_posted,job_link= job_url)
                ins.save()

                
                dbcursor.execute(insert,values)
                connection.commit()
        connection.close()  
        print("the data has been written successfuly!")

    
    allJobs = joboffer.objects.all()
    context = {'JOBS': allJobs}
    print(allJobs)
    print("TESTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT")
    return render(request, 'main_page.html', context)

        
             

   

# def JOBS(request):
#     allJobs = joboffer.objects.all()
#     context = {'JOBS': allJobs}
#     print(allJobs)
#     print("TESTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT")
#     return render(request, 'main_page.html', context)
    
    

    

