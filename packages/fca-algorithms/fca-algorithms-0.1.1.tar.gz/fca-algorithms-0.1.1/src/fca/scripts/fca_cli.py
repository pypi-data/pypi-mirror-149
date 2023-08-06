#!/usr/bin/env python

import os
import argparse
import csv
from ..api_models import Context


INVALID_FILETYPE_MSG = "Error: Invalid file format. {} must be a .txt file."
INVALID_PATH_MSG = "Error: Invalid file path/name. Path {} does not exist."
MANDATORY_ARGUMENTS_MSG = "Either -c or -k params should be specified"
  
  
def validate_file(file_name):
    '''
    validate file name and path.
    '''
    if not valid_path(file_name):
        print(INVALID_PATH_MSG.format(file_name))
        quit()
    elif not valid_filetype(file_name):
        print(INVALID_FILETYPE_MSG.format(file_name))
        quit()
    return
      
def valid_filetype(file_name):
    # validate file type
    return file_name.endswith('.csv')
  
def valid_path(path):
    # validate file path
    return os.path.exists(path)


def main():
    # create a parser object
    parser = argparse.ArgumentParser(description = "FCA cli")
    
    # add argument
    parser.add_argument("-c", "--context", type=str, nargs='?',
                        metavar="context_name",
                        help="Formal context csv file.")
    
    parser.add_argument("-k", "--contexts", type=str, nargs='*',
                        metavar="context_names",
                        help="Formal contexts csv files from the relational context family.")
    
    parser.add_argument("-r", "--relations", type=str, nargs='*',
                        metavar="relation_file_names",
                        help="Relation csv filename in case of RCA. Name is expected to be r_1_3.csv for example if its a "
                             "relation between objects of the contexts 1 and 3 respectively"
                             "  On the other hand, in each row we expect to have the tuple separated by comma e.g., 1,2,3 "
                             "  for a relation between the first, second and third object")
    
    parser.add_argument("--show_hasse", action="store_true",
                        help="If present, the tool will show the hasse diagram")
    
    # parse the arguments from standard input
    args = parser.parse_args()

    if args.contexts:
        K, R = parse_rca(args)
        print(f'### RCA parsed {K}, {R}')
    elif args.context:
        K = parse_fca(args)
        if args.show_hasse:
            K.get_lattice().plot()
    else:
        print(MANDATORY_ARGUMENTS_MSG)
        exit(1)


def parse_rca(args):
    contexts = []
    for ctx_name in args.contexts:
        contexts.append(import_context(ctx_name))
    
    relations = []
    for relation_name in args.relations:
        relations.append(import_relation(relation_name, contexts))
    
    return contexts, relations


def parse_fca(args):
    return import_context(args.context)


def import_context(filename):
    O = []
    A = []
    I = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        loading_attributes = True
        for row in reader:
            if loading_attributes:
                for attr in row[1:]:
                    A.append(attr)
                loading_attributes = False
            else:
                O.append(row[0])
                I.append([])
                for attr_i in row[1:]:
                    I[-1].append(len(attr_i) != 0)
    return Context(O, A, I)


def separate_indexes(filename):
    k = 0
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        row = next(reader)
        k = len(row) # the the arity of the relationship
    # removes .csv, split by _, and then get only the last k elements which should be the indexes
    return filename[:-4].split("_")[-k:]


def import_relation(filename, contexts):
    index_offset = 1
    contexts_indexes = [int(idx) - index_offset for idx in separate_indexes(filename)]  # This is actually the arity of the relation
    R = dimension(contexts, contexts_indexes, 0)
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            to_process = 1
            current = R[int(row[0]) - index_offset]
            while to_process < len(contexts_indexes) - 1:
                current = current[int(row[to_process]) - index_offset]
                to_process += 1
            # At this point current is a set
            current.add(int(row[to_process]) - index_offset)
    return R
            

def dimension(contexts, contexts_indexes, i):
    if i == len(contexts_indexes) - 1:
        return set()
    context = contexts[contexts_indexes[i]]
    context_len = len(context.O)
    return [dimension(contexts, contexts_indexes, i+1) for _ in range(context_len)]


if __name__ == "__main__":
    main()
