import pytest
from particle_picker.parsers.box_parser import BoxFileParser


class TestBoxParser:
    
    def test_parser_initialization(self, sample_box_file):
        parser = BoxFileParser(sample_box_file)
        assert parser.filepath == sample_box_file
        assert parser.data is not None
    
    def test_get_particles(self, sample_box_file):
        parser = BoxFileParser(sample_box_file)
        particles = parser.get_particles()
        
        assert particles is not None
        assert len(particles) == 4
        assert 'x' in particles.columns
        assert 'y' in particles.columns
        assert 'width' in particles.columns
        assert 'height' in particles.columns
    
    def test_get_statistics(self, sample_box_file):
        parser = BoxFileParser(sample_box_file)
        stats = parser.get_statistics()
        
        assert stats['total_particles'] == 4
        assert 'avg_x' in stats
        assert 'avg_y' in stats
        assert 'avg_width' in stats
        assert 'avg_height' in stats
    
    def test_coordinate_values(self, sample_box_file):
        parser = BoxFileParser(sample_box_file)
        particles = parser.get_particles()
        
        assert particles.iloc[0]['x'] == 1234
        assert particles.iloc[0]['y'] == 2345
        assert particles.iloc[0]['width'] == 100
        assert particles.iloc[0]['height'] == 100
    
    def test_nonexistent_file(self, temp_dir):
        nonexistent = temp_dir / "nonexistent.box"
        parser = BoxFileParser(nonexistent)
        assert parser.data is None
    
    def test_empty_file(self, temp_dir):
        empty = temp_dir / "empty.box"
        empty.write_text("")
        
        parser = BoxFileParser(empty)
        assert parser.data is None or len(parser.data) == 0
