import unittest
import history

name = 'test1'

h = history.History(name)

for i in ('a', 'o', 'g'):
    h.remember(i)

h.save()
print(h[0])

 

