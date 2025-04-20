# 🔍 Data De-duplication Web App

This Streamlit app allows users to upload a CSV file, automatically identify and merge duplicate account records based on name similarity and email matching, and download a clean, de-duplicated dataset.

## 🚀 Features

- Upload CSV files containing customer/account data
- Fuzzy matching using name and email fields
- Set similarity threshold (tunable slider)
- Automatic merging of duplicate records
- Download cleaned data as a CSV file

## 📁 Expected Input Format

The uploaded CSV should include at least the following columns:

- `id`: Unique identifier for each record
- `name`: Full name of the person or account
- `email`: Email address of the person or account

Optional fields (e.g., `phone`, `address`, etc.) will be preserved in the final output.

### 🧪 Sample Input

| id | name        | email             | phone      |
|----|-------------|-------------------|------------|
| 1  | John Smith  | john@example.com  | 1234567890 |
| 2  | Jon Smyth   | john@example.com  | 1234567890 |
| 3  | Jane Doe    | jane@example.com  | 0987654321 |
| 4  | J. Smith    | john@example.com  | 1234567890 |

## 🛠️ How It Works

1. Fuzzy match names using `fuzzywuzzy.token_sort_ratio`
2. Confirm match by exact email
3. Group and merge matched pairs
4. Keep lowest `id` as the master record

## 📦 Tech Stack

- [Streamlit](https://streamlit.io/)
- [Pandas](https://pandas.pydata.org/)
- [FuzzyWuzzy](https://github.com/seatgeek/fuzzywuzzy)

## 🧑‍💻 Run Locally

```bash
pip install -r requirements.txt
streamlit run dedup_app.py
