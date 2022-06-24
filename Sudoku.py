#
# "SUDOKU!" EVOLUTIONARY ALGORITHM  
#

from random import choice, random

### EVOLUTIONARY ALGORITHM ###
def import_Sudoku_Problem():
    sudoku_base = []
    sudoku = input("Please enter the filepath to the Sudoku Puzzle")
    with open(sudoku, "r") as f:
        sudoku_base = [list(line.rstrip('\n')) for line in f]
        #print(sudoku_base)
    return sudoku_base

def print_box(sudoku):
    i = 0
    for each in sudoku:
        if i == 0 or i == 3 or i == 6:
            print("-------------------")
        print("| {}{}{} | {}{}{} | {}{}{} |".format(each[0],each[1],each[2],each[3],each[4],each[5],each[6],each[7],each[8]))
        i += 1
        if i ==9:
            print("-------------------")


def evolve():
    Sudoku_base = import_Sudoku_Problem()
    population = create_pop(Sudoku_base) #Initialisation of Population
    fitness_population = evaluate_pop(population) # Analysis of initial population
    for gen in range(NUMBER_GENERATION): # Termination through exhaustion
        mating_pool = select_pop(population, fitness_population) # Selection / Variation
        offspring_population = crossover_pop(mating_pool) # Crossover
        population = mutate_pop(offspring_population) # Mutation
        fitness_population = evaluate_pop(population) # Evaluation
        best_ind, best_fit = best_pop(population, fitness_population) # Replacement
        print ("Gen:%3d" % gen, " |  Fit:%3d" % best_fit) # Output of generation
        print_box(best_ind)


### POPULATION-LEVEL OPERATORS ###
def create_pop(Sudoku_base):
    pop_create = [ create_ind(Sudoku_base) for _ in range(POPULATION_SIZE)]
    #print("create pop created population {}".format(pop_create))
    return  pop_create#creates an entire population

def evaluate_pop(population):
    eval_pop = [ evaluate_ind(individual) for individual in population ]
    #print("Eval_pop returns{}".format(eval_pop))
    return eval_pop # evaluates an entire population

def select_pop(population, fitness_population): #selects a population
    sorted_population = sorted(zip(population, fitness_population), key = lambda ind_fit: ind_fit[1])
    selected_pop = [ individual for individual, fitness in sorted_population[:int(POPULATION_SIZE * TRUNCATION_RATE)] ]
    #print("select_pop produces {} from population {} and fitness population {}".format(selected_pop, population, fitness_population))
    return selected_pop

def crossover_pop(population): #completate a crossover function for each population
    cross_pop = [ crossover_ind(choice(population), choice(population)) for _ in range(POPULATION_SIZE) ]
    #print("crossover_pop produces {} from population {}".format(cross_pop, population))
    return cross_pop

def mutate_pop(population):#mutates a population
    mut_pop = [ mutate_ind(individual) for individual in population ]
    #print("mutate_pop produces {} from population {}".format(mut_pop, population))
    return mut_pop

def best_pop(population, fitness_population): #generates an ideal population?
    pop_best = sorted(zip(population, fitness_population), key = lambda ind_fit: ind_fit[1])[0]
    #print("best_pop produced {} from population {} and fitness population {}".format(pop_best, population, fitness_population))
    return pop_best

def collect_box(individual, box_index1, box_index2):
    box = []
    for i in range(box_index1, box_index1+3):
            for j in range(box_index2, box_index2+3):
                #print(" box_ind is {} with index i = {} j = {}".format(individual[i][j], i, j))
                box.append(individual[i][j])
    #print(box)
    return box

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

   #Calcuates Score horizontally
    for i in range(0,9): #Index either vertically or horizontally
        for j in range(0,9): #Index for Alternative Vertical or horizontal
            for k in range(j,9): #Compare number to each subsequent number to determine collisions
                if individual[i][j] == individual[i][k]:
                    horizontal_score += 1
                if individual[j][i] == individual[i][k]:
                    vertical_score += 1
                if boxes[i][j] == boxes[i][k]:
                    box_score += 1

    return horizontal_score+vertical_score+box_score

### INDIVIDUAL-LEVEL OPERATORS: REPRESENTATION & PROBLEM SPECIFIC ###

alphabet = "123456789"
INDIVIDUAL_SIZE = 9

def create_ind(Sudoku_base): #returns an array length 9 containing arrays of length 9
    for i in range(0,9):
        for j in range(0,9):
            if '.' in Sudoku_base[i][j]:
                Sudoku_base[i][j] = choice(alphabet)
    return Sudoku_base

def evaluate_ind(individual):
    eval_ind = check_target(individual)
    #print("Eval_ind produced {} from individual {}".format(eval_ind, individual))
    return  eval_ind #evaluates individual member of population

def crossover_ind(individual1, individual2):
    #cross_ind = [ choice(ch_pair) for ch_pair in zip(individual1, individual2) ]
    cross_ind = [[],[],[],[],[],[],[],[],[]]
    for i in range(0,9):
        for j in range(0,9):
            cross_ind_item = (individual1[i][j], individual2[i][j])
            cross_ind[i].append(choice(cross_ind_item))
    #print("crossover_ind produced {} from individual 1{} and ind 2 {}".format(cross_ind, individual1, individual2))
    return cross_ind    #applies a crossover function between two members to produce an individual child

def mutate_ind(individual):
    #mut_ind = [ (choice(alphabet) if random() < MUTATION_RATE else ch) for ch in individual ]
    for i in range(0,9):
        for j in range(0,9):
            if random()<MUTATION_RATE:
                individual[i][j] = choice(alphabet)
    #print("Mutate ind produces {} from individual {}".format(mut_ind, individual))
    return individual  #mutates an individual member

### PARAMERS VALUES ###

NUMBER_GENERATION = 1000
POPULATION_SIZE = 500
TRUNCATION_RATE = 0.1
MUTATION_RATE = 0.08


if __name__ == "__main__":
    evolve()
    random.seed(10)