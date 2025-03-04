# Price Monitoring and Violation Detection System

## 📌 Project Overview
In today's competitive market, **product manufacturers** are highly concerned about maintaining their **brand value**. When unauthorized or third-party sellers list a product at a price lower than the **Minimum Advertised Price (MAP)**, it can **decrease the brand's value and impact sales margins**. To tackle this issue, manufacturers and retailers actively monitor seller pricing across various e-commerce platforms.

This system provides an **automated solution** to monitor and track price violations across multiple marketplaces, ensuring compliance with MAP policies.

## 🚀 Key Features
- **Web Scraping** – Collects seller pricing data from multiple e-commerce websites.
- **Dynamic Exchange Rate Handling** – Converts prices based on real-time exchange rates.
- **Threshold-Based Violation Detection** – Identifies sellers exceeding violation limits based on predefined thresholds.
- **Automated Data Processing** – Stores and processes price data efficiently.
- **Database Management** – Organizes and updates violation records for easy tracking.

## 📊 Project Workflow (Pipeline)
1. **Web Scraping** – Extracts seller pricing data from multiple e-commerce websites.
2. **Data Storage** – Stores collected data in a **MySQL database**.
3. **Currency Conversion** – Converts prices to a uniform currency using real-time exchange rates through API.
4. **Price Monitoring** – Compares seller prices with MAP and checks for violations.
5. **Violation Detection** – Identifies sellers exceeding the threshold count of violations.
6. **Reporting & Storage** – Saves violating sellers in a dedicated database table for review.

## 🛠️ Technologies Used
- **Programming Language**: Python 🐍
- **Database**: MySQL 🗄️
- **Web Scraping**: BeautifulSoup, Selenium🌐
- **Currency Conversion**: API-based exchange rate retrieval 💱
- **Data Processing**: Pandas, MySQL 📊

## 📂 Project Structure
```
├── main.py                  # Entry point to run the pipeline
├── store_data.py            # Stores seller price data in MySQL
├── violated_sellers.py      # Identifies sellers exceeding violation thresholds
├── db_connection.py         # Manages database connections
├── currency_cache.py        # Handles exchange rate caching and API requests
├── region_to_curr.py        # Maps regions to currency codes
├── thresholds.json          # Stores predefined violation thresholds
├── config.py                # Configuration file for API keys & database details
└── README.md                # Project documentation
```

## 🔧 Setup Instructions
1. **Clone the Repository**
```bash
git clone <repo_url>
cd <project_directory>
```

2. **Set Up a Virtual Environment (Optional but Recommended)**
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

3. **Install Required Dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure API Keys & Database**
- Update **config.py** with API credentials and database details.

5. **Run the Project**
```bash
python main.py
```

## 📈 Future Enhancements
- **Automated Email Notifications** – Alert manufacturers when sellers violate MAP policies.
- **Dashboard for Visualization** – Interactive UI to monitor price trends and violations.

---
🚀 **With this system, manufacturers can efficiently track price violations, ensuring their brand value remains intact!**
