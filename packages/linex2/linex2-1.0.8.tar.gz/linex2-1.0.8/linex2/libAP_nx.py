import numpy as np
import operator
from sklearn.cluster import KMeans
import networkx as nx
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt


flatten = lambda l: [item for sublist in l for item in sublist]

split_str = "#"


def convergence_plot(scores):
    """
    Shows the convergence plot

    Attributes:
    -----------
    scores - the output of run_search() function

    output - directory name where results should be saved
    """

    plt.figure(figsize=(10, 6))

    sns.set(style="whitegrid")
    plt.rc('font', size=13)  # controls default text sizes
    plt.rc('axes', titlesize=13)  # fontsize of the axes title
    plt.rc('xtick', labelsize=13)  # fontsize of the tick labels
    plt.rc('ytick', labelsize=13)  # fontsize of the tick labels
    plt.rc('legend', fontsize=13)
    wg = pd.DataFrame(scores, columns=["score"])
    ax = sns.lineplot(data=wg, palette="tab10", linewidth=2.5)
    ax.set(xlabel="Iterations")
    ax.set(ylabel="Score")
    plt.show()


class LSOprimizer:
    def __init__(self,
                 G: nx.Graph,
                 L_min: int,
                 L_max: int,
                 T: float = 20,
                 max_iter: int = 100,
                 reaction_penalty: float = 1,
                 plot: bool = True,
                 opt_pat=None,
                 k=2,
                 init_size=None,
                 seed=None,
                 verbose=True,
                 node_scoring=False):
        """
        Given a graph G and gene expression matrix GE finds the optimal subnetwork in G of size at least L_min and
        at most L_max that can provide the optimal patients clustering in k clusters.
        :param G: networkX graph with PPI network
        :param L_min: minimal desired solution subnetwork size
        :param L_max: maximal desired solution subnetwork size
        :param T: temprature parameter for SA
        :param max_iter: maximal allowed number of iterations
        :param plot: convergence plot (True/False)
        :param opt_pat: patients labels (if provided, patients clustering won't be performed
        :param k: nmber of clusters
        :param init_size: initial subnetwork size (default L_max *2)
        :param seed: seed
        :param verbose: True/False
        """
        self.G = G
        self.T = T
        self.L_min = L_min
        self.L_max = L_max
        self.max_iter = max_iter
        self.reaction_penalty = reaction_penalty
        self.plot = plot
        if opt_pat is None:
            self.opt_pat = []
        else:
            self.opt_pat = opt_pat
        self.k = k
        if init_size is None:
            self.init_size = L_max
        else:
            self.init_size = init_size
        self.seed = seed
        self.verbose = verbose
        self.genes = list(self.G.nodes)
        self.nodescoring = node_scoring

    def APUtil(self, u, visited, ap, parent, low, disc, nodes, Time=0):
        """
        A recursive function that find articulation points
        using DFS traversal
        :param u: the vertex to be visited next
        :param visited: keeps tract of visited vertices
        :param ap: stores articulation points
        :param parent: stores parent vertices in DFS tree
        :param low: low value
        :param disc: stores discovery times of visited vertices
        :param nodes: current node set

        for more details: https://www.geeksforgeeks.org/articulation-points-or-cut-vertices-in-a-graph/
        """

        # Count of children in current node
        children = 0

        # Mark the current node as visited and print it
        visited[u] = True

        # Initialize discovery time and low value
        disc[u] = Time
        low[u] = Time
        Time += 1

        # for all the vertices adjacent to this vertex
        for v in self.G.neighbors(u):
            # If v is not visited yet, then make it a child of u
            # in DFS tree and recur for it
            if v in nodes:
                if not visited[v]:
                    parent[v] = u
                    children += 1
                    self.APUtil(v, visited, ap, parent, low, disc, nodes, Time)

                    # Check if the subtree rooted with v has a connection to
                    # one of the ancestors of u
                    low[u] = min(low[u], low[v])

                    # u is an articulation point in following cases
                    # (1) u is root of DFS tree and has two or more children.
                    if parent[u] == -1 and children > 1:
                        ap[u] = True

                    # (2) If u is not root and low value of one of its child is more
                    # than discovery value of u.
                    if parent[u] != -1 and low[v] >= disc[u]:
                        ap[u] = True

                        # Update low value of u for parent function calls
                elif v != parent[u]:
                    low[u] = min(low[u], disc[v])

                    # The function to do DFS traversal. It uses recursive APUtil()

    def is_AP(self, nodes):
        """
        Checks which nodes in the given set of nodes can NOT be removed without breaking
        disconnecting the induced subgraph
        :param nodes: set of nodes that make an induced subgraph of G
        :return: dictionary where each key is a node and each value indicates if a node is
        removable (articulation point)
        """
        visited = dict()
        disc = dict()
        low = dict()
        parent = dict()
        ap = dict()
        for node in nodes:
            visited[node] = False
            disc[node] = float("Inf")
            low[node] = float("Inf")
            parent[node] = -1
            ap[node] = False

        # Call the recursive helper function
        # to find articulation points
        # in DFS tree rooted with vertex 'i'
        for node in nodes:
            if not visited[node]:
                self.APUtil(node, visited, ap, parent, low, disc, set(nodes))

        return ap

    def score(self, nodes):
        """
        scores  given solution which is defined as a subnetwork and patient clusters
        :param nodes: list of nodes used in the solution
        :return: objective function value
        """

        sub = nx.subgraph(self.G, nodes)
        scores = []
        reacs = []
        if not self.nodescoring:
            for ed in sub.edges:
                tmp_edge_data = sub.get_edge_data(*ed)
                scores.append(tmp_edge_data["objective"])
                reacs.append(tmp_edge_data["enzyme_raw_id"])
            return np.sum(scores) / \
                (len(scores) +
                 (self.reaction_penalty * len(set(reacs)))
                 )
        else:
            scores = [val for key, val in dict(sub.nodes(data='objective')).items()]
            if self.reaction_penalty > 0:
                n_enz = len(set(flatten([val for key, val in dict(sub.nodes(data='enzymes')).items()])))
                enz_pen = 1 if n_enz < 1 else n_enz
                # print(enz_pen)
                return np.mean(scores) / (enz_pen * self.reaction_penalty)
            else:
                # print(set(flatten([val for key, val in dict(sub.nodes(data='enzymes')).items()])))
                #n_enz = len(set(flatten([val for key, val in dict(sub.nodes(data='enzymes')).items()])))
                #enz_pen = 1 if n_enz < 1 else n_enz
                #print(np.mean(scores) - (enz_pen * 1.))
                #print(np.mean(scores))
                #print()
                return np.mean(scores)

    @staticmethod
    def static_score(g, reaction_penalty, nodes):
        sub = nx.subgraph(g, nodes)
        scores = []
        reacs = []
        for ed in sub.edges:
            tmp_edge_data = sub.get_edge_data(*ed)
            scores.append(tmp_edge_data["objective"])
            reacs.append(tmp_edge_data["enzyme_raw_id"])

        return np.sum(scores) / \
            (len(scores) +
             (reaction_penalty * len(set(reacs)))
             )

    def dfs(self, node, d, visited=None):
        """
        Recursive DFS
        :param node: starting node
        :param d: length of required subnetwork
        :param visited: should be left empty
        :return: a list of connected nodes of length d
        """

        if visited is None:
            visited = []
        if node not in visited and len(visited) < d:
            visited.append(node)
            for neighbour in self.G.neighbors(node):
                self.dfs(neighbour, d, visited)
        if len(visited) == d:
            return visited

    def get_candidates(self, nodes):
        """
        Outputs first-degree neighbours of given nodes in graph G
        :param nodes: list of nodes that form a subnetwork/solution
        :return: list of first neighbour nodes
        """
        subst_candidates = flatten([[n for n in self.G.neighbors(x)] for x in nodes])
        subst_candidates = set(subst_candidates).difference(set(nodes))
        return subst_candidates

    def insertion(self, nodes):
        """
        Scores all possible insertions
        :param nodes: current solution
        :return: dictionary where key are possible insertions and values are scores
        """
        results = dict()
        size = len(nodes)
        if size < self.L_max:
            candidates = self.get_candidates(nodes)
            for c in candidates:
                nodes_new = nodes + [c]
                sc = self.score(nodes_new)
                results["i" + split_str + c] = sc
        return results

    def deletion(self, nodes, AP):
        """
        Scores all possible deletions
        :param nodes: current solution
        :param AP: articulation points (can't be removed since they separate the subnetwork)
        :return: dictionary where key are possible deletions and values are scores
        """
        results = dict()
        size = len(nodes)

        if size > self.L_min:
            for node in nodes:
                if not AP[node]:
                    nodes_new = list(set(nodes).difference({node}))
                    sc = self.score(nodes_new)
                    results["d" + split_str + str(node)] = sc
        return results

    def subst(self, nodes, AP):
        """
        Scores all possible substitutions
        :param nodes: current solution
        :param AP: articulation points (can't be removed since they separate the subnetwork)
        :return: dictionary where key are possible substitutions and values are scores
        """
        results = dict()
        size = len(nodes)
        if (size < self.L_max) and (size > self.L_min):
            for node in nodes:
                without_node = set(nodes) - {node}
                candidates = self.get_candidates(list(without_node))
                candidates = candidates - {node}
                for c in candidates:
                    if AP[node]:
                        nodes_new = list(without_node.union({c}))
                        if self.is_connected(nodes_new):
                            sc = self.score(nodes_new)
                            results["s" + split_str + str(node) + split_str + str(c)] = sc

                    else:
                        nodes_new = list(without_node.union({c}))
                        sc = self.score(nodes_new)
                        results["s" + split_str + str(node) + split_str + str(c)] = sc

        return results

    def is_connected(self, nodes):
        """
        Checks if a subgraph of G that consists of the given nodes is connected
        :param nodes: list of nodes
        :return: bool
        """
        # sg = self.G.new_vertex_property("bool")
        sg = self.G.subgraph(nodes)
        # g = gt.GraphView(self.G, vfilt=sg)

        return nx.is_connected(sg)

        # comp, _ = gt.label_components(g, vprop=sg)
        # if len(set(comp.a[nodes])) > 1:
        #     return False
        # else:
        #     return True

    @staticmethod
    def do_action_nodes(action, nodes):
        """
        Updates the set of nodes given the action
        :param action: a key from the results dictionary that has a description of an action
        :param nodes: previous solution
        :return: new set of nodes
        """
        if len(action.split(split_str)) == 2:  # inserion or deletion
            act, node = action.split(split_str)
            node = node
            if act == "i":
                nodes = nodes + [node]
            else:
                nodes = list(set(nodes).difference({node}))
        else:  # substitution
            act, node, cand = action.split(split_str)
            node = node
            cand = cand
            nodes = nodes + [cand]
            nodes = list(set(nodes).difference({node}))
        return nodes

    @staticmethod
    def to_key(nodes):
        """
        Creates a string representation of nodes
        :param nodes: node list
        :return: string of nodes
        """
        nodes = sorted(nodes)
        tmp_nodes = "|".join(nodes)
        return tmp_nodes

    def ls_on_genes(self, nodes, solutions, score0, T):
        """
        Runs local search on a gene set
        :param nodes: current node set
        :param solutions: dictionary wth previously used solutions
        :param score0: last objective function score
        :param T: temperature for SA

        :return:
        nodes - new set of nodes
        score1 - new score
        move - True if further optimization was possible
        """
        # SUBNETWORK OPTIMIZATION
        move = False  # indicates if the solution feasible
        AP = self.is_AP(nodes)
        results = {**self.insertion(nodes), **self.deletion(nodes, AP),
                   **self.subst(nodes, AP)}
        # first select the highest scoring solution which doesn't lead to the same set of nodes
        while not move:
            action = max(results.items(), key=operator.itemgetter(1))[0]
            score1 = results[action]
            # check if the solution is feasible
            nodes_new = self.do_action_nodes(action, nodes)
            nodes_new = self.to_key(nodes_new)
            if solutions.get(nodes_new) == None:  # solution wasn't used before
                move = True
            else:
                del results[action]
                if len(results) == 0:
                    if self.verbose:
                        print("no more feasible solutions")
                    return nodes, score0, move

        delta = score0 - score1
        if delta < 0:  # move on
            if self.verbose:
                print(action)
                print("Score after genes LS {0}".format(score1))
            nodes = self.do_action_nodes(action, nodes)

        else:  # SA
            try:
                val = np.exp(-delta / T)
            except RuntimeError:
                val = 0
            p = np.random.uniform()
            if val > p:  # move on
                if self.verbose:
                    print("SA on genes at {0} degrees".format(T))
                    print(action)
                    print("Score after genes LS".format(score1))
                nodes = self.do_action_nodes(action, nodes)
            else:  # terminate if no improvement in two rounds
                if self.verbose:

                    print("too cold for genes SA, no actions taken")
                move = False
                score1 = score0
        return nodes, score1, move

    def compute_seed(self):
        nodes = []
        # for  whatever reason dfs sometimes returns nothing
        no_type = True
        while no_type:
            nodes = self.dfs(np.random.choice(self.genes, 1)[0], self.init_size)
            if nodes is not None:
                no_type = False
        return nodes

    def run_ls(self):
        """
        Runs LS on patients and nodes
        :return:
        best_nodes - optimized node set
        score_max -maximal score
        """

        T0 = self.T
        T = T0
        score_max = -100
        best_nodes = []
        # initialization
        if self.seed is None:
            nodes = self.compute_seed()
        else:
            nodes = self.seed

        start_score = self.score(nodes)
        if self.verbose:
            print(start_score)
        score0 = start_score
        scores = [start_score]
        solutions = dict()
        nodes_keys = self.to_key(nodes)
        solutions[nodes_keys] = ""
        count = 0
        for it in range(self.max_iter):
            #print(it)
            score1 = score0
            nodes_backup = nodes
            nodes, score2, move_genes = self.ls_on_genes(nodes, solutions, score1, T)
            if not self.is_connected(nodes):
                print("something is wrong, network is disconnected")
                return nodes_backup, 0
            T = T0 * (0.9 ** it)  # cool down
            if self.verbose:
                print(it)
            solutions[self.to_key(nodes)] = ""
            scores.append(score2)

            score0 = score2
            if score2 > score_max:
                score_max = score2
                best_nodes = [x for x in nodes]

            count = count + 1
            if not move_genes:
                if self.plot:
                    convergence_plot(scores)
                break
        return best_nodes, score_max, scores

