class Graph:
    """
        Class for storage a graph basic data for calculate its MIP and phi wi
        Created by: José Daniel Cruz y Juan Camilo Gómez

        Attributes:
            name (str): name of the graph
            nodes (list): list of nodes
            index (list): list of index
            initial_state (list): list of initial state
            cm (list): list of cm
            tmp_status (list): list of tmp status-status
            tpm_node (list): list of tpm node-status
            tpm_multidimensional (list): list of tpm multidimensional node-status
        
        Methods:
            create_graph(json): create a graph from json
    """

    def __init__(self):
        self.name = ""
        self.nodes = []
        self.index = []
        self.initial_state = []
        self.cm = []
        self.tmp_status = []
        self.tpm_node = []
        self.tpm_multidimensional = []

    def create_graph(self, json):
        """
            Create a graph from json

            Args:
                json (dict): json with graph data
        """
        self.name = json["name"]
        self.nodes = json["nodes"]
        self.index = json["index"]
        self.initial_state = json["initial_state"]
        self.cm = json["cm"]
        self.tmp_status = json["tmp_status"]
        self.tpm_node = json["tpm_node"]
        self.tpm_multidimensional = json["tpm_multidimensional"]