import os
import sys
import pandas as pd

def import_names(names_file):
    names_dict = dict()
    with open(names_file, "r") as names_in:
        count = 0
        for line in names_in:
            if("scientific" in line):
                line_split = line.split("\t")
                #print(line_split)

                taxa = int(line_split[0])
                name = str(line_split[2])
                names_dict[taxa] = name
        return names_dict
    

def import_nodes(nodes_file):
    taxa_rank_dict = dict()
    taxa_parent_dict = dict()
    rank_taxa_dict = dict()
    with open(nodes_file, "r") as nodes_in:
        count = 0
        for line in nodes_in:
            cleaned_line = line.strip("\n")
            line_split = cleaned_line.split("\t")
            taxa = int(line_split[0])
            parent = int(line_split[2])
            rank = str(line_split[4])
            taxa_rank_dict[taxa] = rank
            taxa_parent_dict[taxa] = parent
            if(rank in rank_taxa_dict):
                rank_taxa_dict[rank].add(taxa)
            else:
                rank_taxa_dict[rank] = set([taxa])

        return taxa_rank_dict, taxa_parent_dict, rank_taxa_dict
    
def lookup_parent(taxa_parent_dict, taxa):
    if(taxa in taxa_parent_dict.keys()):
        return taxa_parent_dict[taxa]
    else:
        return 1

if __name__ == "__main__":
    nodes_file = sys.argv[1]
    names_file = sys.argv[2]


    names_dict = import_names(names_file)
    taxa_rank_dict, taxa_parent_dict, rank_taxa_dict = import_nodes(nodes_file)

    tree_df = pd.DataFrame.from_dict(taxa_parent_dict, orient = "index")
    
    done_flag = False
    rank_count = 1
    #iterate through each column, and look for each parent.  Stopping only when everyone's hit root.
    while(not done_flag):
        tree_df[rank_count] = tree_df[rank_count - 1].apply(lambda x: lookup_parent(taxa_parent_dict, x))
        if(not (tree_df[rank_count]>1).any()):
            done_flag = True
            print("no more parents")
        rank_count += 1

        if(rank_count > 40):
            done_flag = True
            print("timeout")

    print(tree_df)

    for rank in rank_taxa_dict:
        print(rank, rank_taxa_dict[rank])

        
    

    #for key in names_dict.keys():
    #    print(key, names_dict[key])