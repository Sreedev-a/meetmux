# Offline–Online Gap

The existing held-out Phase 2 validation reports **NDCG@3 = 0.9012** and **Recall@3 = 0.9167** over four users in `Phase2_Task20_Portals_Integration_and_Dry_Run`. Those offline values were inspected, not regenerated or tuned in this instrumentation task.

The controlled runtime stream proves online-style metric computability (28.21% CTR, 14.02% apply/impression, 5.34% shortlist/impression), but these simulated-action rates cannot quantify online lift or be directly compared causally with NDCG. A strong offline ranking metric does not guarantee improved user outcomes. Proper validation requires production exposure, randomized variants, position-aware analysis, guardrails and predeclared success criteria. This task changes no model parameters and does not tune against these events; its evaluation focuses on schema validity, completeness and joinability.
