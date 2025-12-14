# Driver Monitoring System (DMS)

A multi-phase Driver Monitoring System that processes camera frames to detect driver state (alert, distracted, drowsy) with real-time local inference. This project demonstrates full-stack competence across computer vision, edge AI, IoT, and cloud-native microservices.

## 🎯 Project Overview

The DMS project aims to build a comprehensive system for monitoring driver behavior to prevent accidents caused by drowsiness and distraction. The system is designed with a phased, iterative approach:

- **Phase 1**: Local webcam-based MVP with landmark-based feature detection (EAR, MAR)
- **Phase 2+**: Edge deployment (Jetson/RPi), optimized models (ONNX/TensorRT), telemetry, analytics, and cloud services

## ✨ Features

### Phase 1 (Current)
- Real-time face detection and landmark extraction from webcam
- Eye Aspect Ratio (EAR) computation for drowsiness detection
- Frame-by-frame processing with FPS monitoring
- Modular architecture for easy extension

### Planned Features
- Mouth Aspect Ratio (MAR) for yawning detection
- Head pose estimation (yaw, pitch, roll)
- Temporal decision engine for state classification
- Edge device deployment
- Cloud telemetry and analytics
- Dashboard and fleet management

## 📋 Prerequisites

- Python 3.8 or higher
- Webcam/camera device
- macOS, Linux, or Windows

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/francisco-alonso/DMS.git
   cd DMS
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv .venv
   ```

3. **Activate the virtual environment**
   - On macOS/Linux:
     ```bash
     source .venv/bin/activate
     ```
   - On Windows:
     ```bash
     .venv\Scripts\activate
     ```

4. **Install dependencies**
   
   For production use:
   ```bash
   pip install -r requirements.txt
   ```
   
   For development (includes testing tools):
   ```bash
   pip install -r requirements-dev.txt
   ```
   
   Or install both:
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

## 🏃 Usage

### Running the Basic Webcam Test

From the project root directory:

```bash
python src/main.py
```

This will:
- Open your default webcam (device_index=0)
- Display the video feed with FPS counter
- Press `q` to quit

### Using a Different Camera

If you have multiple cameras, you can modify `device_index` in `src/main.py`:

```python
source = WebcamFrameSource(device_index=1)  # Use second camera
```

## 📁 Project Structure

```
DMS/
├── adrs/                    # Architecture Decision Records
│   ├── ADR-000.md          # Project purpose and scope
│   ├── ADR-001.md          # Landmark extraction framework selection
│   ├── ADR-002.md          # Local vision processing pipeline architecture
│   └── ADR-003.md          # Temporal decision strategy
├── architecture/            # Architecture diagrams and documentation
│   ├── base-architecture.png
│   └── dms_diagram.xml
├── src/                     # Source code
│   ├── framesource/        # Frame source implementations
│   │   └── webcam.py       # Webcam frame source
│   ├── landmark_extractor/ # Landmark extraction implementations
│   │   └── mediapipe_facemesh.py
│   ├── feature_extractor/  # Feature extraction implementations
│   │   └── ear.py          # Eye Aspect Ratio computation
│   └── main.py             # Main entry point
├── tests/                   # Test suite
│   ├── test_framesource/   # Tests for frame sources
│   ├── test_landmark_extractor/  # Tests for landmark extractors
│   └── test_feature_extractor/   # Tests for feature extractors
├── .github/                 # GitHub configuration
│   ├── workflows/          # CI/CD workflows
│   │   └── ci.yml          # Continuous Integration pipeline
│   └── pull_request_template.md
├── Makefile                # Make commands for development
├── run_tests.py            # Python script for running tests (alternative to Makefile)
├── pytest.ini              # Pytest configuration
├── pyproject.toml           # Project configuration (black, ruff, pytest)
├── requirements.txt        # Production Python dependencies
├── requirements-dev.txt    # Development Python dependencies
├── .gitignore             # Git ignore rules
└── README.md              # This file
```

## 🏗️ Architecture

The system follows a modular pipeline architecture (see ADR-002):

1. **FrameSource**: Captures frames from camera
2. **Preprocessor**: Normalizes frames for processing
3. **LandmarkExtractor**: Detects face and extracts landmarks (MediaPipe)
4. **FeatureExtractor**: Converts landmarks to features (EAR, MAR, etc.)
5. **DecisionEngine**: Interprets features over time to determine driver state
6. **EventSink**: Persists or publishes driver-state events

## 📚 Documentation

### Architecture Decision Records (ADRs)

This project uses ADRs to document technical decisions:

- **[ADR-000](adrs/ADR-000.md)**: Project Purpose, Scope, and High-Level Vision
- **[ADR-001](adrs/ADR-001.md)**: Selection of Landmark Extraction Framework (MediaPipe)
- **[ADR-002](adrs/ADR-002.md)**: Architecture of the Local Vision Processing Pipeline
- **[ADR-003](adrs/ADR-003.md)**: Temporal Decision Strategy for Driver State Detection

## 🔧 Development

### Code Style

The project follows Python best practices. Code is automatically formatted with **black** and linted with **ruff**. Please ensure your code:
- Follows PEP 8 style guidelines
- Includes docstrings for functions and classes
- Is properly commented for complex logic

### Running Tests

The project uses **pytest** for testing. Tests are organized in a modular structure mirroring the source code.

#### Using Makefile (Recommended)

```bash
# Run all tests
make test

