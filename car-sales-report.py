#!/usr/bin/env python3

from collections import defaultdict
import json
import locale
import sys
import reports
import emails

def load_data(filename):
  """Loads the contents of filename as a JSON file."""
  with open(filename) as json_file:
    data = json.load(json_file)
  return data


def format_car(car):
  """Given a car dictionary, returns a nicely formatted name."""
  return "{} {} ({})".format(
      car["car_make"], car["car_model"], car["car_year"])


def process_data(data):
  """Analyzes the data, looking for maximums.

  Returns a list of lines that summarize the information.
  """
  max_revenue = {"revenue": 0}
  max_sales = {"sales": 0}
  
  for item in data:
    # Calculate the revenue generated by this model (price * total_sales)
    # We need to convert the price from "$1234.56" to 1234.56
    item_price = locale.atof(item["price"].strip("$"))
    item_revenue = item["total_sales"] * item_price
    if item_revenue > max_revenue["revenue"]:
      item["revenue"] = item_revenue
      max_revenue = item 
    # TODO: also handle max sales
    # TODO: also handle most popular car_year
    item_sale = item["total_sales"]  
    if item_sale > max_sales["sales"]:
       item["sales"] = item_sale
       max_sales = item
  car_yearlist = defaultdict(int)
  car_years = {"year": 0,
               "sales": 0
  }       
  
  for item in data:
       car_year = item["car"]["car_year"]
       car_yearlist[car_year] += 1
  car_yearlist = dict(car_yearlist)
  car_years["year"] += (max(car_yearlist, key=car_yearlist.get))
  
  for item in data:
       if item["car"]["car_year"] == car_years["year"]:
           car_years["sales"] += item["total_sales"]
  summary = [ 
    "The {} generated the most revenue: ${}".format(
      format_car(max_revenue["car"]), max_revenue["revenue"]),
      "The {} had most sales: {}".format(format_car(max_sales["car"]), max_sales["sales"]),
    "The most popular year was {} with {} sales.".format((car_years["year"]), car_years["sales"])
  ]

  return summary

def cars_dict_to_table(car_data):
  """Turns the data in car_data into a list of lists."""
  table_data = [["ID", "Car", "Price", "Total Sales"]]
  for item in car_data:
    table_data.append([item["id"], format_car(item["car"]), item["price"], item["total_sales"]])
  return table_data

def main(argv):
  """Process the JSON data and generate a full report out of it."""
  data = load_data("car_sales.json")
  summary = ' '.join(process_data(data))
  print(summary)
  cars_dict_to_table
  # TODO: turn this into a PDF report
  reports.generate("/tmp/cars.pdf", "Sales summary for last month", str(summary) + "<br/>", cars_dict_to_table(data)) 

  # TODO: send the PDF report as an email attachment

  sender = "automation@example.com"
  receiver = "student-03-b84e0329a186@example.com"
  subject = "Sales summary for last month"
  body = str(summary)
  message = emails.generate(sender, receiver, subject, body, "/tmp/cars.pdf")
  emails.send(message)

if __name__ == "__main__":
  main(sys.argv)


