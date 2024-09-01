
# Sales-Team-Performance-Analysis-Using-LLM

This project aims to develop a sophisticated backend system that leverages a Large Language Model (LLM) to analyze unit price data and provide insightful feedback on individual units and overall team performance. Designed as an automated advisory tool, the system will aid users in making informed decisions in real estate dealings by considering various factors that impact property prices and values. By processing data and generating insights through multiple API endpoints, the system ensures the delivery of the best possible advice for real estate transactions.


## Features

### Data Ingestion:
- Implements a flexible mechanism to ingest sales data from multiple sheets in an Excel file.
- Ensures data validation and transformation to maintain consistency and accuracy.
### LLM Integration:
- Utilizes GPT to analyze data and generate actionable insights.
### API Endpoints:
- Provides performance feedback on individual sales units.
- Assesses overall team performance.
- Evaluates sales performance trends and forecasts.

## Deployment

Our first step is to clone the repository, that can be done by running the following command in terminal or console of your choice

### 1. Setup
```bash
git clone https://github.com/abdulsaboor938/homeeasy-assesment.git 
```
Now, navigate to the directory of repository you just cloned
```bash
cd sales-team-performance-analysis
```
### 2. Installing dependencies
If you wish, you can install the latest versions of dependencies, but to make things easier and prevent incompatibilities I have included the `requirements.txt`. You can install all required dependencies with running this one single command.
```bash
pip install -r requirements.txt
```
**Note: Ensure that `pip` is installed for this to work, if you are using a virtual environment**

### 3. Finally, Running the project
Just run this command and if everything is installed properly you should have the app up and running.
```bash
python app.py
```

Now that everything is running let's see how this API works and what parameters should be passed to obtain fruitful results from the end-points.





## API Reference

### 1. Individual Sales Representative Performance Analysis

**Endpoint:** 
`/api/rep_performance`

**Method:** 
`GET`

**Parameters:** 

| Parameter | Required | Description                           |
| :-------- | :------- | :------------------------------------ |
| `employee_id` | **Yes**  | Unique identifier for the sales rep    |

**Function:** 
Returns detailed performance analysis and feedback for the specified sales representative.

**Example Request:**
```http
GET /api/rep_performance?employee_id=183
```
**Response (Postman)**:
![Testing of 1st endpoint](https://github.com/abdulsaboor938/homeeasy-assesment/blob/main/screenshots/1.png)

### 2. Overall Sales Team Performance Summary

**Endpoint:** 
`/api/team_performance`

**Method:** 
`GET`

**Parameters:** 

None

**Function:** 
Give performance insights leveraged from entire sales team data.

**Example Request:**
```http
GET /api/team_performance
```
**Response (Postman)**:
![Testing of 2nd endpoint](https://github.com/abdulsaboor938/homeeasy-assesment/blob/main/screenshots/2.png)

### 3. Sales Performance Trends and Forecasting

**Endpoint:** 
`/api/performance_trends`

**Method:** 
`GET`

**Parameters:** 

| Parameter | Required | Description                           |
| :-------- | :------- | :------------------------------------ |
| `time_period` | **Yes**  | Quarterly or Monthly time frame to evaluate and predict performance    |

**Function:** 
Finds the best building deals in the specified neighborhood or unit type.

**Example Request:**
```http
GET /api/performance_trends?time_period=monthly
```
**Response (Postman)**:
![Testing of 3rd endpoint](https://github.com/abdulsaboor938/homeeasy-assesment/blob/main/screenshots/3.png)

## Author

- [@Abdul Saboor](https://www.github.com/abdulsaboor938)

