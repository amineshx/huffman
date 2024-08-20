from bigtp import app
from flask import render_template
from bigtp.forms import Huffman,Shanonfano, Prefix
import math
from collections import Counter


def calculate_entropy_and_efficiency(codes, probabilities):
    entropy = -sum(p * math.log2(p) for p in probabilities)
    average_code_length = sum(len(code) * probability for code, probability in zip(codes, probabilities))
    efficiency = (entropy / average_code_length) * 100

    return [entropy, efficiency]

def is_prefix_cod(codes):
    for i in range(len(codes)):
        for j in range(len(codes)):
            if i != j and codes[j].startswith(codes[i]):
                return False
    return True

class ShannonFanoNode:
    def __init__(self, symbol, probability):
        self.symbol = symbol
        self.probability = probability
        self.code = ""

def shannon_fano_coding(input_string):
    symbols = list(input_string)
    total_symbols = len(symbols)
    symbol_counts = Counter(symbols)
    probabilities = [count / total_symbols for count in symbol_counts.values()]

    nodes = [ShannonFanoNode(symbol, probability) for symbol, probability in zip(symbol_counts.keys(), probabilities)]
    nodes.sort(key=lambda x: x.probability, reverse=True)

    def recursive_shannon_fano(node_list):
        if len(node_list) == 1:
            return

        total_probability = sum(node.probability for node in node_list)
        cumulative_probability = 0
        split_index = 0

        for i, node in enumerate(node_list):
            cumulative_probability += node.probability
            if cumulative_probability >= total_probability / 2:
                split_index = i
                break

        for i, node in enumerate(node_list):
            if i <= split_index:
                node.code += '0'
            else:
                node.code += '1'

        recursive_shannon_fano(node_list[:split_index + 1])
        recursive_shannon_fano(node_list[split_index + 1:])

    recursive_shannon_fano(nodes)

    symbols_list = [node.symbol for node in nodes]
    codes_list = [node.code for node in nodes]

    entropy = round(-sum(p * math.log2(p) for p in probabilities), 2)  
    average_code_length = sum(len(node.code) * node.probability for node in nodes)
    efficiency = round((entropy / average_code_length) * 100, 2)  

    return [symbols_list, codes_list, entropy, efficiency]




def huffmanCode(cahaine):
    def calcul_longueur_code(freq, code):
        longueur = 0
        for (char, frequency) in freq:
            longueur += len(code[char]) * (frequency/len(string))
        return longueur


    def calculate_efficacity(entropie, longueur_code):
        return round((entropie / longueur_code) * 100, 2)
    # on initialise une chaine de caracteres a envoyer


    string = str(cahaine)
    # Creation des noeuds de l'arbre

    
    class NodeTree(object):
        def __init__(self, left=None, right=None):
            self.left = left
            self.right = right

        def children(self):
            return (self.left, self.right)

        def __str__(self):
            return '%s_%s' % (self.left, self.right)

    # implementation du codage de huffman :


    def huffman_code_tree(node, binString=''):
        if type(node) is str:
            return {node: binString}
        (l, r) = node.children()
        d = dict()
        d.update(huffman_code_tree(l, binString + '0'))
        d.update(huffman_code_tree(r, binString + '1'))
        return d


    # Calcul de frequence
    freq = {}
    for x in string:
        if x in freq:
            freq[x] += 1
        else:
            freq[x] = 1

    freq = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    nodes = freq

    while len(nodes) > 1:
        (key1, x1) = nodes[-1]
        (key2, x2) = nodes[-2]
        nodes = nodes[:-2]
        node = NodeTree(key1, key2)
        nodes.append((node, x1 + x2))
        nodes = sorted(nodes, key=lambda x: x[1], reverse=True)

    huffmanCode = huffman_code_tree(nodes[0][0])

    
    list = []
    for (char, frequency) in freq:
        list.append(huffmanCode[char])

    entropie = 0

    for (char, frequency) in freq:
        entropie += -((frequency/len(string))) * math.log2((frequency/len(string)))
    

    longueur = calcul_longueur_code(freq, huffmanCode)
    efficacity = calculate_efficacity(entropie, longueur)
    return [entropie,freq,list, efficacity]


@app.route('/')
@app.route('/home')  
def home_page():
    return render_template('home.html')


@app.route('/huffman', methods=['GET','POST'])
def huffman():
    data = Huffman()
    out = ""
    dataleng = 0
    form_submitted = False
    if data.validate_on_submit():
        out=huffmanCode(data.charchain.data)
        dataleng = len(out[2])
        form_submitted = True
    return render_template('huffman.html',data=data, out=out, dataleng=dataleng, form_submitted=form_submitted)

@app.route('/shanonfano', methods=['GET','POST'])
def shanonfano():
    data = Shanonfano()
    out = ""
    dataleng = 0
    form_submitted = False
    if data.validate_on_submit():
        out=shannon_fano_coding(data.charchain.data)
        dataleng = len(out[0])
        form_submitted = True
    return render_template('shanonfano.html',data=data, out=out, dataleng=dataleng, form_submitted=form_submitted)

@app.route('/prefix', methods=['GET','POST'])
def prefix():
    data = Prefix()
    out = ["",""]
    form_submitted = False
    probabilities = []
    is_prefix_code = False
    if data.validate_on_submit():
        form_submitted = True
        codes= data.codes.data
        print(codes)
        print('0,10,110,1110')
        prob = data.probabilities.data
        codes = codes.split(",")
        prob = prob.split(",")
        for probability in prob :
            probabilities.append(float(probability))
        
        if  is_prefix_cod(codes):
            is_prefix_code = True
            entroeff=calculate_entropy_and_efficiency(codes,probabilities)
            out[0]=entroeff[0]
            out[1]=entroeff[1]

    return render_template('prefix.html',data=data,out=out,form_submitted=form_submitted, is_prefix_code=is_prefix_code)