from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import os
import pandas as pd
import logging
import smtplib
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from email.mime.multipart import MIMEMultipart


#-------------------------------------------------------------------------------------

# kyun ka task schedular as simple path handle nai karta wo os ka describe path follow karta hia to hum usi path ko design kar rai hain 
base_path = os.path.dirname(os.path.abspath(__file__)) # ya py file ka actual path hai
data_dir=os.path.join(base_path, 'data') # is ma hum data folder ka path bhi original file ma add kar rai hain taka schedular eassily samajh saka 
os.makedirs(data_dir, exist_ok=True) # is ma hum directories ki presence make sure kar rai hain 

#-------------------------------------------------------------------------------------
# yahan par ma logs ki output show karwana ka liya eik scraper ka name sa file banai hia or ma logs pass kar rai hain 
scraper_path=os.path.join(base_path, 'scraper.log')
logging.basicConfig(filename=scraper_path, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logging.info("script Started")

# ------------------------------------------------------------------------------------
# yahan ma env sa apna credentials import kar raha hoon eik trha sa 
load_dotenv()
Email=os.getenv("Email")
Password=os.getenv("Password")
Receiver_mail=os.getenv("Receiver_mail")

#-------------------------------------------------------------------------------------

driver = webdriver.Chrome() # driver ma hum na wo browser set kiya jis ma hum website run karna chah rai chrome ki jgha or bhi koi ho skta tha jesa ka firefox
total_jobs=0 # eik variable declare kiya jo ka hum aga chal kar job count karna ka liya use karain ga 
query = 'jobs' # website sa hum jo cheez search karna chah rai usa queury name ka variable ma store kar ka url ma pass kar diya hai 
file=0 # ya hum na pagenation ko handle karna ka liya variable banaya hai 
try:
    for i in range(1, 6): # loop ma hum range set kar rai ka hum na kitna pages scrap karna hain mana abhi ka liya 3 tak set kiya taka data kum rai raha or pagination ka process show ho saka
        driver.get(f"https://www.actuarylist.com/?page={i}&search={query}") # url ma hum page number {i} ka zariya oe jo cheez hum dhoondna chah rai usa {query} ka zariya paas kar diya hai 
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "Job_job-card__YgDAV"))
        )
        elems = driver.find_elements(By.CLASS_NAME, "Job_job-card__YgDAV") # hum class name ka zariya saari jobs find kar ka elems name ka variable ma store kar rai hian 
        page_count = len(elems) # jitni jobs hamain mili eik page par usko page_count ma store kar diya 
        total_jobs+=page_count # page_count ko total_jobs ma add kar diya taka at the end tota number of jobs haasil kar sakain 
        print(f"\nPage {i}: {page_count} jobs found") # jobs count ko simple print kiya hai us current page ki 
        try:
            for elem in elems: # elems ma store saari jobs ko baari baari iterate karna ka liya loop lagaya
                data= elem.get_attribute("outerHTML") # har elem(job) ka outerHTML la kar data ma store karwa rai hain 
                file_path = os.path.join(data_dir, f"{query}_{file}.html")
                with open (file_path,'w',encoding='utf-8') as f: # is ma mana apni asaani ka liya eik data name ka folder banaya hai or har elem ko unique file name da kar us ma store kar raha hoon taka further processing ka liya usa baar baar website sa data scrap na karna para 
                    f.write(data) #data write karwa diya 
                    file+=1 # file ma increment karwa rai taka har agli file ko unique number  mil saka
        except Exception as e:
            logging.error(f"Error saving job_HTML: {e}")
except Exception as e:
    logging.error(f"Error during scraping: {e}")
finally:
    print(f"\nTotal jobs scraped: {total_jobs}") # total number of jobs print kar rai hain 
    driver.quit()

#--------------------------------------------------------------------------------------

data={'company':[], 'job title':[], 'country':[], 'job posted':[], 'job_link':[]}

