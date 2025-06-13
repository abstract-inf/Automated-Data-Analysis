import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

def plot_numerical_distribution(data: pd.DataFrame, column: str, title=None) -> tuple[plt.Figure, plt.Axes]:
    """
    Plot the distribution of a numerical column in a DataFrame.

    :param data: pd.DataFrame - The DataFrame containing the data.
    :param column: str - The name of the numerical column to plot.
    :param title: str - Optional title for the plot.
    :return: tuple[plt.Figure, plt.Axes] - The figure and axes of the plot.
    """
    # Check if the column exists in the DataFrame
    if column not in data.columns:
        raise ValueError(f"Column '{column}' does not exist in the DataFrame.")

    # Create a histogram for the numerical distribution
    fig, ax = plt.subplots(figsize=(10, 6))
    data[column].plot(kind='hist', ax=ax, bins=30, color='skyblue', edgecolor='black')

    # Set plot title and labels
    ax.set_title(title or f'Distribution of {column}', fontsize=16)
    ax.set_xlabel(column, fontsize=14)
    ax.set_ylabel('Frequency', fontsize=14)

    plt.tight_layout()

    return fig, ax

def plot_numerical_boxplot(data: pd.DataFrame, column: str, title=None) -> tuple[plt.Figure, plt.Axes]:
    """
    Plot a boxplot for a numerical column in a DataFrame.

    :param data: pd.DataFrame - The DataFrame containing the data.
    :param column: str - The name of the numerical column to plot.
    :param title: str - Optional title for the plot.
    :return: tuple[plt.Figure, plt.Axes] - The figure and axes of the plot.
    """
    # Check if the column exists in the DataFrame
    if column not in data.columns:
        raise ValueError(f"Column '{column}' does not exist in the DataFrame.")

    # Create a boxplot for the numerical distribution
    fig, ax = plt.subplots(figsize=(10, 6))
    data.boxplot(column=column, ax=ax, patch_artist=True, boxprops=dict(facecolor='lightblue', color='black'),
                 whiskerprops=dict(color='black'), capprops=dict(color='black'), medianprops=dict(color='red'))

    # Set plot title and labels
    ax.set_title(title or f'Boxplot of {column}', fontsize=16)
    ax.set_ylabel(column, fontsize=14)

    plt.tight_layout()

    return fig, ax

def plot_numerical_scatter(data: pd.DataFrame, x_column: str, y_column: str, cat_column:str = None, title=None) -> tuple[plt.Figure, plt.Axes]:
    """
    Plot a scatter plot for two numerical columns in a DataFrame.

    :param data: pd.DataFrame - The DataFrame containing the data.
    :param x_column: str - The name of the x-axis numerical column.
    :param y_column: str - The name of the y-axis numerical column.
    :param title: str - Optional title for the plot.
    :param cat_column: str - The name of the categorical column to color the points by.
    :return: tuple[plt.Figure, plt.Axes] - The figure and axes of the plot.
    """
    # Check if the columns exist in the DataFrame
    for col in [x_column, y_column, cat_column]:
        if col not in data.columns:
            raise ValueError(f"Column '{col}' does not exist in the DataFrame.")

    # Create a scatter plot for the numerical distribution
    fig, ax = plt.subplots(figsize=(10, 6))
    scatter = ax.scatter(data[x_column], data[y_column], c=data[cat_column].astype('category').cat.codes, cmap='viridis', alpha=0.7)

    # Set plot title and labels
    ax.set_title(title or f'Scatter Plot of {x_column} vs {y_column}', fontsize=16)
    ax.set_xlabel(x_column, fontsize=14)
    ax.set_ylabel(y_column, fontsize=14)

    # Add color bar
    cbar = plt.colorbar(scatter, ax=ax)
    cbar.set_label(cat_column, fontsize=14)

    plt.tight_layout()

    return fig, ax