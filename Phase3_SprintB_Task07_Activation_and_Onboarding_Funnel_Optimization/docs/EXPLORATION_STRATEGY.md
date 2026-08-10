# Exploration Strategy

The design-choice fraction is configurable and set to **20%** in the demo: four high-confidence results plus one deterministic, lower-ranked eligible discovery item at K=5. Sampling uses seed 42 in tests. Exploration never bypasses active/expiry/experience filters, never duplicates jobs, and preserves result count. Task 6 impression context records `exploration_item` and source, enabling later preference learning from genuine outcomes without treating exploratory exposure as equivalent to exploitation.
