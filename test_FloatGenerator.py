# test_float_generator.py

from floatGenerator import FloatGenerator
import time
import pytest
from math import isclose
import logging
import plotly.express as px
import pandas as pd

stop_on_first_error = True

def plot_float_data(csv_file, min_value, max_value):
    # Read the CSV file
    df = pd.read_csv(csv_file)
    df.columns = ['Timestamp', 'Float Generated']
    df['Min Limit'] = min_value
    df['Max Limit'] = max_value


    # Create the plot
    fig = px.scatter(df, x='Timestamp', y='Float Generated', title='Float Generated Over Time')

    # Add lines for the min and max limits
    fig.add_scatter(x=df['Timestamp'], y=df['Min Limit'], mode='lines', name='Min Limit')
    fig.add_scatter(x=df['Timestamp'], y=df['Max Limit'], mode='lines', name='Max Limit')

    # Layout Settings
    fig.update_layout(
        xaxis_title='Timestamp',
        yaxis_title='Float Value',
        hovermode='closest'
    )

    # Save the plot as an HTML file
    html_file = f'plotly.html'
    fig.write_html(html_file)



@pytest.mark.parametrize("min_value, max_value", [(27.0, 43.0)])
def test_random_float_generator(min_value, max_value,request):

    #Stores Failure floats usefull if stop_on_first_error is set to False
    out_of_range_values = []

    #Create a generator instance and start it on a new thread
    generator = FloatGenerator()
    generator.start()

    #Initialize the start and end time for the test loop
    start_time = time.time()
    end_time = start_time + generator.minutes


    while time.time() < end_time:
        #Wait for float to be generated in the other thread
        time.sleep(generator.secondperfloat)

        #When the first value is generated start testing
        if generator.values:
            
            #Test the last generated value
            value = generator.values[-1]

            """
            Reading from csv instead of the array could be better to save memory
            df = pd.read_csv('float.csv')
            value = df[Float Generated].iloc[-1]
            
            """
            

            #If the float is clearly less than the other values the last gate is opened
            #If the floating point values are nearly equal instead we use math.isclose to open the gate
            if not (isclose(value, min_value, abs_tol=1e-9) or isclose(value, max_value, abs_tol=1e-9) or (min_value < value < max_value)):

                #log the failure as critical and add them into the list
                logging.critical(f"Value out of range: {value}")
                out_of_range_values.append(value)
                
                #if we are stoping the test on the first error stop the thread and then stop the test by asserting False
                if stop_on_first_error:
                    generator.stop()
                    plot_float_data('float.csv', min_value, max_value) #make a plot of the stored data so far
                    request.node.out_of_range_count = len(out_of_range_values) # Can also be replaced with = 1 and provide same functionality
                    assert False, f"Value out of range: {value}"

    #when all the test are finsihed stop the thread and make plot of the data stored in the csv
    generator.stop()

    #if stop_on_first_error is set to false then assert all the float out of the bound now
    if not stop_on_first_error:
        request.node.out_of_range_count = len(out_of_range_values)
        plot_float_data('float.csv', min_value, max_value)
        assert not out_of_range_values, f"Found out-of-range values: {out_of_range_values}"
    
    plot_float_data('float.csv', min_value, max_value)