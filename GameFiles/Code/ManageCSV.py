from csv import reader


def import_csv(path):
    layout = []
    with open(path) as map:
        area = reader(map, delimiter = ',')
        for row in area: layout.append(list(row))
    return layout

def import_csv_layer(layout):
    layers = []
    for key,val in layout.items():
        csv = (key, import_csv(val))
        layers.append(csv)
    return layers