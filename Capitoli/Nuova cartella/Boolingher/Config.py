
class Config:
    CSV_DATA_DIR = "c:/Users/Gabriele/Documents/GitHub/TESI_GATTO_GABRIELE/Capitoli/Nuova cartella/Boolingher/CSV_Folder"
    initial_equity = 500000.00

    market_data = {
        "source": "csv",
        "frequency": "daily",
        "start_date": "2010-01-01",
        "end_date": "2013-09-01"
    }

    strategy = {
        "lookback": 15,
        "entry_z": 1.5,
        "exit_z": 0.5,
        "base_quantity": 10000,
        "weights": [1.0, -1.213]
    }
    