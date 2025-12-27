import pytest
import pandas as pd
from particle_picker.analysis.statistics import ParticleStatistics


class TestParticleStatistics:
    
    @pytest.fixture
    def sample_dataframe(self):
        return pd.DataFrame({
            'CoordinateX': [1234.5, 1456.7, 2000.0, 2500.0],
            'CoordinateY': [2345.6, 3456.8, 3000.0, 3500.0],
            'MicrographName': ['mic1.mrc', 'mic1.mrc', 'mic2.mrc', 'mic2.mrc'],
            'DefocusU': [28000.0, 28000.0, 29000.0, 29000.0],
            'DefocusV': [27500.0, 27500.0, 28500.0, 28500.0]
        })
    
    def test_initialization(self, sample_dataframe):
        stats = ParticleStatistics(sample_dataframe)
        assert stats.df is not None
        assert stats.micrograph_col == 'MicrographName'
    
    def test_get_distribution_per_micrograph(self, sample_dataframe):
        stats = ParticleStatistics(sample_dataframe)
        distribution = stats.get_distribution_per_micrograph()
        
        assert len(distribution) == 2
        assert distribution['mic1.mrc'] == 2
        assert distribution['mic2.mrc'] == 2
    
    def test_get_coordinate_statistics(self, sample_dataframe):
        stats = ParticleStatistics(sample_dataframe)
        coord_stats = stats.get_coordinate_statistics()
        
        assert 'CoordinateX' in coord_stats
        assert 'CoordinateY' in coord_stats
        assert 'mean' in coord_stats['CoordinateX']
        assert 'std' in coord_stats['CoordinateX']
        assert 'min' in coord_stats['CoordinateX']
        assert 'max' in coord_stats['CoordinateX']
    
    def test_get_defocus_statistics(self, sample_dataframe):
        stats = ParticleStatistics(sample_dataframe)
        defocus_stats = stats.get_defocus_statistics()
        
        assert 'DefocusU' in defocus_stats
        assert 'DefocusV' in defocus_stats
        assert 'mean' in defocus_stats['DefocusU']
    
    def test_get_summary_statistics(self, sample_dataframe):
        stats = ParticleStatistics(sample_dataframe)
        summary = stats.get_summary_statistics()
        
        assert summary['total_particles'] == 4
        assert summary['total_micrographs'] == 2
        assert summary['avg_particles_per_micrograph'] == 2.0
        assert summary['min_particles_per_micrograph'] == 2
        assert summary['max_particles_per_micrograph'] == 2
    
    def test_get_heatmap_data(self, sample_dataframe):
        stats = ParticleStatistics(sample_dataframe)
        heatmap_data = stats.get_heatmap_data(bin_size=500)
        
        assert heatmap_data is not None
        assert 'histogram' in heatmap_data
        assert 'x_edges' in heatmap_data
        assert 'y_edges' in heatmap_data
    
    def test_empty_dataframe(self):
        empty_df = pd.DataFrame()
        stats = ParticleStatistics(empty_df)
        summary = stats.get_summary_statistics()
        
        assert summary['total_particles'] == 0
