import random
import time
# import matplotlib.pyplot as plt 
class thing:
    def __init__(self,weight,value):
        self.weight=int(weight)
        self.value=int(value) 
    
def Read_Config():
    file= open("Algorithm Configuration.txt", "rt")
    file.readline()
    knapsack_size=int(file.readline().split("=",1)[1])
    generation_limit=int(file.readline().split("=",1)[1])
    number_of_population=int(file.readline().split("=",1)[1])
    number_of_last_saved_generations=int(file.readline().split("=",1)[1])
    sel=int(file.readline().split("=",1)[1])
    return knapsack_size,generation_limit,number_of_population,number_of_last_saved_generations , sel
                                

def Read_Things_info():
    things=[]
    number_of_things=0
    file= open("data.txt", "rt")
    file.readline()
    lines=file.readlines()
    for line in lines:
        temp= line.split(",",1)
        obj = thing ( int(temp[0]) , temp[1] )
        things.append(obj)
        number_of_things += 1
    return things , number_of_things

class individual:
    def __init__(self,Chrm):
        self.Chromosome=[]
        self.Chromosome=Chrm
        self.total_weight=0
        self.total_value=0
        for i in range (number_of_things):
            self.total_weight += ( self.Chromosome[i] * things[i].weight )
            self.total_value  += ( self.Chromosome[i] * things[i].value  )
        if self.total_weight > knapsack_size:
            self.fitness=0
        else:
            self.fitness=self.total_value

    def mutation (self):
        if random.randint(1,100) <= 30 :
            index=random.randint(0,number_of_things-1)
            if(self.Chromosome[index]==1):
                self.Chromosome.pop(index)
                self.Chromosome.insert(index,0)
            else :
                self.Chromosome.pop(index)
                self.Chromosome.insert(index,1)
        return self

def Produce_First_Generation(number_of_population , number_of_things):
    population=[]
    while len (population) <= number_of_population:
        chrm=[]
        for i in range (number_of_things): 
            chrm.append( random.randint(0,1) )
        if individual(chrm).fitness != 0 :                      # do not add individual with fitness=0
            population.append ( individual(chrm) )
    return population

def Roulette_Wheel( population , num=1 ):
    sum_of_chances=population[0].fitness
    selected=[]
    RW= [    ( population[0]  , population[0].fitness )  ]
    for indv in population[1:]:
        sum_of_chances += indv.fitness
        RW.append( (indv , sum_of_chances ) )
    
    for i in range (int (num)):
        select=random.randint(0,sum_of_chances)
        for item in RW:
            if select < item[1]:
                selected.append( item[0] )
                break
    
    return selected

def Best_Selection ( population , num=1):
    selected=sorted(population,key=lambda individual: individual.fitness , reverse=True)
    return selected[:int(num)]

def SUS (population,num=1):
    n=int(num)
    selected=[]
    sum_of_chances= population[0].fitness
    SS= [    ( population[0]  , population[0].fitness )  ]
    for indv in population[1:]:
        sum_of_chances += indv.fitness
        SS.append( (indv , sum_of_chances ) )

    step=sum_of_chances/n
    select=random.random() * (step)
    i=0
    while(n>0):
        if select < SS[i][1]:
            selected.append( SS[i][0] )
            select += step
            n=n-1
            i=i-1
        i= i+1
            
    return selected

def Cross_Over_2point ( parents ):
    parent1=parents[0]
    parent2=parents[1]
    point1= random.randint( 1 , number_of_things-1 )
    temp=random.randint( 1 , number_of_things-1 )
    while temp == point1:
        temp=random.randint( 1 , number_of_things-1 )
    if temp>point1:
        point2=temp
    else:
        point2=point1
        point1=temp
    chrm1= parent1.Chromosome [ :point1 ] + parent2.Chromosome [ point1:point2 ] + parent1.Chromosome [ point2: ]
    chrm2= parent2.Chromosome [ :point1 ] + parent1.Chromosome [ point1:point2 ] + parent2.Chromosome [ point2: ]
    child1= individual( chrm1 )
    child2= individual( chrm2 )
    return child1 , child2

