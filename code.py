import random
class thing:
    def __init__(self,weight,value):
        self.weight=int(weight)
        self.value=int(value)

things=[]
number_of_things=0

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
#print(number_of_things)

knapsack_size=165                           #could be changed...

class individual:
    def __init__(self,First_Generation=False,Chrm=[]):
        self.Chromosome=[]
        if First_Generation :
            for i in range (number_of_things):
                self.Chromosome.append( random.randint(0,1) )    
        else:
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
# o1=individual(False ,test)        
# o1=individual(True) 
# print("O1:")
# print("Total weight:" , o1.total_weight)
# print("total value:" , o1.total_value)
# print("fitness:" , o1.fitness)
# print(o1.Chromosome)
# o1.mutation()
# print(o1.Chromosome)








            
           


