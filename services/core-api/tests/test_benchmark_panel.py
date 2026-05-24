from __future__ import annotations


def test_benchmark_panel_public(client):
    resp = client.get("/benchmarks")
    assert resp.status_code == 200
    body = resp.json()
    assert "workloads" in body
    assert "methodology" in body


def test_ready_endpoint(client):
    resp = client.get("/ready")
    assert resp.status_code == 200
    assert resp.json()["status"] in ("ready", "not_ready")
