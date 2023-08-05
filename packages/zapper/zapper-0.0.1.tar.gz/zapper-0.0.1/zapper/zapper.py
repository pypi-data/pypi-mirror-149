from email.policy import default
import json
import click
from zapper.utils import process_file

@click.command()
@click.option('--url', prompt="Enter url to download the file", help="Provide url")
@click.option("--con",help="Number of concurrent connections", default=4, type=int)
def zapp(url, con):
    """Zapper is a utility to help download files concurrently"""
    process_file(url, con)

    


    

def main():
    zapp()

if __name__=="__main__":
    main()