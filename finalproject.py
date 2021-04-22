# This program outputs the appropriate Huntington-Hill and Webster apportionments
# By Maddie London, Sophie Borchart, Katie Encinas
import math
import pandas as pd
import time

def parse():
  filename = input('Please enter the filename containing your data, including the .csv extension: ')
  print('Parsing...')
  data = pd.read_csv(filename, header = None)

  year = data[0][0] # get data year

  state_name = data[0].dropna()
  state_name = state_name.drop(state_name.index[0]) # store the state names 
  state_population = data[1].dropna() # store the state populations 

  total_population = 0
  # calculate the total population
  for s in state_population:
    total_population += s
  return year, state_name, state_population, int(total_population)

def getQuotient(state_pop, divisor):
  quotient = state_pop/divisor
  if quotient < 1:
    return 1
  return quotient


def huntingtonHiill(house_size, state_pop, total_pop):
  print('Calculating divisor...')
  guess = total_pop/len(state_pop)
  apportionments = []
  # try higher d values than guess
  for d in range(int(guess), int(max(state_pop))):
    total_seats = 0
    apportionments = []
    for s in state_pop:
      quotient = getQuotient(s, d)
      mean = getGeometricMean(quotient)
      seat = roundOnGeoMean(quotient, mean)
      total_seats += seat
      apportionments.append(seat)
    if int(total_seats) == int(house_size):
      print('Collecting apportionment data...')
      return d, apportionments
  # try lower d values than guess
  for d in range(int(min(state_pop)), int(guess)):
    total_seats = 0
    apportionments = []
    for s in state_pop:
      quotient = getQuotient(s, d)
      mean = getGeometricMean(quotient)
      seat = roundOnGeoMean(quotient, mean)
      total_seats += seat
      apportionments.append(seat)
    if int(total_seats) == int(house_size):
      print('Collecting apportionment data...')
      return d, apportionments

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

# def webster():

def main():
  year, state_name, state_population, total_pop = parse()
  house_size = input('Please enter your desired house size: ')
  print(huntingtonHiill(house_size, state_population, total_pop))

if __name__ == '__main__':
  start_time = time.time()
  main()
  print("This program executed in %s seconds" % (time.time() - start_time))
  print('Goodbye!')