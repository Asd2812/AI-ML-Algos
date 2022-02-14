# Python3 program to implement traveling salesman
# problem using naive approach.
from cmath import sqrt
from statistics import mean, stdev
from sys import maxsize
from itertools import permutations
import random
import numpy as np
import math

## Question 3 (a)
V = 7
instances_created = []
paths_a = []
final_answers = []

# First we create our 100 instances of 7 cities.
for a in range(100):
    new_vertex = []
    for i in range(7):
        x = [random.random(), random.random()]
        new_vertex.append(x)
    instances_created.append(new_vertex)
    
    # We then iterate through each permutation to find the shortest existing path between our cities
    perm = permutations(new_vertex)
    min_path = 20.0
    best_path_found = []
    for p in perm:
        current_path_weight = 0
        p = list(p)
        path_length = len(p)
        traversed_length = 0
        
        # Below we calculate the distances
        for val in range(path_length):
            if(traversed_length != path_length-1):
                current_path_weight += math.sqrt((p[val+1][0]-p[val][0])**2 + (p[val+1][1] - p[val][1])**2)
                traversed_length += 1
            else:
                current_path_weight += math.sqrt((p[0][0]-p[val][0])**2 + (p[0][1] - p[val][1])**2)
                traversed_length += 1
        
        #Update the distance with the shortest path
        min_path = min(current_path_weight, min_path)
    final_answers.append(min_path)

#Below are our results

print("Values for the Brute Force method with 100 instances of 7 cities.")
print("Longest Path instance found: ", max(final_answers))
print("Shortest Path instance found: ", min(final_answers))
print("Average path length found: ", mean(final_answers))
print("Standard deviation of 100 path instances found: ", stdev(final_answers))


## Question 3 (b).
paths_length_b = []
path_b = []

#Iterate through our created instances and shuffle (i.e. create random tours) for each one
for inst in instances_created:
    random.shuffle(inst)
    path_b.append(inst)
    path_length_traversed = 0
    current_path_weight_b = 0
    
    #We measure said random tour's path length
    for i in range(len(inst)):
        if(path_length_traversed < V-1):
            current_path_weight_b += math.sqrt((inst[i+1][0] - inst[i][0])**2 + (inst[i+1][1] - inst[i][1])**2)
            path_length_traversed += 1
        else:
            current_path_weight_b += math.sqrt((inst[0][0] - inst[i][0])**2 + (inst[0][1] - inst[i][1])**2)
            path_length_traversed+=1
    
    #We save these path lengths
    paths_length_b.append(current_path_weight_b)

print("###################################################################################")

random_correctness_counter = 0

#Check how many of the random tours match the optimal path (checking to the 12th decimal since some tours have an extra decimal with the same value).
for i in range(len(final_answers)):
    if(round(final_answers[i],12) == round(paths_length_b[i],12)):
        random_correctness_counter += 1

#Below we give the answers to the for Question 3.b
print("Values for the random tour creation.")
print("Longest Path instance found: ", max(paths_length_b))
print("Shortest Path instance found: ", min(paths_length_b))
print("Average path length found: ", mean(paths_length_b))
print("Standard deviation of 100 path instances found: ", stdev(paths_length_b))
print("Number of random tours that are optimal: ", random_correctness_counter)

#Question 3.(c)

#We run the algo with the first instance created (to ensure it works)
testing_set = instances_created[0]
testing_set = list(testing_set)


def neighbour_creation(city_set):
    possible_neighbours = []
    
    #Create all possible neighbours, or edge inversions possible when given a specific tour.
    for i in range(len(city_set)):
        for j in range(i+1, len(city_set)):
            tmp = testing_set.copy()
            tmp[i] = testing_set[j]
            tmp[j] = testing_set[i]
            possible_neighbours.append(tmp)
    
    #Below is the list of all possible neighbours.        
    return possible_neighbours



