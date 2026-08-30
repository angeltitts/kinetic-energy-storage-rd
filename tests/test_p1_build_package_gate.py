from pathlib import Path

from prototype.p1_single_rotor.build_package_gate import inspect_build_package


def test_repository_build_package_is_complete():
    repo_root = Path(__file__).resolve().parents[1]
    result = inspect_build_package(repo_root)
    assert result.ok, (result.missing_files, result.missing_invariants)


def test_missing_artifact_fails_closed(tmp_path):
    p1 = tmp_path / "prototype" / "p1_single_rotor"
    p1.mkdir(parents=True)
    result = inspect_build_package(tmp_path)
    assert not result.ok
    assert "BOM.md" in result.missing_files


def test_missing_release_invariant_fails_closed(tmp_path):
    from prototype.p1_single_rotor.build_package_gate import (
        REQUIRED_ARTIFACTS,
        RELEASE_INVARIANTS,
    )

    p1 = tmp_path / "prototype" / "p1_single_rotor"
    p1.mkdir(parents=True)

    for rel in REQUIRED_ARTIFACTS:
        path = p1 / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("placeholder\n", encoding="utf-8")

    for rel, snippets in RELEASE_INVARIANTS.items():
        path = p1 / rel
        path.write_text("\n".join(snippets) + "\n", encoding="utf-8")

    # Deliberately remove one released safety invariant while keeping the file.
    wiring = p1 / "WIRING_RELEASE.md"
    wiring.write_text(
        wiring.read_text(encoding="utf-8").replace("F1 10 A MAX", "F1 unspecified"),
        encoding="utf-8",
    )

    result = inspect_build_package(tmp_path)
    assert not result.ok
    assert any("F1 10 A MAX" in item for item in result.missing_invariants)
