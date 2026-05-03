SELECT
    a.variant,
    COUNT(*) AS architectures,
    ROUND(AVG(am.mred), 4) AS avg_mred,
    ROUND(AVG(sm.energy_saving_pct), 2) AS avg_energy_saving_pct,
    ROUND(AVG(sm.area_saving_pct), 2) AS avg_area_saving_pct,
    ROUND(AVG(ts.balanced_score), 3) AS avg_balanced_score
FROM architectures a
JOIN accuracy_metrics am ON am.architecture_id = a.architecture_id
JOIN synthesis_metrics sm ON sm.architecture_id = a.architecture_id
JOIN tradeoff_scores ts ON ts.architecture_id = a.architecture_id
WHERE a.family = 'M-AxPPA'
GROUP BY a.variant
ORDER BY avg_balanced_score DESC;

