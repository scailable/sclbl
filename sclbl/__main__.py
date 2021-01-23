import click

@click.group()


def main():
    print("print main..")

@main.command()
def upload():
    print("upload")

if __name__ == '__main__':
    print("test sclbl")
    main()