from toolbox import SQLConnection

con = SQLConnection(read_only=False).con
print('connected')
print(con.execute("""select * from universe.CRSP_US_3000""").fetchdf().info())
con.close()