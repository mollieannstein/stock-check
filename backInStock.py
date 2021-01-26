import time
import smtplib
import requests
from datetime import datetime 
from bs4 import BeautifulSoup

def stock_check(url):
    soup = BeautifulSoup(url.content, "html.parser") 
    stock = soup.find("b", string="out of stock") #walmart
    # stock = soup.find_all(attrs={"data-test": "soldOutBlock"}) # finding data-* tags to avoid soup syntax error
    stock_status = str(stock)
    return stock_status # returns "out of stock" from soup string

def send_email(address, password, message):
    server = smtplib.SMTP("smtp.gmail.com", 587) # gmail server
    server.ehlo()
    server.starttls()
    server.login(address,password) # login to email account
    message = str(message) # message that will be emailed
    server.sendmail(address,address,message) # send the email through dedicated server
    return

def stock_check_listener(url, address, password, run_hours):
    listen = True # listen boolean
    start = datetime.now() # start time
    while(listen): # while listen = True, run loop
        # Not Available - gamestop  
        if "out of stock" in stock_check(url): #check page
            now = datetime.now()
            print(str(now) + ": Not in stock.")
        else:
            now = datetime.now()
            message = str(now) + ": BACK IN STOCK!"
            print(message)
            send_email(address, password, message)
            listen = False

        duration = (now - start)
        seconds = duration.total_seconds()
        hours = int(seconds/3600)
        if hours >= run_hours: # check run time
            print("Finished.")
            listen = False

        time.sleep(3*60) # Wait N minutes to check again.    
    return

if __name__=="__main__":

    # Set url and userAgent header to send request
    page = "https://www.walmart.com/ip/Xbox-Series-X/443574645"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
    'Content-Type': 'text/html'}

    # URL request
    url = requests.get(url=page,
                       headers=headers)

    # Run listener to stream stock checks.
    address = "{{EMAIL}}" # email
    password = "{{PASSWORD}}" # password
    stock_check_listener(url=url,
                         address=address,
                         password=password,
                         run_hours=24) 