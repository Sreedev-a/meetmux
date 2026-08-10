from .candidate_features import normalize
def normalized_requirements(job): return {normalize(k):float(v) for k,v in job.required_skills.items()}
