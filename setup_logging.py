import logging
def setup_logging():
    # Configuration du logging pour inclure le nom du fichier et la ligne de code
    logging.basicConfig(
        level=logging.INFO,
        #format='%(asctime)s - %(levelname)s - %(filename)s - line %(lineno)d - %(message)s',
        format='%(asctime)s - %(filename)s - %(message)s',
        handlers=[logging.StreamHandler()]
    )
    logging.info("Logging setup completed\n")