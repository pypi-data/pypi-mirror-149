from cameo_claw.client import Client
from cameo_claw.remote import square

client = Client()
lst = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
it = client.map(square, lst)
print(f'result:{next(it)}')
print(f'result:{next(it)}')
print(f'result:{next(it)}')
