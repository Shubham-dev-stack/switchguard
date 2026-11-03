import os
import json
import pytest
from dashboard.server import CyberDeckHandler

def test_dashboard_files_exist():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dashboard_dir = os.path.join(base_dir, "dashboard")
    
    assert os.path.exists(os.path.join(dashboard_dir, "index.html"))
    assert os.path.exists(os.path.join(dashboard_dir, "static", "css", "cyberdeck.css"))
    assert os.path.exists(os.path.join(dashboard_dir, "static", "js", "three_background.js"))
    assert os.path.exists(os.path.join(dashboard_dir, "static", "js", "topology.js"))
    assert os.path.exists(os.path.join(dashboard_dir, "static", "js", "dashboard.js"))

def test_dashboard_html_structure():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    html_path = os.path.join(base_dir, "dashboard", "index.html")
    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()

    assert "SwitchGuard CyberDeck" in html
    assert "space-canvas" in html
    assert "topology-canvas" in html
    assert "metric-mtta" in html
    assert "metric-mttr" in html
    assert "trigger-chaos-btn" in html
    assert "postmortem-modal" in html
