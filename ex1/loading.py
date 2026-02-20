import sys
import importlib
from types import ModuleType

# # Imports to get autocomplete while writing the code
# import numpy as np
# import matplotlib.pyplot as plt
# import pandas as pd


def import_module(module_name: str) -> list[ModuleType, list[str]]:
    """Helper to import a module and return its object + status."""
    try:
        mod = importlib.import_module(module_name)
        return mod, ["[OK]", "ready", getattr(mod, "__version__", "unknown")]
    except ImportError:
        return None, ["[MISSING]", "not installed", "N/A"]


def main() -> None:
    print("\nLOADING STATUS: Loading programs...\n")

    print("Checking dependencies:")
    pd, pd_status = import_module("pandas")
    _, mp_status = import_module("matplotlib")
    plt, plt_status = import_module("matplotlib.pyplot")
    np, np_status = import_module("numpy")

    modules_info = [
        (pd_status, "pandas", "Data manipulation"),
        (mp_status, "matplotlib", "Visualization_version"),
        (plt_status, "matplotlib.pyplot", "Visualization"),
        (np_status, "numpy", "Numerical computations"),
    ]

    # No version for pyplot so I get the one from matplotlib
    plt_status[2] = mp_status[2]

    missing_modules = []

    for status, name, desc in modules_info:
        print(f"{status[0]} {name} ({status[2]}) - {desc} {status[1]}")
        if status[0] == "[MISSING]":
            missing_modules.append(name)

    if missing_modules:
        print("\nERROR: Missing dependencies: "
              f"{', '.join(missing_modules)}")
        print("Use poetry install or pip install -r requirements.txt")
        print("Exciting program...")
        sys.exit(1)

    print("\nAnalyzing Matrix films...")

    data = [{
        "title": "The Matrix",
        "year": 1999,
        "rating": 8.7
    }, {
        "title": "The Matrix Reloaded",
        "year": 2003,
        "rating": 7.2
    }, {
        "title": "The Matrix Revolutions",
        "year": 2003,
        "rating": 6.8
    }, {
        "title": "The Matrix Resurrections",
        "year": 2021,
        "rating": 5.7
    }]

    df = pd.DataFrame(data)
    print(df)

    print("\nAnalysis complete!")

    years = df["year"]
    ratings = df["rating"]

    # Create figure (larger than default)
    plt.figure(figsize=(10, 6))

    # Plot the main line with markers
    plt.plot(years,
             ratings,
             marker='o',
             linestyle='-',
             color='b',
             label='Movie Ratings')

    # Trend Line using numpy from :
    # https://www.geeksforgeeks.org/data-visualization/drawing-scatter-trend-lines-using-matplotlib/
    slope, intercept = np.polyfit(x=years, y=ratings, deg=1)
    trend_poly = np.poly1d([slope, intercept])

    # Plot the trend line
    plt.plot(
        years,  # x
        trend_poly(years),  # y
        color='red',
        linestyle='--',
        linewidth=2,
        label='Trend Line')

    # Add labels for specific movies from:
    # https://www.geeksforgeeks.org/python/matplotlib-pyplot-annotate-in-python/
    for i, txt in enumerate(df["title"]):
        plt.annotate(text=txt,
                     xy=(years[i], ratings[i]),
                     xytext=(5, 5),
                     textcoords='offset points',
                     fontsize=8)

    # Display labels
    plt.xlabel("Year")
    plt.ylabel("IMDb Rating")
    plt.title("Matrix Saga Ratings Over Time")

    # Display a gray grid
    plt.grid(True, linestyle='--', alpha=0.7)

    # Display the legend of the slopes top right
    plt.legend()

    # Save fig into a png
    save_path = "matrix_analysis.png"
    plt.savefig(save_path)
    print(f"Results saved to: {save_path}\n")

    plt.show()

    # Raindrop animation:
    # from https://matplotlib.org/stable/gallery/animation/rain.html


if __name__ == "__main__":
    main()
