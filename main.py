import os
import sys

def main():
    print("Launching Crypto Phase Space HFT Dashboard...")
    os.system(f"{sys.executable} -m streamlit run app.py")

if __name__ == "__main__":
    main()
