from random import randrange
letters = ['g', 'a', 'v', 'l', 'i', 'c', 'm', 'f', 'y', 'w', 'p', 's', 't', 'n', 'q', 'd', 'e', 'h', 'k', 'r']
seq = ""
for i in range(12):
    seq += letters[randrange(20)]
print(seq)

