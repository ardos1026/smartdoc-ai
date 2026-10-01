from app.utils import get_app_info
from app.document_loader import load_document


def test_get_app_info():
    info = get_app_info()

    assert info["name"] == "SmartDoc AI"
    assert info["version"] == "0.1.0"
    assert info["status"] == "running"


def test_load_text_document():
    content = load_document("sample.txt")

    assert "SmartDoc AI" in content
    assert "cloud-native" in content