def Child_Production (parents):
    childs=[]
    count=0
    while len (childs) < len(parents)-1 :
        child1 , child2 =Cross_Over_2point( parents[count:count+2] )
        childs.append( child1.mutation() )
        childs.append( child2.mutation() )
        count +=2
    if len(parents) %2 != 0 :
        childs.append( parents[count].mutation() )
    return childs

class generation :
    def __init__(self,population):
        sum=0
        self.max_fitness=-1
        for indv in population:
            if indv.fitness > self.max_fitness:
                self.max_fitness=indv.fitness
                self.max_chromosome=indv.Chromosome

            sum += indv.fitness

        self.avg_fitness= sum/ len(population)

    def show_info(self):
        print("Max Fitness:", self.max_fitness, "   Fitness Average" , self.avg_fitness)

def show_saves(saved_generations,how='info'):
    if how=='info':
        for item in saved_generations:
            item.show_info()
    elif how=='bar chart':
        avg_vals=[]
        gen_nums=[]
        for i in range ( len(saved_generations) ):
            gen_nums.append( int (generation_limit-len(saved_generations) + i + 1)  )       #global
        for pop in saved_generations:
            avg_vals.append( pop.avg_fitness )
        plt.bar(gen_nums , avg_vals)
        plt.title('Average Fitness Of Generations' , fontsize=14)
        # plt.xlable('Generation number' , fontsize=14)
        # plt.ylable('Average Fitness' , fontsize=14)
        plt.show

# main :

saved_generations=[]
knapsack_size, generation_limit, number_of_population, number_of_last_saved_generations , sel = Read_Config()
things , number_of_things = Read_Things_info()
if sel == 1:
    selection_function=Roulette_Wheel
elif sel == 2:
    selection_function=Best_Selection
elif sel==3:
    selection_function=SUS

population=Produce_First_Generation(number_of_population,number_of_things)                      # Primary population production
generation_count=1
temp_max=-1
temp_avg=-1
t1=time.time()
while generation_count <= generation_limit :
    parents= selection_function( population , number_of_population * 1.2 )                      # Parents Selection
    childs= Child_Production(parents)                                                           # Child Production
    population= selection_function ( parents + childs , number_of_population )                  # Survivors Selection ( ?? + ?? )
    if generation_count > generation_limit - number_of_last_saved_generations :
        saved_generations.append( generation (population)  )
        if saved_generations[-1].max_fitness > temp_max :
            best_pop_index= saved_generations.index( saved_generations[-1] )
            temp_max=saved_generations[-1].max_fitness
            temp_avg=saved_generations[-1].avg_fitness
        elif saved_generations[-1].max_fitness == temp_max :
            if saved_generations[-1].avg_fitness >= temp_avg:
                temp_avg=saved_generations[-1].avg_fitness
                best_pop_index= saved_generations.index(saved_generations[-1] )
        

    generation_count+=1
t2=time.time()
maxs=[]
avgs=[]
print("------------------------------------------------------")
print("Saved Generations :")
print("------------------------------------------------------")
show_saves(saved_generations,'info')
# show_saves(saved_generations,'bar chart')
print()
print("------------------------------------------------------")
print("Final Results:")
print("------------------------------------------------------")
print("Best Generation Info:")
print("Generation no.", generation_limit - number_of_last_saved_generations + best_pop_index +1 ,":")
print("Max Value:" , saved_generations[best_pop_index].max_fitness)
print("Avg Value:" , saved_generations[best_pop_index].avg_fitness)
print("Max Value Chromosome:" , saved_generations[best_pop_index].max_chromosome)
print()
print("Execution Time:" , t2-t1)

   











        








            
           


