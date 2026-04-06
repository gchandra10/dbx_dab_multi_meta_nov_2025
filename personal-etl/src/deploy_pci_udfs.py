import sys

catalog = sys.argv[1]
schema = sys.argv[2]

# spark.sql(f"""
#   CREATE OR REPLACE FUNCTION {catalog}.{schema}.encrypt_pci(col STRING)
#   RETURNS BINARY
#   RETURN base64(aes_encrypt(
#     col,
#     secret('secret_scope', 'secret_key')
#   ))
# """)

spark.sql(f"""
  CREATE OR REPLACE FUNCTION {catalog}.{schema}.encrypt_pci(col STRING)
  RETURNS STRING
  RETURN base64(aes_encrypt(col, 'hardcoded_4_demo'))
""")


# spark.sql(f"""
#   CREATE OR REPLACE FUNCTION {catalog}.{schema}.decrypt_pci(cipher_b64 STRING)
#   RETURNS STRING
#   RETURN CAST(
#     aes_decrypt(
#       unbase64(cipher_b64),
#       secret('secret_scope', 'secret_key')
#     ) AS STRING
# )          
# """)

spark.sql(f"""
  CREATE OR REPLACE FUNCTION {catalog}.{schema}.decrypt_pci(cipher_b64 STRING)
  RETURNS STRING
  RETURN CAST(
    aes_decrypt(unbase64(cipher_b64), 'hardcoded_4_demo') AS STRING
  )
""")