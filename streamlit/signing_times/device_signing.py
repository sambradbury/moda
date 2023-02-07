import os
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

dir_path = os.getcwd()
csv_path = os.path.join(dir_path, 'streamlit/signing_times/data/signing_data.csv')
source_data = pd.read_csv(csv_path)

test_strategies = source_data['Test Strategy'].unique().tolist()
test_strategies.pop(4) # Excludes null value from list
devices = source_data['Model Name'].unique().tolist()
devices.pop(7) # Excludes null value from list

device_colors = {'Model One': '#00cc00', 'Model T': '#006600', 'Nano S': '#99ccff','Nano X': '#0099ff','Nano S+': '#0000ff','Mk3': '#ff6666','Mk4': '#cc0000'}

def makeFig(test_strategy, model_names, y_ax_metric, y_data, title):
    filtered_data = source_data.loc[
        source_data['Test Strategy'].isin([test_strategy])
        & source_data['Model Name'].isin(model_names)]
    fig = px.line(
        filtered_data,
        x=y_ax_metric,
        y=y_data,
        color='Model Name',
        color_discrete_map=device_colors
        )
    fig.update_xaxes(
        range=[10,510],
        tickvals=[25,50,100,250,500])
    fig.update_layout(
        autosize=True,
        title={
            'text' : title,
            'xanchor': 'center'
            }
        )
    return fig

with st.form(key='viz_settings'):
    test_strategy = st.selectbox("Test Strategy:", test_strategies, index=0)
    model_names = st.multiselect("Model Names:", devices, default=devices)
    y_ax_metric = st.selectbox("X-Axis Metric", ['UTXOs', 'Unsigned PSBT (kB)'], index=0)

    submit_button = st.form_submit_button()

if submit_button:

    pre_fig = makeFig(test_strategy, model_names, y_ax_metric, 'Pre-Confirmation Duration (minutes)', 'Pre-Confirmation Duration')

    st.plotly_chart(pre_fig, use_container_width=True)

    post_fig = makeFig(test_strategy, model_names, y_ax_metric, 'Post-Confirmation Duration (minutes)', 'Post-Confirmation Duration')

    st.plotly_chart(post_fig, use_container_width=True)
