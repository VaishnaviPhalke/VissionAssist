from fastapi.testclient import TestClient
from pathlib import Path
from app.main import app
from mlops.batch_inference import run_batch_inference
from mlops.explainability_audit import run_explainability_audit
from mlops.sagemaker_pipeline import build_sagemaker_pipeline_definition
from mlops.airflow_dag import task_validate_dataset, task_validate_gate

client = TestClient(app)


def test_health():
    response = client.get('/api/health')
    assert response.status_code == 200
    data = response.json()
    assert data['ok'] is True


def test_map():
    response = client.get('/api/map')
    assert response.status_code == 200
    assert 'nodes' in response.json()


def test_navigation():
    response = client.get('/api/navigation', params={'destination': 'Library'})
    assert response.status_code == 200
    assert response.json()['ok'] is True


def test_wheelchair_navigation():
    # Route to CSE Dept with wheelchair persona: should prune stairs_1 and use elevator
    response = client.get('/api/navigation', params={'destination': 'CSE Department', 'persona': 'wheelchair'})
    assert response.status_code == 200
    data = response.json()
    assert data['ok'] is True
    assert 'steps' in data
    # Verify stairs_1 is not in path
    node_ids = [s['node_id'] for s in data['steps']]
    assert 'stairs_1' not in node_ids
    assert 'Wheelchair' in data['persona_advice']


def test_demo_status():
    response = client.get('/api/demo/status')
    assert response.status_code == 200
    data = response.json()
    assert 'features' in data
    assert 'model' in data


def test_detect_endpoint():
    from io import BytesIO
    from PIL import Image

    img = Image.new('RGB', (320, 320), color=(100, 150, 200))
    buf = BytesIO()
    img.save(buf, format='JPEG')
    buf.seek(0)

    response = client.post('/api/detect', files={'file': ('test.jpg', buf, 'image/jpeg')}, data={'persona': 'bvi'})
    assert response.status_code == 200
    data = response.json()
    assert 'detections' in data
    assert data['image_width'] == 320
    assert data['image_height'] == 320
    assert 'mlops_telemetry' in data
    assert 'safepath_profile' in data
    assert 'ground_profiler' in data['safepath_profile']
    assert 'overhead_clearance' in data['safepath_profile']
    assert 'environmental_reliability' in data['safepath_profile']


def test_ocr_endpoint():
    from io import BytesIO
    from PIL import Image

    img = Image.new('RGB', (200, 100), color=(255, 255, 255))
    buf = BytesIO()
    img.save(buf, format='JPEG')
    buf.seek(0)

    response = client.post('/api/ocr', files={'file': ('ocr.jpg', buf, 'image/jpeg')})
    assert response.status_code == 200
    data = response.json()
    assert 'ok' in data


def test_mlops_metrics_endpoint():
    response = client.get('/api/mlops/metrics')
    assert response.status_code == 200
    data = response.json()
    assert data['ok'] is True
    assert 'monitor_summary' in data
    assert data['target_classes_count'] == 15


def test_mlops_drift_endpoint():
    response = client.get('/api/mlops/drift')
    assert response.status_code == 200
    data = response.json()
    assert data['ok'] is True
    assert 'drift_rate' in data
    assert 'retraining_needed' in data


def test_safepath_hazards_endpoint():
    response = client.get('/api/safepath/hazards')
    assert response.status_code == 200
    data = response.json()
    assert data['ok'] is True
    assert 'active_hazards' in data


