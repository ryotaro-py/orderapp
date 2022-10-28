import matplotlib.pyplot as plt
import io
import base64

def Output_Graph():
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    img = buffer.getvalue()
    graph = base64.b64encode(img)
    graph = graph.decode("UTF-8")
    buffer.close()
    return graph


def plot_graph(x, y, title, ylabel):
    plt.bar(x,y)
    plt.xticks([1,2,3,4,5,6,7,8,9,10,11,12])
    plt.title(title)
    plt.xlabel("month")
    plt.ylabel(ylabel)
    graph = Output_Graph()
    return graph