for file in os.listdir(data_dir): # os ko use karta hua hum data ki directory masa sab files baari baari khol rai taka usa read kar sakain
    try: # in case agar koi error aajai to usko handle karna ka liya 
        file_path = os.path.join(data_dir, file)
        with open (file_path, encoding='utf-8') as f: # har file ko open kar rai or sath make sure kiya hai encoding taka agar in case koi special letter ho to wo problem na create kara
            html_doc=f.read() # har file ka data ko read kar ka variable ma store kar rai hain 
        soup= BeautifulSoup(html_doc, 'lxml') # soup object bana rai jis ma hum apni file or eik parser pass kar rai jo ka hamari file ko parse karna ma help karta 
        # class name ki madad sa mana company name find kiya or usa variable ma store karwa diya taka aaga usa intemaal kar sakain
        company=soup.find('p', class_='Job_job-card__company__7T9qY')
        company_title=company.get_text()
        # class name ki madad sa mana job position find kiya or usa variable ma store karwa diya taka aaga usa intemaal kar sakain
        position=soup.find('p', class_='Job_job-card__position__ic1rc')
        position_title=position.get_text()
        # class name ki madad sa mana country find kiya or usa variable ma store karwa diya taka aaga usa intemaal kar sakain
        country=soup.find('a', class_='Job_job-card__country__GRVhK')
        country_name=country.get_text()
        # class name ki madad sa mana pata kiya ka kitna time/din phla job post hui find kiya or usa variable ma store karwa diya taka aaga usa intemaal kar sakain
        job=soup.find('p', class_='Job_job-card__posted-on__NCZaJ')
        job_posted=job.get_text()
        # # class name ki madad sa mana job link find kiya or usa variable ma store karwa diya taka aaga usa intemaal kar sakain or us link ki madad sa hum apni us job par direct bhi ho skta hian 
        link=soup.find('a', class_='Job_job-page-link__a5I5g')
        job_link="https://www.actuarylist.com" + link['href']
        
        #is ma hum apna data ko panda ki library use karta us ka object ma pass kar rai hain jo ka hum na uper banaya tha 
        data['company'].append(company_title)
        data['job title'].append(position_title)
        data['job posted'].append(job_posted)
        data['country'].append(country_name)
        data['job_link'].append(job_link)
        
    except Exception as e:
        logging.error(f"Error in Parsing File: {e}")
#is ma hum na pandas ka data frame liya hai jis ma data store ho raha 
df=pd.DataFrame(data=data)
df=df.drop_duplicates(subset=['job title','company']) # job duplication sa bachna ka liya hum pandas ka hi build-in function use kar rai hian 
csv_path=os.path.join(base_path,'data.csv') 
df.to_csv(csv_path, index=False) # saara data hum apni file ko paas kar rai jo ka hum na data.csv ka name sa banai hai 
logging.info("CSV saved sucessfully")

#-----------------------------------------------------------------------------------------

try:
    subject = "Job Scraper Summary"
    body = f"Scraper ran successfully.\nTotal Jobs Scraped: {total_jobs}"

    msg = MIMEMultipart() # eik container ko initialize kar rai hian hum jis ma hum apna mail text ya koi file jo hum attach karna chahta rakhain ga 
    msg['From'] = Email # sender ki mail pass kar rai env sa 
    msg['To'] = Receiver_mail # jis ko mail send ki us ki email pass kar rai 
    msg['Subject'] = subject # ya hissa subject line ko set kar raha hai jo hum na uper hi define kiya tha 
    msg.attach(MIMEText(body, 'plain')) # jo hum  na text likha ya pass kiya wo yahan aai ga 

    # yahan hum apni resultant csv file ko email ka sath attach kar rai hian 
    with open(csv_path, 'rb') as file: # yahan hum na apni csv file ko binary format ma read ma open kiya hai 
        part = MIMEBase('application', 'octet-stream') # yaaan hum apni attachment file ki type fix kar rai hian (jo ka hum na binary select ki thi uper)
        part.set_payload(file.read())
        encoders.encode_base64(part) # yahan hum file ko base64 ma encode kar rai hian jo ka email attachemnt ka standard hai 
        part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(csv_path)}') # is ma hum simple apni csv file ko mail ma header assign karrai hain 
        msg.attach(part)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server: # yahan hum apni us request ko gmail ka server ka sath connect kar rai hian ssl ki madad sa port 465 par 
        server.login(Email, Password) # yahan hum authentication handle kar rai hian sender ki 
        server.sendmail(Email, Receiver_mail, msg.as_string()) # or finally hum na mail send kar di 
 
    logging.info("Email notification sent")

except Exception as e:
    logging.error(f"Error sending email: {e}")