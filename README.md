
# Google Play Store Bubble Chart Dashboard

## Project Overview

This project is an interactive Streamlit dashboard that analyzes
Google Play Store applications using a Bubble Chart.

The dashboard visualizes the relationship between:

- Application Size (MB)
- Average Application Rating
- Number of Installs

The dashboard uses two datasets:

1. Play Store Data(3).csv
2. User Reviews(3).csv

## Technologies Used

- Python
- Streamlit
- Pandas
- NumPy
- Plotly
- Regular Expressions

## Project Structure

PlayStore_Bubble_Chart/
│
├── app.py
├── requirements.txt
├── README.md
├── Play Store Data(3).csv
└── User Reviews(3).csv

## Data Processing

The application performs the following operations:

1. Loads the Play Store dataset.
2. Loads the User Reviews dataset.
3. Cleans application size values.
4. Converts application sizes into MB.
5. Converts install counts into numerical values.
6. Calculates average sentiment subjectivity for each app.
7. Merges both datasets using the App column.
8. Applies the specified filtering conditions.
9. Generates an interactive Plotly Bubble Chart.

## Filtering Conditions

The following conditions are applied:

- Rating must be greater than 3.5.
- Category must belong to the specified nine categories.
- Reviews must be greater than 500.
- App name must not contain the letter S (case-insensitive).
- Average sentiment subjectivity must be greater than 0.5.
- Installs must be greater than 50,000.
- App size must be available.

## Categories and Translations

| Original Category | Graph Display |
|-------------------|---------------|
| Game | Game |
| Beauty | सौंदर्य |
| Business | வணிகம் |
| Comics | Comics |
| Communication | Communication |
| Dating | Partnersuche |
| Entertainment | Entertainment |
| Social | Social |
| Events | Events |

## Bubble Chart Configuration

- X-axis: Application Size (MB)
- Y-axis: Average Rating
- Bubble Size: Number of Installs
- Bubble Color: Application Category
- Game Category: Pink (#FF69B4)

Hovering over a bubble displays:

- App Name
- Category
- Application Size
- Rating
- Number of Reviews
- Number of Installs
- Average Sentiment Subjectivity

## Time Restriction

The Bubble Chart is available only between:

5:00 PM IST and 7:00 PM IST.

Outside this time window, the chart is hidden and a warning
message is displayed.

The dashboard checks the time every 60 seconds.

## Installation Instructions

### Step 1: Create a Virtual Environment

Windows:

python -m venv venv

### Step 2: Activate Virtual Environment

Windows CMD:

venv\Scripts\activate

PowerShell:

.\venv\Scripts\Activate.ps1

### Step 3: Install Dependencies

pip install -r requirements.txt

### Step 4: Run the Application

streamlit run app.py

### Step 5: Open Dashboard

The application normally opens at:

http://localhost:8501

## Deployment

The application can be deployed using Streamlit Community Cloud.

1. Upload the project to GitHub.
2. Open Streamlit Community Cloud.
3. Connect your GitHub repository.
4. Select app.py as the main file.
5. Deploy the application.

## Expected Output

The dashboard displays:

1. Total Applications.
2. Average Rating.
3. Average Application Size.
4. Total Installs.
5. Interactive Bubble Chart.
6. Category Selection Filter.
7. Filtered Application Details.
8. Download Filtered Data option.

## Author

Google Play Store App Analysis
Interactive Data Visualization Project
