SELECT
    a.family,
    a.variant,
    a.m_bits,
    a.l_bits,
    a.k_bits,
    ROUND(am.mred, 4) AS mred,
    ROUND(sm.energy_saving_pct, 2) AS energy_saving_pct,
    ROUND(sm.area_saving_pct, 2) AS area_saving_pct,
    ROUND(ts.balanced_score, 3) AS balanced_score
FROM architectures a
JOIN accuracy_metrics am ON am.architecture_id = a.architecture_id
JOIN synthesis_metrics sm ON sm.architecture_id = a.architecture_id
JOIN tradeoff_scores ts ON ts.architecture_id = a.architecture_id
ORDER BY sm.energy_saving_pct DESC
LIMIT 20;

