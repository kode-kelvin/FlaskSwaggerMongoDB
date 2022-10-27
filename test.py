# num = 25.75
# print(isinstance(num, (int, float)))
# # Output True

# num = '28Jessa'
# print(isinstance(num, (int, float)))
# # Output False

# import uuid

# print(uuid.uuid4())

# import random
# id = ''.join(str(random.randint(0,10)) for x in range(6))
# id = int(id)
# print(id)
# print(type(id))


from random import randint                                                             
# id = randint(1_000, 999_999)
# print(id, type(id))

def randomNumb():
    id = randint(1_000, 999_999)
    return id

k = randomNumb()
print(k, type(k))