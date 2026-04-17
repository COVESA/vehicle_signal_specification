#!/usr/bin/env python3

from __future__ import annotations
from pathlib import Path
import pytest
import logging
import generate as gen_module
from generate import convert_vspec3_files

# ── Test data ──
TEST_DIR = Path(__file__).resolve().parent
INPUT_FILE = TEST_DIR / "dummyData/test_input.vspec3"
INPUT2_FILE = TEST_DIR / "dummyData/test_input_2.vspec3"
EXPECTED_FILE = TEST_DIR / "dummyData/expected_output.vspec"
CONFIG_FILE = TEST_DIR / "config/gomplateConfig.yaml"


def normalize(text: str) -> str:
    """Strip trailing whitespace from each line and leading/trailing blank lines.

    Gomplate template substitution often leaves trailing spaces where
    ``{{ template ... }}`` tags were.
    """
    return "\n".join(line.rstrip() for line in text.strip().splitlines())


def read_input_test_data() -> str:
    """Read input from test data files."""

    assert INPUT_FILE.exists(), f"Test input not found: {INPUT_FILE}"
    vspec3_input = INPUT_FILE.read_text(encoding="utf-8")
    return vspec3_input


def read_input_test_data_2() -> str:
    """Read input2 from test data files."""

    assert INPUT2_FILE.exists(), f"Test input not found: {INPUT2_FILE}"
    vspec3_input = INPUT2_FILE.read_text(encoding="utf-8")
    return vspec3_input


def read_output_test_data() -> str:
    """Read expected output from test data files."""

    assert EXPECTED_FILE.exists(), f"Expected output not found: {EXPECTED_FILE}"
    expected_output = EXPECTED_FILE.read_text(encoding="utf-8")
    return expected_output


def read_config_test_data() -> str:

    assert CONFIG_FILE.exists(), f"Config file not found: {CONFIG_FILE}"
    gomplate_config = CONFIG_FILE.read_text(encoding="utf-8")
    return gomplate_config


