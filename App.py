from flask import Flask, render_template
import requests

app = Flask(__name__)

# Esplora API URL
BASE_URL = "https://blockstream.info/liquid/api"

# Fetch latest blocks
def fetch_blocks(limit=10):
    try:
        response = requests.get(f"{BASE_URL}/blocks")
        response.raise_for_status()
        return response.json()[:limit]  # Limit to latest `limit` blocks
    except Exception as e:
        print(f"Error fetching blocks: {e}")
        return []

# Fetch transaction details
def fetch_transaction(txid):
    try:
        response = requests.get(f"{BASE_URL}/tx/{txid}")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching transaction {txid}: {e}")
        return {}

# Flask route for dashboard
@app.route('/')
def dashboard():
    # Fetch blocks
    blocks = fetch_blocks(limit=10)
    
    # Initialize transactions and assets
    transactions = []
    asset_distribution = {}

    if blocks:
        latest_block = blocks[0]
        tx_ids = latest_block.get("tx", [])
        
        # Fetch details for the first 5 transactions
        for txid in tx_ids[:5]:
            tx_details = fetch_transaction(txid)
            transactions.append(tx_details)
            
            # Analyze asset distribution in each transaction
            if "vout" in tx_details:
                for output in tx_details["vout"]:
                    asset_id = output.get("asset")
                    if asset_id:
                        asset_distribution[asset_id] = asset_distribution.get(asset_id, 0) + 1

    # Render template with all variables
    return render_template('dashboard.html', blocks=blocks, transactions=transactions, assets=asset_distribution)


@app.route('/asset/<asset_id>')
def asset_analysis(asset_id):
    # Fetch data for specific asset
    try:
        response = requests.get(f"{BASE_URL}/asset/{asset_id}")
        response.raise_for_status()
        asset_data = response.json()
    except Exception as e:
        return f"Error fetching asset {asset_id}: {e}"
    
    return jsonify(asset_data)

@app.route('/transaction/<txid>')
def transaction_analysis(txid):
    # Fetch details for specific transaction
    tx_data = fetch_transaction(txid)
    return jsonify(tx_data)

if __name__ == '__main__':
    app.run(debug=True)
