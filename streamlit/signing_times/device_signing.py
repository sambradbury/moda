import os
import pandas as pd
import streamlit as st
import plotly.express as px

dir_path = os.getcwd()
csv_path = os.path.join(dir_path, 'streamlit/signing_times/data/signing_data.csv')
source_data = pd.read_csv(csv_path)

test_strategies = source_data['Test Strategy'].dropna().unique().tolist()
devices = source_data['Model Name'].dropna().unique().tolist()

device_colors = {
    'Model One': '#00cc00',
    'Model T': '#006600',
    'Nano S': '#99ccff',
    'Nano X': '#0099ff',
    'Nano S+': '#0000ff',
    'Mk3': '#ff6666',
    'Mk4': '#cc0000'
    }

def makeFig(test_strategy, model_names, x_ax_metric, y_data, title):
    filtered_data = source_data.loc[
        source_data['Test Strategy'].isin([test_strategy])
        & source_data['Model Name'].isin(model_names)]

    ticks = filtered_data[x_ax_metric].dropna().unique().tolist()
    x_min = min(ticks)
    x_max = max(ticks)

    fig = px.line(
        filtered_data,
        x=x_ax_metric,
        y=y_data,
        markers=True,
        line_shape='spline',
        color='Model Name',
        color_discrete_map=device_colors,
        )
    fig.update_xaxes(
        range=[x_min * .5, x_max * 1.05],
        tickvals=ticks
        )
    fig.update_traces(connectgaps=False)
    fig.update_layout(
        autosize=True,
        title={
            'text' : title,
            'xanchor': 'left'
            }
        )
    return fig

test_strategy = st.selectbox("Test Strategy:", test_strategies, index=0)
model_names = st.multiselect("Model Names:", devices, default=devices)
x_ax_metric = st.selectbox("X-Axis Metric", ['UTXOs', 'Unsigned PSBT (kB)'], index=0)

if model_names:
    pre_fig = makeFig(
        test_strategy,
        model_names,
        x_ax_metric,
        y_data='Pre-Confirmation Duration (minutes)',
        title='Pre-Confirmation Duration'
        )

    st.plotly_chart(pre_fig, use_container_width=True, sharing='streamlit')

    post_fig = makeFig(
        test_strategy,
        model_names,
        x_ax_metric,
        y_data='Post-Confirmation Duration (minutes)',
        title='Post-Confirmation Duration'
        )

    st.plotly_chart(post_fig, use_container_width=True, sharing='streamlit')

else: st.write("Error: Select at least one value for 'Model Names'")
