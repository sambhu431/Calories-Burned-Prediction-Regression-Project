
# Importing Libraries
import pickle
from flask import Flask , render_template , request 
import pandas as pd
import logging 

# Creating a Flask Application Instance
app = Flask(__name__)

# Importing Pickle Files
xgBoostReg = pickle.load(open('pickle_files/xgbModelRegressor.pkl','rb'))
columnPreprocessor = pickle.load(open('pickle_files/columnPreprocessor.pkl','rb'))

# Label Encoding Values In Dictionary 
gender_encoding = {'Female': 0, 'Male': 1}
workout_type_encoding = {'Cardio': 0, 'HIIT': 1, 'Strength': 2, 'Yoga': 3}


# LOGGING
"""
logging.basicConfig(filename='checkLogDataFrame.log', level=logging.INFO, format='%(asctime)s - %(message)s')
def log_dataframe(df, name):
    logging.info('\n%s:\n%s', name, df)
"""

# Defining a Flask Route for Prediction
@app.route('/',methods=['GET','POST'])
def predict_datapoint():
    # Exceptional Handling
    try:
        
        # Predicted results will be stored in here and will be displayed on page
        results=""
        
        if request.method=="POST":
            # User Input Values
            Age = float(request.form.get('Age')),
            Weight = float(request.form.get('Weight')),
            Height = float(request.form.get('Height')),
            Max_BPM = float(request.form.get('Max_BPM')),
            Avg_BPM = float(request.form.get('Avg_BPM')),
            Resting_BPM = float(request.form.get('Resting_BPM')),
            Session_Duration = float(request.form.get('Session_Duration')),
            Fat_Percentage = float(request.form.get('Fat_Percentage')),
            Water_Intake = float(request.form.get('Water_Intake')),
            Workout_Frequency = float(request.form.get('Workout_Frequency')),
            Experience_Level = float(request.form.get('Experience_Level')),
            BMI = float(request.form.get('BMI')),

            gender_input = request.form.get('Gender_Encoded')
            workout_type_input = request.form.get('Workout_Type_Encoded')
            
            # Retrieving Values From Label Encoded Dictionary
            gender_numerical = gender_encoding.get(gender_input)
            workout_type_numerical = workout_type_encoding.get(workout_type_input)

            # Creating A New Dictionary With Retrieved Label Encoded Values
            genWorkDict = {
                "Gender_Encoded" : [gender_numerical],
                "Workout_Type_Encoded" : [workout_type_numerical] 
                }
            # Converting Into "genWorkDict" DataFrame
            genderWorkoutDF = pd.DataFrame(genWorkDict)

            # This log file will be helpful to determine how dataframe saves the user input
#           log_dataframe(genderWorkoutDF,"genderWorkoutDF")

            # Creating The User Input Into Dictionary To Convert Into DataFrame
            input_data = {
                'Age': Age,
                'Weight (kg)': Weight,
                'Height (m)': Height,
                'Max_BPM': Max_BPM,
                'Avg_BPM': Avg_BPM,
                'Resting_BPM': Resting_BPM,
                'Session_Duration (hours)': Session_Duration,
                'Fat_Percentage': Fat_Percentage,
                'Water_Intake (liters)': Water_Intake,
                'Workout_Frequency (days/week)': Workout_Frequency,
                'Experience_Level': Experience_Level,
                'BMI': BMI
                }
            
            # Converted The User Input Values Into "numericalFeatures" DataFrame
            numericalFeatures = pd.DataFrame(input_data)

            # Created a log to get an insight of how the dataframe is stored
#           log_dataframe(numericalFeatures,"numericalFeatures")

            # Concatenated Both "numericalFeatures" and "genderWorkoutDF" DataFrames For Further Operations
            gymCaloriesData = pd.concat([numericalFeatures,genderWorkoutDF],axis=1)

            # Created a log to get an insight of how the dataframe is stored
#           log_dataframe(gymCaloriesData,"gymCaloriesData")

            # Transforming the new DataFrame "gymCaloriesData" using imported pickle file 
            inputScaled = columnPreprocessor.transform(gymCaloriesData)
            # Predicting the scaled dataframe using imported pickle file "xgBoostReg"
            results = xgBoostReg.predict(inputScaled) 
            # This will display the 0th index of the predicted result
            results = results[0]

        return render_template('home.html',results=results)
    
    except Exception as e:
        return render_template('home.html', results=str(e))
   


if __name__ == "__main__":
    app.run(debug=True)






