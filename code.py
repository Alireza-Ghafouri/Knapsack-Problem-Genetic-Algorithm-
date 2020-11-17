import random
class thing:
    def __init__(self,weight,value):
        self.weight=int(weight)
        self.value=int(value)

things=[]
population=[]
number_of_things=0
number_of_population= 12                      #could be changed...


# reading data from file 

file= open("data.txt", "rt")
file.readline()
lines=file.readlines()
for line in lines:
    temp= line.split(",",1)
    obj = thing ( int(temp[0]) , temp[1] )
    things.append(obj)
    number_of_things += 1

# for t in things:
#     print(t.weight,"    " , t.value)
# print(number_of_things)

knapsack_size=165                           #could be changed...

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
            



# print( "testing...")
# test=[0,1,0,0,1,1,0,0,0,0]
# o1=individual(test)        
# o1=individual(True) 
# print("O1:")
# print("Total weight:" , o1.total_weight)
# print("total value:" , o1.total_value)
# print("fitness:" , o1.fitness)
# print(o1.Chromosome)
# o1.mutation()
# print(o1.Chromosome)

def Produce_First_Generation(number_of_population):
    chrm=[]
    for i in range (number_of_population):
        for ii in range (number_of_things): 
            chrm.append( random.randint(0,1) )
        if individual(chrm).fitness != 0 :                      # do not add individual with fitness=0
            population.append ( individual(chrm) ) 

# print( "testing...")
# Produce_First_Generation(number_of_population)
# for item in population:
#     print(item.Chromosome)


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


print( "testing" )
t1=[0,1,0,0,0,0,0,1,0,0]
t2=[0,0,0,1,0,0,0,0,1,0] 
t3=[1,0,0,0,0,0,0,0,0,0] 
t4=[0,0,0,0,0,0,0,0,0,1]
o1=individual(t1)
o2=individual(t2)
o3=individual(t3)
o4=individual(t4)
o=[o1,o2,o3,o4]
print("o1.fitness:" , o1.fitness)
print("o2.fitness:" , o2.fitness)
print("o3.fitness:" , o3.fitness)
print("o4.fitness:" , o4.fitness)
print("selected:")
for i in Roulette_Wheel(o):
    print(i.fitness) 


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

    
# print( "testing" )
# t1=[0,2,4,6,8,10,12,14,16,18]
# t2=[1,3,5,7,9,11,13,15,17,19]
# p1=individual(t1)
# p2=individual(t2)
# p=[p1,p2]
# print ("parents:")
# print(p1.Chromosome)
# print(p2.Chromosome)
# print("childs:")
# ch= Cross_Over_2point(p)
# print(ch[0].Chromosome)
# print(ch[1].Chromosome)

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


# print( "testing" )
# t1=[0,1,0,0,1,0,0,1,0,0]
# t2=[0,0,0,1,0,0,0,0,1,0] 
# t3=[1,0,0,1,0,1,0,1,0,0] 
# t4=[0,0,0,0,1,0,0,0,0,1]
# p1=individual(t1)
# p2=individual(t2)
# p3=individual(t3)
# p4=individual(t4)
# p=[p1,p2,p3,p4]
# print("parents:")
# for item in p:
#     print(item.Chromosome)
# print("childs:")
# ch= Childeren_Production(p)
# for item in ch:
#     print(item.Chromosome)





        








            
           


