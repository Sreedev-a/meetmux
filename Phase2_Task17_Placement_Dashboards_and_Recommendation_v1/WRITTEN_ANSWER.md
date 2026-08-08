# Placement Dashboards & Recommendation v1

I shipped recommendation v1 as a callable Flask service. It restricts candidates to active jobs at verified companies, ranks with the approved four-feature configuration, provides feature values and model version, validates result limits, and uses a transparent recency fallback for cold-start users. The generated demo response uses a real-shaped request, and tests verify ranking, hard filters, and endpoint validation.
