import math
def safe_rate(n,d):return n/d if d else 0.0
def precision_at_k(ranked,relevant,k): return safe_rate(sum(x in relevant for x in ranked[:k]),k)
def recall_at_k(ranked,relevant,k): return safe_rate(sum(x in relevant for x in ranked[:k]),len(relevant))
def ndcg_at_k(ranked,relevant,k):
 dcg=sum((x in relevant)/math.log2(i+2) for i,x in enumerate(ranked[:k])); ideal=sum(1/math.log2(i+2) for i in range(min(k,len(relevant)))); return safe_rate(dcg,ideal)
def mrr(ranked,relevant): return next((1/i for i,x in enumerate(ranked,1) if x in relevant),0.0)
def absolute_lift(b,t):return t-b
def relative_lift(b,t):return safe_rate(t-b,b) if b else None
def non_empty_rate(responses):return safe_rate(sum(bool(r.recommendations) for r in responses),len(responses))
def fallback_rate(responses):return safe_rate(sum(r.fallback_used for r in responses),len(responses))
