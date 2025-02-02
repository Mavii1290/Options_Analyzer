import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import plotly.graph_objects as go




def create_oi_volume_charts(calls, puts, discrete_palette):
    # Ensure that OptionType is correctly assigned
    calls_df = calls[['strike', 'openInterest', 'volume']].copy()
    calls_df['OptionType'] = 'Call'  # Assign a valid category

    puts_df = puts[['strike', 'openInterest', 'volume']].copy()
    puts_df['OptionType'] = 'Put'  # Assign a valid category

    combined = pd.concat([calls_df, puts_df], ignore_index=True)

    # Convert 'OptionType' to a categorical data type
    combined['OptionType'] = pd.Categorical(combined['OptionType'], categories=['Call', 'Put'])

    # Ensure the color palette is valid (convert to a list if needed)
    if isinstance(discrete_palette, str):
        color_map = {
            "Plotly": ['#636EFA', '#EF553B'],  # Default Plotly colors (blue & red)
            "Pastel": ['#FFB6C1', '#87CEFA'],  # Light pink & light blue
            "Dark2": ['#1B9E77', '#D95F02']  # Green & orange
        }
        discrete_palette = color_map.get(discrete_palette, ['#636EFA', '#EF553B'])

    # --- Open Interest Bar Chart ---
    fig_oi = px.bar(
        combined,
        x='strike',
        y='openInterest',
        color='OptionType',  # Ensuring color is mapped to OptionType
        color_discrete_sequence=discrete_palette,  # Using a valid color sequence
        title='Open Interest by Strike',
        barmode='group',
    )
    fig_oi.update_layout(
        xaxis_title='Strike Price',
        yaxis_title='Open Interest',
        hovermode='x unified'
    )
    fig_oi.update_xaxes(rangeslider=dict(visible=True))

    # --- Volume Bar Chart ---
    fig_volume = px.bar(
        combined,
        x='strike',
        y='volume',
        color='OptionType',  # Ensuring color is mapped to OptionType
        color_discrete_sequence=discrete_palette,  # Using a valid color sequence
        title='Volume by Strike',
        barmode='group',
    )
    fig_volume.update_layout(
        xaxis_title='Strike Price',
        yaxis_title='Volume',
        hovermode='x unified'
    )
    fig_volume.update_xaxes(rangeslider=dict(visible=True))

    return fig_oi, fig_volume



def create_treemap(calls, puts, continuous_scale, expiry_date):
    # Add 'expiry' column manually since it's not in the DataFrame
    calls['expiry'] = puts['expiry'] = expiry_date  # Add expiry information

    # Prepare DataFrames for calls and puts
    calls_df = calls[['strike', 'expiry', 'openInterest', 'volume']].copy()
    calls_df['OptionType'] = 'Call'

    puts_df = puts[['strike', 'expiry', 'openInterest', 'volume']].copy()
    puts_df['OptionType'] = 'Put'

    # Combine the data
    combined = pd.concat([calls_df, puts_df], ignore_index=True)
    
    # Create the treemap visualization
    fig = px.treemap(
        combined,
        path=['OptionType', 'expiry', 'strike'],
        values='volume',
        color='openInterest',
        color_continuous_scale=continuous_scale,
        title="Treemap (Volume Size, OI Color)"
    )
    fig.update_layout(margin=dict(t=50, l=25, r=25, b=25))
    return fig

def create_donut_chart(call_volume, put_volume, discrete_palette):
    labels = ['Calls', 'Puts']
    values = [call_volume, put_volume]

    # Ensure discrete_palette is a list of valid color names or hex values
    if isinstance(discrete_palette, str):
        # Example list of colors (you can customize this as needed)
        discrete_palette = ['#1f77b4', '#ff7f0e']  # Blue and Orange as default colors

    fig = px.pie(
        names=labels,
        values=values,
        hole=0.3,
        color=labels,
        color_discrete_sequence=discrete_palette  # Pass the list of colors
    )
    fig.update_layout(title_text='Call vs Put Volume Ratio')
    fig.update_traces(hoverinfo='label+percent+value')
    return fig

def create_gex_bubble_chart(calls, puts):
    calls_gex = calls[['strike', 'gamma', 'openInterest']].copy()
    calls_gex['GEX'] = calls_gex['gamma'] * calls_gex['openInterest'] * 100
    calls_gex['Type'] = 'Call'
    
    puts_gex = puts[['strike', 'gamma', 'openInterest']].copy()
    puts_gex['GEX'] = puts_gex['gamma'] * puts_gex['openInterest'] * 100
    puts_gex['Type'] = 'Put'
    
    gex_df = pd.concat([calls_gex, puts_gex], ignore_index=True)
    
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=gex_df.loc[gex_df['Type'] == 'Call', 'strike'],
        y=gex_df.loc[gex_df['Type'] == 'Call', 'GEX'],
        mode='markers',
        name='Calls',
        marker=dict(
            size=gex_df.loc[gex_df['Type'] == 'Call', 'GEX'].abs() / 1000,
            color='green',
            opacity=0.6,
            line=dict(width=1, color='DarkSlateGrey')
        ),
        hovertemplate='Strike: %{x}<br>Gamma Exp: %{y}'
    ))

    fig.add_trace(go.Scatter(
        x=gex_df.loc[gex_df['Type'] == 'Put', 'strike'],
        y=gex_df.loc[gex_df['Type'] == 'Put', 'GEX'],
        mode='markers',
        name='Puts',
        marker=dict(
            size=gex_df.loc[gex_df['Type'] == 'Put', 'GEX'].abs() / 1000,
            color='red',
            opacity=0.6,
            line=dict(width=1, color='DarkSlateGrey')
        ),
        hovertemplate='Strike: %{x}<br>Gamma Exp: %{y}'
    ))

    fig.update_layout(
        title='Gamma Exposure (GEX) Bubble Chart',
        xaxis_title='Strike Price',
        yaxis_title='Gamma Exposure',
        hovermode='closest',
        showlegend=True
    )
    
    return fig


# Function to create bar charts
def create_bar_chart(data, exposure_col, title):
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=data[data['type'] == 'Call']['strike'],
        y=data[data['type'] == 'Call'][exposure_col],
        name='Calls',
        marker_color='blue',
        opacity=0.6
    ))
    fig.add_trace(go.Bar(
        x=data[data['type'] == 'Put']['strike'],
        y=-data[data['type'] == 'Put'][exposure_col],
        name='Puts',
        marker_color='red',
        opacity=0.6
    ))
    fig.update_layout(
        title=title,
        xaxis_title='Strike Price',
        yaxis_title=exposure_col.replace('_', ' ').title(),
        barmode='overlay',
        yaxis=dict(title='Exposure', tickvals=[-max(data[exposure_col].max(), -data[exposure_col].min()), 0, max(data[exposure_col].max(), -data[exposure_col].min())]),
        hovermode='x unified'
    )
    return fig
