# A while loop is used to ask the user for a price area until a valid answer is given.
# This type of loop is suitable for this type of program because the user's response does not interrupt the program but runs until a conditional statement.
def get_price_area():
  while True:
    price_area = input("Enter price area (1-4): ")

    if price_area == '':
      break

    try:
      price_area = price_area.strip()
      price_area = int(price_area)

      if price_area < 1 or price_area > 4:
        print("Please enter one of the specified areas (1-4).")
        continue
      else:
        return int(price_area)

    except:
      print("Try again!")
      continue


def get_year():
  while True:
    year = input("Enter the year to be presented (2018-2023): ")

    if year == '':
      break

    try:
      year = year.strip()
      year = int(year)

      if year < 2018 or year > 2023:
        print("Please enter one of the specified years (2018-2023).")
        continue
      else:
        return int(year)

    except:
      print("Try again!")
      continue


def create_diagram(area, year):
  months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]  # Initialize the diagram with the x-axis grading as jan-dec
  plt.figure(figsize=(10, 10))  # To enlarge the diagram

  # Call the read_file function and then save the value in lgh_data and villa_data respectively
  lgh_data = read_file('lghpriser.csv')
  villa_data = read_file('villapriser.csv')

  # Save the file headers in the variables lgh_header and villa_header.
  lgh_header = lgh_data[0]  # Get the headers on row 0 of the file over lgh prices
  villa_header = villa_data[0]  # Get row 0 of the file over lgh prices
  new_labels = ["Fixed price 1 year - villa", "Flexible price - villa"]  # Changed to new labels

  if year == 2023:
    month_index = 7
  else:
    month_index = 12

  try:
    start, end = get_year_index(year)  # Use a conditional statement to find the start and end of the index and save it in the variables start and end

    for column in [f"SE{area}-Fast price 1 year", f"SE{area}-Flexible price"]:  # Area 1-4 specifies which column to iterate over
      index = lgh_header.index(column)
      y_lgh = [float(row[index]) for row in lgh_data[start:end]]  # start and end determine the year that is printed out (eg 1:13 corresponds to 2018)
      y_villa = [float(row[index]) for row in villa_data[start:end]]

      # Todo change to new labels
      plt.plot(months[:month_index], y_lgh, label=f"{column} - Lgh {year}")
      plt.plot(months[:month_index], y_villa, label=f"{column} - Villa {year}")

    show_diagram(area, year)  # The program calls the function that prints out the diagram after the loop is finished

  except ValueError:
    print("Your area or year could not be found, please enter a new one")


# The program's main function calls functions to retrieve data and create diagrams
def main():
  user_area = get_price_area()  # Calls the function that asks the user for a price area and saves it in the variable
  print("Selected price area:", user_area)
