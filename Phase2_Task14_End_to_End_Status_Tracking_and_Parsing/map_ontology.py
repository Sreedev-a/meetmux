import json,re
from pathlib import Path
ROOT=Path(__file__).parent
def map_document(doc,ontology):
 text=doc["text"].lower(); mapped=[]
 for node in ontology["skills"]:
  terms=[node["name"]]+node["aliases"]
  evidence=next((t for t in terms if re.search(r"(?<!\w)"+re.escape(t.lower())+r"(?!\w)",text)),None)
  if evidence: mapped.append({"skill_id":node["id"],"canonical_name":node["name"],"domain":node["domain"],"evidence":evidence})
 mentioned=set(re.findall(r"#[a-z0-9_+-]+",text)); known={"#"+t.lower().replace(" ","_") for n in ontology["skills"] for t in [n["name"]]+n["aliases"]}
 return {"document_id":doc["id"],"ontology_version":ontology["version"],"mapped_skills":mapped,"unresolved_tags":sorted(mentioned-known)}
def main():
 ont=json.loads((ROOT/"data/ontology.json").read_text()); docs=json.loads((ROOT/"data/documents.json").read_text()); out=[map_document(d,ont) for d in docs]; (ROOT/"outputs").mkdir(exist_ok=True); (ROOT/"outputs/ontology_mappings.json").write_text(json.dumps(out,indent=2)+"\n"); print(json.dumps({"documents":len(out),"mapped":sum(len(x["mapped_skills"]) for x in out),"unresolved":sum(len(x["unresolved_tags"]) for x in out)},indent=2))
if __name__=="__main__": main()
