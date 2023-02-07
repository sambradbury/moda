import os
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

cwd = os.getcwd()
source_data = pd.read_csv(cwd + '/data/signing_data.csv')
test_strategies = source_data['Test Strategy'].unique().tolist()
devices = source_data['Model Name'].unique().tolist()

with st.form(key='viz_settings'):
    test_strategy = st.selectbox("Test Strategy:", test_strategies, index=0)
    model_names = st.multiselect("Model Names:", devices, default=devices)
    y_ax_metric = st.selectbox("X-Axis Metric", ['UTXOs', 'Unsigned PSBT (kB)'], index=0)

    submit_button = st.form_submit_button()

if submit_button:

    pre_conf_data = source_data.loc[
                                source_data['Test Strategy'].isin([test_strategy])
                                & source_data['Model Name'].isin(model_names)]
    pre_fig = px.line(pre_conf_data, x=y_ax_metric, y='Staging Duration (pre-confirmation)', color='Model Name')
    pre_fig.update_layout(
        autosize=True,
        title={
            'text' : 'Staging Duration (pre-confirmation)',
            'xanchor': 'center'
            }
        )

    st.plotly_chart(pre_fig, use_container_width=True)

    post_conf_data = source_data.loc[
                                source_data['Test Strategy'].isin([test_strategy])
                                & source_data['Model Name'].isin(model_names)]
    post_fig = px.line(post_conf_data, x=y_ax_metric, y='Signing Duration (post-confirmation)', color='Model Name')
    post_fig.update_layout(
        autosize=True,
        title={
            'text' : 'Signing Duration (post-confirmation)',
            'xanchor': 'center'
            }
        )
    st.plotly_chart(post_fig, use_container_width=True)




# mainFig = go.Figure()

# x_data=df['UTXOs'].tolist()
# y_data=df['Staging Duration (pre-confirmation)'].tolist()

# trace = go.Scatter3d(x=x_data, y=y_data)

# trace.marker.size=1

# mainFig.add_trace(trace)


# layout = Layout(
#     showlegend=True,
#     scene=Scene(
#         xaxis=XAxis(title='Bitcoin Days'),
#         yaxis=YAxis(title='Average Price ($)'),
#         zaxis=ZAxis(title='Total Revenue (S)')
#     )
# )
# mainFig.layout=layout
# mainFig.update_layout(
# height = 1000
# )

