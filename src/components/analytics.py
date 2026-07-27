import pandas as pd
from datetime import datetime


def process_analytics_data(raw_data):
    """
    Raw DB data ko charts ke liye ready karo
    """
    if not raw_data:
        return None

    # Step 3.1 — Flat list banao
    rows = []
    for record in raw_data:
        ts = record.get('timestamp')

        rows.append({
            'student_id':   record['student_id'],
            'student_name': record['students']['name'] 
                           if record.get('students') else 'Unknown',
            'subject_id':   record['subject_id'],
            'subject_name': record['subjects']['name'],
            'subject_code': record['subjects']['subject_code'],
            'is_present':   bool(record.get('is_present', False)),
            'timestamp':    ts,
            'date':         ts[:10] if ts else None,
            'week':         (
                datetime.fromisoformat(ts).strftime('%Y-W%W')
                if ts else None
            ),
        })

    df = pd.DataFrame(rows)
    return df


def get_chart1_data(df):
    """
    Chart 1: Har subject ka attendance %
    """
    summary = df.groupby(
        ['subject_id', 'subject_name', 'subject_code']
    ).agg(
        total=('is_present', 'count'),
        present=('is_present', 'sum')
    ).reset_index()

    summary['percentage'] = (
        summary['present'] / summary['total'] * 100
    ).round(1)

    summary['absent'] = (
        summary['total'] - summary['present']
    )

    return summary


def get_chart2_data(df):
    """
    Chart 2: Week by week trend
    """
    weekly = df.groupby(
        ['week', 'subject_name']
    ).agg(
        total=('is_present', 'count'),
        present=('is_present', 'sum')
    ).reset_index()

    weekly['percentage'] = (
        weekly['present'] / weekly['total'] * 100
    ).round(1)

    return weekly.sort_values('week')


def get_chart3_data(df):
    """
    Chart 3: Kaun sabse zyada absent hai
    """
    student_summary = df.groupby(
        ['student_id', 'student_name']
    ).agg(
        total=('is_present', 'count'),
        present=('is_present', 'sum')
    ).reset_index()

    student_summary['absent'] = (
        student_summary['total'] - 
        student_summary['present']
    )

    student_summary['percentage'] = (
        student_summary['present'] / 
        student_summary['total'] * 100
    ).round(1)

    student_summary['status'] = student_summary[
        'percentage'
    ].apply(
        lambda x: '✅ Safe' if x >= 75 else '⚠️ Low'
    )

    return student_summary.sort_values(
        'percentage', ascending=True
    )


def get_chart4_data(df):
    """
    Chart 4: Overall present vs absent
    """
    total = len(df)
    present = df['is_present'].sum()
    absent = total - present

    return {
        'labels': ['Present', 'Absent'],
        'values': [int(present), int(absent)],
        'total': total,
        'percentage': round(present / total * 100, 1)
    }

import plotly.express as px
import plotly.graph_objects as go


def make_bar_chart(chart1_df):
    """
    Chart 1: Bar chart — subject wise attendance %
    """
    fig = px.bar(
        chart1_df,
        x='subject_name',
        y='percentage',
        color='percentage',
        color_continuous_scale=[
            [0.0,  '#EB4459'],   # Red  — 0%
            [0.75, '#FFA500'],   # Orange — 75%
            [1.0,  '#2ECC71'],   # Green — 100%
        ],
        text='percentage',
        title='📊 Attendance % by Subject',
        labels={
            'subject_name': 'Subject',
            'percentage': 'Attendance %'
        },
        hover_data=['present', 'total', 'absent']
    )

    # 75% line add karo
    fig.add_hline(
        y=75,
        line_dash='dash',
        line_color='red',
        annotation_text='75% Required',
        annotation_position='top right'
    )

    fig.update_traces(
        texttemplate='%{text}%',
        textposition='outside'
    )

    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='black',
        showlegend=False,
        height=350
    )

    return fig


def make_line_chart(chart2_df):
    """
    Chart 2: Line chart — week by week trend
    """
    fig = px.line(
        chart2_df,
        x='week',
        y='percentage',
        color='subject_name',
        markers=True,
        title='📈 Weekly Attendance Trend',
        labels={
            'week': 'Week',
            'percentage': 'Attendance %',
            'subject_name': 'Subject'
        }
    )

    fig.add_hline(
        y=75,
        line_dash='dash',
        line_color='red',
        annotation_text='75% Minimum'
    )

    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='black',
        height=350
    )

    return fig


def make_student_chart(chart3_df):
    """
    Chart 3: Horizontal bar — student wise attendance
    """
    colors = [
        '#2ECC71' if p >= 75 else '#EB4459'
        for p in chart3_df['percentage']
    ]

    fig = go.Figure(go.Bar(
        x=chart3_df['percentage'],
        y=chart3_df['student_name'],
        orientation='h',
        marker_color=colors,
        text=chart3_df['percentage'].apply(
            lambda x: f'{x}%'
        ),
        textposition='outside',
        hovertemplate=(
            '<b>%{y}</b><br>'
            'Attendance: %{x}%<br>'
            '<extra></extra>'
        )
    ))

    fig.add_vline(
        x=75,
        line_dash='dash',
        line_color='orange',
        annotation_text='75%'
    )

    fig.update_layout(
        title='👥 Student-wise Attendance',
        xaxis_title='Attendance %',
        yaxis_title='Student',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='black',
        height=max(300, len(chart3_df) * 40)
    )

    return fig


def make_pie_chart(chart4_data):
    """
    Chart 4: Pie chart — overall present vs absent
    """
    fig = go.Figure(go.Pie(
        labels=chart4_data['labels'],
        values=chart4_data['values'],
        hole=0.4,
        marker_colors=['#2ECC71', '#EB4459'],
        textinfo='label+percent',
        hovertemplate=(
            '<b>%{label}</b><br>'
            'Count: %{value}<br>'
            'Percentage: %{percent}<br>'
            '<extra></extra>'
        )
    ))

    fig.update_layout(
        title='🍕 Overall Attendance Split',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='black',
        height=350,
        annotations=[{
            'text': f"{chart4_data['percentage']}%",
            'x': 0.5,
            'y': 0.5,
            'font_size': 20,
            'showarrow': False
        }]
    )

    return fig