def test_safepath_report_hazard():
    response = client.post(
        '/api/safepath/report_hazard',
        data={
            'node_id': 'auditorium',
            'hazard_type': 'wet_floor',
            'description': 'Cleaning in progress',
            'severity': 'HIGH'
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data['ok'] is True
    assert data['hazard']['node_id'] == 'auditorium'


def test_safepath_personas_endpoint():
    response = client.get('/api/safepath/personas')
    assert response.status_code == 200
    data = response.json()
    assert data['ok'] is True
    assert len(data['personas']) >= 4


def test_unit_iv_batch_inference():
    """Unit IV: Offline Batch Inference Pipeline test"""
    batch_dir = Path(__file__).resolve().parent.parent / "runs" / "test_batch_frames"
    summary = run_batch_inference(image_dir=batch_dir, batch_size=2)
    assert summary['status'] == 'SUCCESS'
    assert summary['dataset_size'] > 0
    assert 'latency_metrics_ms' in summary
    assert summary['throughput_fps'] > 0


def test_unit_v_explainability_audit():
    """Unit V: Explainability & Subgroup Fairness Audit test"""
    audit = run_explainability_audit()
    assert audit['status'] == 'PASSED'
    assert len(audit['subgroups_evaluated']) >= 3
    assert 'fairness_results' in audit
    assert (Path(__file__).resolve().parent.parent / "docs" / "MODEL_CARD.md").exists()


def test_unit_vi_sagemaker_pipeline():
    """Unit VI: AWS SageMaker Cloud Pipeline Specification test"""
    spec = build_sagemaker_pipeline_definition()
    assert spec['PipelineName'] == 'VisionAssist-Retraining-Pipeline'
    assert len(spec['Steps']) >= 4
    step_names = [s['Name'] for s in spec['Steps']]
    assert 'YoloV8CloudTrainingStep' in step_names
    assert 'QualityGateConditionStep' in step_names


def test_unit_iii_airflow_tasks():
    """Unit III: Airflow standalone task execution test"""
    val_res = task_validate_dataset()
    assert val_res['status'] == 'SUCCESS'
    gate_res = task_validate_gate()
    assert 'evaluated_metrics' in gate_res
    assert gate_res['passed'] is True


def test_android_app_page():
    response = client.get('/android')
    assert response.status_code == 200
    assert 'VisionAssist' in response.text
    assert 'Start Assistance' in response.text


def test_android_overview():
    response = client.get('/api/android/overview')
    assert response.status_code == 200
    data = response.json()
    assert data['ok'] is True
    assert 'system_status' in data
    assert len(data['quick_modules']) == 4
    assert 'emergency_contacts' in data


def test_android_nearby_hazards():
    response = client.get('/api/android/hazards/nearby')
    assert response.status_code == 200
    data = response.json()
    assert data['ok'] is True
    assert 'hazards' in data


def test_android_report_hazard_and_admin_action():
    # 1. Report from Android
    res = client.post(
        '/api/android/hazards/report',
        data={
            'category': 'Blocked Path',
            'location_name': 'Auditorium Ramp',
            'description': 'Scaffolding pole obstruction',
            'severity': 'HIGH'
        }
    )
    assert res.status_code == 200
    rep_data = res.json()
    assert rep_data['ok'] is True
    hazard_id = rep_data['hazard']['id']

    # 2. Check Admin Overview sees it
    admin_res = client.get('/api/admin/overview')
    assert admin_res.status_code == 200
    admin_data = admin_res.json()
    assert admin_data['ok'] is True
    assert any(h['id'] == hazard_id for h in admin_data['hazard_reports'])

    # 3. Admin verifies hazard
    action_res = client.post(
        '/api/admin/hazards/action',
        data={'hazard_id': hazard_id, 'action': 'verify'}
    )
    assert action_res.status_code == 200
    assert action_res.json()['new_status'] == 'VERIFIED'

    # 4. Admin resolves hazard
    resolve_res = client.post(
        '/api/admin/hazards/action',
        data={'hazard_id': hazard_id, 'action': 'resolve'}
    )
    assert resolve_res.status_code == 200
    assert resolve_res.json()['new_status'] == 'RESOLVED'


# ========================================================
# MLOps & SAFE-Loop Governance Verification Tests
# ========================================================

def test_mlops_model_registry_metadata():
    """1. Can register models and retrieve metadata with SHA-256 checksums."""
    res = client.get('/api/mlops/models')
    assert res.status_code == 200
    data = res.json()
    assert data['ok'] is True
    assert 'active_model' in data
    assert len(data['models']) >= 2
    for m in data['models']:
        assert 'version' in m
        assert 'checksum' in m
        assert 'evaluation_metrics' in m
        assert 'status' in m


def test_mlops_safeloop_failing_safety_gate_blocks_release():
    """2. A deliberately failing safety test blocks candidate release."""
    res = client.post(
        '/api/mlops/safeloop/evaluate',
        data={'candidate_version': 'v2.4.0-unsafe-candidate', 'auto_promote': False, 'inject_failure': True}
    )
    assert res.status_code == 200
    data = res.json()
    assert data['ok'] is True
    assert data['passed'] is False
    assert data['decision'] == 'REJECTED'
    assert len(data['violations']) > 0
    assert any('CRITICAL VIOLATION' in v for v in data['violations'])


def test_mlops_safeloop_passing_gate_promotes_model():
    """3. An approved candidate passes evaluation and can be promoted to active PRODUCTION."""
    # 1. Run gate with auto_promote=True
    eval_res = client.post(
        '/api/mlops/safeloop/evaluate',
        data={'candidate_version': 'v2.4.0-candidate', 'auto_promote': True, 'inject_failure': False}
    )
    assert eval_res.status_code == 200
    eval_data = eval_res.json()
    assert eval_data['passed'] is True
    assert eval_data['decision'] == 'APPROVED'

    # 2. Verify active model in registry is updated
    reg_res = client.get('/api/mlops/models')
    active_m = reg_res.json()['active_model']
    assert active_m['version'] == 'v2.4.0-candidate'
    assert active_m['status'] == 'PRODUCTION'


def test_mlops_emergency_rollback_and_active_version_persisted():
    """4. Can restore the previous model version and verify the backend uses it."""
    # Rollback to v2.3.1
    rollback_res = client.post(
        '/api/mlops/models/rollback',
        data={'target_version': 'v2.3.1', 'reason': 'Verification rollback to champion'}
    )
    assert rollback_res.status_code == 200
    rb_data = rollback_res.json()
    assert rb_data['ok'] is True
    assert rb_data['active_model']['version'] == 'v2.3.1'
    assert rb_data['active_model']['status'] == 'PRODUCTION'

    # Verify audit log recorded the rollback
    audit_res = client.get('/api/mlops/audit')
    assert audit_res.status_code == 200
    events = audit_res.json()['audit_events']
    assert any(e['event_type'] == 'MODEL_ROLLBACK' and e['version'] == 'v2.3.1' for e in events)


def test_mlops_safeloop_error_evidence_human_review_and_audit_trail():
    """5. A reviewed error report flows through the SAFE-Loop workflow with human validation."""
    # Step 1: User submits failure report
    submit_res = client.post(
        '/api/safeloop/evidence/submit',
        data={
            'category': 'Missed Obstacle',
            'predicted_label': 'clear',
            'actual_label': 'low_curb',
            'notes': 'Unpainted step down near Canteen entrance',
            'user_id': 'bvi_student_07',
            'privacy_consent': True
        }
    )
    assert submit_res.status_code == 200
    rep_id = submit_res.json()['report']['id']
    assert submit_res.json()['report']['status'] == 'PENDING_REVIEW'

    # Step 2: Human-in-the-loop SME reviews & labels
    review_res = client.post(
        '/api/safeloop/evidence/review',
        data={
            'report_id': rep_id,
            'approved': True,
            'corrected_label': 'curb_edge',
            'reviewer': 'Senior Accessibility Coordinator'
        }
    )
    assert review_res.status_code == 200
    rev_data = review_res.json()['report']
    assert rev_data['status'] == 'REVIEWED_APPROVED'
    assert rev_data['corrected_label'] == 'curb_edge'
    assert rev_data['reviewed_by'] == 'Senior Accessibility Coordinator'


def test_android_multilingual_setup_and_12_screens():
    """Verify that Android accessibility client serves all 12 screens and multilingual onboarding."""
    res = client.get('/android')
    assert res.status_code == 200
    html = res.text

    # Verify all 12 screens exist
    for screen_num in range(1, 13):
        screen_id = f"screen{screen_num:02d}"
        assert f'id="{screen_id}"' in html, f"Missing {screen_id} in Android app"

    # Verify Multilingual setup controls exist
    assert 'data-lang="en-US"' in html
    assert 'data-lang="hi-IN"' in html
    assert 'data-lang="mr-IN"' in html
    assert 'data-lang="es-ES"' in html
    assert 'data-lang="ta-IN"' in html

    # Verify basic real-time object detection priority elements
    assert 'id="cameraVideo"' in html
    assert 'id="cameraOverlay"' in html
    assert 'id="liveProximityHud"' in html
    assert 'id="btnSetupToDetect"' in html
    assert 'simulateObstacle' in html



