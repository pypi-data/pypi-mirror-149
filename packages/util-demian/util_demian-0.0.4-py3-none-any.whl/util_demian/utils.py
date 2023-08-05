import os
import datetime
import json
import textwrap
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import logging

logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(levelname)s: [%(name)s] %(message)s')
ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.setLevel(logging.ERROR)


def get_json(path: str):
    # 치과의 json 파일을 불러온다.
    with open(os.path.join(path), 'r', encoding='UTF8') as f:
        json_data = json.load(f)
    logger.info(json_data)
    return json_data


def mail_to(title: str, text: str, mail_addr='hj3415@hanmail.net') -> bool:
    # 메일을 보내는 함수
    login_id_pass = ('hj3415@gmail.com', 'orlhfaqihcdytvsw')
    # 로그인 인자의 두번째 앱비밀번호는 구글계정 관리에서 설정함.
    smtp = ('smtp.gmail.com', 587)

    msg = MIMEMultipart()
    msg['From'] = login_id_pass[0]
    msg['Subject'] = title
    msg['To'] = mail_addr
    msg.attach(MIMEText(datetime.datetime.today().strftime('%I:%M%p') + '\n' + textwrap.dedent(text)))

    smtp = smtplib.SMTP(smtp[0], smtp[1])
    smtp.ehlo()
    try:
        smtp.starttls()
        smtp.login(login_id_pass[0], login_id_pass[1])
        smtp.sendmail(login_id_pass[0], mail_addr, msg.as_string())
        print(f'Sent mail to {mail_addr} successfully.')
        return True
    except:
        print(f'Unknown error occurred during sending mail to {mail_addr}.')
        return False
    finally:
        smtp.close()


def make_robots() -> str:
    robots_contents = """User-agent: *
Disallow: /admin
Allow: /

User-agent: Mediapartners-Google
Allow: /

User-agent: bingbot
Crawl-delay: 30"""
    return robots_contents


def make_up_vendor_css(theme: str) -> list:
    animate = os.path.join('vendor', 'animate.css', 'animate.min.css')
    bootstrap = os.path.join('vendor', 'bootstrap', 'css', 'bootstrap.min.css')
    bi = os.path.join('vendor', 'bootstrap-icons', 'bootstrap-icons.css')
    bx = os.path.join('vendor', 'boxicons', 'css', 'boxicons.min.css')
    fontawesome = os.path.join('vendor', 'fontawesome-free', 'css', 'all.min.css')
    glightbox = os.path.join('vendor', 'glightbox', 'css', 'glightbox.min.css')
    remixicon = os.path.join('vendor', 'remixicon', 'remixicon.css')
    swiper = os.path.join('vendor', 'swiper', 'swiper-bundle.min.css')
    aos = os.path.join('vendor', 'aos', 'aos.css')

    if theme == 'mentor_ds':
        return [animate, aos, bootstrap, bi, bx, remixicon, swiper]
    if theme == 'medilab_ds':
        return [animate, bootstrap, bi, bx, fontawesome, glightbox, remixicon, swiper]
    elif theme == 'bethany_ds':
        return [aos, bootstrap, bi, bx, glightbox, remixicon, swiper]


def make_up_vendor_js(theme: str) -> list:
    bootstrap = os.path.join('vendor', 'bootstrap', 'js', 'bootstrap.bundle.min.js')
    glightbox = os.path.join('vendor', 'glightbox', 'js', 'glightbox.min.js')
    phpemailform = os.path.join('vendor', 'php-email-form', 'validate.js')
    purecounter = os.path.join('vendor', 'purecounter', 'purecounter.js')
    swiper = os.path.join('vendor', 'swiper', 'swiper-bundle.min.js')
    aos = os.path.join('vendor', 'aos', 'aos.js')
    isotope = os.path.join('vendor', 'isotope-layout', 'isotope.pkgd.min.js')

    if theme == 'mentor_ds':
        return [aos, bootstrap, phpemailform, swiper, purecounter]
    if theme == 'medilab_ds':
        return [bootstrap, glightbox, isotope, phpemailform, swiper, purecounter]
    elif theme == 'bethany_ds':
        return [aos, bootstrap, glightbox, isotope, phpemailform, swiper, purecounter]
