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
   ```bash
   pip install -r requirements.txt
   ```

   Note: MediaPipe will be added to requirements in a future update (see ADR-001).

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
├── ADRs/                    # Architecture Decision Records
│   ├── ADR-000.md          # Project purpose and scope
│   ├── ADR-001.md          # Landmark extraction framework selection
│   ├── ADR-002.md          # Local vision processing pipeline architecture
│   └── ADR-003.md          # Temporal decision strategy
├── Architecture/            # Architecture diagrams and documentation
│   ├── base-architecture.png
│   └── dms_diagram.xml
├── src/                     # Source code
│   ├── framesource/        # Frame source implementations
│   │   └── webcam.py       # Webcam frame source
│   └── main.py             # Main entry point
├── .github/                 # GitHub templates
│   └── pull_request_template.md
├── requirements.txt         # Python dependencies
├── .gitignore              # Git ignore rules
└── README.md               # This file
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

- **[ADR-000](ADRs/ADR-000.md)**: Project Purpose, Scope, and High-Level Vision
- **[ADR-001](ADRs/ADR-001.md)**: Selection of Landmark Extraction Framework (MediaPipe)
- **[ADR-002](ADRs/ADR-002.md)**: Architecture of the Local Vision Processing Pipeline
- **[ADR-003](ADRs/ADR-003.md)**: Temporal Decision Strategy for Driver State Detection

## 🔧 Development

### Code Style

The project follows Python best practices. Please ensure your code:
- Follows PEP 8 style guidelines
- Includes docstrings for functions and classes
- Is properly commented for complex logic

### Running Tests

(Test framework to be added in future updates)

### Contributing

1. Create a feature branch from `main`
2. Make your changes
3. Ensure all tests pass
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
- [ ] MediaPipe integration
- [ ] EAR/MAR feature extraction
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

## ⚠️ Important Notes

- This is a **learning and portfolio project**, not a certified automotive product
- Phase 1 is hardware-free and designed for development
- Personal data collection and privacy are important considerations
- Full vehicle integration is not planned until basic detection is validated

## 📝 License

(To be determined)

## 👤 Author

**Francisco Lopez**

## 🙏 Acknowledgments

- MediaPipe team for the excellent landmark detection framework
- OpenCV community for computer vision tools

---

For detailed technical decisions, please refer to the [ADRs directory](ADRs/).

