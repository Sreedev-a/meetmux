import json,re
from pathlib import Path
ROOT=Path(__file__).parent
ONTOLOGY={"python":["python","python3"],"sql":["sql","postgresql","mysql"],"machine_learning":["machine learning","ml"],"fastapi":["fastapi"],"docker":["docker"]}
def parse(doc):
 text=doc["text"]; lower=text.lower(); found=[]
 for canonical,aliases in ONTOLOGY.items():
  hits=[]
  for alias in aliases:
   for m in re.finditer(r"(?<!\w)"+re.escape(alias)+r"(?!\w)",lower): hits.append({"text":text[m.start():m.end()],"start":m.start(),"end":m.end()})
  if hits: found.append({"canonical_skill":canonical,"confidence":1.0,"evidence":hits})
 years=[float(x) for x in re.findall(r"(\d+(?:\.\d+)?)\+?\s+years?",lower)]
 return {"document_id":doc["id"],"document_type":doc["type"],"parser_version":"0.1.0","skills":found,"years_experience":max(years) if years else None}
def main():
 docs=json.loads((ROOT/"data/documents.json").read_text()); out=[parse(d) for d in docs]; (ROOT/"outputs").mkdir(exist_ok=True); (ROOT/"outputs/structured_documents.json").write_text(json.dumps(out,indent=2)+"\n"); print(json.dumps({"documents":len(out),"structured_skills":sum(len(x["skills"]) for x in out)},indent=2))
if __name__=="__main__": main()
