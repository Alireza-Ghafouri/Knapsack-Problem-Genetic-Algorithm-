import random
class thing:
    def __init__(self,weight,value):
        self.weight=int(weight)
        self.value=int(value) 
    
def Read_Config():
    file= open("Algorithm Configuration.txt", "rt")
    knapsack_size=file.readline().split("=",1)
    generation_limit=file.readline().split("=",1)
    number_of_population=file.readline().split("=",1)
    return knapsack_size,generation_limit,number_of_population
                                

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
    return things

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
            self.fitness=self.total_weight

    def mutation (self):
        if random.randint(1,100) <= 2 :
            index=random.randint(0,number_of_things-1)
            if(self.Chromosome[index]==1):
                self.Chromosome.pop(index)
                self.Chromosome.insert(index,0)
            else :
                self.Chromosome.pop(index)
                self.Chromosome.insert(index,1)

def Produce_First_Generation(number_of_population):
    population=[]
    chrm=[]
    for i in range (number_of_population):
        for ii in range (number_of_things): 
            chrm.append( random.randint(0,1) )
        if individual(chrm).fitness != 0 :                      # do not add individual with fitness=0
            population.append ( individual(chrm) )
    return population

def Roulette_Wheel( population , num=1 ):
    sum_of_chances=population[0].fitness
    selected=[]
    RW= [    ( population[0]  , population[0].fitness )  ]
    for item in population[1:]:
        sum_of_chances += item.fitness
        RW.append( (item , sum_of_chances ) )
    
    for i in range (num):
        select=random.randint(0,sum_of_chances)
        for item in RW:
            if select < item[1]:
                selected.append( item[0] )
                break
    
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
    childs=[child1,child2]
    return childs

def Childeren_Production (parents):
    childs=[]
    count=0
    if len(parents) %2 :
        print("The number of parents is not even!")
        exit

    while count < len(parents) :
        childs += Cross_Over_2point( parents[count:count+2] )
        count += 2
    return childs






        








            
           


