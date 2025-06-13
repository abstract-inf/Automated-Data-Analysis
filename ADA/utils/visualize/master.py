import os
import pandas as pd
from pathlib import Path
import json
import matplotlib.pyplot as plt
import sys
from importlib import import_module

current_dir = Path(__file__).parent
data_path = current_dir.parent.parent / "saved_data"
dataset_path = current_dir.parent.parent / "datasets"
vc_path = current_dir / "visualize_categorical_data.py"

def ensure_directory(path: Path) -> Path:
    """Ensure the directory exists, create if it doesn't. Returns the path."""
    try:
        path.mkdir(parents=True, exist_ok=True)
        return path
    except Exception as e:
        print(f"Error creating directory {path}: {str(e)}")
        sys.exit(1)

def load_data(file_path) -> pd.DataFrame:
    """Load data from CSV file with validation."""
    file_path = Path(file_path)
    try:
        if not file_path.exists():
            raise FileNotFoundError(f"Data file not found: {file_path}")
        return pd.read_csv(file_path)
    except Exception as e:
        print(f"Error loading data: {str(e)}")
        sys.exit(1)

def load_json(file_path: Path) -> dict:
    """Load JSON file with validation."""
    try:
        if not file_path.exists():
            raise FileNotFoundError(f"JSON file not found: {file_path}")
        with open(file_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading JSON: {str(e)}")
        sys.exit(1)

def import_categorical_visualization_functions():
    """Dynamically import visualization functions."""
    try:
        spec = import_module("ADA.utils.visualize.visualize_categorical_data")
        return {
            'plot_dist': spec.plot_categorical_distribution,
            'plot_pie': spec.plot_categorical_piechart,
            'plot_stacked': spec.stacked_bar_plot,
            'plot_sankey': spec.plot_sankey_diagram
        }
    except Exception as e:
        print(f"Error importing visualization functions: {str(e)}")
        sys.exit(1)

def visualize_categorical_data(
    data_file: Path,
    columns_categories_file: Path,
    selected_features_file: Path,
    save_path: Path = None,
    target_col = None
) -> None:
    """Main visualization function with enhanced error handling."""
    # Initialize paths
    save_path = save_path or data_path / "visualizations/Categorical"
    ensure_directory(save_path)
    
    # Load data and configs
    data = load_data(data_file)
    columns_categories = load_json(columns_categories_file)
    selected_features = load_json(selected_features_file)
    
    # Get visualization functions
    viz = import_categorical_visualization_functions()
    
    # Process categorical columns
    cat_columns = (
        columns_categories.get('nominal', []) + 
        columns_categories.get('ordinal', [])
    )
    
    # Create individual visualizations
    for column in cat_columns:
        if column in data.columns and column in selected_features:
            print(f"Visualizing {column}...")
            
            # Bar chart
            bar_path = ensure_directory(save_path / "Bar Charts")
            fig, _ = viz['plot_dist'](data, column)
            fig.savefig(bar_path / f"{column}_bar.png", bbox_inches='tight')
            plt.close(fig)
            
            # Pie chart
            pie_path = ensure_directory(save_path / "Pie Charts")
            fig, _ = viz['plot_pie'](data, column)
            fig.savefig(pie_path / f"{column}_pie.png", bbox_inches='tight')
            plt.close(fig)
    
    # Create multi-variable visualizations
    if len(cat_columns) >= 2:
        # Stacked bar plots
        stacked_path = ensure_directory(save_path / "Stacked Bar Charts")
        for col1 in range(len(cat_columns)):
            for col2 in range(len(cat_columns)):
                if col1 == col2:
                    continue
                try:
                    fig, _ = viz['plot_stacked'](data, cat_columns[col1], cat_columns[col2])
                    fig.savefig(
                        stacked_path / f"stacked_{cat_columns[col1]}_vs_{cat_columns[col2]}.png",
                        bbox_inches='tight'
                    )
                    plt.close(fig)
                except Exception as e:
                    print(f"Error creating stacked plot for {cat_columns[col1]} vs {cat_columns[col2]}: {str(e)}")
        
        # Sankey diagram
        sankey_path = ensure_directory(save_path / "Sankey Diagrams")
        try:
            fig,_ = viz['plot_sankey'](data, cat_columns)
            fig.write_image(
                sankey_path / "sankey_diagram.png",
                engine="kaleido",
                scale=2
            )
        except Exception as e:
            print(f"Error creating Sankey diagram: {str(e)}")
vn_path = current_dir / "visualize_numerical_data.py"

def import_numerical_visualization_functions():
    """Dynamically import numerical visualization functions."""
    try:
        spec = import_module("ADA.utils.visualize.visualize_numerical_data")
        return {
            'plot_distribution': spec.plot_numerical_distribution,
            'plot_boxplot': spec.plot_numerical_boxplot,
            'plot_scatter': spec.plot_numerical_scatter
        }
    except Exception as e:
        print(f"Error importing numerical visualization functions: {str(e)}")
        sys.exit(1)
def visulize_numerical_data(
    data_file: Path,
    columns_categories_file: Path,
    selected_features_file: Path,
    save_path: Path = None,
    target_col = None
) -> None:
    save_path = save_path or data_path / "visualizations/Numerical"
    ensure_directory(save_path)
    
    # Load data and configs
    data = load_data(data_file)
    columns_categories = load_json(columns_categories_file)
    selected_features = load_json(selected_features_file)

    # Get visualization functions
    viz = import_numerical_visualization_functions()
    # Process numerical columns
    num_columns = (
        columns_categories.get('continuous', []) +
        columns_categories.get('discrete', [])
    )
    # Create individual visualizations
    for column in num_columns:
        if column in data.columns and column in selected_features:
            print(f"Visualizing {column}...")

            # Distribution plot
            dist_path = ensure_directory(save_path / "Numerical Distribution")
            fig, _ = viz['plot_distribution'](data, column)
            fig.savefig(dist_path / f"{column}_distribution.png", bbox_inches='tight')
            plt.close(fig)

            # Boxplot
            boxplot_path = ensure_directory(save_path / "Box Plots")
            fig, _ = viz['plot_boxplot'](data, column)
            fig.savefig(boxplot_path / f"{column}_boxplot.png", bbox_inches='tight')
            plt.close(fig)
            # Scatter plot (if applicable)
            if len(num_columns) > 1:
                scatter_path = ensure_directory(save_path / "Scatter Plots")
                for other_column in num_columns:
                    if other_column != column:
                        try:
                            fig, _ = viz['plot_scatter'](data, column, other_column,  target_col) 
                            fig.savefig(
                                scatter_path / f"{column}_vs_{other_column}_scatter.png",
                                bbox_inches='tight'
                            )
                            plt.close(fig)
                        except Exception as e:
                            print(f"Error creating scatter plot for {column} vs {other_column}: {str(e)}")
def visualize_data(
    data_file: Path,
    save_path: Path = None,
    target_col: str = None
) -> None:
    """Main function to visualize both categorical and numerical data."""
    print("Starting visualization process...")
    visualize_categorical_data(data_file, data_path / "columns_categories.json", data_path / "selected_features.json", save_path, target_col)
    visulize_numerical_data(data_file, data_path / "columns_categories.json", data_path / "selected_features.json", save_path, target_col)
    print("Visualization process completed.")
if __name__ == "__main__":
    # Configure paths
    input_files = {
        'data_file': dataset_path / "titanic.csv",
        'columns_categories_file': data_path / "columns_categories.json",
        'selected_features_file': data_path / "selected_features.json"
    }
    
    # Verify all input files exist
    for name, path in input_files.items():
        if not path.exists():
            print(f"Error: {name} not found at {path}")
            sys.exit(1)
    
    # Run visualization
    visualize_categorical_data(**input_files)
    visulize_numerical_data(**input_files)
    print("Visualization process completed successfully.")