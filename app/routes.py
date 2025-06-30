# app/routes.py
from flask import render_template, request
from app import app
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import matplotlib
matplotlib.use('Agg')

# Load data
DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'covid_clinical_trials.csv')
df = pd.read_csv(DATA_PATH)
df['Start Date'] = pd.to_datetime(df['Start Date'], errors='coerce')

# Ensure static dir exists
STATIC_PATH = os.path.join(os.path.dirname(__file__), 'static')
os.makedirs(STATIC_PATH, exist_ok=True)

def save_plot(fig, filename):
    plot_path = os.path.join(STATIC_PATH, filename)
    fig.savefig(plot_path, bbox_inches='tight')
    plt.close(fig)
    return filename  # only return filename like 'filtered_status.png'

@app.route('/', methods=['GET', 'POST'])
def dashboard():
    statuses = sorted(df['Status'].dropna().unique())
    phases = sorted(df['Phases'].dropna().unique())

    selected_status = request.form.get('status_filter', 'All')
    selected_phase = request.form.get('phase_filter', 'All')

    filtered_df = df.copy()
    if selected_status != 'All':
        filtered_df = filtered_df[filtered_df['Status'] == selected_status]
    if selected_phase != 'All':
        filtered_df = filtered_df[filtered_df['Phases'] == selected_phase]

    if not filtered_df.empty:
        fig, ax = plt.subplots(figsize=(10, 6))
        filtered_df['Status'].value_counts().plot(kind='bar', ax=ax, color='skyblue')
        ax.set_title('COVID-19 Trial Status (Filtered)')
        ax.set_ylabel('Count')
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
        plot_file = save_plot(fig, 'filtered_status.png')
    else:
        plot_file = None

    return render_template("index.html",
                           plot_path=plot_file,
                           statuses=['All'] + statuses,
                           phases=['All'] + phases,
                           selected_status=selected_status,
                           selected_phase=selected_phase)
