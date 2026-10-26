import sys
from pathlib import Path

ROOT = Path("d:/VIT/SEM-3/mlops/cp/VisionAssist_Web_Complete/VisionAssist_Web")
css_content = (ROOT / "static" / "styles.css").read_text(encoding="utf-8")

html_content = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <meta name="theme-color" content="#092c35" />
  <meta name="description" content="VisionAssist AI 2.0: Inclusive Campus, Smarter AI, Safer Journeys. SafePath Accessibility & MLOps Platform." />
  
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;700&display=swap" rel="stylesheet">
  
  <title>VisionAssist AI 2.0 • Inclusive Campus, Smarter AI, Safer Journeys</title>
  
  <!-- Inline styles guarantee 100% immediate rendering without browser caching issues -->
  <style>
{css_content}
  </style>
  <link rel="stylesheet" href="/static/styles.css?v=2026.10.26.1" />
</head>
<body>

  <!-- ==========================================================================
       GLOBAL TOP HEADER
       ========================================================================== -->
  <header class="global-header">
    <div class="brand-section">
      <div class="brand-logo-icon">
        <svg viewBox="0 0 24 24">
          <path d="M12 4.5C7 4.5 2.73 7.61 1 12c1.73 4.39 6 7.5 11 7.5s9.27-3.11 11-7.5c-1.73-4.39-6-7.5-11-7.5zM12 17c-2.76 0-5-2.24-5-5s2.24-5 5-5 5 2.24 5 5-2.24 5-5 5zm0-8c-1.66 0-3 1.34-3 3s1.34 3 3 3 3-1.34 3-3-1.34-3-3-3z"/>
        </svg>
      </div>
      <div class="brand-title-wrap">
        <h1>VisionAssist AI 2.0 <span>SAFE-Loop</span></h1>
        <p>Inclusive Campus. Smarter AI. Safer Journeys.</p>
      </div>
    </div>

    <!-- Center Search Bar -->
    <div class="header-search-wrap">
      <span class="search-icon">🔍</span>
      <input type="text" id="globalSearchInput" placeholder="Search building, room, facility, or keyword..." />
    </div>

    <!-- Right Header Actions -->
    <div class="header-actions">
      <button class="notif-bell-btn" id="bellBtn" title="Notifications">
        <span>🔔</span>
        <span class="notif-badge">3</span>
      </button>

      <button class="header-btn" id="campusSelectBtn">
        <span>🏛️</span>
        <span>Main Campus</span>
        <span style="font-size:0.7rem;">▾</span>
      </button>

      <div class="user-profile-chip">
        <div class="user-avatar-circle">AD</div>
        <div class="user-info-text">
          <strong>Admin</strong>
          <small>Campus Manager</small>
        </div>
      </div>
    </div>
  </header>

  <!-- ==========================================================================
       MAIN APP CONTAINER (SIDEBAR + MAIN CONTENT)
       ========================================================================== -->
  <div class="app-container">
    
    <!-- LEFT SIDEBAR -->
    <aside class="app-sidebar" id="sidebar">
      <nav class="sidebar-menu-list">
        <a class="sidebar-link active" data-tab="dashboard">
          <span class="sidebar-icon">📊</span>
          <span>Dashboard</span>
        </a>
        <a class="sidebar-link" data-tab="map">
          <span class="sidebar-icon">🗺️</span>
          <span>Campus Map</span>
        </a>
        <a class="sidebar-link" data-tab="navigation">
          <span class="sidebar-icon">🧭</span>
          <span>Navigation & Routes</span>
        </a>
        <a class="sidebar-link" data-tab="hazards">
          <span class="sidebar-icon">⚠️</span>
          <span>Hazards & Reports</span>
          <span class="sidebar-badge">5</span>
        </a>
        <a class="sidebar-link" data-tab="assistant">
          <span class="sidebar-icon">👁️</span>
          <span>Live Assistant</span>
        </a>
        <a class="sidebar-link" data-tab="ocr">
          <span class="sidebar-icon">🔤</span>
          <span>OCR & Text Reader</span>
        </a>

        <!-- MLOps Collapsible Group -->
        <div class="sidebar-group-header">
          <span>MLOps Platform</span>
          <span>▾</span>
        </div>
        <div class="sidebar-submenu">
          <a class="sidebar-sublink" data-tab="lifecycle">
            <span>🛡️</span>
            <span>Model Lifecycle</span>
          </a>
          <a class="sidebar-sublink" data-tab="dataset">
            <span>📁</span>
            <span>Dataset Management</span>
          </a>
          <a class="sidebar-sublink" data-tab="experiments">
            <span>🔬</span>
            <span>Experiments (MLflow)</span>
          </a>
          <a class="sidebar-sublink" data-tab="registry">
            <span>📦</span>
            <span>Model Registry</span>
          </a>
          <a class="sidebar-sublink" data-tab="safeloop">
            <span>⚖️</span>
            <span>Quality Gate (SAFE-Loop)</span>
          </a>
          <a class="sidebar-sublink" data-tab="drift">
            <span>📈</span>
            <span>Monitoring & Drift</span>
          </a>
        </div>

        <a class="sidebar-link" data-tab="student">
          <span class="sidebar-icon">🎓</span>
          <span>Student Perf. (Unit I)</span>
        </a>
        <a class="sidebar-link" data-tab="users">
          <span class="sidebar-icon">👥</span>
          <span>User Management</span>
        </a>
        <a class="sidebar-link" data-tab="analytics">
          <span class="sidebar-icon">📈</span>
          <span>Analytics & Reports</span>
        </a>
        <a class="sidebar-link" data-tab="settings">
          <span class="sidebar-icon">⚙️</span>
          <span>Settings</span>
        </a>
      </nav>

      <!-- Sidebar Status Card -->
      <div class="sidebar-status-card">
        <div class="status-header-pill">
          <div class="pulse-dot"></div>
          <span>All Systems Operational</span>
        </div>
        <div class="status-row">
          <span>API Services</span>
          <span>Online</span>
        </div>
        <div class="status-row">
          <span>Model Inference</span>
          <span>Online</span>
        </div>
        <div class="status-row">
          <span>Database</span>
          <span>Online</span>
        </div>
        <div class="status-row">
          <span>Cloud Sync</span>
          <span>Online</span>
        </div>
      </div>
    </aside>

    <!-- ==========================================================================
         MAIN VIEWPORT
         ========================================================================== -->
    <main class="main-viewport">

      <!-- VIEW 1: EXECUTIVE DASHBOARD (DEFAULT) -->
      <div class="view-panel active" id="viewDashboard">

        <!-- ROW 1: 6 TOP KPI CARDS -->
        <section class="kpi-row">
          <div class="kpi-card">
            <div class="kpi-icon-wrap kpi-icon-teal">👤</div>
            <div class="kpi-content">
              <strong>248</strong>
              <p>Active Users</p>
              <div class="kpi-subtag subtag-green">▲ +12% from last week</div>
            </div>
          </div>

          <div class="kpi-card">
            <div class="kpi-icon-wrap kpi-icon-red">⚠️</div>
            <div class="kpi-content">
              <strong>12</strong>
              <p>Active Hazards</p>
              <div class="kpi-subtag subtag-red">3 high risk</div>
            </div>
          </div>

          <div class="kpi-card">
            <div class="kpi-icon-wrap kpi-icon-blue">♿</div>
            <div class="kpi-content">
              <strong>94%</strong>
              <p>Accessible Route Coverage</p>
              <div class="kpi-subtag subtag-green">▲ +2% from last month</div>
            </div>
          </div>

          <div class="kpi-card">
            <div class="kpi-icon-wrap kpi-icon-orange">📄</div>
            <div class="kpi-content">
              <strong>1,320</strong>
              <p>Texts Read (OCR)</p>
              <div class="kpi-subtag subtag-orange">Today</div>
            </div>
          </div>

          <div class="kpi-card">
            <div class="kpi-icon-wrap kpi-icon-purple">🧠</div>
            <div class="kpi-content">
              <strong>v2.3.1</strong>
              <p>Current Model (Production)</p>
              <div class="kpi-subtag subtag-green">✔ Quality Gate Passed</div>
            </div>
          </div>

          <div class="kpi-card">
            <div class="kpi-icon-wrap kpi-icon-cyan">⏱️</div>
            <div class="kpi-content">
              <strong>86 ms</strong>
              <p>Avg. Inference Time</p>
              <div class="kpi-subtag subtag-green">▼ -18% from last week</div>
            </div>
          </div>
        </section>

        <!-- ROW 2: CAMPUS DIGITAL TWIN (2/3) + ALERTS & REPORTS (1/3) -->
        <section class="middle-grid">
          
          <!-- LEFT 2/3: CAMPUS DIGITAL TWIN -->
          <div class="card-panel">
            <div class="panel-header-row">
              <div class="panel-title-box">
                <h3>🏛️ Campus Digital Twin</h3>
                <p>Interactive map with accessible routes, facilities, hazards and live updates</p>
              </div>
              <button class="panel-action-btn" id="a11yViewSelect">Accessibility View ▾</button>
            </div>

            <div class="map-subcontrols">
              <div class="map-search-input">
                <span class="icon">🔍</span>
                <input type="text" id="mapSearchInput" placeholder="Search location, facility, or node..." />
              </div>

              <div class="floor-pills-wrap">
                <span class="floor-label">Floor:</span>
                <button class="floor-pill active" data-floor="all">All</button>
                <button class="floor-pill" data-floor="G">G</button>
                <button class="floor-pill" data-floor="1">1</button>
                <button class="floor-pill" data-floor="2">2</button>
                <button class="floor-pill" data-floor="3">3</button>
              </div>
            </div>

            <!-- Visual Campus Map Canvas -->
            <div class="map-canvas-container">
              <canvas id="campusMapCanvas"></canvas>
              
              <!-- Floating Map Legend -->
              <div class="map-legend-overlay">
                <div class="legend-item"><span class="legend-dot" style="background:#0284c7;"></span> 📍 Your Location</div>
                <div class="legend-item"><span class="legend-dot" style="background:#00d2ff;"></span> ━ Accessible Route</div>
                <div class="legend-item"><span class="legend-dot" style="background:#10b981;"></span> 🚪 Entrance</div>
                <div class="legend-item"><span class="legend-dot" style="background:#8b5cf6;"></span> 🛗 Elevator</div>
                <div class="legend-item"><span class="legend-dot" style="background:#f59e0b;"></span> 🪜 Stairs</div>
                <div class="legend-item"><span class="legend-dot" style="background:#ef4444;"></span> ⚠️ Hazard (High)</div>
                <div class="legend-item"><span class="legend-dot" style="background:#06b6d4;"></span> ♿ Accessible Toilet</div>
              </div>

              <!-- Map Zoom Buttons -->
              <div class="map-zoom-controls">
                <button class="map-zoom-btn" id="mapZoomIn" title="Zoom In">+</button>
                <button class="map-zoom-btn" id="mapZoomOut" title="Zoom Out">−</button>
                <button class="map-zoom-btn" id="mapRecenter" title="Recenter">🎯</button>
              </div>
            </div>

            <!-- Bottom Map Filter Toggles -->
            <div class="map-filter-bar">
              <button class="filter-chip-btn active" data-layer="buildings">🏢 Buildings</button>
              <button class="filter-chip-btn active" data-layer="routes">♿ Accessible Routes</button>
              <button class="filter-chip-btn active" data-layer="hazards">⚠️ Hazards</button>
              <button class="filter-chip-btn active" data-layer="elevators">🛗 Elevators</button>
              <button class="filter-chip-btn active" data-layer="stairs">🪜 Stairs</button>
              <button class="filter-chip-btn active" data-layer="toilets">🚻 Toilets</button>
              <button class="filter-chip-btn active" data-layer="cafeteria">☕ Cafeteria</button>
            </div>
          </div>

          <!-- RIGHT 1/3: RECENT ALERTS & REPORTS -->
          <div class="card-panel">
            <div class="panel-header-row">
              <div class="panel-title-box">
                <h3>🔔 Recent Alerts & Reports</h3>
                <p>Live verified campus micro-hazards</p>
              </div>
              <button class="panel-action-btn" id="viewAllAlertsBtn">View All</button>
            </div>

            <div class="alerts-list-wrap" id="alertsFeedList">
              <!-- Item 1: Stairs Blockage -->
              <div class="alert-item-card">
                <div class="alert-thumb" style="background:#fee2e2;">🪜</div>
                <div class="alert-details">
                  <strong>Stairs – Temporary Blockage</strong>
                  <p>Near Science Block • 20 m away</p>
                </div>
                <div class="alert-meta">
                  <span class="risk-pill risk-high">High Risk</span>
                  <small>10 min ago Reported</small>
                </div>
              </div>

              <!-- Item 2: Wet Floor -->
              <div class="alert-item-card">
                <div class="alert-thumb" style="background:#fef3c7;">⚠️</div>
                <div class="alert-details">
                  <strong>Wet Floor</strong>
                  <p>Canteen (1st Floor) • 35 m away</p>
                </div>
                <div class="alert-meta">
                  <span class="risk-pill risk-med">Medium Risk</span>
                  <small>25 min ago Verified</small>
                </div>
              </div>

              <!-- Item 3: Crowded Corridor -->
              <div class="alert-item-card">
                <div class="alert-thumb" style="background:#fef3c7;">👥</div>
                <div class="alert-details">
                  <strong>Crowded Corridor</strong>
                  <p>Library Block • 60 m away</p>
                </div>
                <div class="alert-meta">
                  <span class="risk-pill risk-med">Medium Risk</span>
                  <small>1 hour ago Reported</small>
                </div>
              </div>

              <!-- Item 4: Elevator Out of Service -->
              <div class="alert-item-card">
                <div class="alert-thumb" style="background:#fee2e2;">🛗</div>
                <div class="alert-details">
                  <strong>Elevator Out of Service</strong>
                  <p>Admin Block • 80 m away</p>
                </div>
                <div class="alert-meta">
                  <span class="risk-pill risk-high">High Risk</span>
                  <small>2 hours ago Verified</small>
                </div>
              </div>

              <!-- Item 5: Tree Branch -->
              <div class="alert-item-card">
                <div class="alert-thumb" style="background:#dbeafe;">🌿</div>
                <div class="alert-details">
                  <strong>Tree Branch – Low Height</strong>
                  <p>Main Path • 120 m away</p>
                </div>
                <div class="alert-meta">
                  <span class="risk-pill risk-low">Low Risk</span>
                  <small>3 hours ago Reported</small>
                </div>
              </div>
            </div>

            <!-- Big Report Button -->
            <button class="report-hazard-btn" id="openReportHazardModalBtn">
              <span>➕</span>
              <span>Report New Hazard</span>
            </button>
          </div>
        </section>

        <!-- ROW 3: THREE CARDS (ACTIVE NAV SESSION, MODEL PERFORMANCE, SAFE-LOOP QUALITY GATE) -->
        <section class="tri-card-row">
          
          <!-- 1. Active Navigation Session -->
          <div class="card-panel">
            <div class="panel-header-row">
              <div class="panel-title-box">
                <h3>🧭 Active Navigation Session</h3>
                <p>Main Entrance ➔ Library (1st Floor)</p>
              </div>
              <button class="panel-action-btn" style="color:#ef4444;" id="endNavSessionBtn">End Session</button>
            </div>

            <div class="nav-session-meta">
              <span class="nav-tag-pill">♿ Step-free Route</span>
              <span class="nav-tag-pill">⏱️ ~4 minutes</span>
              <span class="nav-tag-pill">📏 250 m</span>
            </div>

            <div class="nav-steps-list">
              <div class="nav-step-item">
                <div class="step-num-badge">1</div>
                <div class="step-instruction">
                  <strong>Walk straight for 30 meters</strong>
                  <small>Towards Academic Block</small>
                </div>
                <span class="step-distance">30 m</span>
              </div>

              <div class="nav-step-item">
                <div class="step-num-badge">2</div>
                <div class="step-instruction">
                  <strong>Turn right</strong>
                  <small>Follow tactile paving</small>
                </div>
                <span class="step-distance">20 m</span>
              </div>

              <div class="nav-step-item">
                <div class="step-num-badge">3</div>
                <div class="step-instruction">
                  <strong>Continue to the lift (left side)</strong>
                  <small>Braille buttons available</small>
                </div>
                <span class="step-distance">15 m</span>
              </div>

              <div class="nav-step-item">
                <div class="step-num-badge">4</div>
                <div class="step-instruction">
                  <strong>Library entrance ahead</strong>
                  <small>Automatic sliding door</small>
                </div>
                <span class="step-distance">10 m</span>
              </div>
            </div>

            <div class="nav-audio-controls">
              <button class="audio-ctrl-btn" id="navRepeatBtn"><span>🔁</span> <span>Repeat</span></button>
              <button class="audio-ctrl-btn" id="navNextBtn"><span>⏭️</span> <span>Next</span></button>
              <button class="audio-ctrl-btn" id="navPauseBtn"><span>⏸️</span> <span>Pause</span></button>
            </div>
          </div>

          <!-- 2. Model Performance (Current vs Previous) -->
          <div class="card-panel">
            <div class="panel-header-row">
              <div class="panel-title-box">
                <h3>📊 Model Performance</h3>
                <p>Current vs Previous (YOLOv8)</p>
              </div>
              <button class="panel-action-btn">Object Detection ▾</button>
            </div>

            <div class="model-kpi-subgrid">
              <div class="model-kpi-box">
                <small>mAP@50</small>
                <strong>0.91</strong>
                <span>▲ +3%</span>
              </div>
              <div class="model-kpi-box">
                <small>Recall (Crit.)</small>
                <strong>0.96</strong>
                <span>▲ +5%</span>
              </div>
              <div class="model-kpi-box">
                <small>Precision</small>
                <strong>0.89</strong>
                <span>▲ +2%</span>
              </div>
              <div class="model-kpi-box">
                <small>F1 Score</small>
                <strong>0.92</strong>
                <span>▲ +3%</span>
              </div>
            </div>

            <!-- SVG Line Comparison Chart -->
            <div class="chart-canvas-wrap">
              <svg width="100%" height="100%" viewBox="0 0 320 120" preserveAspectRatio="none">
                <!-- Grid Lines -->
                <line x1="10" y1="20" x2="310" y2="20" stroke="#f1f5f9" stroke-width="1" />
                <line x1="10" y1="55" x2="310" y2="55" stroke="#f1f5f9" stroke-width="1" />
                <line x1="10" y1="90" x2="310" y2="90" stroke="#f1f5f9" stroke-width="1" />

                <!-- Previous v2.2.0 (Orange) -->
                <polyline fill="none" stroke="#f59e0b" stroke-width="2" stroke-dasharray="3,3"
                  points="20,70 70,75 120,65 170,80 220,55 270,70" />

                <!-- Current v2.3.1 (Teal) -->
                <polyline fill="none" stroke="#0d9488" stroke-width="2.5"
                  points="20,45 70,35 120,38 170,48 220,30 270,36" />

                <!-- Data Points -->
                <circle cx="20" cy="45" r="4" fill="#0d9488" />
                <circle cx="70" cy="35" r="4" fill="#0d9488" />
                <circle cx="120" cy="38" r="4" fill="#0d9488" />
                <circle cx="170" cy="48" r="4" fill="#0d9488" />
                <circle cx="220" cy="30" r="4" fill="#0d9488" />
                <circle cx="270" cy="36" r="4" fill="#0d9488" />

                <!-- Category Labels -->
                <text x="20" y="112" font-size="8" fill="#64748b" text-anchor="middle">Obstacles</text>
                <text x="70" y="112" font-size="8" fill="#64748b" text-anchor="middle">Stairs</text>
                <text x="120" y="112" font-size="8" fill="#64748b" text-anchor="middle">Elevators</text>
                <text x="170" y="112" font-size="8" fill="#64748b" text-anchor="middle">People</text>
                <text x="220" y="112" font-size="8" fill="#64748b" text-anchor="middle">Vehicles</text>
                <text x="270" y="112" font-size="8" fill="#64748b" text-anchor="middle">Low Light</text>
              </svg>
            </div>

            <div style="display:flex; justify-content:center; gap:16px; margin-top:8px; font-size:0.72rem; font-weight:700;">
              <span style="color:#0d9488;">● Current (v2.3.1)</span>
              <span style="color:#f59e0b;">- - Previous (v2.2.0)</span>
            </div>
          </div>

          <!-- 3. SAFE-Loop Quality Gate -->
          <div class="card-panel">
            <div class="panel-header-row">
              <div class="panel-title-box">
                <h3>⚖️ SAFE-Loop Quality Gate</h3>
                <p>Zero critical regression policy</p>
              </div>
              <button class="panel-action-btn" id="viewGateDetailsBtn">View Details</button>
            </div>

            <div class="gate-stages-list" id="gateStagesContainer">
              <div class="gate-stage-item">
                <span class="stage-title"><span>1.</span> Data Validation</span>
                <span class="stage-badge badge-passed">✔ Passed (v1.2)</span>
              </div>
              <div class="gate-stage-item">
                <span class="stage-title"><span>2.</span> Training (SageMaker)</span>
                <span class="stage-badge badge-passed">✔ Completed</span>
              </div>
              <div class="gate-stage-item">
                <span class="stage-title"><span>3.</span> Scenario Evaluation</span>
                <span class="stage-badge badge-passed">✔ Passed (12/12)</span>
              </div>
              <div class="gate-stage-item">
                <span class="stage-title"><span>4.</span> Risk Analysis</span>
                <span class="stage-badge badge-passed">✔ No Regressions</span>
              </div>
              <div class="gate-stage-item" style="background:#ccfbf1; border-color:#99f6e4;">
                <span class="stage-title"><strong>5. Gate Decision</strong></span>
                <span class="stage-badge badge-passed" style="background:#0d9488; color:#fff;">✔ Approved Staging</span>
              </div>
              <div class="gate-stage-item">
                <span class="stage-title"><span>6.</span> Deploy to Staging</span>
                <span class="stage-badge badge-running">🔄 In Progress</span>
              </div>
              <div class="gate-stage-item">
                <span class="stage-title"><span>7.</span> Production Rollout</span>
                <span class="stage-badge badge-pending">⏱ Pending</span>
              </div>
            </div>

            <div class="gate-action-buttons">
              <button class="btn-gate-test btn-gate-pass" id="runGateCheckBtn">
                <span>✔</span> <span>Verify Gate</span>
              </button>
              <button class="btn-gate-test btn-gate-fail" id="simulateGateFailureBtn">
                <span>⚠️</span> <span>Inject Failure Demo</span>
              </button>
            </div>
          </div>
        </section>

        <!-- ROW 4: BOTTOM THREE PANELS -->
        <section class="bottom-tri-row">
          
          <!-- 1. Dataset Coverage & Examples -->
          <div class="card-panel">
            <div class="panel-header-row">
              <div class="panel-title-box">
                <h3>📁 Dataset Coverage & Examples</h3>
                <p>1,320 images across 5 conditions (DVC v1.2)</p>
              </div>
              <button class="panel-action-btn">View Dataset</button>
            </div>

            <div class="dataset-thumbs-strip">
              <div class="dataset-thumb-box">
                <div class="dataset-icon-circle" style="background:#fef3c7;">☀️</div>
                <span>Normal Light</span>
              </div>
              <div class="dataset-thumb-box">
                <div class="dataset-icon-circle" style="background:#ede9fe;">🌙</div>
                <span>Low Light</span>
              </div>
              <div class="dataset-thumb-box">
                <div class="dataset-icon-circle" style="background:#fee2e2;">📦</div>
                <span>Occlusion</span>
              </div>
              <div class="dataset-thumb-box">
                <div class="dataset-icon-circle" style="background:#cffafe;">👥</div>
                <span>Crowded</span>
              </div>
              <div class="dataset-thumb-box">
                <div class="dataset-icon-circle" style="background:#d1fae5;">🏛️</div>
                <span>Corridors</span>
              </div>
            </div>
          </div>

          <!-- 2. Experiment Tracking (MLflow) -->
          <div class="card-panel">
            <div class="panel-header-row">
              <div class="panel-title-box">
                <h3>🔬 Experiment Tracking (MLflow)</h3>
                <p>CampusObstacles Active Run History</p>
              </div>
              <button class="panel-action-btn">View All</button>
            </div>

            <table class="mlflow-table">
              <thead>
                <tr>
                  <th>Run ID</th>
                  <th>Model Version</th>
                  <th>mAP@50</th>
                  <th>Crit. Recall</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>#1023</td>
                  <td><strong>v2.3.1</strong></td>
                  <td>0.91</td>
                  <td>0.96</td>
                  <td><span class="stage-badge badge-passed">Approved</span></td>
                </tr>
                <tr>
                  <td>#1022</td>
                  <td><strong>v2.3.0</strong></td>
                  <td>0.88</td>
                  <td>0.91</td>
                  <td><span class="stage-badge badge-rejected">Rejected</span></td>
                </tr>
                <tr>
                  <td>#1021</td>
                  <td><strong>v2.2.1</strong></td>
                  <td>0.87</td>
                  <td>0.89</td>
                  <td><span class="stage-badge" style="background:#fef3c7; color:#b45309;">Staging</span></td>
                </tr>
              </tbody>
            </table>
          </div>

          <!-- 3. System Health & Services -->
          <div class="card-panel">
            <div class="panel-header-row">
              <div class="panel-title-box">
                <h3>⚡ System Health & Services</h3>
                <p>Live cluster telemetry & SLA metrics</p>
              </div>
              <button class="panel-action-btn">View All</button>
            </div>

            <div class="services-health-grid">
              <div>
                <div class="service-item-row">
                  <span>🟢 API Server</span>
                  <span>Healthy</span>
                </div>
                <div class="service-item-row">
                  <span>🟢 Model Inference</span>
                  <span>Healthy</span>
                </div>
                <div class="service-item-row">
                  <span>🟢 Database</span>
                  <span>Healthy</span>
                </div>
                <div class="service-item-row">
                  <span>🟢 Cloud (AWS)</span>
                  <span>Healthy</span>
                </div>
                <div class="service-item-row">
                  <span>🟢 Mobile Sync</span>
                  <span>Healthy</span>
                </div>
              </div>

              <div style="display:flex; flex-direction:column; gap:8px;">
                <div class="telemetry-mini-card">
                  <small>Live Inference Load</small>
                  <strong>42 req/min</strong>
                </div>
                <div class="telemetry-mini-card">
                  <small>Uptime (30 days)</small>
                  <strong style="color:#059669;">99.8%</strong>
                </div>
              </div>
            </div>
          </div>
        </section>

      </div> <!-- /viewDashboard -->

      <!-- VIEW 2: LIVE ASSISTANT (WEBCAM & YOLOV8 PERCEPTION) -->
      <div class="view-panel" id="viewAssistant">
        <div class="camera-workspace-card">
          <div class="panel-header-row">
            <div class="panel-title-box">
              <h3>👁️ Live Visual Assistant & SafePath AI</h3>
              <p>Real-time YOLOv8 object detection, obstacle distance, overhead clearance & spatial voice</p>
            </div>
            <div style="display:flex; gap:10px;">
              <select id="personaSelect" style="padding:6px 12px; border-radius:var(--radius-full); border:1px solid var(--card-border); font-size:0.8rem; font-weight:700;">
                <option value="bvi">Persona: Visually Impaired (BVI)</option>
                <option value="wheelchair">Persona: Wheelchair / Stroller</option>
                <option value="elderly">Persona: Elderly / Assisted</option>
                <option value="emergency">Persona: Emergency Evacuation</option>
              </select>
            </div>
          </div>

          <div class="camera-feed-box">
            <video id="video" playsinline></video>
            <canvas id="overlay"></canvas>
            <div class="camera-placeholder" id="cameraPlaceholder">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"></path>
                <circle cx="12" cy="13" r="4"></circle>
              </svg>
              <h4>Camera Offline</h4>
              <p>Click "Start Assistance" to stream live webcam frames</p>
            </div>
          </div>

          <!-- SafePath HUD Telemetry -->
          <div style="display:grid; grid-template-columns:repeat(3, 1fr); gap:12px; max-width:720px; margin:0 auto 16px;">
            <div class="telemetry-mini-card" id="groundHudCard">
              <small>Ground Traversability</small>
              <strong id="groundHud" style="color:#059669;">Nominal</strong>
            </div>
            <div class="telemetry-mini-card" id="overheadHudCard">
              <small>Overhead Clearance</small>
              <strong id="overheadHud" style="color:#059669;">Clear (&gt;2.1m)</strong>
            </div>
            <div class="telemetry-mini-card" id="ttcHudCard">
              <small>Time-To-Collision (TTC)</small>
              <strong id="ttcHud" style="color:#0284c7;">Safe</strong>
            </div>
          </div>

          <div class="camera-actions-row">
            <button class="report-hazard-btn" id="startBtn" style="max-width:200px;">
              <span>📹</span> <span>Start Assistance</span>
            </button>
            <button class="panel-action-btn" id="describeBtn" style="padding:10px 20px; font-weight:800;">
              <span>🗣️</span> <span>Describe Scene</span>
            </button>
            <button class="panel-action-btn" id="voiceBtn" style="padding:10px 20px; font-weight:800;">
              <span>🎙️</span> <span>Enable Voice</span>
            </button>
          </div>

          <!-- Detection Log -->
          <div style="margin-top:18px; background:#f8fafc; border-radius:var(--radius-md); padding:12px; border:1px solid var(--card-border);">
            <div style="display:flex; justify-content:space-between; margin-bottom:8px; font-size:0.8rem; font-weight:700;">
              <span>Live Detected Objects (<span id="detCount">0</span>)</span>
              <span id="latencyBadge" style="color:#059669;">Latency: -- ms</span>
            </div>
            <div id="detectionList" style="display:flex; gap:8px; flex-wrap:wrap; font-size:0.75rem;">
              <span style="color:#94a3b8;">No active detections yet.</span>
            </div>
          </div>
        </div>
      </div> <!-- /viewAssistant -->

      <!-- VIEW 3: STUDENT PERFORMANCE CASE STUDY (UNIT I & V) -->
      <div class="view-panel" id="viewStudent">
        <div class="card-panel">
          <div class="panel-header-row">
            <div class="panel-title-box">
              <h3>🎓 Student Academic Performance Prediction & SHAP Explainability</h3>
              <p>Unit I Tabular ML Lifecycle + Unit V Explainable AI Model Card</p>
            </div>
            <span class="stage-badge badge-passed">RandomForestRegressor v1.0</span>
          </div>

          <form class="student-perf-form" id="studentPerfForm">
            <div class="form-group">
              <label>Study Hours per Week (1 - 15 hrs)</label>
              <input type="number" id="studyHoursInput" value="7.5" min="1" max="15" step="0.5" />
            </div>
            <div class="form-group">
              <label>Attendance Rate (50% - 100%)</label>
              <input type="number" id="attendanceInput" value="92.0" min="50" max="100" step="1" />
            </div>
            <div class="form-group">
              <label>Parental Education Level</label>
              <select id="parentEduInput">
                <option value="High School">High School</option>
                <option value="Bachelor" selected>Bachelor's Degree</option>
                <option value="Master">Master's / Ph.D.</option>
              </select>
            </div>
            <div class="form-group">
              <label>Extracurricular Activities</label>
              <select id="extraInput">
                <option value="Yes" selected>Yes (Active)</option>
                <option value="No">No</option>
              </select>
            </div>
            <div class="form-group" style="grid-column: span 2;">
              <label>Previous Semester Examination Score (0 - 100)</label>
              <input type="number" id="prevScoreInput" value="78.0" min="0" max="100" step="1" />
            </div>
            <div style="grid-column: span 2; display:flex; justify-content:flex-end;">
              <button type="button" class="report-hazard-btn" id="predictStudentBtn" style="max-width:240px;">
                <span>🔮</span> <span>Predict Academic Outcome</span>
              </button>
            </div>
          </form>

          <!-- Result & SHAP Attribution Cards -->
          <div id="studentResultCard" style="display:none; background:#f0fdf4; border:1px solid #bbf7d0; border-radius:var(--radius-lg); padding:18px; margin-top:14px;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
              <div>
                <span style="font-size:0.75rem; font-weight:700; color:#15803d; text-transform:uppercase;">Predicted Outcome</span>
                <h2 style="font-size:1.8rem; font-weight:800; color:#14532d;" id="predictedScoreVal">84.5 / 100</h2>
              </div>
              <div style="text-align:right;">
                <span class="stage-badge badge-passed" id="predictedRiskVal">Low Risk (Excelling)</span>
                <small style="display:block; color:#15803d; margin-top:4px;">Confidence: 94.2%</small>
              </div>
            </div>

            <h4 style="font-size:0.85rem; font-weight:800; color:#14532d; margin-bottom:8px;">SHAP Feature Attribution (Impact on Prediction):</h4>
            <div id="shapBarsContainer" style="display:flex; flex-direction:column; gap:6px; font-size:0.78rem;">
              <!-- Dynamic SHAP attribution bars -->
            </div>
            <p style="font-size:0.7rem; color:#166534; margin-top:12px; font-style:italic;">
              Governance Disclaimer: This prediction is generated solely for academic early-intervention planning and counselor review. Predictions are assistive and must not be used for high-stakes automated decisions.
            </p>
          </div>
        </div>
      </div> <!-- /viewStudent -->

      <!-- VIEW 4: MLOPS LIFECYCLE EXPLORER (UNIT I) -->
      <div class="view-panel" id="viewLifecycle">
        <div class="card-panel">
          <div class="panel-header-row">
            <div class="panel-title-box">
              <h3>🛡️ End-to-End MLOps Lifecycle Explorer</h3>
              <p>Complete 10-stage execution pipeline from Problem Formulation to Controlled Retraining</p>
            </div>
            <button class="panel-action-btn" id="refreshLifecycleBtn">🔄 Refresh Status</button>
          </div>

          <div id="lifecycleStagesList" style="display:flex; flex-direction:column; gap:10px; margin-top:12px;">
            <!-- Dynamically populated from /api/mlops/lifecycle -->
          </div>
        </div>
      </div> <!-- /viewLifecycle -->

    </main>
  </div>

  <!-- ==========================================================================
       MODAL: REPORT MICRO-HAZARD
       ========================================================================== -->
  <div class="modal-overlay" id="hazardModal">
    <div class="modal-content-box">
      <div class="modal-header">
        <h3>⚠️ Report Campus Micro-Hazard</h3>
        <button class="modal-close-btn" id="closeHazardModalBtn">✕</button>
      </div>

      <form id="hazardForm">
        <div class="form-group" style="margin-bottom:12px;">
          <label>Campus Node / Location</label>
          <select id="hazardNodeSelect">
            <option value="main_entrance">Main Entrance</option>
            <option value="admin_block">Admin Block</option>
            <option value="library">Library Block</option>
            <option value="science_block">Science Block</option>
            <option value="cse_dept">CSE Department</option>
            <option value="canteen">Canteen & Cafeteria</option>
            <option value="stairs_1">Science Block Stairs (Outdoor)</option>
          </select>
        </div>

        <div class="form-group" style="margin-bottom:12px;">
          <label>Hazard Type</label>
          <select id="hazardTypeSelect">
            <option value="stairs_blockage">Stairs Blockage / Under Construction</option>
            <option value="wet_floor">Wet Floor / Slick Tiles</option>
            <option value="crowded_corridor">Crowded Bottleneck / Obstacle</option>
            <option value="elevator_fault">Elevator Out of Service</option>
            <option value="low_hanging">Low Hanging Tree Branch / Sign</option>
          </select>
        </div>

        <div class="form-group" style="margin-bottom:12px;">
          <label>Severity Level</label>
          <select id="hazardSeveritySelect">
            <option value="HIGH">High Risk (Blocks Wheelchairs & BVI)</option>
            <option value="MEDIUM">Medium Risk (Requires Caution)</option>
            <option value="LOW">Low Risk (Minor Inconvenience)</option>
          </select>
        </div>

        <div class="form-group" style="margin-bottom:18px;">
          <label>Description & Notes</label>
          <input type="text" id="hazardDescInput" placeholder="e.g. Mop cleaning in progress, tiles slippery" required />
        </div>

        <button type="submit" class="report-hazard-btn">
          <span>🚀</span> <span>Submit Verified Hazard</span>
        </button>
      </form>
    </div>
  </div>

  <!-- Hidden legacy binding hooks for backward compatibility -->
  <div style="display:none;">
    <span id="modelBadge"></span>
    <span id="cameraBadge"></span>
    <span id="fpsBadge"></span>
    <span id="driftBadge"></span>
    <span id="eriBadge"></span>
    <span id="audioBadge"></span>
    <span id="detectorNote"></span>
    <span id="voiceStatus"></span>
    <span id="sessionLog"></span>
    <input type="text" id="destinationInput" />
    <button id="findBtn"></button>
    <button id="ocrBtn"></button>
    <div id="ocrResult"></div>
    <div id="navResult"></div>
    <div id="navPersonaAdvice"></div>
    <div id="fleetHazardsList"></div>
    <button id="reportHazardBtn"></button>
    <canvas id="mapCanvas"></canvas>
  </div>

  <script src="/static/app.js"></script>
</body>
</html>
"""

(ROOT / "static" / "index.html").write_text(html_content, encoding="utf-8")
print(f"Generated static/index.html successfully! Size: {len(html_content)} bytes")
