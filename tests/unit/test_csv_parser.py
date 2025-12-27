import pytest
from particle_picker.parsers.csv_parser import CSVParticleParser


class TestCSVParser:
    
    def test_parser_initialization(self, sample_csv_file):
        parser = CSVParticleParser(sample_csv_file)
        assert parser.filepath == sample_csv_file
        assert parser.data is not None
    
    def test_get_particles(self, sample_csv_file):
        parser = CSVParticleParser(sample_csv_file)
        particles = parser.get_particles()
        
        assert particles is not None
        assert len(particles) == 4
        assert 'CoordinateX' in particles.columns
        assert 'CoordinateY' in particles.columns
        assert 'MicrographName' in particles.columns
    
    def test_get_micrograph_names(self, sample_csv_file):
        parser = CSVParticleParser(sample_csv_file)
        micrograph_names = parser.get_micrograph_names()
        
        assert len(micrograph_names) == 2
    
    def test_get_particles_per_micrograph(self, sample_csv_file):
        parser = CSVParticleParser(sample_csv_file)
        counts = parser.get_particles_per_micrograph()
        
        assert counts['micrograph_001.mrc'] == 2
        assert counts['micrograph_002.mrc'] == 2
    
    def test_get_statistics(self, sample_csv_file):
        parser = CSVParticleParser(sample_csv_file)
        stats = parser.get_statistics()
        
        assert stats['total_particles'] == 4
        assert 'columns' in stats
        assert 'CoordinateX_mean' in stats
        assert 'CoordinateY_mean' in stats
    
    def test_nonexistent_file(self, temp_dir):
        nonexistent = temp_dir / "nonexistent.csv"
        parser = CSVParticleParser(nonexistent)
        assert parser.data is None
    
    def test_malformed_csv(self, temp_dir):
        malformed = temp_dir / "malformed.csv"
        malformed.write_text("not,a,valid\ncsv,file")
        
        parser = CSVParticleParser(malformed)
        assert parser.data is not None
