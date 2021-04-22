# This program outputs the appropriate Huntington-Hill and Webster apportionments
# By Maddie London, Sophie Borchart, Katie Encinas
import math
import pandas as pd
import numpy as np
import time
import re
import csv

def parse():
  filename = input('Please enter the filename containing your data, including the .csv extension: ')
  print('Parsing...')
  data = pd.read_csv(filename, header = None)

  state_name = data[0].dropna()
  year = 0
  # If the user had provided the year (optional)
  if hasNumbers(data[0][0]):
    year = data[0][0] # get year
    state_name = state_name.drop(state_name.index[0]) # store the state names 
  state_population = data[1].dropna() # store the state populations 
  total_population = 0
  # calculate the total population
  for s in state_population:
    total_population += s
  return year, state_name, state_population.tolist(), int(total_population)

def hasNumbers(inputString):
  return bool(re.search(r'\d', inputString))

def getQuotient(state_pop, divisor):
  quotient = state_pop/divisor
  if quotient < 1:
    return 1
  return quotient

def huntingtonHill(house_size, state_pop, total_pop):
  # print('Calculating divisor...')
  guess = total_pop/len(state_pop)
  apportionments = []
  
  # try higher d values than guess
  for d in range(int(guess), int(total_pop)):
    total_seats = 0
    apportionments = []
    apportionments.append('Huntington Hill')
    for s in state_pop:
      quotient = getQuotient(s, d)
      mean = getGeometricMean(quotient)
      seat = roundOnGeoMean(quotient, mean)
      total_seats += seat
      apportionments.append(seat)
    if int(total_seats) == int(house_size):
      # print('Collecting Huntington Hill apportionment data...')
      return apportionments
 
  # try lower d values than guess
  for d in range(1, int(guess)):
    total_seats = 0
    apportionments = []
    apportionments.append('Huntington Hill')
    for s in state_pop:
      quotient = getQuotient(s, d)
      mean = getGeometricMean(quotient)
      seat = roundOnGeoMean(quotient, mean)
      total_seats += seat
      apportionments.append(seat)
    if int(total_seats) == int(house_size):
      # print('Collecting Huntington Hill apportionment data...')
      return apportionments
  
  return 0

def getGeometricMean(quotient):
  roundUp = math.ceil(quotient)
  roundDown = math.floor(quotient)
  result = roundDown * roundUp
  geometricMean = (result)**(1/2)
  return geometricMean

def roundOnGeoMean(quotient, mean):
  seat = 0
  if quotient < mean: 
    seat = math.floor(quotient)
  else: 
    seat = math.ceil(quotient)
  return seat

def webster(house_size, state_pop, total_pop):
  # print('Calculating divisor...')
  guess = total_pop/len(state_pop)
  apportionments = []
  
  # try higher d values than guess
  for d in range(int(guess), int(total_pop)):
    total_seats = 0
    apportionments = []
    apportionments.append('Webster')
    for s in state_pop:
      quotient = getQuotient(s, d)
      seat = round(quotient)
      total_seats += seat
      apportionments.append(seat)
    if int(total_seats) == int(house_size):
      # print('Collecting Webster apportionment data...')
      return apportionments
  
  # try lower d values than guess
  for d in range(1, int(guess)):
    total_seats = 0
    apportionments = []
    apportionments.append('Webster')
    for s in state_pop:
      quotient = getQuotient(s, d)
      seat = round(quotient)
      total_seats += seat
      apportionments.append(seat)
    if int(total_seats) == int(house_size):
      # print('Collecting Webster apportionment data...')
      return apportionments
    
  return 0

def test(filename, min, max, type, state_name, state_pop, total_pop):
  
  list_of_apportionments = []
  state_name.insert(0, 'State')
  # print(state_name)
  list_of_apportionments.append(state_name)
  
  # Perform Huntington Hill apportionments
  if type == 'hh':
    for i in range(min, max):
      list_of_apportionments.append(huntingtonHill(i, state_pop, total_pop))
  # Perform Webster apportionments
  elif type == 'w':
    for i in range(min, max):
      list_of_apportionments.append(webster(i, state_pop, total_pop))
  # Perform both Huntington Hill and Webster apportionments
  elif type == 'b':
    for i in range(min, max):
      list_of_apportionments.append(huntingtonHill(i, state_pop, total_pop))
      list_of_apportionments.append(webster(i, state_pop, total_pop))
  
  rows = np.array(list_of_apportionments).T
  
  with open(filename, 'w') as csvfile: 
    print('Writing to output file...')
    csvwriter = csv.writer(csvfile)
    csvwriter.writerows(rows) 
    print(f'Results written to {filename}')
  return 0

def main():
  year, state_name, state_population, total_pop = parse()
  state_name = state_name.tolist()
  min = input('Please enter your desired minimum house size: ')
  max = input('Please enter your desired maximum house size: ')
  apportionment_type = 'b'
  output_filename = 'output.csv'
  test(output_filename, int(min), int(max), apportionment_type, state_name, state_population, total_pop)

  return 0

if __name__ == '__main__':
  start_time = time.time()
  main()
  print("This program executed in %s seconds" % (time.time() - start_time))
  print('Goodbye!')