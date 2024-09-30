import requests

def get_orders(shopify_store_url, access_token):
    # https://shopify.dev/docs/api/usage/pagination-rest
    url = f"https://{shopify_store_url}/admin/api/2024-07/orders.json?status=any"
    headers = {
        "Content-Type": "application/json",
        "X-Shopify-Access-Token": access_token
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Query failed with status code {response.status_code}: {response.text}")

def get_order_count(shopify_store_url, access_token):
    url = f"https://{shopify_store_url}/admin/api/2024-07/count.json?status=any"
    headers = {
        "Content-Type": "application/json",
        "X-Shopify-Access-Token": access_token
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Query failed with status code {response.status_code}: {response.text}")


