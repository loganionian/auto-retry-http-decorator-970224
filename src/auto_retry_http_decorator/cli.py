import click
import requests
from auto_retry import retry

@click.command()
@click.argument("url")
@click.option("--max-attempts", default=3, help="Maximum number of retry attempts.")
@click.option("--delay", default=1, help="Initial delay in seconds before retrying.")
def cli(url, max_attempts, delay):
    """
    CLI for fetching data from a URL with retry logic.

    URL is the endpoint to fetch data from.
    """
    @retry(max_attempts=max_attempts, delay=delay)
    def fetch_data(url):
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    try:
        data = fetch_data(url)
        click.echo(data)
    except Exception as e:
        click.echo(f"Failed to fetch data: {e}", err=True)

if __name__ == "__main__":
    cli()