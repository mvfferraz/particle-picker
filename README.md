# Particle Picker Statistics Dashboard

Dashboard and CLI for analyzing cryo-EM particle picking results.

**Author:** Matheus Ferraz | **License:** MIT

## Features

- Web dashboard (interactive) and CLI
- Support: `.star`, `.csv`, `.box` files
- Statistics, visualizations, and quality metrics

## Installation
```bash
./setup.sh
source venv/bin/activate
```

## Usage

**Dashboard:**
```bash
make run-dashboard  # Access at http://localhost:8050
```

**CLI:**
```bash
make analyze FILE=data/particles.star TYPE=star
make compare FILES='file1.star file2.star' TYPE=star
```

See `CLI.md` for complete documentation.

## Development
```bash
make install-dev  # Install with dev dependencies
make test         # Run tests
make lint         # Check code quality
make format       # Format code
```

## Project Structure
```
particle_picker/
├── parsers/      # File parsers
├── analysis/     # Statistics
├── visualization/# Plots
├── dashboard/    # Web app
└── cli/          # Command line
```

## Contributing

1. Fork repository
2. Create feature branch
3. Add tests
4. Submit pull request

## Support

Open an issue on the repository for questions or problems.
