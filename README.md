# electricity-price-analysis
In this assignment, we will therefore investigate how these prices have varied for household customers and villa customers during the years 2018-2023.

Task description

The electricity prices have varied significantly in recent years.

In this assignment, we will therefore investigate how these prices have varied for household customers and villa customers during the years 2018-2023.

The electricity prices are retrieved from the website of the Swedish Energy Market Inspectorate (EI) (https://ei.se/) and are stored in CSV files called lghpriser.csv and villapriser.csv (the two figures below show parts of the content of these files).

The file contains the electricity price per month for variable price, fixed price 1 year and fixed price 3 years for price areas SE1-SE4 (as you probably already know, Sweden has 4 electricity price areas where SE1 is located in the north and SE4 in the south).

lghpriser.csv:
print(lgh_data[0:3])

Output
[['Ar', 'manad', 'SE1-Fast pris 1 ar', 'SE1-Fast pris 3 ar', 'SE1-Rorligt pris', 'SE2-Fast pris 1 ar', 'SE2-Fast pris 3 ar', 'SE2-Rorligt pris', 'SE3-Fast pris 1 ar', 'SE3-Fast pris 3 ar', 'SE3-Rorligt pris', 'SE4-Fast pris 1 ar', 'SE4-Fast pris 3 ar', 'SE4-Rorligt pris'], ['2018', 'januari', '64.12', '63.98', '67.81', '63.87', '63.76', '67.92', '64.95', '65.31', '68.28', '66.07', '66.34', '69.38'], ['2018', 'februari', '66.01', '64.29', '77.14', '65.82', '63.96', '77.42', '67.04', '65.54', '77.96', '68.02', '66.58', '78.91']]
