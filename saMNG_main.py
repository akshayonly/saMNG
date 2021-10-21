"""
Title: Single Article Mesh Graph Network
Author: Akshay Shirsath
Logo Icon Source: www.flaticon.com
"""
############################################
############## Libraries ###################

# Web Application
import streamlit as st
import streamlit.components.v1 as components
from PIL import Image
import os 

# Fetching PubMed article metadata
from Bio import Entrez
from Bio import Medline
import numpy as np

import networkx as nx
from pyvis.network import Network

############################################
########### Custom Function ################

@st.cache
def pubmedData(pmid):
    """
    Returns PubMed data associated with PMID
    """
    Entrez.email = 'akishirsath@gmail.com'

    handle = Entrez.efetch(
      db="pubmed", 
      id=pmid, 
      rettype="medline", 
      retmode="text")

    records = Medline.parse(handle)
    records = list(records)[0]
    
    return records

def removeSpecialChar(string):
    """
    Removes special characters from given string
    """
    special_characters = ['!','#','$','%','@','[',']',' ',']','_', "*", ","]
    
    for i in special_characters:
        string = string.replace(i,' ').strip()
    
    return string

############################################
################## Main ####################

# Logo
image = Image.open('saMNG_logo.png')
st.image(image, use_column_width=True)

st.markdown("This web application visualizes MeSH terms in the PubMed article as Network-Graph representation.")

expander_bar = st.expander("About Site")
expander_bar.markdown("""
* **version 1.8**
* **Python Libraries:** streamlit, pyvis, networkx, biopython.
* **Data source:** PubMed Entrez
* **Author:** Akshay Shirsath   
* **Compare Two Topics:** [Click-Here](https://tcmng.herokuapp.com/)
""")

st.subheader('Enter PubMed Article URL')
default_url = "https://pubmed.ncbi.nlm.nih.gov/21371747/"
user_url = st.text_input('Replace below URL:', default_url)

pmid = user_url.split('/')[3]

if st.button('Show Graph'):

	st.spinner()
	with st.spinner(text=f'Fetching {pmid} PMID data...'):
		pubmed_data = pubmedData(pmid)
		
		title = pubmed_data.get('TI')

		authors = pubmed_data.get('AU')

		source = pubmed_data.get('SO')

		mesh = pubmed_data.get('MH')



	st.subheader('Article Info')
	text = ", ".join(authors)+" | "+title+" | "+source
	st.info(text)

	graph_components = dict()
	unique_words = set()

	for terms in mesh:
	    process_string = removeSpecialChar(terms)
	    clean_string = [word.strip() for word in process_string.split("/")]
	    
	    if len(clean_string)>1:
	        secondary_node = clean_string[0]
	        tertiary_nodes = clean_string[1:]
	        graph_components[secondary_node] = tertiary_nodes
	        
	        for word in clean_string:
	            unique_words.add(word.strip())
	    else:
	        secondary_node = clean_string[0]
	        graph_components[secondary_node] = "None"
	        unique_words.add(secondary_node)

	num_unique_words = len(unique_words)        


	paper_title = pubmed_data['TI']
	no_words_paper_title= len(paper_title.split())
	sentence_break = int(np.floor(no_words_paper_title/2))
	part_one = "-".join(paper_title.split(' ')[:sentence_break])
	part_two = "-".join(paper_title.split(' ')[sentence_break:])
	root_node = part_one + "\n" + part_two

	G = nx.Graph()

	G.add_node(root_node, size=24, title=f"PMID-{pmid}", color="#00ACEA")

	G.add_nodes_from(graph_components.keys(), size=16, color="#FEDB41")


	for key in graph_components.keys():
	    values = graph_components.get(key)
	    G.add_edge(root_node, key, weight=1.5)
	    if isinstance(values, list) and len(values)!=0:
	        for value in values:
	            G.add_node(value, color="#00EFD1")
	            G.add_edge(key, value)
	            
	    if isinstance(values, str) and values!='None':
	        G.add_node(values, color="#00EFD1")
	        G.add_edge(key, values)

	nt = Network(height="500px", width="65%", bgcolor='#dcdde1', font_color='#2f3640')
	nt.from_nx(G)
	nt.set_options("""
	var options = {
	  "physics": {
	    "barnesHut": {
	      "gravitationalConstant": -7700,
	      "centralGravity": 0,
	      "springLength": 120
	    },
	    "minVelocity": 0.75
	  }
	}
	""")

	nt.write_html(f'{pmid}.html')
	
	st.subheader('MeSH Graph')
	st.info('NOTE: Interact with mouse')

	HtmlFile = open(f"{pmid}.html", 'r', encoding='utf-8')
	source_code = HtmlFile.read() 
	components.html(source_code, height = 1200, width=1100)

try:
    os.remove(f'{pmid}.html')
except OSError:
    pass	

st.stop()    
