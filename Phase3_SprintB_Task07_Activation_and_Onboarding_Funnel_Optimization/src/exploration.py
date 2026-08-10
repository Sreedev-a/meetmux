import random
def select_exploration(ranked,count,seed=42):
 if count<=0:return []
 pool=ranked[max(1,len(ranked)//3):] or ranked
 return random.Random(seed).sample(pool,min(count,len(pool)))
