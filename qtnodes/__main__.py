"""Manual tests."""

from PySide2 import QtWidgets

from .knob import InputKnob, OutputKnob
from .header import Header
from .node import Node
from .widget import NodeGraphWidget


class Integer(Node):

    def __init__(self, *args, **kwargs):
        super(Integer, self).__init__(*args, **kwargs)
        self.addHeader(Header(node=self, text="Int"))
        self.addKnob(OutputKnob(name="value"))
        self.value = 0
        # self.header.fillColor = QtGui.QColor(36, 128, 18)

    def run(self):
        self.knob("value").send(self.value)


class Float(Node):

    def __init__(self, *args, **kwargs):
        super(Float, self).__init__(*args, **kwargs)
        self.addHeader(Header(node=self, text="Float"))
        self.addKnob(OutputKnob(name="value"))
        self.value = 0
        # self.header.fillColor = QtGui.QColor(24, 129, 163)

    def run(self):
        self.knob("value").send(self.value)


class Multiply(Node):

    def __init__(self, *args, **kwargs):
        super(Multiply, self).__init__(*args, **kwargs)
        self.addHeader(Header(node=self, text=self.__class__.__name__))
        self.addKnob(InputKnob(name="x"))
        self.addKnob(InputKnob(name="y"))
        self.addKnob(OutputKnob(name="value"))
        # self.header.fillColor = QtGui.QColor(163, 26, 159)

    def run(self):
        result = self.data["x"] * self.data["y"]
        self.knob("value").send(result)


class Divide(Multiply):

    def __init__(self, *args, **kwargs):
        super(Divide, self).__init__(*args, **kwargs)
        # self.header.fillColor = QtGui.QColor(26, 163, 159)

    def run(self):
        result = self.data["x"] / self.data["y"]
        self.knob("value").send(result)


class Add(Multiply):

    def __init__(self, *args, **kwargs):
        super(Add, self).__init__(*args, **kwargs)
        # self.header.fillColor = QtGui.QColor(105, 128, 23)

    def run(self):
        result = self.data["x"] + self.data["y"]
        self.knob("value").send(result)


class Subtract(Multiply):

    def __init__(self, *args, **kwargs):
        super(Subtract, self).__init__(*args, **kwargs)
        # self.header.fillColor = QtGui.QColor(23, 51, 128)

    def run(self):
        result = self.data["x"] - self.data["y"]
        self.knob("value").send(result)


class Output(Node):

    def __init__(self, *args, **kwargs):
        super(Output, self).__init__(*args, **kwargs)
        self.addHeader(Header(node=self, text="Output"))
        self.addKnob(InputKnob(name="output"))
        # self.header.fillColor = self.fillColor
        # self.header.textColor = QtGui.QColor(10, 10, 10)

    def run(self):
        print(self.data["output"])


class BigNode(Node):

    def __init__(self, *args, **kwargs):
        super(BigNode, self).__init__(*args, **kwargs)
        self.addHeader(Header(node=self, text="BigNode"))
        self.addKnob(InputKnob(name="i1"))
        self.addKnob(OutputKnob(name="o1"))
        self.addKnob(InputKnob(name="i2"))
        self.addKnob(OutputKnob(name="o2"))
        self.addKnob(InputKnob(name="i3"))
        self.addKnob(OutputKnob(name="o3"))
        self.addKnob(InputKnob(name="i4"))
        self.addKnob(OutputKnob(name="o4"))
        self.addKnob(InputKnob(name="i5"))
        self.addKnob(OutputKnob(name="o5"))
        self.addKnob(InputKnob(name="i6"))
        self.addKnob(OutputKnob(name="o6"))
        self.addKnob(InputKnob(name="i7"))
        self.addKnob(OutputKnob(name="o7"))
        self.addKnob(InputKnob(name="i8"))
        self.addKnob(OutputKnob(name="o8"))
        self.addKnob(InputKnob(name="i9"))
        self.addKnob(OutputKnob(name="o9"))


class Directory(Node):

    def __init__(self, *args, **kwargs):
        super(Directory, self).__init__(*args, **kwargs)
        self.addHeader(Header(node=self, text="Directory"))
        self.addKnob(InputKnob(name="parent"))
        self.addKnob(OutputKnob(name="children"))


class File(Node):

    def __init__(self, *args, **kwargs):
        super(File, self).__init__(*args, **kwargs)
        self.addHeader(Header(node=self, text="File"))
        self.addKnob(InputKnob(name="parent"))


class MaxObject(Node):

    def __init__(self):
        super(MaxObject, self).__init__()
        self.addHeader(Header(node=self, text=self.__class__.__name__))
        self.addKnob(InputKnob(name="children"))
        self.addKnob(OutputKnob(name="parent"))


def test():
    app = QtWidgets.QApplication([])

    graph = NodeGraphWidget()
    graph.setGeometry(100, 100, 800, 600)
    graph.show()

    graph.registerNodeClass(Integer)
    graph.registerNodeClass(Float)
    graph.registerNodeClass(Multiply)
    graph.registerNodeClass(Divide)
    graph.registerNodeClass(Add)
    graph.registerNodeClass(Subtract)
    graph.registerNodeClass(Output)
    graph.registerNodeClass(BigNode)
    graph.registerNodeClass(File)
    graph.registerNodeClass(Directory)
    graph.registerNodeClass(MaxObject)

    nodeInt1 = Integer(scene=graph.scene)
    nodeInt2 = Integer(scene=graph.scene)
    nodeMult = Multiply(scene=graph.scene)
    nodeOut = Output(scene=graph.scene)

    graph.addNode(nodeInt1)
    graph.addNode(nodeInt2)
    graph.addNode(nodeMult)
    graph.addNode(nodeOut)

    nodeInt2.moveBy(100, 250)
    nodeMult.moveBy(200, 100)
    nodeOut.moveBy(400, 150)

    nodeInt1.knob("value").connectTo(nodeMult.knob("x"))
    nodeInt2.knob("value").connectTo(nodeMult.knob("y"))
    nodeMult.knob("value").connectTo(nodeOut.knob("output"))

    nodeInt1.value = 12
    nodeInt2.value = 4

    nodeInt1.run()
    nodeInt2.run()

    app.exec_()


if __name__ == '__main__':
    test()


"""
todos

- bug: sometimes a node's background rectangle is not cleared when deleting nodes

- make graphviz layouting aware of actual node width and height
- decouple identifier and display name in all items, so it can be changed
- edit nodes: possibly like in nuke, with an extra floating widget or a sidebar
- attach data to nodes and let them modify it: callbacks? custom signals?
- evaluate the graph, graph traversal, show some values in the ui?
- global settings, like 'restrict user from editing Edges'
- tests!

"""
