#
# "SUDOKU!" EVOLUTIONARY ALGORITHM  
#


from random import choice, random
from collections import Counter

"""
Function to import the Sudoku Base problem from file.
Problem should be 9 lines by 9 characters each consisting either '.' or integer 1-9
"""
def import_Sudoku_Problem():
    sudoku_base = []
    sudoku = input("Please enter the filepath to the Sudoku Puzzle")
    with open(sudoku, "r") as f:
        sudoku_base = [list(line.rstrip('\n')) for line in f]
        #print(sudoku_base)
    return sudoku_base


"""
Function to print state of a sudoku generation
"""
def print_box(sudoku):
    i = 0
    for each in sudoku:
        if i == 0 or i == 3 or i == 6:
            print("-------------------")
        print("| {}{}{} | {}{}{} | {}{}{} |".format(each[0],each[1],each[2],each[3],each[4],each[5],each[6],each[7],each[8]))
        i += 1
        if i ==9:
            print("-------------------")


def outputFitnessTracker(fitness_tracker):
    with open ("sudoku_output.txt","a") as f:
        f.write(','.join([str(x) for x in fitness_tracker]) + "\n")
    f.close()

"""
Main Function of Program to control Flow of the Evolutionary Algorithm
"""
def evolve():
    #Defining Static Values defining the stocastic biases of the EA

    SUDOKU_BASE = import_Sudoku_Problem()
    NUMBER_GENERATION = 100 #Number of generations that will be created 
    POPULATION_SIZE = 10000 #Number of population members created in each generation
    TRUNCATION_RATE = 0.2 #Determines Percentage of top solution fits selected to bias crossovers and mutations
    MUTATION_RATE = 0.05 #Determines the probability of an individual value of population mutating to diffrent value
    ALPHABET = "123456789"

    #Defining, creating and evaulating an initial population generation 
    for i in range(0,5):
        Fitness_tracker = []
        population = create_pop(SUDOKU_BASE, POPULATION_SIZE, ALPHABET)
        fitness_population = evaluate_pop(population)

    #Loop defined by Number of generations to iteratively generate and evolve new populations
        for gen in range(NUMBER_GENERATION):
            #create a pool for random selection based evolution by taking the a percentege of 
            #the top fitting individuals of a population based on the truncation rate 
            mating_pool = select_pop(population, fitness_population, POPULATION_SIZE, TRUNCATION_RATE)

            #use the created pool to create 'sexually' a new population generation 
            offspring_population = crossover_pop(mating_pool, POPULATION_SIZE)

            #Allow randomly some members of population individuals to mutate
            population = mutate_pop(offspring_population, SUDOKU_BASE, MUTATION_RATE, ALPHABET)

            #evaluate the fitness of all individuals of a population
            fitness_population = evaluate_pop(population)

            #Select the individual from the population with the lowest fitness score
            best_ind, best_fit = best_pop(population, fitness_population)

            #output the best member of the generation to output to console
            print ("Gen:%3d" % gen, " |  Fit:%3d" % best_fit) # Output of generation
            print_box(best_ind)
            Fitness_tracker.append(best_fit)

        outputFitnessTracker(Fitness_tracker)



### POPULATION-LEVEL OPERATORS ###
"""
Function to generate an entire population of individuals 
"""
def create_pop(Sudoku_base, POPULATION_SIZE, ALPHABET):
    pop_create = [ create_ind(Sudoku_base, ALPHABET) for _ in range(POPULATION_SIZE)]
    return  pop_create


"""
Function to evaluate an entire population of individuals 
"""
def evaluate_pop(population):
    eval_pop = [ evaluate_ind(individual) for individual in population ]
    #print("Eval_pop returns{}".format(eval_pop))
    return eval_pop # evaluates an entire population


"""
Function to select the top percentage of individuals in a population based on the truncation rate 
"""
def select_pop(population, fitness_population, POPULATION_SIZE, TRUNCATION_RATE): #selects a population
    sorted_population = sorted(zip(population, fitness_population), key = lambda ind_fit: ind_fit[1])
    selected_pop = [ individual for individual, fitness in sorted_population[:int(POPULATION_SIZE * TRUNCATION_RATE)] ]
    return selected_pop


"""
Function to randomly generate a population of individuals by comparing randomly two existing members of the prior population 
"""
def crossover_pop(population, POPULATION_SIZE): #completate a crossover function for each population
    cross_pop = [ crossover_ind(choice(population), choice(population)) for _ in range(POPULATION_SIZE) ]
    return cross_pop


