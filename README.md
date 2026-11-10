# RECOMMENDATIONS FOR TYPE CAR SELECTION SYSTEM USING K-NEAREST NEIGHBOR (KNN) COLLABORATIVE FILTERING (WEB BASED)

Final Project

A car is vehicle that is very much needed at this time. Many of the users when they want to choose a car only know some of the information they like without knowing the information of other similar cars. Car selection system recommendation is a system that can be used by users in choosing a car. By applying car selection recommendations, users will get more information about the car they want to choose and other cars that may not be known by the user at all. In the recommendation of the car selection system, the authors apply the K-Nearest Neighbor (KNN) Collaborative Filtering method based on web applications where recommendations are made based on the proximity of testing data to training data. The proximity of the data (data similarity) is used to recommend the car to the user. The final results obtained in this Final Project are to help provide car recommendations that are in accordance with the wishes of the application users and a web-based application of the Car Selection System Recommendation with the KNN method.

## About

This repository contains a web-based **Car Selection System Recommendation** built using the **K-Nearest Neighbor (KNN) Collaborative Filtering** algorithm. The system helps users discover cars that match their preferences by finding similar vehicles based on user ratings and car features.

### Key Features

- **KNN Collaborative Filtering** — Recommends cars by computing similarity between user ratings and car attributes.
- **Web-Based Application** — Built with Python (Flask/Django) and served as a web application.
- **CSV Data Import** — Supports importing car data and user ratings from CSV files.
- **Dynamic Rating Update** — Allows users to update ratings for cars to refine recommendations.

### Technologies Used

- Python
- Flask / WSGI
- Pandas / NumPy (for data handling and KNN computations)
- CSV data storage

### How It Works

1. The system loads car data and user ratings from CSV files.
2. When a user selects a car, the KNN algorithm computes the similarity between that car and all other cars.
3. The most similar cars (nearest neighbors) are recommended to the user.
4. Users can update their ratings to improve future recommendations.

### Project Structure

```
.
├── cari.py              # Main application logic and KNN recommendation engine
├── importcsv.py         # CSV import utility
├── updaterating.py      # Rating update utility
├── wsgi.py              # WSGI entry point for web deployment
├── Database/            # Contains training and testing datasets
├── static/              # Static assets (CSS, JS, images)
├── templates/           # HTML templates
└── requirements.txt     # Python dependencies
```

### How to Run

```bash
pip install -r requirements.txt
python wsgi.py
```

Open your browser and navigate to the local server URL (typically `http://localhost:8000` or as shown in the console output).

### License

See [LICENSE](LICENSE) for details.
