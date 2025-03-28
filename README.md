<h2>Project Description: System for Processing, Analyzing, and Visualizing Financial Data</h2>

This project aims to provide an integrated system for collecting, processing, storing, analyzing, and visualizing financial data. The system consists of five interconnected services, each with a specific role.

The Data Ingestion Service is responsible for gathering data from various financial sources, such as stock exchanges and APIs (Yahoo Finance), using the HTTP protocol.

The Real-Time Processing Service utilizes Celery task Streaming and Scheduling to process data in real time, including filtering, aggregation, and transformation, using redis as a broker.

The Data Storage Service ensures efficient data storage in a PostgreSQL database for structured data.

The Data Analysis Service applies machine learning algorithms and statistical analysis to detect trends, generate predictions, and prepare reports based on historical and real-time data, using the pandas model.

The Data Visualization Service provides the web interface with a built chart for visualizing analyzed data using Plotly, displaying graphs and tables to support better decision-making.

By integrating these services, the system will deliver a fast, scalable, and reliable solution for real-time financial analysis.

Mockup: https://www.figma.com/design/V3mX8VN8F7U72oBzyZqgG5/MOCKUP-FOR-SMA?node-id=0-1&p=f&t=0CeB3qTEfKYRdInP-0
<h1></h1>


❗❗❗ Video in case host fails:
https://www.youtube.com/watch?v=f2HpL1EnWrU

<br>

<br>

![Financial Data Pipeline](Architecture/High-Level/Stock%20Market%20Analytics%20High-Level%20Architecture%20Diagram.png)

