# 📊 App Size vs Average Rating - Bubble Chart Dashboard

A Python-based interactive data visualization dashboard that analyzes the relationship between mobile application size and average rating.

## 📌 Project Overview

This project uses Google Play Store application data and sentiment subjectivity information to create an interactive Plotly bubble chart.

The dashboard analyzes:

- App Size (MB)
- Average Rating
- Number of Installs
- Reviews
- Sentiment Subjectivity
- Application Categories

## 🎯 Filtering Conditions

The dashboard applies the following conditions:

- Average Rating > 3.5
- Reviews > 500
- Installs > 50,000
- Sentiment Subjectivity > 0.5
- App name must not contain the letter "S"
- Categories:
  - Game
  - Beauty
  - Business
  - Comics
  - Communication
  - Dating
  - Entertainment
  - Social
  - Events

## 📊 Visualization

The bubble chart represents:

- X-axis → App Size (MB)
- Y-axis → Average Rating
- Bubble Size → Number of Installs
- Color → App Category

The Game category is highlighted in pink.

## 🌐 Category Translation

| Category | Display Language |
|---|---|
| Beauty | Hindi |
| Business | Tamil |
| Dating | German |

## ⏰ Time Restriction

The visualization is available only between:

**5:00 PM – 7:00 PM IST**

Outside this time window, the dashboard hides the bubble chart.

## 🛠️ Technologies Used

- Python
- Pandas
- Plotly
- Dash
- Dash Bootstrap Components
- CSV Dataset

## 🚀 How to Run

Clone the repository:

```bash
git clone YOUR_GITHUB_REPOSITORY_URL