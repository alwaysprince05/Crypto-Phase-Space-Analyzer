## Creator/Dev: Prince Maurya

# Crypto Phase Space

## What is this project about?
Crypto Phase Space is a Python project that visualizes the dynamics of the cryptocurrency market (BTC) in a 3D animated phase space. It downloads historical BTC price data, computes log returns, velocity, and acceleration, and displays the market's trajectory in a visually engaging animated 3D plot.

### Features
- Downloads BTC historical price data using yfinance
- Computes log returns, velocity, and acceleration
- Visualizes the market trajectory in phase space (returns, velocity, acceleration)
- Animated 3D plot with smooth trajectory and rotating camera

### Getting Started
1. Clone the repository to your local machine:
   ```bash
   git clone https://github.com/princemaurya/Crypto-Phase-Space-Analyzer.git
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the visualization:
   ```bash
   python main.py
   ```

### Project Structure
- `main.py`: Entry point, runs the visualization
- `data_loader.py`: Downloads and processes BTC price data
- `state_space.py`: Computes phase space coordinates
- `phase_visualizer.py`: Handles 3D animation and plotting
- `requirements.txt`: Python dependencies
- `README.md`: Project documentation
