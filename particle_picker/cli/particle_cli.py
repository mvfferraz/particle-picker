import argparse
import sys
from pathlib import Path
import json

from particle_picker.parsers.star_parser import StarFileParser
from particle_picker.parsers.csv_parser import CSVParticleParser
from particle_picker.parsers.box_parser import BoxFileParser
from particle_picker.analysis.statistics import ParticleStatistics

def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Particle Picker Statistics CLI - Analyze cryo-EM particle picking results',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  %(prog)s analyze -i data/particles.star -t star
  %(prog)s analyze -i data/particles.csv -t csv --output stats.json
  %(prog)s analyze -i data/particles.star -t star --verbose
  %(prog)s compare -i file1.star file2.star -t star
        '''
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    analyze_parser = subparsers.add_parser('analyze', help='Analyze a single particle picking file')
    analyze_parser.add_argument('-i', '--input', required=True, help='Input file path')
    analyze_parser.add_argument('-t', '--type', required=True, choices=['star', 'csv', 'box'], 
                               help='File type')
    analyze_parser.add_argument('-o', '--output', help='Output file for statistics (JSON format)')
    analyze_parser.add_argument('-v', '--verbose', action='store_true', 
                               help='Show detailed statistics')
    
    compare_parser = subparsers.add_parser('compare', help='Compare multiple particle picking files')
    compare_parser.add_argument('-i', '--input', nargs='+', required=True, 
                               help='Input file paths')
    compare_parser.add_argument('-t', '--type', required=True, choices=['star', 'csv', 'box'], 
                               help='File type')
    compare_parser.add_argument('-o', '--output', help='Output file for comparison (JSON format)')
    
    list_parser = subparsers.add_parser('list', help='List micrographs and particle counts')
    list_parser.add_argument('-i', '--input', required=True, help='Input file path')
    list_parser.add_argument('-t', '--type', required=True, choices=['star', 'csv', 'box'], 
                            help='File type')
    list_parser.add_argument('-s', '--sort', choices=['name', 'count'], default='count',
                            help='Sort by name or particle count')
    list_parser.add_argument('--reverse', action='store_true', help='Reverse sort order')
    
    export_parser = subparsers.add_parser('export', help='Export data to different formats')
    export_parser.add_argument('-i', '--input', required=True, help='Input file path')
    export_parser.add_argument('-t', '--type', required=True, choices=['star', 'csv', 'box'], 
                              help='Input file type')
    export_parser.add_argument('-o', '--output', required=True, help='Output file path')
    export_parser.add_argument('-f', '--format', choices=['csv', 'json'], default='csv',
                              help='Output format')
    
    return parser

def load_file(filepath, file_type):
    filepath = Path(filepath)
    
    if not filepath.exists():
        print(f"Error: File not found: {filepath}")
        sys.exit(1)
    
    try:
        if file_type == 'star':
            parser = StarFileParser(filepath)
            return parser.get_particles()
        elif file_type == 'csv':
            parser = CSVParticleParser(filepath)
            return parser.get_particles()
        elif file_type == 'box':
            parser = BoxFileParser(filepath)
            return parser.get_particles()
    except Exception as e:
        print(f"Error loading file: {e}")
        sys.exit(1)

def command_analyze(args):
    print(f"\nAnalyzing: {args.input}")
    print(f"File type: {args.type}")
    print("-" * 60)
    
    df = load_file(args.input, args.type)
    
    if df is None or df.empty:
        print("Error: No particle data found in file")
        sys.exit(1)
    
    stats = ParticleStatistics(df)
    summary = stats.get_summary_statistics()
    
    print(f"\nSummary Statistics:")
    print(f"  Total particles: {summary['total_particles']:,}")
    print(f"  Total micrographs: {summary['total_micrographs']:,}")
    
    if summary['total_micrographs'] > 0:
        print(f"  Average particles per micrograph: {summary['avg_particles_per_micrograph']:.2f}")
        print(f"  Min particles per micrograph: {summary['min_particles_per_micrograph']}")
        print(f"  Max particles per micrograph: {summary['max_particles_per_micrograph']}")
        print(f"  Std deviation: {summary['std_particles_per_micrograph']:.2f}")
    
    if args.verbose:
        print(f"\nCoordinate Statistics:")
        coord_stats = stats.get_coordinate_statistics()
        for coord, values in coord_stats.items():
            print(f"  {coord}:")
            print(f"    Mean: {values['mean']:.2f}")
            print(f"    Std: {values['std']:.2f}")
            print(f"    Min: {values['min']:.2f}")
            print(f"    Max: {values['max']:.2f}")
        
        defocus_stats = stats.get_defocus_statistics()
        if defocus_stats:
            print(f"\nDefocus Statistics:")
            for defocus, values in defocus_stats.items():
                print(f"  {defocus}:")
                print(f"    Mean: {values['mean']:.2f}")
                print(f"    Std: {values['std']:.2f}")
                print(f"    Min: {values['min']:.2f}")
                print(f"    Max: {values['max']:.2f}")
    
    if args.output:
        output_data = {
            'file': str(args.input),
            'summary': summary,
        }
        
        if args.verbose:
            output_data['coordinate_stats'] = stats.get_coordinate_statistics()
            output_data['defocus_stats'] = stats.get_defocus_statistics()
        
        with open(args.output, 'w') as f:
            json.dump(output_data, f, indent=2)
        
        print(f"\nStatistics saved to: {args.output}")

def command_compare(args):
    print(f"\nComparing {len(args.input)} files:")
    print("-" * 60)
    
    results = []
    
    for filepath in args.input:
        print(f"\nProcessing: {filepath}")
        df = load_file(filepath, args.type)
        
        if df is None or df.empty:
            print(f"  Warning: No data found in {filepath}")
            continue
        
        stats = ParticleStatistics(df)
        summary = stats.get_summary_statistics()
        summary['file'] = str(filepath)
        results.append(summary)
        
        print(f"  Particles: {summary['total_particles']:,}")
        print(f"  Micrographs: {summary['total_micrographs']:,}")
        print(f"  Avg per micrograph: {summary['avg_particles_per_micrograph']:.2f}")
    
    print("\n" + "=" * 60)
    print("Comparison Summary:")
    print("=" * 60)
    
    for i, result in enumerate(results, 1):
        print(f"\n{i}. {Path(result['file']).name}")
        print(f"   Particles: {result['total_particles']:,}")
        print(f"   Micrographs: {result['total_micrographs']:,}")
        print(f"   Avg: {result['avg_particles_per_micrograph']:.2f}")
    
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\nComparison saved to: {args.output}")

def command_list(args):
    print(f"\nListing micrographs from: {args.input}")
    print("-" * 60)
    
    df = load_file(args.input, args.type)
    
    if df is None or df.empty:
        print("Error: No particle data found in file")
        sys.exit(1)
    
    stats = ParticleStatistics(df)
    distribution = stats.get_distribution_per_micrograph()
    
    if distribution.empty:
        print("No micrograph information found in file")
        sys.exit(1)
    
    if args.sort == 'name':
        distribution = distribution.sort_index(ascending=not args.reverse)
    else:
        distribution = distribution.sort_values(ascending=not args.reverse)
    
    print(f"\nTotal micrographs: {len(distribution)}")
    print(f"Total particles: {distribution.sum():,}\n")
    
    print(f"{'Micrograph':<50} {'Particles':>10}")
    print("-" * 62)
    
    for micrograph, count in distribution.items():
        micrograph_name = Path(micrograph).name if '/' in micrograph or '\\' in micrograph else micrograph
        print(f"{micrograph_name:<50} {count:>10,}")

def command_export(args):
    print(f"\nExporting: {args.input}")
    print(f"Output format: {args.format}")
    print(f"Output file: {args.output}")
    print("-" * 60)
    
    df = load_file(args.input, args.type)
    
    if df is None or df.empty:
        print("Error: No particle data found in file")
        sys.exit(1)
    
    output_path = Path(args.output)
    
    try:
        if args.format == 'csv':
            df.to_csv(output_path, index=False)
            print(f"\nSuccessfully exported {len(df):,} particles to CSV")
        
        elif args.format == 'json':
            df.to_json(output_path, orient='records', indent=2)
            print(f"\nSuccessfully exported {len(df):,} particles to JSON")
        
        print(f"Output saved to: {output_path}")
        
    except Exception as e:
        print(f"Error exporting data: {e}")
        sys.exit(1)

def main():
    parser = parse_arguments()
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    if args.command == 'analyze':
        command_analyze(args)
    elif args.command == 'compare':
        command_compare(args)
    elif args.command == 'list':
        command_list(args)
    elif args.command == 'export':
        command_export(args)

if __name__ == '__main__':
    main()