def find_best_neighbour(nset):
    
    #Set the first possible neighbour as the best. Note that the original tour is also in the neighbourhood.
    curr_min_path_selected = 0
    best_path = nset[0]
    curr_min_path_selected = calc_first_dist(best_path, V)
    
    # Iterate through each of the possible neighbours
    for potn in nset:
        curr_path_length = 0
        tmp = 0
        # Calculate the path of the given neighbour
        curr_path_length = calc_first_dist(potn, V)
        
        # Check to see if said path and tour is better than the previous one
        if(curr_path_length < curr_min_path_selected):
            curr_min_path_selected = curr_path_length
            best_path = potn
    
    return best_path, curr_min_path_selected

#Simple calculation function to measure the length of a tour
def calc_first_dist(city_set, dist):
    curr_path = 0
    traversed_nodes = 0
    for i in range(len(city_set)):
        #If we are measuring the distance between two cities, when we are not at the last edge of the tour.
        if(traversed_nodes < dist-1):
            curr_path += math.sqrt((city_set[i+1][0] - city_set[i][0])**2 + (city_set[i+1][1] - city_set[i][1])**2)
            traversed_nodes +=1
        else:
            #This is here to measure the distance between the last city and the first (since it's a tour)
            curr_path += math.sqrt((city_set[0][0] - city_set[i][0])**2 + (city_set[0][1] - city_set[i][1])**2)
            traversed_nodes = 0
    return curr_path



def tsp(cit_set, dist):
    #Fix the temporary best answer as the random tour given.
    curr_answer = cit_set
    curr_path_for_ans = calc_first_dist(cit_set,dist)
    #Calculate its best neighbour
    neighbours_list = neighbour_creation(cit_set)
    best_n, best_n_path = find_best_neighbour(neighbours_list)
    
    while(best_n_path < curr_path_for_ans):
        # If the shortest length tour of the neighbourhood < than the current one, said tour becomes the current best. Repeat best neighbour calculation.
        curr_answer = best_n
        curr_path_for_ans = best_n_path
        neighbours_list = neighbour_creation(curr_answer)
        best_n, best_n_path = find_best_neighbour(neighbours_list)
    
    return curr_answer, curr_path_for_ans



print("###################################################################################")
answ_c = []
speciality = 0
equality_counter = 0

tmp = tsp(testing_set, V)

# Iterate through all instances to calculate said optimal tour using the hill climbing algorithm, and add the length to a list
for i in range(len(instances_created)):
    testing_set = instances_created[i]
    answ_c.append(tsp(testing_set, V)[1])
    if(round(tsp(testing_set, V)[1], 12) == round(final_answers[i], 12)):
        equality_counter +=1
    

# Give all stats for 3.c
print("Values for the Hill Climbing method with 100 instances of 7 cities.")
print("Longest Path instance found: ", max(answ_c))
print("Shortest Path instance found: ", min(answ_c))
print("Average path length found: ", mean(answ_c))
print("Standard deviation of 100 path instances found: ", stdev(answ_c))
        
print("Here are how many values match between our AI algo and the brute force algo: ", equality_counter)

print("###################################################################################")
print("###################################################################################")


#Question 3.(d)

## NOTICE: I have written my code for part 3.d below. However I commented it out since I have run it twice between last night and today and both times,
# I run out of memory before it completes. As I wanted to ensure I submitted my code prior to the deadline I left it in, but I don't have the data yet.
# If it works on the 3rd try then I will submit the newer version of the assignment with updated data. Thank you.
           

new_instances = []
answ_d = []

for i in range(100):
    vertex_set = []
    for j in range(100):
        x = [random.random(), random.random()]
        vertex_set.append(x)
    new_instances.append(vertex_set)

for inst in new_instances:
    random.shuffle(inst)

new_testing_set = []

for i in range(len(new_instances)):
    new_testing_set = new_instances[i]
    answ_d.append(tsp(new_testing_set, 100)[1])
    
print("Values for the Hill Climbing method with 100 instances of 100 cities.")
print("Longest Path instance found: ", max(answ_d))
print("Shortest Path instance found: ", min(answ_d))
print("Average path length found: ", mean(answ_d))
print("Standard deviation of 100 path instances found: ", stdev(answ_d))
    
    
    






