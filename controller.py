from crawler import crawler
from persistencia import grava_pg
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    df = crawler()
    grava_pg(df)

if __name__ == '__main__':
    main()