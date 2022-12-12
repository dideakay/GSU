import random as random
import numpy as np

SIZE = 100
stock = [30, 40, 20, 40, 20]
products = ["A", "B", "C", "D", "E"]
prices = [1, 4, 6, 4, 4,
          3, 8, 2, 5, 15,
          3, 12,3, 5, 5,
          2, 6, 10, 2, 4,
          10,5, 12, 6, 3]
current_population = []
current_fitness = []
max_score = 0

def matrix_print(m):
    result = ""
    for product in range (5):
        result = result + (f'{products[product]} | ')
        for city in range (5):
            value = m[product*5 + city]
            if(value<10):
                result = result + (f' {value} ')
            else:
                result = result + (f'{value} ')
        result = result + (f'\n')
    print(result)

def population_print(p, size):
    for i in range(size):
        print(f'--------INDIVIDUAL {i}-------')
        matrix_print(p[i])
        #fitness_fn(p[i])

def create_population(size):
    new_population = []
    
    for i in range (size):
        visited_cities = []
        #let's choose visited cities at random
        for i in range (5):
            visited_cities.append(random.randint(0,1))
        temp_stock = [30, 40, 20, 40, 20]
        new_individual = create_individual(temp_stock, visited_cities)
        current_population.append(new_individual)
        new_population.append(new_individual)
    return new_population
    

def create_individual(stock, cities):
    individual = []
    for product in range (5):
        for city in range (5):
            amount = 0
            #0 sales if city is not visited
            if (cities[city]==0):
                individual.append(amount)
            else:
                current_stock = stock[product]
                #choose between 0<=n<=stock[product] randomly
                if(current_stock != 0):
                    #if in the last city and still got stock, finish it
                    amount = current_stock
                    if(city != 4):
                        amount = random.randint(0, current_stock)
                individual.append(amount)
                stock[product] -= amount
    return individual

def fitness_fn(x):
    f = 0
    fbase = 0
    city_sales = []
    gain_matrice = np.empty([5,5])
    
    #fbase
    for product in range (5):
        for city in range (5):
            gain = prices[product*5 + city]*x[product*5 + city]
            fbase += gain
            gain_matrice[city][product] = gain
  
    #f1
    visited_every_city = 1
    sum_sales_per_city = [] #will be useful for f3
    for city in range (5):
        city_sum = 0
        city_sales.append([])
        for product in range (5):
            sale_amount=x[product*5 + city]
            city_sum += sale_amount
            city_sales[city].append(sale_amount) #will be useful for f2, includes every city's sales in 2d array
        if ((city_sum == 0)):
            visited_every_city = 0
        sum_sales_per_city.append(city_sum)
    f1 = visited_every_city*100

    #f2
    f2 = 0
    bonus_percent = 0
    for city in range (5):
        diff = (max(city_sales[city])-min(city_sales[city]))
        bonus_percent = (max((20-diff), 0))/100
        for product in range (5):
            f2 += bonus_percent*(gain_matrice[product][city])
    
    #f3
    f3 = 0
    for city in range (5):
        maxf3=max(sum_sales_per_city)
        minf3=min(sum_sales_per_city)
        diff_f3 = maxf3-minf3
        f3_percentage = (max((20-diff_f3), 0))/100
        f3 += fbase*f3_percentage

    f = fbase + f1 + f2 + f3
    return f

def random_selection(population):
    l = random.choices(population, weights=current_fitness, k=2)
    return l[0], l[1]     

#to be implemented
#mutate(child, alphabet):
    #c = random.random(1, len(c))
    #letter = random.random(alphabet)
    #child[c] = letter

def reproduce(x, y):
    #to avoid selling more than the stocks, matrice is divided by its lines which represent products
    c = random.randint(0, 4)
    child = x[0: c*5] + y[c*5:]
    return child

def find_most_fit(population):
    max = 0
    index = 0
    current_fitness.clear()
    for i in range(SIZE):
        score = fitness_fn(population[i])
        current_fitness.append(score)
        if score > max:
            max = score
            index = i
    return index, max
    

def GA(population):
    fit_index = 0
    for j in range (100):
        new_population = []
        print(f'-------iteration: {j} ----------')
        for i in range (len(population)-1):
            x, y = random_selection(population)
            child = reproduce(x, y)

            #if(random(true, false, probability)): #to be implemented
                #child = mutate(child)

            new_population.append(child)
        
        #the fittest will survive directly, it is immortal for this generation
        new_population.append(population[fit_index])
        fit_index, score = find_most_fit(new_population)
        print(f'max score: {score}')
        population = new_population

    print("\nfittest individual\n")
    matrix_print(population[fit_index])     

new_population = create_population(SIZE)
fit_index, score = find_most_fit(current_population)
print(f'max score: {score}') #initial population's maximum fitness score
GA(current_population)

#population_print(current_population, SIZE) #can be used to examine individuals

