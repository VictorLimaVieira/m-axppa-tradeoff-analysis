DROP TABLE IF EXISTS tradeoff_scores;
DROP TABLE IF EXISTS synthesis_metrics;
DROP TABLE IF EXISTS accuracy_metrics;
DROP TABLE IF EXISTS architectures;

CREATE TABLE architectures (
    architecture_id INTEGER PRIMARY KEY,
    family TEXT NOT NULL,
    variant TEXT NOT NULL,
    baseline_source TEXT NOT NULL,
    w_bits INTEGER NOT NULL,
    m_bits INTEGER,
    l_bits INTEGER,
    k_bits INTEGER NOT NULL,
    approximation_strategy TEXT NOT NULL,
    is_literature_baseline INTEGER NOT NULL,
    selected_for_synthesis INTEGER NOT NULL
);

CREATE TABLE accuracy_metrics (
    architecture_id INTEGER PRIMARY KEY,
    input_vectors INTEGER NOT NULL,
    ssim REAL NOT NULL,
    ncc REAL NOT NULL,
    mae REAL NOT NULL,
    mre REAL NOT NULL,
    mred REAL NOT NULL,
    accuracy_rank INTEGER NOT NULL,
    FOREIGN KEY (architecture_id) REFERENCES architectures (architecture_id)
);

CREATE TABLE synthesis_metrics (
    architecture_id INTEGER PRIMARY KEY,
    technology_node_nm INTEGER NOT NULL,
    supply_voltage REAL NOT NULL,
    clock_mhz INTEGER NOT NULL,
    energy_saving_pct REAL NOT NULL,
    area_saving_pct REAL NOT NULL,
    power_mw REAL NOT NULL,
    area_um2 REAL NOT NULL,
    delay_ns REAL NOT NULL,
    pdp REAL NOT NULL,
    edp REAL NOT NULL,
    FOREIGN KEY (architecture_id) REFERENCES architectures (architecture_id)
);

CREATE TABLE tradeoff_scores (
    architecture_id INTEGER PRIMARY KEY,
    normalized_error REAL NOT NULL,
    normalized_energy_saving REAL NOT NULL,
    normalized_area_saving REAL NOT NULL,
    balanced_score REAL NOT NULL,
    pareto_optimal_energy_error INTEGER NOT NULL,
    pareto_optimal_area_error INTEGER NOT NULL,
    FOREIGN KEY (architecture_id) REFERENCES architectures (architecture_id)
);

