# GENETIC ALGORITHM
# Initialize Population: Generate a random population of solutions.
# Evaluate Fitness: Compute fitness for each solution.
# Selection: Select solutions based on fitness to create the next generation.
# Crossover: Combine two parents to create offspring.
# Mutation: Introduce (or not) random change in solution.
# Repeat until target (or maximum number of generations) is reached.

import random
import string
import time  # For adding delays
import os

targetSequence = "tortowe ciocho"
populationSize = 50
selectionRate = 0.5
elitismCount = 2
mutationRate = 0.1

def clearTerminal():
    # Clear the terminal screen
    os.system('cls' if os.name == 'nt' else 'clear')
    

def generateSequence(length):
    # Define the pool of characters: lowercase letters + space
    characters = string.ascii_lowercase + " "
    
    # Generate a random sequence of the specified length
    sequence = ''.join(random.choices(characters, k=length))
    return sequence


def initializePopulation(size):
    return [generateSequence(len(targetSequence)) for _ in range(size)]


def fitness(sequence, target):
    # Count the number of matching characters in the same position
    matches = sum(1 for s, t in zip(sequence, target) if s == t)
    
    # Normalize the fitness score to be between 0 and 1
    return matches / len(target)  


def evaluatePopulation(pop, target):
    # Create a list of tuples (sequence, fitness score)
    fitnessScores = [(individual, fitness(individual, target)) for individual in pop]
    return fitnessScores


def selectPopulation(fitnessScores, selectionRate=0.6, elitismCount=2):
    # Sort the population by fitness (descending order)
    sortedPopulation = sorted(fitnessScores, key=lambda x: x[1], reverse=True)
    
    # Select elite members
    eliteMembers = sortedPopulation[:elitismCount]
    
    # Select additional members based on the selection rate
    selectedCount = int(len(fitnessScores) * selectionRate)
    selectedMembers = sortedPopulation[:selectedCount]
    
    return eliteMembers + selectedMembers[elitismCount:]


def mutate(sequence, mutationRate):
    # Convert the sequence to a list of characters
    sequenceList = list(sequence)
    
    for i in range(len(sequenceList)):
        if random.random() < mutationRate:
            # Randomly pick a new character from the pool
            characters = string.ascii_lowercase + " "
            sequenceList[i] = random.choice(characters)
    
    # Convert the list back to a string
    return ''.join(sequenceList)


def crossoverPopulation(selectedPopulation, mutationRate=0.05):
    # Create a list to store offspring
    offspring = []
    
    # Shuffle the selected population to randomize pairings
    random.shuffle(selectedPopulation)
    
    # Perform crossover on pairs of individuals
    for i in range(0, len(selectedPopulation) - 1, 2):
        parent1, parent2 = selectedPopulation[i][0], selectedPopulation[i + 1][0]  # Extract sequences
        crossoverPoint = random.randint(1, len(parent1) - 1)  # Random crossover point
        
        # Create offspring by combining parts of parents
        child1 = parent1[:crossoverPoint] + parent2[crossoverPoint:]
        child2 = parent2[:crossoverPoint] + parent1[crossoverPoint:]
        
        # Apply mutation
        child1 = mutate(child1, mutationRate)
        child2 = mutate(child2, mutationRate)

        offspring.append(child1)
        offspring.append(child2)
    
    return offspring


def nextGeneration(currentPopulation, targetSequence):
    # Perform crossover to generate offspring
    offspring = crossoverPopulation(currentPopulation)
    
    # Evaluate the fitness of both the current population and offspring
    combinedPopulation = currentPopulation + offspring
    fitnessScores = [(individual[0], fitness(individual[0], targetSequence)) for individual in combinedPopulation]
    
    # Sort by fitness and select the top individuals to form the new population
    sortedPopulation = sorted(fitnessScores, key=lambda x: x[1], reverse=True)
    newPopulation = sortedPopulation[:len(currentPopulation)]  # Keep the same population size
    
    return newPopulation


def geneticAlgorithm(targetSequence, populationSize, selectionRate=0.5, elitismCount=2, mutationRate=0.05, delay=0.1):
    # Initialize the population
    population = initializePopulation(populationSize)
    fitnessScores = evaluatePopulation(population, targetSequence)
    generation = 0

    while True:
        generation += 1
        clearTerminal()
        
        # Check if any sequence matches the target
        for sequence, score in fitnessScores:
            if sequence == targetSequence:
                print(f"Target sequence found in generation {generation}: '{sequence}'")
                print("Population:")
                for seq, score in fitnessScores:
                    print(f"  Sequence: '{seq}' | Fitness: {score:.2f}")

                return sequence, generation
        
        # Selection
        selectedPopulation = selectPopulation(fitnessScores, selectionRate, elitismCount)
        
        # Crossover with mutation
        offspring = crossoverPopulation(selectedPopulation, mutationRate)
        
        # Evaluate offspring fitness
        offspringWithFitness = [(child, fitness(child, targetSequence)) for child in offspring]
        
        # Replace the population
        fitnessScores = sorted(fitnessScores + offspringWithFitness, key=lambda x: x[1], reverse=True)[:populationSize]

        # Get the best individual of the current generation
        bestSequence, bestFitness = fitnessScores[0]
        
        # Display current generation information
        print(f"\nGeneration {generation}")
        print(f"Best Sequence: '{bestSequence}' | Fitness: {bestFitness:.2f}")
        print("Current Population:")
        for seq, score in fitnessScores:
            print(f"  Sequence: '{seq}' | Fitness: {score:.2f}")

        time.sleep(delay)


geneticAlgorithm(targetSequence, populationSize, selectionRate, elitismCount, mutationRate, 0.05)