"""
Function to take a population and allow for random mutations to occur in individuals of said population 
"""
def mutate_pop(population, Sudoku_base, MUTATION_RATE, ALPHABET):#mutates a population
    mut_pop = [ mutate_ind(individual, Sudoku_base, MUTATION_RATE, ALPHABET) for individual in population ]
    #print("mutate_pop produces {} from population {}".format(mut_pop, population))
    return mut_pop


"""
Function to select the best fitting individual of the current population
"""
def best_pop(population, fitness_population): #generates an ideal population?
    pop_best = sorted(zip(population, fitness_population), key = lambda ind_fit: ind_fit[1])[0]
    #print("best_pop produced {} from population {} and fitness population {}".format(pop_best, population, fitness_population))
    return pop_best




### TARGET COMPARISON FUNCTIONS ###

"""
Function to collect together s singular subgrid of the sudoku into a list for easier comparison
"""
def collect_box(individual, box_index1, box_index2):
    box = []
    for i in range(box_index1, box_index1+3):
            for j in range(box_index2, box_index2+3):
                box.append(individual[i][j])
    return box


"""
Function to determine the fitness of an individual passed from a population based on the completion rules of sudoku
For each repeat value of an integer 1-9, there is an increase in fitness score
"""
def check_target(individual):
    #Define and initialise variables for components of fitness value - Horizontal, Vertical and box collisions
    horizontal_score = 0
    vertical_score = 0
    box_score = 0

    #Collate the 3x3 subgrids of sudoku into 1x9 lists to check for collisions
    boxes = []
    #print("Creating boxes from individual {}".format(individual))
    boxes.append(collect_box(individual, 0, 0))
    boxes.append(collect_box(individual, 0, 3))
    boxes.append(collect_box(individual, 3, 0))
    boxes.append(collect_box(individual, 0, 6))
    boxes.append(collect_box(individual, 6, 0))
    boxes.append(collect_box(individual, 3, 3))
    boxes.append(collect_box(individual, 3, 6))
    boxes.append(collect_box(individual, 6, 3))
    boxes.append(collect_box(individual, 6, 6))
    #print("Boxes = {}".format(boxes))

    horizontals = []
    for i in range(0,9):
        horizontal = []
        for j in range(0,9):
            horizontal.append(individual[j][i])
        horizontals.append(horizontal)

   #Calcuates Score horizontally
    for i in range(0,9): #Index either vertically or horizontally
        #Compare number to each subsequent number to determine collisions
        horizontal_ind = Counter(individual[i])
        vertical_ind = Counter(horizontals[i])
        box_ind = Counter(boxes[i])
        for key in horizontal_ind:
            horizontal_score += horizontal_ind[key]-1
        for key in vertical_ind:
            vertical_score += vertical_ind[key]-1
        for key in box_ind:
            box_score += box_ind[key]-1
    total_score = horizontal_score+vertical_score+box_score
    return horizontal_score+vertical_score+box_score




### INDIVIDUAL-LEVEL OPERATORS: REPRESENTATION & PROBLEM SPECIFIC ###
"""
Function to create randomly an individual of a population
"""
def create_ind(Sudoku_base, ALPHABET): 
    initial_pop = []
    for i in range(0,9):
        row = []
        for j in range(0,9):
            if '.' in Sudoku_base[i][j]:
                row.append(choice(ALPHABET))
            else:
                row.append(Sudoku_base[i][j])
        initial_pop.append(row)
    return initial_pop


"""
function to evaluate the fitness of an individual of a population
"""
def evaluate_ind(individual):
    eval_ind = check_target(individual)
    return  eval_ind


"""
Function to create a new individual based on random selection between two provided individuals
"""
def crossover_ind(individual1, individual2):
    cross_ind = [[],[],[],[],[],[],[],[],[]]
    for i in range(0,9):
        for j in range(0,9):
            cross_ind_item = (individual1[i][j], individual2[i][j])
            cross_ind[i].append(choice(cross_ind_item))
    return cross_ind 


"""
Function which allows for members of an individual of a population to mutate randomly
"""
def mutate_ind(individual, Sudoku_Base, MUTATION_RATE, ALPHABET):
    for i in range(0,9):
        for j in range(0,9):
            if random()<MUTATION_RATE:
                individual[i][j] = choice(ALPHABET)
            if Sudoku_Base[i][j] != '.':
                individual[i][j] = Sudoku_Base[i][j]
    return individual  #mutates an individual member


if __name__ == "__main__":
    evolve()
    #random.seed(10)