from data_loader import download_btc_data, get_close_prices
from state_space import compute_phase_space
from phase_visualizer import PhaseVisualizer


def main():
    print("Downloading BTC price data...")
    df = download_btc_data()
    prices = get_close_prices(df)
    print("Computing phase space coordinates...")
    log_returns, velocity, acceleration = compute_phase_space(prices)
    print("Launching 3D phase space animation...")
    visualizer = PhaseVisualizer(log_returns, velocity, acceleration)
    visualizer.animate()

if __name__ == "__main__":
    main()
