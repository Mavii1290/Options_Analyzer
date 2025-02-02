
# **Real-Time Stock Options Data Streamlit App**

This **Streamlit app** allows users to view **real-time stock options data**, including visualizations for **Open Interest**, **Volume**, and **Gamma Exposure**. The app fetches **stock data**, calculates **technical indicators** like **RSI** and **moving averages**, and presents **interactive charts** like **treemaps**, **donut charts**, and **bar charts**. 

## Features

- **Display of stock price and volume** in real-time.
- **Technical Indicators**: Includes **RSI**, **50-day** and **200-day moving averages**, and **Delta** (a placeholder for options Greeks).
- **Interactive visualizations**:
  - **Treemaps**: Showing the relationship between options (Strike Price vs Open Interest vs Volume).
  - **Donut charts**: Visualize the volume ratio between Calls and Puts.
  - **Bar charts**: Display Open Interest and Volume by Strike Price.
- **Filtering**: Select different expiration dates, and view only the data where **Volume > Open Interest**.
  
---

## **Table of Contents**

1. [Project Setup](#project-setup)
2. [Dependencies](#dependencies)
3. [How to Run the App](#how-to-run-the-app)
4. [App Usage](#app-usage)
5. [Visuals](#visuals)
6. [License](#license)

---

## **Project Setup**

Follow these steps to set up the project on your local machine.

### Step 1: Clone the Repository

Clone this repository to your local machine.

```bash
git clone https://github.com/yourusername/my_streamlit_project.git
cd my_streamlit_project
```

### Step 2: Create a Virtual Environment (Optional)

It's recommended to use a virtual environment to manage dependencies.

```bash
# For macOS/Linux
python3 -m venv venv
source venv/bin/activate

# For Windows
python -m venv venv
venv\Scriptsctivate
```

### Step 3: Install Dependencies

Install the required libraries listed in `requirements.txt`:

```bash
pip install -r requirements.txt
```

---

## **Dependencies**

This project requires the following dependencies:

- **Streamlit**: The web framework to build and run the app.
- **yfinance**: To fetch stock data and options chain data from Yahoo Finance.
- **Plotly**: For interactive visualizations like treemaps, donut charts, and bar charts.
- **TA-Lib**: For calculating technical indicators like RSI and moving averages.
- **Pandas**: For data manipulation.

To install these dependencies, run the following command:

```bash
pip install streamlit yfinance plotly talib pandas
```

---

## **How to Run the App**

1. After setting up the virtual environment and installing dependencies, run the Streamlit app:

```bash
streamlit run app.py
```

2. This will launch the app in your browser, where you can interact with the various features.

---

## **App Usage**

1. **Enter a Stock Ticker**:
   - Enter a valid stock ticker symbol (e.g., `AAPL`, `TSLA`) in the input field to fetch real-time data for that stock.
   
2. **View Key Metrics**:
   - The app will display key metrics like **Current Price**, **Volume**, and **Technical Indicators** (RSI, moving averages, etc.) using `st.metric` at the top.

3. **Select Expiry Date(s)**:
   - You can choose multiple expiry dates for the options data by selecting from the **expiry date** dropdown.
   
4. **Interactive Visualizations**:
   - **Donut Chart**: Displays the **Call vs Put Volume Ratio**. The **size** of the donut segments corresponds to the total volume of calls and puts.
   - **Treemap**: A hierarchical visualization where the size of each box represents **Volume** and the color represents **Open Interest**.
   - **OI and Volume Bar Charts**: Displays the **Open Interest** and **Volume** by **Strike Price**.
   
5. **Apply Filters**:
   - You can filter options data by selecting the option to only show data where **Volume > Open Interest**.

6. **View Top 10 Calls/Puts by Volume**:
   - The app will display tables of the **top 10 calls** and **puts** by **volume**, with filtering and sorting options.

---

## **Visuals**

### 1. **Real-Time Stock Metrics**:
   - **Current Price**: Displays the latest price of the stock.
   - **Volume**: Displays the latest volume for the stock.
   - **Technical Indicators**: Shows RSI, 50-day moving average, and 200-day moving average.

**Example Output**:
   
```
Current Price: $150.25
Current Volume: 5.1M
RSI: 58.6
50-day MA: $148.30
200-day MA: $140.45
Delta: 0.45
```

### 2. **Donut Chart for Volume Ratio**:
   - This chart shows the **Call vs Put Volume Ratio**. The **size** of the donut segments corresponds to the total volume of calls and puts.

**Visual Example**:

![Donut Chart Example](https://yourimageurl.com/donut_chart.png)

### 3. **Treemap**:
   - A **Treemap** visualization showing:
     - **Hierarchy**: Option Type → Expiry → Strike.
     - **Size**: Volume.
     - **Color**: Open Interest (with continuous color scale).

**Visual Example**:

![Treemap Example](https://yourimageurl.com/treemap_example.png)

### 4. **OI & Volume Bar Charts**:
   - **Bar Charts** showing **Open Interest** and **Volume** by **Strike Price**.
   
**Visual Example**:

![OI Bar Chart](https://yourimageurl.com/oi_bar_chart.png)
![Volume Bar Chart](https://yourimageurl.com/volume_bar_chart.png)

### 5. **Top 10 Calls/Puts by Volume**:
   - Display of the **top 10 calls** and **puts** sorted by **volume**, with a clean tabular format showing strike prices, volumes, open interest, bid sizes, and ask sizes.

**Visual Example**:

| Ticker | Strike | Volume | Open Interest | Bid Size | Ask Size |
|--------|--------|--------|---------------|----------|----------|
| AAPL   | 150.00 | 2000   | 1500          | 100      | 50       |
| AAPL   | 155.00 | 1500   | 1400          | 80       | 60       |
| ...    | ...    | ...    | ...           | ...      | ...      |

---

## **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

### Notes:
- Make sure to replace the **visual example URLs** with actual image URLs if needed, or you can skip them if you're not including images in the README.
- If you want to include more technical indicators or advanced features, you can expand on the instructions and examples here. 

By following the steps in the README, users will be able to set up and run the app seamlessly!
