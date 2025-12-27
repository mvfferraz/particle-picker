import pytest
from pathlib import Path
import tempfile
import shutil


@pytest.fixture
def temp_dir():
    temp_path = Path(tempfile.mkdtemp())
    yield temp_path
    shutil.rmtree(temp_path)


@pytest.fixture
def sample_star_content():
    return """
data_optics

loop_
_rlnVoltage #1 
_rlnImagePixelSize #2 
_rlnSphericalAberration #3 
_rlnAmplitudeContrast #4 
_rlnOpticsGroup #5 
_rlnImageSize #6 
_rlnImageDimensionality #7 
_rlnOpticsGroupName #8 
300.000000 1.770000 2.700000 0.100000 1 360 2 opticsGroup1

data_particles

loop_
_rlnCoordinateX #1 
_rlnCoordinateY #2 
_rlnMicrographName #3 
_rlnDefocusU #4 
_rlnDefocusV #5 
1234.5 2345.6 micrograph_001.mrc 28000.0 27500.0
1456.7 3456.8 micrograph_001.mrc 28000.0 27500.0
2000.0 3000.0 micrograph_002.mrc 29000.0 28500.0
2500.0 3500.0 micrograph_002.mrc 29000.0 28500.0
"""


@pytest.fixture
def sample_csv_content():
    return """CoordinateX,CoordinateY,MicrographName
1234.5,2345.6,micrograph_001.mrc
1456.7,3456.8,micrograph_001.mrc
2000.0,3000.0,micrograph_002.mrc
2500.0,3500.0,micrograph_002.mrc
"""


@pytest.fixture
def sample_box_content():
    return """1234 2345 100 100
1456 3456 100 100
2000 3000 100 100
2500 3500 100 100
"""


@pytest.fixture
def sample_star_file(temp_dir, sample_star_content):
    star_file = temp_dir / "test.star"
    star_file.write_text(sample_star_content)
    return star_file


@pytest.fixture
def sample_csv_file(temp_dir, sample_csv_content):
    csv_file = temp_dir / "test.csv"
    csv_file.write_text(sample_csv_content)
    return csv_file


@pytest.fixture
def sample_box_file(temp_dir, sample_box_content):
    box_file = temp_dir / "test.box"
    box_file.write_text(sample_box_content)
    return box_file
