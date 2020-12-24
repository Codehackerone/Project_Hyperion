import wolframalpha
from email.mime.text import MIMEText
import smtplib
from twilio.rest import Client
import datetime
import pytz
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait

def getLocation():
    chrome_options = Options()
    chrome_options.add_argument("--use-fake-ui-for-media-stream")
    timeout = 20
    driver = webdriver.Chrome(chrome_options=chrome_options,executable_path="C:\chromedriver.exe")
    driver.get("https://mycurrentlocation.net/")
    wait = WebDriverWait(driver, timeout)
    longitude = driver.find_elements_by_xpath('//*[@id="longitude"]')
    longitude = [x.text for x in longitude]
    longitude = str(longitude[0])
    latitude = driver.find_elements_by_xpath('//*[@id="latitude"]')
    latitude = [x.text for x in latitude]
    latitude = str(latitude[0])
    driver.quit()
    return (latitude,longitude)


def calculate():
    query = "calculate 1+2"
    app_id = "E97G5Q-WJEE77J6QL"
    client = wolframalpha.Client(app_id)
    indx = query.lower().split().index('calculate')
    query = query.split()[indx + 1:]
    res = client.query(' '.join(query))
    answer = next(res.results).text
    print("The answer is " + answer)


def sendEmail(to, content, subject):
    from_email = "janinakano1@gmail.com"
    from_password = "pythonlearn1234"
    msg = MIMEText(content, 'html')
    msg['Subject'] = subject
    msg['To'] = to
    msg['From'] = from_email
    gmail = smtplib.SMTP('smtp.gmail.com', 587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(from_email, from_password)
    gmail.send_message(msg)


def twilio():
    account_sid = 'ACdc011508d67a48c7bca7464c43076994'
    auth_token = 'c6aed281db6b7cadf682e1fd0b75be00'
    client = Client(account_sid, auth_token)

    message = client.messages \
        .create(
        body="hello",
        from_='+12053902313',
        to='+916290376589'
    )

    print(message.sid)


def time():
    current_time = datetime.datetime.now(pytz.timezone('Asia/Kolkata'))
    timenow = str(current_time.hour) + " hours and " + str(current_time.minute) + " minutes"
    print("Sir, the time is " + timenow)


def youtube():
    options=Options()
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=options,executable_path="C:\chromedriver.exe")
    driver.implicitly_wait(1)
    driver.maximize_window()
    query = "youtube despacito"
    indx = query.lower().split().index('youtube')
    query = query.split()[indx + 1:]
    driver.get("http://www.youtube.com/results?search_query=" + '+'.join(query))
    return


# sendEmail('soumyajitdatta123@gmail.com', 'content', 'subject')
