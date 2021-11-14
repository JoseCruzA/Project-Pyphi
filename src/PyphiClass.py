import pyphi
import numpy as np

class Pyphi:
    """
        Class for calculate the phi and the MIP of a graph
        with different configurations
        Created by José Daniel Cruz y Juan Camilo Gómez

        Attributes:
            graph_name (str): name of the graph
            tpm (np.array): tpm of the graph
            cm (np.array): cm of the graph
            labels (list): labels of the graph
            node_index (list): index of the nodes
            state (list): initial state of the graph
            config (str): configuration name fir this proob
            with_cm (bool): if the graph has a cm or not
    """

    def __init__(self, graph, path: str, with_cm = False):
        pyphi.config.load_file("config/" + path)
        self.graph_name = str(graph.name)
        self.tpm = np.array(graph.tpm_node)
        self.cm = np.array(graph.cm)
        self.labels = graph.nodes
        self.node_index = graph.index
        self.state = graph.initial_state
        self.config = path.replace("pyphi_config_", "").replace(".yml", "")
        self.with_cm = with_cm

    def calculate(self):
        """
            Calculate the phi and the MIP of the graph
        """
        # Network with the arguments
        network = pyphi.Network(self.tpm, node_labels=self.labels) if not self.with_cm else pyphi.Network(self.tpm, self.cm, node_labels=self.labels)

        # Subsystem for evaluate
        subsystem = pyphi.Subsystem(network, self.state, self.node_index)
        # 
        sia = pyphi.compute.sia(subsystem)

        self.write_result(sia)

    def write_result(self, sia):
        """
            Write the result of the phi and the MIP of the graph in a txt file

            Args:
                sia (pyphi.Subsystem): subsystem of the graph
        """
        cm = "_cm" if self.with_cm else ""
        file = open("assets/results/" + self.graph_name.replace(" ", "_") + "_" + self.config + cm + ".txt", "w+")
        file.write("MIP: " + str(sia.cut) + "\n")
        file.write("Phi: Φ = " + str(sia.phi) + "\n")
        file.write("Time: " + str(sia.time) + "s")