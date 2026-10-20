"""Local release staging. Live publication remains unavailable pending acceptance."""
from __future__ import annotations
import json
from pathlib import Path


class ReleaseError(Exception):
    def __init__(self, code, message):
        self.code, self.message = code, message
        super().__init__(f"[{code}] {message}")


class ReleaseGate:
    def __init__(self, mode="manual"):
        self.mode, self.approved, self.staging_path = mode, False, None

    def stage(self, data_path):
        self.staging_path = Path(data_path)
        self.approved = False
        return True

    def validate(self, required_fields):
        if not self.staging_path or not self.staging_path.is_file():
            raise ReleaseError("NO_STAGING", "A saved manifest is required")
        manifest = json.loads(self.staging_path.read_text())
        if any(k not in manifest for k in required_fields):
            raise ReleaseError("MISSING_FIELDS", "Staged manifest lacks required fields")
        return validate_release(manifest, self.staging_path.parent)

    def approve(self):
        raise ReleaseError("APPROVAL_REQUIRED", "Automated approval is disabled. Live release needs independent review, explicit user approval and an implemented publication integration.")


def create_release_manifest(issue, inventory_id, data_dir):
    return {"schema_version": 1, "release_id": f"rel_{issue.get('issue_id', 'unknown')}",
            "data_cutoff": issue.get("cutoff_utc"), "issue_id": issue.get("issue_id"),
            "version": issue.get("version", 1), "mode": issue.get("mode"),
            "coverage_status": issue.get("coverage_status", "incomplete"),
            "review_status": issue.get("review_status", "pending"),
            "inventory_snapshot_id": inventory_id}


def validate_release(manifest, data_dir):
    required = ("schema_version", "release_id", "data_cutoff", "issue_id", "inventory_snapshot_id")
    if any(not manifest.get(k) for k in required):
        raise ReleaseError("MISSING_FIELDS", "Release identity/cutoff fields missing")
    if manifest.get("mode") != "production" or manifest.get("coverage_status") != "complete" or manifest.get("review_status") != "approved":
        raise ReleaseError("NOT_READY", "Fixture, incomplete, or unreviewed content cannot be released")
    # Self-reported booleans do not establish a reviewed export bound to evidence.
    raise ReleaseError("NOT_IMPLEMENTED", "Production evidence-to-release binding has not passed acceptance")


def publish_release(manifest, data_dir, output_dir):
    validate_release(manifest, data_dir)
    raise ReleaseError("NOT_IMPLEMENTED", "Live publication is not implemented")
