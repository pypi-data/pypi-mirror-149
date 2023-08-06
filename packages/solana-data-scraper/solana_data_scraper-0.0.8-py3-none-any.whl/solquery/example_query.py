import os
from query import Query

# Get API key associated with user's environment
API_KEY = os.environ.get("BITQUERY_API_KEY")
print(f"Bitquery API Key used: {API_KEY}")

# Create query object with API key
query = Query(API_KEY)

# Query to get random transfers
QUERY = """
query MyQuery {
  solana(network: solana) {
    instructions: instructions(
      success: {is: true}
      options: {limit: 10}
      time: {after: "2022-04-29T00:00:00"}
      programId: {is: "So1endDq2YkqhipRh3WViPa8hdiSpxWy6z3Z6tMCpAo"}
    ) {
      program {
        id
        name
        parsedName
      }
      action {
        name
        type
      }
      data {
        base58
      }
      external
      transaction {
        signature
        success
        transactionIndex
        feePayer
      }
      accountsCount
    }
  }
}
"""
result = query.run(QUERY, to_df=True)
print(f"Results: {result}")

# Query to get random transfers
QUERY = """
    query MyQuery {
      solana(network: solana) {
        transfers(
          time: {between: ["%s", "%s"]}
          options: {limit: 25000}
          success: {is: true}
          receiverAddress: {is: "DdZR6zRFiUt4S5mg7AV1uKB2z1f1WzcNYCaTEEWPAuby"}
        ) {
          amount
          transaction {
            signer
            signature
          }
          block {
            timestamp {
              iso8601
            }
          }
          currency {
            address
            decimals
          }
        }
      }
    }
"""

# This example takes a long time to run
result = query.run_batch(
    QUERY, "2022-04-28T00:00:00", "2022-05-01T00:00:00", batch_freq="6H"
)
print(f"Results: {result}")
print(result.shape)
result.to_csv("./example.csv", index=False)
