class thing:
    def __init__(self,weight,value):
        self.weight=weight
        self.value=value

things=[]

# reading data from file 

file= open("data.txt", "rt")
file.readline()
lines=file.readlines()
for line in lines:
    temp= line.split(",",1)
    obj = thing ( int(temp[0]) , temp[1] )
    things.append(obj)

#for t in things:
#    print(t.weight,"    " , t.value)


