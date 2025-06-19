import plotly.express as px
import pandas as pd

def plot_ranking(df_result):
    """
    Membuat grafik batang vertikal untuk menampilkan hasil ranking.
    df_result: DataFrame yang memiliki kolom 'Alternatif' dan 'Skor'
    """
    fig = px.bar(
        df_result,
        x='Alternatif',
        y='Skor',
        color='Skor',
        text='Skor',
        color_continuous_scale='Viridis',
        title='Ranking Alternatif Berdasarkan Skor',
        labels={'Skor': 'Nilai Preferensi'}
    )
    fig.update_traces(texttemplate='%{text:.4f}', textposition='outside')
    fig.update_layout(
        xaxis_title='Alternatif',
        yaxis_title='Skor',
        uniformtext_minsize=8,
        uniformtext_mode='hide',
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    return fig
