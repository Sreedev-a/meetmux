import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
WEIGHTS = {"skills": .65, "experience": .15, "location": .1, "work_mode": .1}


def score(student, job):
    required = job["required_skills"]
    attainment = [min(student["skills"].get(k, 0) / v, 1) for k, v in required.items()]
    parts = {
        "skills": sum(attainment) / len(attainment),
        "experience": min(student["experience"] / max(job["min_experience"], .1), 1),
        "location": float(job["location"] in student["locations"] or job["work_mode"] == "remote"),
        "work_mode": float(job["work_mode"] in student["work_modes"]),
    }
    return round(sum(parts[k] * WEIGHTS[k] for k in WEIGHTS), 6), all(x >= 1 for x in attainment)


def rank_jobs(student, jobs):
    return sorted([{"job_id":j["job_id"], "score":score(student,j)[0], "eligible":score(student,j)[1]} for j in jobs], key=lambda x:(-x["score"],x["job_id"]))


def rank_candidates(job, students):
    return sorted([{"student_id":s["student_id"], "score":score(s,job)[0], "eligible":score(s,job)[1]} for s in students], key=lambda x:(-x["score"],x["student_id"]))


def main():
    data=json.loads((ROOT/"data/marketplace.json").read_text())
    result={"jobs_for_students":{s["student_id"]:rank_jobs(s,data["jobs"]) for s in data["students"]},"candidates_for_jobs":{j["job_id"]:rank_candidates(j,data["students"]) for j in data["jobs"]}}
    (ROOT/"outputs").mkdir(exist_ok=True); (ROOT/"outputs/rankings.json").write_text(json.dumps(result,indent=2)+"\n"); print(json.dumps(result,indent=2))

if __name__=="__main__": main()
