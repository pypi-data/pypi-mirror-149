from typing import Dict, Union

datasets_metadata_dict: Dict[str, Dict[str, Union[int, str, Dict[str, str]]]] = {
    "AirfoilSelfNoise": {
        "num_of_features": 5,
        "num_of_rows": 1503,
        "target_type": "regression",
        "features": {
            "Frequency": "Integer",
            "Angle_of_Attack": "Double",
            "Chord_Length": "Double",
            "Free_Stream_Velocity": "Double",
            "Suction_thickness": "Double",
        },
        "target": {"SSPL": "Double"},
    },
    "auto_mpg": {
        "num_of_features": 7,
        "num_of_rows": 398,
        "target_type": "regression",
        "features": {
            "Cylinders": "Integer",
            "Displacement": "Double",
            "Horsepower": "Double",
            "Weight": "Integer",
            "Acceleration": "Double",
            "Model_Year": "Integer",
            "Origin": "Integer",
        },
        "target": {"MPG": "Double"},
    },
    "Sensor_Node_ALE": {
        "num_of_features": 4,
        "num_of_rows": 107,
        "target_type": "regression",
        "features": {
            "Anchor_Ratio": "Integer",
            "Trans_Range": "Integer",
            "Node_Density": "Integer",
            "Iterations": "Integer",
        },
        "target": {"Ale": "Double"},
    },
    "Bike_Sharing_Daily": {
        "num_of_features": 13,
        "num_of_rows": 731,
        "target_type": "time series regression",
        "time_index": "Date",
        "features": {
            "Date": "Datetime",
            "Season": "Integer",
            "Year": "Integer",
            "Month": "Integer",
            "Holiday": "Integer",
            "Weekday": "Integer",
            "Working_Day": "Integer",
            "Weather": "Integer",
            "Temp": "Double",
            "Humidity": "Double",
            "Wind_Speed": "Double",
            "Casual": "Integer",
            "Registered": "Integer",
        },
        "target": {
            "Count": "Integer",
        },
    },
    "Beijing_Air_Quality": {
        "num_of_features": 15,
        "num_of_rows": 35064,
        "target_type": "regression",
        "features": {
            "Year": "Integer",
            "Month": "Integer",
            "Day": "Integer",
            "Hour": "Integer",
            "PM10": "Double",
            "SO2": "Double",
            "NO2": "Double",
            "CO": "Double",
            "O3": "Double",
            "Temperature": "Double",
            "Pressure": "Double",
            "Dew_Point_Temp": "Double",
            "Rain": "Double",
            "Wind_Direction": "Categorical",
            "Wind_Speed": "Double",
        },
        "target": {
            "PM2.5": "Double",
        },
    },
    "Bike_Sharing_Hourly": {
        "num_of_features": 14,
        "num_of_rows": 17379,
        "target_type": "time series regression",
        "time_index": "Date",
        "features": {
            "Date": "Datetime",
            "Season": "Integer",
            "Year": "Integer",
            "Month": "Integer",
            "Hour": "Integer",
            "Holiday": "Integer",
            "Weekday": "Integer",
            "Working_Day": "Integer",
            "Weather": "Integer",
            "Temp": "Double",
            "Humidity": "Double",
            "Wind_Speed": "Double",
            "Casual": "Integer",
            "Registered": "Integer",
        },
        "target": {
            "Count": "Integer",
        },
    },
}
