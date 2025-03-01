import yfinance as yf
import dash
from dash import dcc, html
import plotly.graph_objects as go
from dash.dependencies import Input, Output
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense


# Function to fetch real-time stock data
def get_realtime_data(ticker='ADBE'):
    stock = yf.Ticker(ticker)
    hist = stock.history(period='1d', interval='5m')
    df = hist[['Open', 'High', 'Low', 'Close']].reset_index()
    df['Datetime'] = df['Datetime'].dt.strftime('%Y-%m-%d %H:%M')
    return df


# Function to calculate technical indicators
def calculate_indicators(df):
    df['SMA_10'] = df['Close'].rolling(window=10).mean()
    df['SMA_20'] = df['Close'].rolling(window=20).mean()
    df['EMA_10'] = df['Close'].ewm(span=10, adjust=False).mean()
    return df


# Function to prepare data for LSTM model
def prepare_data(df, time_step=10):
    scaler = MinMaxScaler(feature_range=(0, 1))
    df_scaled = scaler.fit_transform(df[['Close']])
    X, y = [], []
    for i in range(len(df_scaled) - time_step - 1):
        X.append(df_scaled[i:(i + time_step), 0])
        y.append(df_scaled[i + time_step, 0])
    X, y = np.array(X), np.array(y)
    X = np.reshape(X, (X.shape[0], X.shape[1], 1))
    return X, y, scaler


# Function to train LSTM model
def train_model(df):
    X, y, scaler = prepare_data(df)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    model = Sequential([
        LSTM(50, return_sequences=True, input_shape=(X_train.shape[1], 1)),
        LSTM(50, return_sequences=False),
        Dense(25),
        Dense(1)
    ])

    model.compile(optimizer='adam', loss='mean_squared_error')
    model.fit(X_train, y_train, epochs=10, batch_size=16, verbose=1)
    return model, scaler


# Function to predict future price
def predict_future(df, model, scaler, time_step=10):
    last_data = df[['Close']].tail(time_step).values
    last_data_scaled = scaler.transform(last_data)
    last_data_scaled = np.reshape(last_data_scaled, (1, time_step, 1))
    predicted_price = model.predict(last_data_scaled)
    return scaler.inverse_transform(predicted_price)[0][0]


# Function to generate buy/hold/sell signal
def generate_signal(predicted_price, current_price):
    if predicted_price > current_price * 1.01:
        return "BUY"
    elif predicted_price < current_price * 0.99:
        return "SELL"
    else:
        return "HOLD"


# Train the model once at startup
data = get_realtime_data()
model, scaler = train_model(data)

# Dash App Setup
app = dash.Dash(__name__)
app.layout = html.Div([
    html.H1("Real-Time ADBE Stock Candlestick Chart with Predictions"),
    dcc.Graph(id='candlestick-chart'),
    html.Button('Analyze Data', id='analyze-button', n_clicks=0),
    html.Button('Predict Future Price', id='predict-button', n_clicks=0),
    html.Div(id='prediction-output', style={'font-size': '24px', 'margin-top': '20px'}),
    dcc.Interval(id='interval-component', interval=10 * 1000, n_intervals=0)
])


@app.callback(
    Output('candlestick-chart', 'figure'),
    [Input('interval-component', 'n_intervals'), Input('analyze-button', 'n_clicks')]
)
def update_chart(_, analyze_clicks):
    candlestick_df = get_realtime_data()
    if analyze_clicks > 0:
        candlestick_df = calculate_indicators(candlestick_df)
    fig = go.Figure()

    # Add candlestick chart
    fig.add_trace(go.Candlestick(
        x=candlestick_df['Datetime'],
        open=candlestick_df['Open'],
        high=candlestick_df['High'],
        low=candlestick_df['Low'],
        close=candlestick_df['Close'],
        name='Candlestick'
    ))

    if analyze_clicks > 0:
        fig.add_trace(go.Scatter(x=candlestick_df['Datetime'], y=candlestick_df['SMA_10'], mode='lines', name='SMA 10'))
        fig.add_trace(go.Scatter(x=candlestick_df['Datetime'], y=candlestick_df['SMA_20'], mode='lines', name='SMA 20'))
        fig.add_trace(go.Scatter(x=candlestick_df['Datetime'], y=candlestick_df['EMA_10'], mode='lines', name='EMA 10'))

    fig.update_layout(title='Adobe Inc. (ADBE) Real-Time Candlestick Chart',
                      xaxis_title='Time', yaxis_title='Price',
                      xaxis_rangeslider_visible=False)
    return fig


@app.callback(
    Output('prediction-output', 'children'),
    Input('predict-button', 'n_clicks')
)
def update_prediction(n_clicks):
    if n_clicks > 0:
        df = get_realtime_data()
        prediction = predict_future(df, model, scaler)
        current_price = df['Close'].iloc[-1]
        signal = generate_signal(prediction, current_price)
        return f"Predicted Next Close Price: {prediction:.2f} | Suggested Action: {signal}"
    return ""


if __name__ == '__main__':
    app.run_server(debug=True)