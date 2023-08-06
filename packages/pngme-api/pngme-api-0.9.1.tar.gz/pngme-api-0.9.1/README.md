<p align="center">
  <img src="https://admin.pngme.com/logo.png" alt="Pngme" width="100" height="100">
</p>

<h3 align="center">Python API Client</h3>

This package exposes a synchronous and asynchronous client used to interact with Pngme's financial data APIs.

## Install

Install the latest version with:

```bash
pip3 install pngme-api
```

## Quick start

Create a `Client` instance using your API `token` found in the [Pngme Dashboard](https://admin.pngme.com):

```python
from pngme.api import Client

token = "" # your API token
client = Client(token)
```

> If you're using [`asyncio`](https://docs.python.org/3/library/asyncio.html), you can import and use the `AsyncClient` instead. See [using with asyncio](#using-with-asyncio).

We can list or search the available [`/users`](https://developers.api.pngme.com/reference/get_users):

```python
users = client.users.get()
users = client.users.get(search="2343456789012")
```

For a user of interest, we can get a list of the user's [`/institutions`](https://developers.api.pngme.com/reference/get_users-user-uuid-institutions):

```python
user_uuid = "33b6215d-3d75-4271-801c-6da27603a8be"

institutions = client.institutions.get(user_uuid=user_uuid)
```

Then for a given institution, we can get a list of the user's [`/transactions`](https://developers.api.pngme.com/reference/get_users-user-uuid-institutions-institution-id-transactions), [`/balances`](https://developers.api.pngme.com/reference/get_users-user-uuid-institutions-institution-id-balances), or [`/alerts`](https://developers.api.pngme.com/reference/get_users-user-uuid-institutions-institution-id-alerts):

```python
user_uuid = "33b6215d-3d75-4271-801c-6da27603a8be"
institution_id = "zenithbank"

transactions = client.transactions.get(user_uuid=user_uuid, institution_id=institution_id)
balances = client.balances.get(user_uuid=user_uuid, institution_id=institution_id)
alerts = client.alerts.get(user_uuid=user_uuid, institution_id=institution_id)
```

## asyncio

We can make multiple requests concurrently using `asyncio` by creating a `Client` instance with your API `token` found in the [Pngme Dashboard](https://admin.pngme.com):

```python
from pngme.api import AsyncClient

token = "" # your API token
client = AsyncClient(token)
```

Similar to the synchronous `Client`, we can list or search the available [`/users`](https://developers.api.pngme.com/reference/get_users):

```python
async def get_users(client: AsyncClient):
    users = await client.users.get()
    return users

users = asyncio.run(get_users(client))
```

This is helpful to concurrently execute multiple requests, such as fetching a user's transaction history across all accounts by iterating over institutions associated with a user:

```python
async def get_transactions(client: AsyncClient, user_uuid: str):
    # Find institutions where the user has one or more accounts
    institutions = await client.institutions.get(user_uuid)

    # Concurrently fetch transactions for all institutions
    institution_ids = [institution.institution_id for institution in institutions]
    coroutines = [
        client.transactions.get(user_uuid, institution_id)
        for institution_id in institution_ids
    ]
    transactions = await asyncio.gather(*coroutines)

    # Associate transactions with the relevant institution_id
    return dict(zip(institution_ids, transactions))

user_uuid = "33b6215d-3d75-4271-801c-6da27603a8be"
transactions = asyncio.run(get_transactions(client, user_uuid))
```

## Next steps

* Browse the Pngme [Feature Library](https://github.com/pngme/pngme-feature-library) to see how data scientists integrate our APIs into decisioning workflows
* Explore the definitions of each response field in the [API Docs](https://developers.api.pngme.com/reference/getting-started-with-your-api)
