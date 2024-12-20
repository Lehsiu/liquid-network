# Plan B Assignment

**Author**: Ivy (@lehsiuchen)

---

## Introduction

This assignment focuses on **Liquid Network**, designing:
- A **backend Flask application** for data fetching and processing.
- A **frontend dashboard** for visualized data representation.

The application integrates **Blockstream Esplora API** to:
- Fetch the latest blocks, transactions, and asset analysis.
- Analyze asset details, including **Liquid Bitcoin (L-BTC)**.
- Provide user-friendly insights through visualized data.

This report outlines the implementation and explains the principles briefly.

---

## Backend Implementation

### 1. Fetching Blocks and Transactions
- Blocks and transactions are fetched using the **Esplora API**.
- A retry mechanism is implemented to prevent API overload, ensuring responsible usage of public explorers.

### 2. Asset Analysis
- Identifies whether an asset is **L-BTC** or a custom token.
- Extracts details such as:
  - Asset name
  - Issued amount
  - Burned amount
- Generates user-friendly explanations.

### 3. Logic and Tooling
- Enables data fetching for other time periods.
- Supports multiple transaction patterns, including:
  - **Multisig usage**
  - **Explicit outputs**
  - **Single-asset transactions**

---

## Frontend Implementation

- **Flask templates** render:
  - Blocks
  - Transactions
  - Asset analysis results
- **Chart.js** visualizes transaction counts for the latest blocks.

### Features:
1. **Responsive Design**: Ensures compatibility across devices.
2. **Auto-Refresh**: Automatically refreshes every two minutes to maintain data freshness.

---

## Principles and Improvements

### Principles:
- The **Liquid Network**, a Bitcoin sidechain, provides high transaction privacy with assets like **L-BTC** and custom tokens.
- The application:
  - Uses APIs to fetch transactions.
  - Analyzes output scripts and transaction patterns, such as multisig usage.

### Suggested Improvements:
1. **Local Node Support**:
   - Reduce dependency on public APIs by deploying a local node.
2. **Advanced Pattern Recognition**:
   - Enhance analysis to identify specific patterns like **Boltz swaps**.

---

## Achievements and Future Plans

### Achievements:
- Demonstrated fundamental transaction analysis on Liquid Network.
- Combined backend data processing with frontend visualization.

### Future Goals:
1. Add local node integration to reduce reliance on public APIs.
2. Enhance pattern recognition for more complex transaction types.

---

## How to Use This Project

### Prerequisites:
- **Python 3.x** installed
- Install Flask and required dependencies:
  ```bash
  pip install flask requests chart.js
- Run the Flask application:
  ```bash
  python app.py
- Open browser and visit:
  ```bash
  http://127.0.0.1:5000
