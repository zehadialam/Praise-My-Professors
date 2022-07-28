from flask import Blueprint, render_template
import json
import math
import requests

views = Blueprint(__name__, "views")


def create_reviews_list(tid):
    tempreviewslist = []
    num_of_reviews = get_total_reviews(tid)
    num_of_pages = math.ceil(num_of_reviews / 20)
    for i in range(1, num_of_pages + 1):
        page = requests.get(
            "https://www.ratemyprofessors.com/paginate/professors/ratings?tid="
            + str(tid)
            + "&filter=&courseCode=&page="
            + str(i)
        )
        temp_jsonpage = json.loads(page.content)
        temp_list = temp_jsonpage["ratings"]
        tempreviewslist.extend(temp_list)
    return tempreviewslist


def get_total_reviews(tid):
    page = requests.get(
        "https://www.ratemyprofessors.com/paginate/professors/ratings?tid="
        + str(tid)
        + "&filter=&courseCode=&page=1"
    )
    temp_jsonpage = json.loads(page.content)
    num_of_reviews = temp_jsonpage["remaining"] + 20
    return num_of_reviews


def calculate_average_rating(reviews):
    sum = 0
    total = 0
    for review in reviews:
        if review["rOverall"] >= 4.0:
            sum += review["rOverall"]
            total += 1
    average = sum / total
    return round(average, 1)


def calculate_total_positive_reviews():
    total_reviews = 0
    for review in reviews:
        if review["rOverall"] >= 4.0:
            total_reviews += 1
    return total_reviews


def calculate_five_stars():
    total = 0
    for review in reviews:
        if review["rOverall"] == 5.0:
            total += 1
    return total


def calculate_four_stars():
    total = 0
    for review in reviews:
        if review["rOverall"] == 4.0:
            total += 1
    return total


def calculate_five_star_percentage(reviews):
    total_reviews = calculate_total_positive_reviews()
    total_five_stars = calculate_five_stars()
    return round((total_five_stars / total_reviews) * 100)


def calculate_four_star_percentage(reviews):
    total_reviews = calculate_total_positive_reviews()
    total_four_stars = calculate_four_stars()
    return round((total_four_stars / total_reviews) * 100)


reviews = create_reviews_list(2148458)
total_reviews = calculate_total_positive_reviews()
average_rating = calculate_average_rating(reviews)
five_stars_percentage = calculate_five_star_percentage(reviews)
four_stars_percentage = calculate_four_star_percentage(reviews)
five_stars = calculate_five_stars()
four_stars = calculate_four_stars()


@views.route("/")
def home():
    return render_template("index.html", reviews=reviews, average_rating=average_rating, five_stars_percentage=five_stars_percentage, four_stars_percentage=four_stars_percentage, total_reviews=total_reviews
    ,five_stars=five_stars, four_stars=four_stars)
