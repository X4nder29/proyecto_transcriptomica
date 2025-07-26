from workers import CheckWorker


class AppState:

    java_check_worker = CheckWorker(["java", "--version"])
    wsl_check_worker = CheckWorker(["wsl", "--version"])
    kraken2_check_worker = CheckWorker(["wsl", "which", "kraken2"])
    krona_check_worker = CheckWorker(["wsl", "which", "ktImportText"])
