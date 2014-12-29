import sqlite3 as lite
import pandas as pd


cities = (('New York City', 'NY'),('Boston', 'MA'),
    ('Chicago', 'IL'),    ('Miami', 'FL'),
    ('Dallas', 'TX'),    ('Seattle', 'WA'),
    ('Portland', 'OR'),    ('San Francisco', 'CA'),
    ('Los Angeles', 'CA'),    ('Las Vegas', 'NV'),
    ('Atlanta', 'GA'))
weather = (('New York City', 2013, 'July', 'January', 62), 
	('Boston',          2013,    'July',        'January',     59), ('Chicago',         2013,    'July',        'January',     59), 
	('Miami',           2013,    'August',      'January',     84), ('Dallas',          2013,   'July',        'January',     77),
	('Seattle',         2013,    'July',        'January',     61), ('Portland',        2013,    'July',        'December',    63),
	('San Francisco',   2013,    'September',   'December',    64),('Los Angeles',     2013,  'September',   'December',    75)
	)


# Here you connect to the database. The `connect()` method returns a connection object.
con = lite.connect('getting_started.db')

with con:
  # From the connection, you get a cursor object. The cursor is what goes over the records that result from a query.
  cur = con.cursor()    
  
  # Creating cities and weather tabels 
  cur.execute('DROP TABLE IF EXISTS cities')
  cur.execute('CREATE TABLE cities (name text, state text)')
  cur.execute('DROP TABLE IF EXISTS weather')
  cur.execute('CREATE TABLE weather (city text, year integer, warm_month text, cold_month text, average_high integer)')

  #Populating tables with data ...
  cur.executemany("INSERT INTO cities VALUES(?,?)", cities)
  cur.executemany("INSERT INTO weather VALUES(?,?,?,?,?)", weather)

  # You're fetching the data from the cursor object. Because you're only fetching one record, you'll use the `fetchone()` method. 
  # If fetching more than one record, use the `fetchall()` method.

  cur.execute("SELECT name, state, year, warm_month, cold_month FROM cities INNER JOIN weather ON name = city")

  rows = cur.fetchall()
  cols = [desc[0] for desc in cur.description]

  df = pd.DataFrame(rows, columns=cols)
  list_value = ['July']
 
  warmest_cities =  df[df['warm_month'].isin(list_value)]
	

  # Finally, print the result.

  for index, row in warmest_cities.iterrows():
  	print "%s, %s is warmest in %s" % (row['name'], row['state'], row['warm_month'])
