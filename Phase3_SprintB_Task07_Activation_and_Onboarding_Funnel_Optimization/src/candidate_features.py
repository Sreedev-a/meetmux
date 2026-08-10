import re
ALIASES={"python3":"python","python_programming":"python","postgres":"sql","postgresql":"sql","ml":"machine_learning","machine_learning":"machine_learning"}
def normalize(value:str)->str:
 key=re.sub(r"[^a-z0-9]+","_",value.strip().lower()).strip("_")
 return ALIASES.get(key,key)
def normalized_scores(scores): return {normalize(k):float(v) for k,v in scores.items()}
