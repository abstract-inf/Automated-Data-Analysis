# visualize.py
import pandas as pd
import matplotlib.pyplot as plt

class Visualize:
    @staticmethod
    def create_bar_chart_categorical(data: pd.DataFrame, column: str) -> None:
        """
        Creates a bar chart for a single categorical column.
        """
        pass

    @staticmethod
    def create_pie_chart_categorical(data: pd.DataFrame, column: str) -> None:
        """
        Creates a pie chart for a single categorical column.
        """
        pass

    @staticmethod
    def create_stacked_bar_chart(data: pd.DataFrame, col1: str, col2: str) -> None:
        """
        Creates a stacked bar chart for two categorical columns.
        """
        pass

    @staticmethod
    def create_all_of_cat_bar_charts(data: pd.DataFrame, categorical_columns: list) -> None:
        """
        Creates bar charts for all categorical columns.
        """
        pass

    @staticmethod
    def create_frequency_bar_charts(data: pd.DataFrame, column: str, num_top_days: int) -> None:
        """
        Creates frequency bar charts for a column, potentially showing top N frequent days.
        """
        pass

    @staticmethod
    def create_histogram(data: pd.DataFrame, column: str) -> None:
        """
        Creates a histogram for a numerical column.
        """
        pass

    @staticmethod
    def create_scatter_plot(data: pd.DataFrame, x_column: str, y_column: str) -> None:
        """
        Creates a scatter plot for two numerical columns.
        """
        pass

    @staticmethod
    def create_scatter_plot_3d(data: pd.DataFrame, x_column: str, y_column: str, z_column: str) -> None:
        """
        Creates a 3D scatter plot for three numerical columns.
        """
        pass

    @staticmethod
    def create_num_cat_scatter_plot(data: pd.DataFrame, num_col: str, cat_col: str, color_by_cat: bool = True) -> None:
        """
        Creates a scatter plot with numerical and categorical columns, potentially coloring by category.
        """
        pass

    @staticmethod
    def create_time_series_moving_line(data: pd.DataFrame, time_col: str, value_col: str) -> None:
        """
        Creates a moving line chart for time series data.
        """
        pass

    @staticmethod
    def create_time_series_moving_line_between_two_num_cols(data: pd.DataFrame, time_col: str, num_col1: str, num_col2: str) -> None:
        """
        Creates a moving line chart for time series data between two numerical columns.
        """
        pass