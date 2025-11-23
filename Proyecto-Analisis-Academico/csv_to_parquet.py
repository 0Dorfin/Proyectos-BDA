import pandas as pd
from pathlib import Path

ruta_csv = Path('C:/Users/Dorfin/Documents/prueba')
ruta_parquet = Path('C:/Users/Dorfin/Documents/Parquet')
ruta_parquet.mkdir(exist_ok=True)

for f in ruta_csv.glob('*.csv'):
    df = pd.read_csv(f)
    out = ruta_parquet / (f.stem + ".parquet")
    df.to_parquet(out, engine='pyarrow', compression='snappy')