# ── Tests ───
class TestVspec3Conversion:

    def test_conversion_produces_expected_output(
        self, workspace: dict[str, Path], gomplate_cmd: str, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Given a test.vspec3 input, gomplate should render the expected .vspec output."""

        # Prepare the environment and dummy input data
        vspec3_input = read_input_test_data()
        expected_output = read_output_test_data()

        spec_dir = workspace["spec"]
        generated_dir = workspace["generated"]
        root_dir = workspace["root"]

        input_file = spec_dir / "test.vspec3"
        input_file.write_text(vspec3_input, encoding="utf-8")

        gomplate_config = read_config_test_data()
        gomplate_config_file = spec_dir / "gomplate_config.yaml"
        gomplate_config_file.write_text(gomplate_config, encoding="utf-8")

        monkeypatch.setattr(gen_module, "SPEC_DIR", spec_dir)
        monkeypatch.setattr(gen_module, "GENERATED_DIR", generated_dir)
        monkeypatch.setattr(gen_module, "CONFIG_PATH", gomplate_config_file)
        monkeypatch.setattr(gen_module, "ROOT_DIR", root_dir)

        # convert the vspec3 input dummy file
        convert_vspec3_files(gomplate_cmd)

        # check the output
        output_file = generated_dir / "test.vspec"
        assert output_file.exists(), f"Expected output not found: {output_file}"

        actual = normalize(output_file.read_text(encoding="utf-8"))
        expected = normalize(expected_output)

        assert actual == expected, (
            f"Output mismatch.\n"
            f"Expected :\n{expected}\n"
            f"Actual :\n{actual}\n"
        )

    def test_output_file_has_vspec_extension(
        self, workspace: dict[str, Path], gomplate_cmd: str, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Output file should have .vspec extension, not .vspec3."""

        # Prepare the environment and dummy input data
        vspec3_input = read_input_test_data()

        spec_dir = workspace["spec"]
        generated_dir = workspace["generated"]
        root_dir = workspace["root"]

        input_file = spec_dir / "test.vspec3"
        input_file.write_text(vspec3_input, encoding="utf-8")

        gomplate_config = read_config_test_data()
        gomplate_config_file = spec_dir / "gomplate_config.yaml"
        gomplate_config_file.write_text(gomplate_config, encoding="utf-8")

        monkeypatch.setattr(gen_module, "SPEC_DIR", spec_dir)
        monkeypatch.setattr(gen_module, "GENERATED_DIR", generated_dir)
        monkeypatch.setattr(gen_module, "CONFIG_PATH", gomplate_config_file)
        monkeypatch.setattr(gen_module, "ROOT_DIR", root_dir)

        # convert the vspec3 input dummy file
        convert_vspec3_files(gomplate_cmd)

        # check the output
        vspec3_outputs = list(generated_dir.rglob("*.vspec3"))
        vspec_outputs = list(generated_dir.rglob("*.vspec"))

        assert len(vspec3_outputs) == 0, "No .vspec3 files should exist in generated/"
        assert len(vspec_outputs) == 1, "Exactly one .vspec file should be generated"

    def test_no_vspec3_files_skips_gracefully(
        self, workspace: dict[str, Path], gomplate_cmd: str, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """When spec/ has no .vspec3 files, conversion should skip without error."""

        # Prepare the environment and dummy input data
        monkeypatch.setattr(gen_module, "SPEC_DIR", workspace["spec"])
        monkeypatch.setattr(gen_module, "GENERATED_DIR", workspace["generated"])
        monkeypatch.setattr(gen_module, "ROOT_DIR", workspace["spec"])
        # convert the vspec3 input dummy file
        convert_vspec3_files(gomplate_cmd)

        # check the output
        generated_files = list(workspace["generated"].rglob("*"))
        assert len(generated_files) == 0, "No files should be generated from empty spec/"

    def test_subdirectory_structure_preserved(
        self, workspace: dict[str, Path], gomplate_cmd: str, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Nested directory structure in spec/ should be mirrored in generated/."""

        # Prepare the environment and dummy input data
        vspec3_input = read_input_test_data()

        root_dir = workspace["root"]
        spec_dir = workspace["spec"]
        generated_dir = workspace["generated"]

        nested_dir = spec_dir / "sub" / "dir"
        nested_dir.mkdir(parents=True)

        input_file = nested_dir / "test.vspec3"
        input_file.write_text(vspec3_input, encoding="utf-8")

        gomplate_config = read_config_test_data()
        gomplate_config_file = spec_dir / "gomplate_config.yaml"
        gomplate_config_file.write_text(gomplate_config, encoding="utf-8")

        monkeypatch.setattr(gen_module, "SPEC_DIR", spec_dir)
        monkeypatch.setattr(gen_module, "GENERATED_DIR", generated_dir)
        monkeypatch.setattr(gen_module, "CONFIG_PATH", gomplate_config_file)
        monkeypatch.setattr(gen_module, "ROOT_DIR", root_dir)

        # convert the vspec3 input dummy file
        convert_vspec3_files(gomplate_cmd)

        # check the output
        output_file = generated_dir / "sub" / "dir" / "test.vspec"
        assert output_file.exists(), f"Nested output not found: {output_file}"

    def test_conversion_produces_failed_output(
        self, workspace: dict[str, Path], gomplate_cmd: str, monkeypatch: pytest.MonkeyPatch, caplog
    ) -> None:
        """Given a test.vspec3 input with wrong datasource, gomplate should fail to render output"""

        # Prepare the environment and dummy input data
        vspec3_input = read_input_test_data_2()

        spec_dir = workspace["spec"]
        generated_dir = workspace["generated"]
        root_dir = workspace["root"]

        input_file = spec_dir / "test.vspec3"
        input_file.write_text(vspec3_input, encoding="utf-8")

        gomplate_config = read_config_test_data()
        gomplate_config_file = spec_dir / "gomplate_config.yaml"
        gomplate_config_file.write_text(gomplate_config, encoding="utf-8")

        monkeypatch.setattr(gen_module, "SPEC_DIR", spec_dir)
        monkeypatch.setattr(gen_module, "GENERATED_DIR", generated_dir)
        monkeypatch.setattr(gen_module, "CONFIG_PATH", gomplate_config_file)
        monkeypatch.setattr(gen_module, "ROOT_DIR", root_dir)

        with caplog.at_level(logging.ERROR):
            with pytest.raises(SystemExit):
                convert_vspec3_files(gomplate_cmd)

        assert "failed to render template" in caplog.text
        assert "undefined datasource" in caplog.text
        assert "AnotherSpecification" in caplog.text
