# Incident Response Dashboard

This is an interactive **Incident Response Dashboard** built with **Streamlit**, **Plotly**, and **Pandas**. It allows users to visualize and analyze incident response data, including attack severity, attack types, and trends over time.

### Table of Contents:
1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Installation](#installation)
4. [Usage](#usage)
5. [Contributing](#contributing)
6. [License](#license)

## Project Overview

The **Incident Response Dashboard** provides a visual representation of incidents, attack severity, attack types, and the distribution of these parameters. The dashboard also includes filtering options based on date ranges and attack types, as well as the ability to set custom alerts for high-severity incidents.

This dashboard leverages the power of **Streamlit** for easy deployment, **Plotly** for interactive visualizations, and **Pandas** for data manipulation.

## Features

- **Data Filtering**: Filter incidents based on date ranges.
- **Attack Severity Trends**: Visualize attack severity trends over time.
- **Forecasted Attack Severity**: View the forecasted severity of incidents.
- **Attack Type Selection**: Filter the data based on specific attack types.
- **Search Functionality**: Search for specific incidents or attack types.
- **Severity Threshold Alerts**: Set custom alerts to monitor high-severity incidents.
- **Interactive Visualizations**: Utilize interactive charts for better understanding and decision-making.

## Installation

Follow these steps to set up the project locally:

1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/incident-response-dashboard.git
   cd incident-response-dashboard
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On Windows:
     ```bash
     .\venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Make sure the `data` folder is available with the `feature_engineered_incident_data.csv` file.

## Usage

1. Start the Streamlit app by running the following command:
   ```bash
   streamlit run notebooks/Dashboard.py
   ```

2. This will launch the dashboard in your default web browser.

3. You can use the provided controls (sliders, dropdowns, and search) to interact with the dashboard and view the incident data.

## Contributing

If you would like to contribute to the project, feel free to fork the repository and submit a pull request with improvements or bug fixes.

### How to Contribute:
1. Fork the repository.
2. Clone your fork:
   ```bash
   git clone https://github.com/your-username/incident-response-dashboard.git
   ```
3. Create a new branch:
   ```bash
   git checkout -b feature-branch
   ```
4. Make your changes and commit them:
   ```bash
   git commit -m "Add a feature or fix a bug"
   ```
5. Push the changes to your fork:
   ```bash
   git push origin feature-branch
   ```
6. Open a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
