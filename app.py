from flask import Flask, request, jsonify
import openai
import pandas as pd

app = Flask(__name__)

# Define the API key for OpenAI (replace 'your-api-key' with your actual key)
openai.api_key = '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'

@app.route('/api/rep_performance', methods=['GET'])
def rep_performance():
    # Get the employee_id from the request parameters
    employee_id = request.args.get('employee_id')
    
    if not employee_id:
        return jsonify({"error": "Employee ID is required"}), 400
    
    try:
        employee_id = int(employee_id)
    except ValueError:
        return jsonify({"error": "Employee ID must be an integer"}), 400
    
    # Load the CSV data into a DataFrame
    df = pd.read_csv('sales_performance_data.csv')

    # Create a column named calls by adding ('mon_call', 'tue_call', 'wed_call', 'thur_call', 'fri_call', 'sat_call', 'sun_call')
    df['calls'] = df['mon_call'] + df['tue_call'] + df['wed_call'] + df['thur_call'] + df['fri_call'] + df['sat_call'] + df['sun_call']
    df['texts'] = df['mon_text'] + df['tue_text'] + df['wed_text'] + df['thur_text'] + df['fri_text'] + df['sat_text'] + df['sun_text']

    # The dated column is as follows: 2022-07-26, create a week_number column that shows the week number of the year
    df['week_number'] = pd.to_datetime(df['dated']).dt.isocalendar().week

    # Create a day column that shows the day of the week
    df['day'] = pd.to_datetime(df['dated']).dt.day_name()

    # Drop all rows where day is not Friday
    df = df[df['day'] == 'Friday']

    # Selecting only required columns
    df = df[['employee_id', 'employee_name', 'dated', 'lead_taken', 'tours_booked', 'applications', 'tours_per_lead', 'apps_per_tour',
            'apps_per_lead', 'revenue_confirmed', 'revenue_pending', 'revenue_runrate', 'tours_in_pipeline', 'estimated_revenue', 
            'tours', 'tours_runrate', 'tours_scheduled', 'tours_pending', 'tours_cancelled', 'calls', 'texts', 'week_number']]

    # Filter the DataFrame for the given employee_id
    temp = df[df['employee_id'] == employee_id]
    
    if temp.empty:
        return jsonify({"error": "No data found for the given Employee ID"}), 404
    
    # Convert the DataFrame to CSV format (as a string)
    csv_data = temp.to_csv(index=False)
    
    # Define the prompt template
    prompt = f"""
    ### Task:
    Analyze the performance of a sales agent based on the provided data. Generate a detailed performance analysis report in HTML format, ensuring that all headings are enclosed in <h2> or <h3> tags, and that bullet points are enclosed in <ul> and <li> tags. The report should include the following sections:
    1. **Overview of Key Metrics:** Summarize key metrics like leads taken, tours booked, applications, and revenue confirmed.
    2. **Conversion Metrics:** Analyze conversion rates such as tours per lead, applications per tour, and applications per lead.
    3. **Revenue Analysis:** Provide insights into revenue metrics, including confirmed revenue, pending revenue, and revenue runrate.
    4. **Pipeline and Pending Tours:** Assess the status of tours in the pipeline and estimate potential revenue.
    5. **Communication Metrics:** Review the number of calls and texts and their potential impact on performance.
    6. **Week Number Comparison:** Compare performance across different weeks, focusing on notable differences and trends.
    7. **Summary and Recommendations:** Summarize the strengths and areas for improvement and provide actionable recommendations for the agent.

    ### Data:
    The data below is a CSV format representing the performance metrics of a sales agent. Use this data to generate the feedback report:

    {csv_data}

    ### Output Format:
    Please generate the report using HTML tags, ensuring that headings and bullet points are correctly formatted. For example:

    <h2>Overview of Key Metrics</h2>
    <ul>
    <li>Total leads taken: 1117</li>
    <li>Total tours booked: 130</li>
    ...
    </ul>
    """
    
    # Call the GPT API using the new method
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": prompt,
            },
        ],
        max_tokens=2048,
        temperature=0.7,
        top_p=1.0,
        n=1,
        stop=None
    )
    
    # Extract the generated response text
    output_text = completion.choices[0].message['content'].strip()
    
    # Return the response in HTML format
    return f"<html><body><pre>{output_text}</pre></body></html>"