# Run tests with coverage report
make test-cov

# Format code with black
make format

# Run linter (ruff)
make lint

# Auto-fix linting issues
make lint-fix

# Run format check, lint, and tests (CI check)
make check

# Clean generated files
make clean

# Show all available commands
make help
```

#### Using Python Script (Alternative)

If you don't have `make` installed, you can use the Python script:

```bash
# Run all tests
python run_tests.py test

# Run tests with coverage
python run_tests.py test-cov

# Format code
python run_tests.py format

# Run linter
python run_tests.py lint

# Auto-fix linting issues
python run_tests.py lint-fix

# Run all checks (format check + lint + tests)
python run_tests.py check

# Format, lint-fix, and run tests with coverage
python run_tests.py all
```

#### Test Structure

Tests are organized to mirror the source code structure:
- `tests/test_framesource/` - Tests for frame source implementations
- `tests/test_landmark_extractor/` - Tests for landmark extraction
- `tests/test_feature_extractor/` - Tests for feature extraction

All tests use mocking to avoid requiring hardware (webcam) or external services.

### Continuous Integration

The project uses GitHub Actions for CI/CD. The pipeline automatically:
- Checks code formatting with **black**
- Runs linting with **ruff**
- Executes tests across Python 3.8, 3.9, 3.10, 3.11, and 3.12
- Generates code coverage reports

See [`.github/workflows/ci.yml`](.github/workflows/ci.yml) for details.

### Contributing

1. Create a feature branch from `main`
2. Make your changes
3. Run `make check` or `python run_tests.py check` to ensure:
   - Code is properly formatted
   - No linting errors
   - All tests pass
4. Submit a pull request using the provided template

See [`.github/pull_request_template.md`](.github/pull_request_template.md) for PR guidelines.

## 📊 Monitoring & Metrics

The system tracks:
- Frame processing rate (FPS)
- Detection latency (ms per frame)
- False positive / false negative rates
- Event throughput (for future telemetry)

## 🗺️ Roadmap

### Phase 1 (Current)
- [x] Basic webcam frame capture
- [x] Architecture design and documentation
- [x] MediaPipe integration
- [x] EAR feature extraction
- [x] Test framework and CI/CD pipeline
- [ ] MAR feature extraction
- [ ] Temporal decision engine
- [ ] Logging and metrics collection

### Phase 2 (Planned)
- [ ] Edge device deployment (Jetson/RPi)
- [ ] Model optimization (ONNX/TensorRT)
- [ ] Cloud telemetry integration
- [ ] Time-series analytics

### Phase 3+ (Future)
- [ ] Dashboard and visualization
- [ ] Fleet management
- [ ] MLOps pipeline
- [ ] Custom model training

## 🔍 Troubleshooting

### Common Issues

#### "Works on my machine" Problems

If you encounter issues when pulling code from another developer:

1. **Check Python version**
   - Required: Python 3.8-3.12
   - Check with: `python --version`
   - If wrong version, use `pyenv` or update Python

2. **Reinstall dependencies**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

3. **OpenCV installation issues**
   - **Linux**: May need system packages: `sudo apt-get install libopencv-dev python3-opencv`
   - **macOS**: Usually works with `pip install opencv-contrib-python`
   - **Windows**: May need Visual C++ redistributables
   - If `opencv-contrib-python` fails, try `opencv-python` (some features may be limited)

4. **MediaPipe installation issues**
   - **Windows**: May require additional setup
   - **ARM systems** (Raspberry Pi, Apple Silicon): May need to build from source
   - Check MediaPipe [installation guide](https://google.github.io/mediapipe/getting_started/install.html)

5. **Webcam not detected**
   - Check permissions (macOS: System Preferences → Security & Privacy)
   - Try different `device_index` values (0, 1, 2...)
   - On Linux, check: `ls /dev/video*`
   - Tests don't require webcam (they use mocks)

6. **Import errors**
   - Ensure you're in the project root directory
   - Verify virtual environment is activated
   - Check that `src/` directory has `__init__.py` files

7. **Test failures**
   - Run `make clean` to remove cached files
   - Ensure all dependencies are installed: `pip install -r requirements-dev.txt`
   - Check Python version compatibility

#### Platform-Specific Notes

- **macOS**: Generally works well. May need to grant camera permissions.
- **Linux**: May require system packages for OpenCV. Check distribution-specific guides.
- **Windows**: May need Visual C++ redistributables. Use PowerShell or Git Bash.

#### Getting Help

1. Check that your Python version matches: `python --version`
2. Verify all dependencies: `pip list`
3. Check GitHub Issues for similar problems

## ⚠️ Important Notes

- This is a **learning and portfolio project**, not a certified automotive product
- Phase 1 is hardware-free and designed for development
- Personal data collection and privacy are important considerations
- Full vehicle integration is not planned until basic detection is validated
- **For development**: Always use a virtual environment to avoid dependency conflicts

## 📝 License

(To be determined)

## 👤 Author

**Francisco Lopez**

## 🙏 Acknowledgments

- MediaPipe team for the excellent landmark detection framework
- OpenCV community for computer vision tools

---

For detailed technical decisions, please refer to the [ADRs directory](adrs/).

