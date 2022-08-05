from concepts import Context

r = Context.fromfile('concepts_data.csv', frmat='csv')

r.lattice.graphviz(view=True)