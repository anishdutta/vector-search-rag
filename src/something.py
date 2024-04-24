

a = f'''
Elon Reeve Musk (/ilɒn/; EE-lon; born June 28, 1971) is a businessman and investor. 
He is the founder, chairman, CEO, and CTO of SpaceX; 
angel investor, CEO, product architect, 
and former chairman of Tesla, Inc.; 
owner, executive chairman, and CTO of X Corp.; 
founder of the Boring Company and xAI; co-founder of Neuralink and OpenAI; 
and president of the Musk Foundation. He is one of the wealthiest people in the world, 
with an estimated net worth of US$190 billion as of March 2024.
'''

for i in range(0, len(a), 10):
    print(a[i:i+10])