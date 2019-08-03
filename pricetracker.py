import requests
from bs4 import BeautifulSoup
import smtplib
import time


def get_url():
    URL = "https://www.amazon.com/Sony-Full-Frame-Mirrorless-Interchangeable-Lens-ILCE7M3/dp/B07B43WPVK/ref=as_li_ss_tl?ascsub&cv_ct_id=amzn1.osp.1dc5564e-c096-4d12-b13f-6be135cd1c3c&cv_ct_pg=search&cv_ct_wn=osp-search&keywords=a7iii&pd_rd_i=B07B43WPVK&pd_rd_r=44a55e9a-4635-4e26-84c7-efc2c799aa67&pd_rd_w=dzYyC&pd_rd_wg=P7TTD&pf_rd_p=43ba9e17-96f5-4491-b054-e546013f7dc4&pf_rd_r=JNE8TQBMD6QDHSW3G8VG&qid=1564591663&s=gateway&linkCode=sl1&tag=lejimmy00-20&linkId=966450b360c4c041a7f13f6f09de7572&language=en_US"

    headers = {
        "User Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36"
    }

    print("Requesting URL...")
    page = requests.get(URL, headers=headers)

    soup = BeautifulSoup(page.content, "html.parser")

    title = soup.find(id="productTitle").get_text().strip()
    price = soup.find(id="priceblock_ourprice").get_text()
    conv_price = float(
        price.replace("$", "").replace(",", "")
    )

    return title, conv_price


def send_email(title, conv_price):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login("le.jimmy91@gmail.com", "ewdlehowahwgpiwd")

    subject = "Price Alert for {}".format(title)
    body = (
        "The curerent price is ${}! ".format(conv_price)
        + "Link to Amazon here: "
        + "https://amzn.to/31d6uQh"
    )

    msg = f"Subject: {subject}\n\n{body}"

    server.sendmail(
        "le.jimmy91@gmail.com", "lejimmy91@gmail.com", msg
    )

    print("Email has been sent!")

    server.quit()


def check_price():

    title, conv_price = get_url()

    print("Checking price...")
    if conv_price < 1700:
        print("Price is below $1,700!  Sending email.")
        send_email(title, conv_price)
    print("Finished checking price.")
    print("")


while True:
    check_price()
    time.sleep(86400)
