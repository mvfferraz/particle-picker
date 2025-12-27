import pytest
from pathlib import Path
from particle_picker.parsers.star_parser import StarFileParser
from particle_picker.analysis.statistics import ParticleStatistics


class TestCompleteWorkflow:
    
    def test_star_to_statistics_workflow(self, sample_star_file):
        parser = StarFileParser(sample_star_file)
        particles = parser.get_particles()
        
        assert particles is not None
        
        stats = ParticleStatistics(particles)
        summary = stats.get_summary_statistics()
        
        assert summary['total_particles'] == 4
        assert summary['total_micrographs'] == 2
        
        distribution = stats.get_distribution_per_micrograph()
        assert len(distribution) == 2
    
    def test_multiple_parsers_same_data(self, sample_star_file, sample_csv_file):
        star_parser = StarFileParser(sample_star_file)
        csv_parser = CSVParticleParser(sample_csv_file)
        
        star_particles = star_parser.get_particles()
        csv_particles = csv_parser.get_particles()
        
        star_stats = ParticleStatistics(star_particles)
        csv_stats = ParticleStatistics(csv_particles)
        
        star_summary = star_stats.get_summary_statistics()
        csv_summary = csv_stats.get_summary_statistics()
        
        assert star_summary['total_particles'] == csv_summary['total_particles']


from particle_picker.parsers.csv_parser import CSVParticleParser
