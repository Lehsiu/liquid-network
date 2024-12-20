from flask import Flask, render_template, jsonify
import requests
from time import sleep

app = Flask(__name__)

# Esplora API URL
ESPLORA_BASE_URL = "https://blockstream.info/liquid/api"

# Fetch latest blocks
def fetch_blocks(limit=10):
    try:
        response = fetch_with_rate_limit(f"{ESPLORA_BASE_URL}/blocks")
        return response[:limit] if response else []  # Limit to latest `limit` blocks
    except Exception as e:
        print(f"Error fetching blocks: {e}")
        return []

# Fetch block transactions
def fetch_block_transactions(block_id):
    try:
        url = f"{ESPLORA_BASE_URL}/block/{block_id}/txs"
        print(f"Fetching transactions for block: {block_id}")
        response = requests.get(url)
        response.raise_for_status()
        txs_data = response.json()
        print(f"Transactions in block {block_id}: {txs_data}")
        return txs_data
    except Exception as e:
        print(f"Error fetching transactions for block {block_id}: {e}")
        return []

# Analyze asset details
def analyze_asset(asset_id):
    try:
        url = f"{ESPLORA_BASE_URL}/asset/{asset_id}"
        print(f"Fetching asset details from: {url}")
        response = requests.get(url)
        response.raise_for_status()
        asset_data = response.json()
        print(f"Asset data for {asset_id}: {asset_data}")

        is_lbtc = "chain_stats" in asset_data and "issuance_txin" not in asset_data
        chain_stats = asset_data.get("chain_stats", {})
        issued_amount = chain_stats.get("peg_in_amount", 0)
        burned_amount = chain_stats.get("burned_amount", 0)

    
        return {
            "is_lbtc": is_lbtc,
            "name": asset_data.get("name", "L-BTC" if is_lbtc else "Unknown"),
            "ticker": asset_data.get("ticker", "L-BTC" if is_lbtc else "Unknown"),
            "precision": asset_data.get("precision", "Unknown"),
            "issued_amount": issued_amount,
            "burned_amount": burned_amount,
            "has_blinded_issuances": chain_stats.get("has_blinded_issuances", False)
        }
    except Exception as e:
        print(f"Error analyzing asset {asset_id}: {e}")
        return {
            "is_lbtc": False,
            "name": "Unknown",
            "ticker": "Unknown",
            "precision": "Unknown",
            "issued_amount": 0,
            "burned_amount": 0,
            "has_blinded_issuances": False
        }
def format_asset_analysis(asset_analysis):
    """
    Formats the explanation for an asset analysis based on its data.
    """
    if asset_analysis["is_lbtc"]:
        explanation = (

            f"The total issued amount is {asset_analysis['issued_amount'] / 1e8:.2f} L-BTC, "
            f"withdrawals back to the Bitcoin mainnet {asset_analysis['burned_amount'] / 1e8:.2f}  "
        )
    elif asset_analysis["name"] != "Unknown":
        explanation = (
            f"The asset '{asset_analysis['name']}' (Ticker: {asset_analysis['ticker']}) is a custom asset on the Liquid Network. "
            f"It has a total issued amount of {asset_analysis['issued_amount'] / 1e8:.2f}, "
            f"with {asset_analysis['burned_amount'] / 1e8:.2f} burned. "
            f"Burning in this context usually indicates asset recovery or supply reduction."
        )
    else:
        explanation = (
            f"Unknown asset with ID {asset_analysis.get('asset_id', 'N/A')}. "
            f"No additional details are available for this asset."
        )
    
    return explanation


# Fetch data with rate limiting
def fetch_with_rate_limit(url, retry_limit=3, delay=1):
    for attempt in range(retry_limit):
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error fetching data from {url}: {e}")
            sleep(delay)
    return None

@app.route('/')
def dashboard():
    # Fetch the latest blocks
    blocks = fetch_blocks(limit=10)

    transactions = []  
    asset_distribution = {}  
    asset_explanations = []  

    
    if blocks:
        latest_block = blocks[0]
        print("Latest block data:", latest_block)

        # Fetch transactions for the latest block
        block_transactions = fetch_block_transactions(latest_block["id"])

        if block_transactions:
            for tx_details in block_transactions[:5]:  # Limit to 5 transactions
                for vout in tx_details.get("vout", []):
                    asset_id = vout.get("asset")
                    if asset_id:
                        vout["asset_analysis"] = analyze_asset(asset_id)
                        explanation = format_asset_analysis(vout["asset_analysis"])
                        asset_explanations.append({"asset_id": asset_id, "explanation": explanation})
                    else:
                        vout["asset_analysis"] = {
                            "is_lbtc": False,
                            "name": "Unknown",
                            "ticker": "Unknown",
                        }
                transactions.append(tx_details)

    print("Transactions passed to the template:", transactions)

    return render_template(
        'dashboard.html',
        blocks=blocks,
        transactions=transactions,
        assets=asset_distribution,
        asset_explanations=asset_explanations  
    )

if __name__ == '__main__':
    app.run(debug=True)
