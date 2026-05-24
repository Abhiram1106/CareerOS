from __future__ import annotations


def probe_openvino() -> dict:
    """Report OpenVINO availability — embedding IR bench runs only when model artifacts exist."""
    try:
        from openvino.runtime import Core  # noqa: PLC0415

        core = Core()
        devices = core.available_devices
        return {
            "status": "available",
            "devices": list(devices),
            "note": "Model IR not bundled — run export step before latency measurement.",
        }
    except ImportError:
        return {
            "status": "skipped",
            "devices": [],
            "note": "openvino package not installed in this environment.",
        }
    except Exception as exc:  # pragma: no cover - hardware specific
        return {
            "status": "error",
            "devices": [],
            "note": str(exc),
        }
