import click
import os

FIGURE_EXTENSIONS = ['png', 'jpg', 'eps', 'ps']


@click.command()
@click.argument('path')
@click.option('-e', '--extension')
def main(path, extension):
    if not os.path.exists(path):
        print("Path doesn't exist", path)
        return 1

    figures = []
    # look for all figures in project
    for root, dirt, find_file in os.walk(path):
        for file in find_file:
            if file[file.find('.') + 1:] in FIGURE_EXTENSIONS:
                if extension:
                    figures.append(file)
                else:
                    figures.append(file[:file.find('.')])

    # scan all TEX  files looking for references to figures
    for root, dirt, find_file in os.walk(path):
        for file in find_file:
            if file[-4:] != '.tex':
                continue

            fs = open(os.path.join(root, file), 'r')
            data = fs.read()

            for figure in figures:
                if figure in data:
                    figures.remove(figure)
            fs.close()
    print(figures)
    return 0


if __name__ == '__main__':
    main()
