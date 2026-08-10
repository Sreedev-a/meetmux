from src.metrics import absolute_lift,mrr,ndcg_at_k,precision_at_k,recall_at_k,relative_lift,safe_rate
def test_ranking_metrics():
 ranked=["a","b","c"];rel={"a","c"};assert precision_at_k(ranked,rel,2)==.5 and recall_at_k(ranked,rel,2)==.5 and ndcg_at_k(ranked,rel,3)>0 and mrr(ranked,rel)==1
def test_lifts_and_zero():assert round(absolute_lift(.4,.5),8)==.1 and relative_lift(.5,.75)==.5 and relative_lift(0,.2) is None and safe_rate(1,0)==0
