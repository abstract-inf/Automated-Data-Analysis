import matplotlib.pyplot as plt
import pandas as pd
import plotly.graph_objects as go


def plot_categorical_distribution(data: pd.DataFrame, column: str, title=None) -> tuple[plt.Figure, plt.Axes]:
    """
    Plot the distribution of a categorical column in a DataFrame.

    :param data: pd.DataFrame - The DataFrame containing the data.
    :param column: str - The name of the categorical column to plot.
    :param title: str - Optional title for the plot.
    :return: tuple[plt.Figure, plt.Axes] - The figure and axes of the plot.
    """
    # Check if the column exists in the DataFrame
    if column not in data.columns:
        raise ValueError(f"Column '{column}' does not exist in the DataFrame.")

    # Count the occurrences of each category
    counts = data[column].value_counts()

    # Create a bar plot for the categorical distribution
    fig, ax = plt.subplots(figsize=(10, 6))
    counts.plot(kind='bar', ax=ax, color='skyblue')
    
    # Set plot title and labels
    ax.set_title(title or f'Distribution of {column}', fontsize=16)
    ax.set_xlabel(column, fontsize=14)
    ax.set_ylabel('Count', fontsize=14)
    
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    return fig, ax

def plot_categorical_piechart(data: pd.DataFrame, column: str, title=None) -> tuple[plt.Figure, plt.Axes]:
    """
    Plot a pie chart for the distribution of a categorical column in a DataFrame.

    :param data: pd.DataFrame - The DataFrame containing the data.
    :param column: str - The name of the categorical column to plot.
    :param title: str - Optional title for the plot.
    :return: tuple[plt.Figure, plt.Axes] - The figure and axes of the plot.
    """
    # Check if the column exists in the DataFrame
    if column not in data.columns:
        raise ValueError(f"Column '{column}' does not exist in the DataFrame.")

    # Count the occurrences of each category
    counts = data[column].value_counts()

    # Create a pie chart for the categorical distribution
    fig, ax = plt.subplots(figsize=(8, 8))
    counts.plot(kind='pie', ax=ax, autopct='%1.1f%%', startangle=90, colors=plt.cm.Paired.colors)
    
    # Set plot title
    ax.set_title(title or f'Distribution of {column}', fontsize=16)
    
    plt.ylabel('')  # Hide y-label for better aesthetics
    plt.tight_layout()
    
    return fig, ax
def stacked_bar_plot(data: pd.DataFrame, column1:str, column2:str, title=None) -> tuple[plt.Figure, plt.Axes]:
    """
    Create a stacked bar plot for 2 categorical columns in a DataFrame.
    :param data: pd.DataFrame - The DataFrame containing the data.
    :param column1: str - name of categorical column to plot.
    :param column2: str - name of categorical column to plot.
    :param title: str - Optional title for the plot.
    :return: tuple[plt.Figure, plt.Axes] - The figure and axes of the plot.

    """
    if column1 not in data.columns or column2 not in data.columns:
        raise ValueError(f"Columns '{column1}' or '{column2}' do not exist in the DataFrame.")

    # Create a crosstab to get counts for each combination of categories
    crosstab = pd.crosstab(data[column1], data[column2])

    # Create a stacked bar plot
    fig, ax = plt.subplots(figsize=(10, 6))
    crosstab.plot(kind='bar', stacked=True, ax=ax, colormap='Paired')

    # Set plot title and labels
    ax.set_title(title or f'Stacked Bar Plot of {column1} vs {column2}', fontsize=16)
    ax.set_xlabel(column1, fontsize=14)
    ax.set_ylabel('Count', fontsize=14)

    plt.xticks(rotation=45)
    plt.tight_layout()

    return fig, ax
def plot_sankey_diagram(data: pd.DataFrame, columns: list[str], title=None) -> tuple[plt.Figure, plt.Axes]:
    """
    Create a Sankey diagram for the flow between two categorical columns in a DataFrame.

    :param data: pd.DataFrame - The DataFrame containing the data.
    :param columns: list[str] - List of two categorical columns to plot.
    :param title: str - Optional title for the plot.
    :return: tuple[plt.Figure, plt.Axes] - The figure and axes of the plot.
    """
    if len(columns) < 2:
        raise ValueError("Sankey diagram requires at least two columns.")

    # Check if both columns exist in the DataFrame
    nodes = []
    node_labels = []
    
    for col in columns:
        unique_values = data[col].astype(str).unique()
        node_labels.extend([f"{col}: {val}" for val in unique_values])
        nodes.extend(unique_values)
    
    # Create mapping from label to index
    label_to_index = {label: idx for idx, label in enumerate(node_labels)}
    
    # Define links between nodes
    links = []
    
    # Create links between consecutive columns
    for i in range(len(columns) - 1):
        source_col = columns[i]
        target_col = columns[i + 1]
        
        # Group by source and target to get counts
        grouped = data.groupby([source_col, target_col]).size().reset_index(name='count')
        
        for _, row in grouped.iterrows():
            source_label = f"{source_col}: {row[source_col]}"
            target_label = f"{target_col}: {row[target_col]}"
            
            links.append({
                'source': label_to_index[source_label],
                'target': label_to_index[target_label],
                'value': row['count']
            })
    
    # Create the Sankey diagram
    fig = go.Figure(go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=node_labels,
            color="blue"
        ),
        link=dict(
            source=[link['source'] for link in links],
            target=[link['target'] for link in links],
            value=[link['value'] for link in links]
        )
    ))
    
    fig.update_layout(title_text=title, font_size=14, width=len(columns)*200, height=600)
    
    return fig, None  # Sankey diagram does not return Axes object