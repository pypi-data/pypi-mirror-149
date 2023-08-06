# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['solquery']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.22.3,<2.0.0', 'pandas>=1.4.2,<2.0.0', 'requests>=2.27.1,<3.0.0']

setup_kwargs = {
    'name': 'solana-data-scraper',
    'version': '0.0.8',
    'description': 'Python library for scraping blockchain data from Bitquery',
    'long_description': '# Scrape Solana Blockchain Data\n\nThis python library scrapes blockchain from https://bitquery.io/ from their GraphQL endpoints.\n\nThis requires you to supply your own Bitquery API token.\n\nCopyright (c) 2022 Friktion Labs\n\n# Functionalities\n\n- Queries Bitquery for blockchain data\n- Batches queries to get around compute limits\n\n# Setup\n\n1. `pip3 install solana-data-scraper`\n2. Create an account at https://bitquery.io/\n3. Retrieve API Key\n4. In command line, `export BITQUERY_API_KEY=XXXXXXX`\n\n# Example\n\n```\nimport os\nfrom solquery.Query import Query\n\n# Get API key associated with user\'s environment\nAPI_KEY = os.environ.get("BITQUERY_API_KEY")\nprint(f"Bitquery API Key used: {API_KEY}")\n\n# Create query object with API key\nquery = Query(API_KEY)\n\n# Query to get random transfers\nQUERY = """\nquery MyQuery {\n  solana(network: solana) {\n    instructions: instructions(\n      success: {is: true}\n      options: {limit: 10}\n      time: {after: "2022-04-29T00:00:00"}\n      programId: {is: "So1endDq2YkqhipRh3WViPa8hdiSpxWy6z3Z6tMCpAo"}\n    ) {\n      program {\n        id\n        name\n        parsedName\n      }\n      action {\n        name\n        type\n      }\n      data {\n        base58\n      }\n      external\n      transaction {\n        signature\n        success\n        transactionIndex\n        feePayer\n      }\n      accountsCount\n    }\n  }\n}\n"""\nresult = query.run(QUERY, to_df=True)\nprint(f"Results: {result}")\n\n# Query to get random transfers\nQUERY = """\n    query MyQuery {\n      solana(network: solana) {\n        transfers(\n          time: {between: ["%s", "%s"]}\n          options: {limit: 25000}\n          success: {is: true}\n          receiverAddress: {is: "DdZR6zRFiUt4S5mg7AV1uKB2z1f1WzcNYCaTEEWPAuby"}\n        ) {\n          amount\n          transaction {\n            signer\n            signature\n          }\n          block {\n            timestamp {\n              iso8601\n            }\n          }\n          currency {\n            address\n            decimals\n          }\n        }\n      }\n    }\n"""\n\n# This example takes a long time to run\nresult = query.run_batch(\n    QUERY, "2022-04-28T00:00:00", "2022-05-01T00:00:00", batch_freq="6H"\n)\nprint(f"Results: {result}")\nprint(result.shape)\nresult.to_csv("./example.csv", index=False)\n```\n',
    'author': 'thiccythot',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://app.friktion.fi',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
