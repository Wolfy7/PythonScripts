import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import requests
from requests.exceptions import HTTPError
from bs4 import BeautifulSoup

SMTP_SERVER = [SMTP_SERVER_ADRESS]
SMTP_PORT = [SMTP_SERVER_PORT]
SENDER_ACCOUNT = [SENDER_ACCOUNT]
SENDER_PASSWORD = SENDER_PASSWORD
SENDER_NAME = [SENDER_NAME]
RECEIVER = [RECEIVER]

BASE_URL = 'https://www.kinopolis.de'
URL = BASE_URL + '/kg/events/filmreihe/erster-kinobesuch'


def greate_html(movie):
    specs = "<p>"
    for key, value in movie["movie_specs"].items():
        specs += key + ": <strong>" + value + " </strong>"
    specs += "</p>"

    events = ""
    for date, event in movie["events"].items():
        events += "<h2 style=\"margin: 0px 0px 6px 0px;\">" + date + "</h2>"
        for info in event:
            events += f"""
    <a href="{info["ticketing_link"]}" style="cursor: pointer;text-decoration: none;display: inline-block;">
    <span style="background-color: #205ac3; color: white; text-align: center;display: block;width: 160px;">{info["event"]}</span>
    <span style="text-align: center;text-decoration: none;display: block;width: 160px;font-size: 28px;color: #333;">{info["time"]}</span>
    <span style="color: #333;background-color: #ececec;border-top: 1px solid #fff;display: block;width: 160px;text-align: center;">{info["cinema"]}</span>
    </a>
            """

    html = """\
<html>
<body style='font-family: "Calibri";'>
    <h1 style="text-align: center;"><a href="{link}">{title}</a></h1>
    <img class="img-fluid" src="{img_src}" alt="{title}" style="float: left;height: 400px;margin-right: 12px;">
    <div style="display: flow-root;">
    {movie_specs}
    <p style="font-size: 18px;">
    {movie_description}
    </p>
    {movie_events}
</div>
</body>
</html>
    """.format(
        link = movie["movie_link"],
        title = movie["title"],
        img_src = movie["movie_img_src"],
        movie_specs = specs,
        movie_description = movie["description"],
        movie_events = events
    )
    return html


def send_email(html):
    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(SENDER_ACCOUNT, SENDER_PASSWORD)

    message = MIMEMultipart('alternative')
    message['From'] = SENDER_NAME
    message['To'] = RECEIVER
    message['Subject'] = "Mein erster Kinobesuch - " + URL

    message.attach(MIMEText(html, 'html'))
    text = message.as_string()

    server.sendmail(SENDER_NAME, RECEIVER, text)
    server.quit
    print("E-Mail wurde versandt.")


def find_movies():
    print("Suche nach aktuellen Veranstalltungen auf", URL, "...")
    try:
        # Get the Website
        response = requests.get(URL)

        # If the response was successful, no Exception will be raised
        response.raise_for_status()
    except HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"Other error occurred: {err}")
    else:
        # Parse the response
        soup = BeautifulSoup(response.content, 'html.parser')

        movies = {}
        for movie in soup.find_all("section", class_="movie"):
            movie_details = {}
            movie_id = movie.get("id")
            title = movie.find(class_="hl-link").text
            description = movie.find(class_="text").text
            movie_link = BASE_URL + movie.find(class_="link").get("href")

            for img in movie.find_all(class_="img-fluid"):
                if(img["alt"] == title):
                    movie_details["movie_img_src"] = img["src"]

            movie_spec = {}
            for movie_specs in movie.find_all(class_="movie__specs-el"):
                spec = movie_specs.text.strip().split(":", 1)
                movie_spec[spec[0]] = spec[1]

            dates = {}
            for movie_prog in movie.find_all(class_="movie__prog-el"):
                date = movie_prog.find(class_="prog-hl").text

                shows = []
                for prog_day in movie_prog.find_all(class_="prog__day"):
                    show = {}
                    show["ticketing_link"] = BASE_URL + prog_day.get("href")
                    show["event"] = prog_day.find(class_="prog__label").text
                    show["time"] = prog_day.find(class_="prog__time").text
                    show["cinema"] = prog_day.find(class_="prog__cinema").text
                    shows.append(show)

                dates[date] = shows
            movie_details["events"] = dates
            movie_details["title"] = title
            movie_details["description"] = description
            movie_details["movie_specs"] = movie_spec
            movie_details["movie_link"] = movie_link
            movies[movie_id] = movie_details
    return movies


def main():
    print("*" * 6, "Mein erster Kinobesuch", "*" * 6)
    file = "movies.txt"
    know_movies = []

    if os.path.isfile(file):
        with open(file) as f:
            know_movies = f.read().splitlines()

    movies = find_movies()
    for movie in movies.keys():
        # print(movie)
        # print(movies[movie])

        if movie in know_movies:
            print("Movie already know")
        else:
            print("New movie")
            html = greate_html(movies[movie])
            send_email(html)
            f = open(file, "a")
            f.write(movie + "\n")
            f.close()


if __name__ == '__main__':
    main()
