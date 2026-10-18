import pandas as pd
from pathlib import Path
from IPython.display import display
# from postgres_sql.connector import connect

company_csv_path = Path(r"F:\Kodowanie\git_my\ML_Stock\data\company.csv")
df_stock_metadata=pd.read_csv(company_csv_path)
display(df_stock_metadata)

df_stock_metadata_agg = (
    df_stock_metadata
    .pivot(index=["symbol", "company_name"], columns="field", values="value")
    .reset_index()
)

display(df_stock_metadata_agg)
print(df_stock_metadata_agg.columns)
# query = "SELECT * FROM stock_data.metadata"

# with connect() as connection:
#     cursor = connection.cursor()
#     cursor.execute(query)
#     rows = cursor.fetchall()
#     columns = [column[0] for column in cursor.description]

# df_from_db = pd.DataFrame.from_records(rows, columns=columns)
# display(df_from_db)