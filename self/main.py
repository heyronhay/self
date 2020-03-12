import click

@click.command()
def main():
    with open("test.txt", "w") as f:
        f.write("blah")

    print("Main!")