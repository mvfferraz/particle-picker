import pytest
from particle_picker.parsers.star_parser import StarFileParser


class TestStarParser:
    
    def test_parser_initialization(self, sample_star_file):
        parser = StarFileParser(sample_star_file)
        assert parser.filepath == sample_star_file
        assert parser.particles_data is not None
        assert parser.optics_data is not None
    
    def test_get_particles(self, sample_star_file):
        parser = StarFileParser(sample_star_file)
        particles = parser.get_particles()
        
        assert particles is not None
        assert len(particles) == 4
        assert 'CoordinateX' in particles.columns
        assert 'CoordinateY' in particles.columns
        assert 'MicrographName' in particles.columns
    
    def test_get_optics(self, sample_star_file):
        parser = StarFileParser(sample_star_file)
        optics = parser.get_optics()
        
        assert optics is not None
        assert len(optics) == 1
        assert 'Voltage' in optics.columns
    
    def test_get_micrograph_names(self, sample_star_file):
        parser = StarFileParser(sample_star_file)
        micrograph_names = parser.get_micrograph_names()
        
        assert len(micrograph_names) == 2
        assert 'micrograph_001.mrc' in micrograph_names
        assert 'micrograph_002.mrc' in micrograph_names
    
    def test_get_particles_per_micrograph(self, sample_star_file):
        parser = StarFileParser(sample_star_file)
        counts = parser.get_particles_per_micrograph()
        
        assert counts['micrograph_001.mrc'] == 2
        assert counts['micrograph_002.mrc'] == 2
    
    def test_get_statistics(self, sample_star_file):
        parser = StarFileParser(sample_star_file)
        stats = parser.get_statistics()
        
        assert stats['total_particles'] == 4
        assert stats['unique_micrographs'] == 2
        assert stats['avg_particles_per_micrograph'] == 2.0
        assert stats['min_particles_per_micrograph'] == 2
        assert stats['max_particles_per_micrograph'] == 2
    
    def test_nonexistent_file(self, temp_dir):
        nonexistent = temp_dir / "nonexistent.star"
        with pytest.raises(FileNotFoundError):
            StarFileParser(nonexistent)
    
    def test_empty_file(self, temp_dir):
        empty_file = temp_dir / "empty.star"
        empty_file.write_text("")
        
        parser = StarFileParser(empty_file)
        assert parser.particles_data is None
        assert parser.optics_data is None