@app.route('/api/team_performance', methods=['GET'])
def team_performance():
    # Load the CSV data into a DataFrame
    df = pd.read_csv('sales_performance_data.csv')

    # Create a column named calls by adding ('mon_call', 'tue_call', 'wed_call', 'thur_call', 'fri_call', 'sat_call', 'sun_call')
    df['calls'] = df['mon_call'] + df['tue_call'] + df['wed_call'] + df['thur_call'] + df['fri_call'] + df['sat_call'] + df['sun_call']
    df['texts'] = df['mon_text'] + df['tue_text'] + df['wed_text'] + df['thur_text'] + df['fri_text'] + df['sat_text'] + df['sun_text']

    # The dated column is as follows: 2022-07-26, create a week_number column that shows the week number of the year
    df['week_number'] = pd.to_datetime(df['dated']).dt.isocalendar().week

    # Create a day column that shows the day of the week
    df['day'] = pd.to_datetime(df['dated']).dt.day_name()

    # Drop all rows where day is not Friday
    df = df[df['day'] == 'Friday']

    # Selecting only required columns
    df = df[['employee_id', 'employee_name', 'created', 'lead_taken', 'tours_booked', 'applications', 'tours_per_lead', 'apps_per_tour',
            'apps_per_lead', 'revenue_confirmed', 'revenue_pending', 'revenue_runrate', 'tours_in_pipeline', 'estimated_revenue', 
            'tours', 'tours_runrate', 'tours_scheduled', 'tours_pending', 'tours_cancelled', 'calls', 'texts', 'week_number']]
    
    temp = df.copy()

    # group by week_number and sum the values into a single row and skip the employee_id and employee_name, for created column use min value
    temp = temp.groupby('week_number').agg({'created':'min','lead_taken':'sum','tours_booked':'sum','applications':'sum','tours_per_lead':'mean','apps_per_tour':'mean','apps_per_lead':'mean','revenue_confirmed':'sum','revenue_pending':'sum','revenue_runrate':'mean','tours_in_pipeline':'sum','estimated_revenue':'sum','tours':'sum','tours_runrate':'mean','tours_scheduled':'sum','tours_pending':'sum','tours_cancelled':'sum','calls':'sum','texts':'sum'}).reset_index()

    # Convert the DataFrame to CSV format (as a string)
    csv_data = temp.to_csv(index=False)

    # Define the prompt template
    prompt = f"""
        {csv_data}

        This is this is data for sales department, provide detailed analysis covering all the aspects and also give any useful insights that can be derived from the data. generate atleast 1500 words.
        """
    
    # Call the GPT API using the new method
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": prompt,
            },
        ],
        max_tokens=2048,
        temperature=0.7,
        top_p=1.0,
        n=1,
        stop=None
    )
    
    # Extract the generated response text
    output_text = completion.choices[0].message['content'].strip()
    
    # Return the response in HTML format
    return f"<html><body><pre>{output_text}</pre></body></html>"


@app.route('/api/performance_trends', methods=['GET'])
def performance_trends():
    # Load the CSV data into a DataFrame
    df = pd.read_csv('sales_performance_data.csv')

    # Create a column named calls by adding ('mon_call', 'tue_call', 'wed_call', 'thur_call', 'fri_call', 'sat_call', 'sun_call')
    df['calls'] = df['mon_call'] + df['tue_call'] + df['wed_call'] + df['thur_call'] + df['fri_call'] + df['sat_call'] + df['sun_call']
    df['texts'] = df['mon_text'] + df['tue_text'] + df['wed_text'] + df['thur_text'] + df['fri_text'] + df['sat_text'] + df['sun_text']

    # The dated column is as follows: 2022-07-26, create a week_number column that shows the week number of the year
    df['week_number'] = pd.to_datetime(df['dated']).dt.isocalendar().week

    # Create a day column that shows the day of the week
    df['day'] = pd.to_datetime(df['dated']).dt.day_name()

    # Drop all rows where day is not Friday
    df = df[df['day'] == 'Friday']

    # Get the time_period parameter
    time_period = request.args.get('time_period', 'monthly')

    # Validate time_period
    if time_period not in ['monthly', 'quarterly']:
        return jsonify({'error': 'Invalid time_period parameter. Must be "monthly" or "quarterly".'}), 400

    # Define a function to aggregate data based on the time_period
    def aggregate_data(df, period):
        if period == 'monthly':
            df['period'] = pd.to_datetime(df['dated']).dt.to_period('M')
        elif period == 'quarterly':
            df['period'] = pd.to_datetime(df['dated']).dt.to_period('Q')

        # Group by the specified period and aggregate
        temp = df.groupby('period').agg({'created':'min', 'lead_taken':'sum', 'tours_booked':'sum', 'applications':'sum', 
                                         'tours_per_lead':'mean', 'apps_per_tour':'mean', 'apps_per_lead':'mean',
                                         'revenue_confirmed':'sum', 'revenue_pending':'sum', 'revenue_runrate':'mean',
                                         'tours_in_pipeline':'sum', 'estimated_revenue':'sum', 'tours':'sum',
                                         'tours_runrate':'mean', 'tours_scheduled':'sum', 'tours_pending':'sum',
                                         'tours_cancelled':'sum', 'calls':'sum', 'texts':'sum'}).reset_index()
        return temp

    # Aggregate data based on time_period
    aggregated_df = aggregate_data(df, time_period)

    # Convert the DataFrame to CSV format (as a string)
    csv_data = aggregated_df.to_csv(index=False)

    # Define the prompt template
    prompt = f"""
        ### Task:
        Analyze the trends and forecast future performance based on the provided data. The data is aggregated by {time_period}.
        
        ### Data:
        {csv_data}

        ### Output Format:
        Provide detailed insights into the trends observed and any forecasts for future performance based on the data provided. Format the response in HTML using appropriate headings and bullet points. generate atleast 1500 words
    """
    
    # Call the GPT API using the new method
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": prompt,
            },
        ],
        max_tokens=2048,
        temperature=0.7,
        top_p=1.0,
        n=1,
        stop=None
    )
    
    # Extract the generated response text
    output_text = completion.choices[0].message['content'].strip()
    
    # Return the response in HTML format
    return f"<html><body><pre>{output_text}</pre></body></html>"

if __name__ == '__main__':
    app.run()
