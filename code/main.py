from __future__ import print_function
import os
import utils 
import argparse 
import point 
import one_step_approximator
from IPython.core.debugger import Pdb
MAX = float('inf')

def print_output(output,output_file):
    if output_file == '':
        fh = None
    else:
        fh = open(output_file,'w')
    #
    print(len(output),file=fh)
    for mp in output:
        print(mp[0],mp[1] ,file=fh)
    #
    if fh:
        fh.close()


def main(input_file,output_file):
    #Pdb().set_trace()
    k,error_type,points  = utils.read_input(input_file)
    error_fn = utils.get_error_fn(error_type)
    ssa = one_step_approximator.get_one_step_approximator(error_type, points)
    n = len(points)
    if k >= n:
        output = [(p.x,p.y) for p in points]
        print_output(output,output_file)
        return
    #base case - 
    #size of error - table k x n
    error_table = []
    back_pointers = []
    last_error_row = [0]*n
    this_back_pointers = [-1]*n
    for j in range(k-1,n):
        last_error_row[j],this_back_pointers[j] = ssa.get_approximation(j,n-1)
    #
    #Pdb().set_trace()
    back_pointers.append(this_back_pointers)
    for i in range(k-1):
        step_no = i+2
        this_error_row = [0]*n
        this_back_pointers = [-1]*n
        #at step i
        for j in range(k-step_no,n):
            #num_points_on_right = n-j
            if (n-j) == step_no:
                this_error_row[j] = 0
                this_back_pointers[j] = (points[j].y,j+1)
                break 
            #
            current_min = MAX 
            current_min_index = -1
            current_ssay = -1
            for l in range(j+1,n-i):
                this_ssa_e,this_ssa_y = ssa.get_approximation(j,l-1)
                this_score = ssa.combine(last_error_row[l], this_ssa_e)
                if this_score < current_min:
                    current_min = this_score
                    current_min_index = l
                    current_ssay = this_ssa_y 
                #
            #
            this_error_row[j] = current_min
            this_back_pointers[j] = (current_ssay, current_min_index)
            if step_no == k:
                break
        #
        last_error_row = this_error_row
        back_pointers.append(this_back_pointers)

    output = []
    current_x_ind = 0
    current_back_pointer = back_pointers[-1][current_x_ind]
    for i in range(k-2,-1,-1):
        output.append((points[current_x_ind].x, current_back_pointer[0]))
        current_x_ind = current_back_pointer[1]
        current_back_pointer = back_pointers[i][current_x_ind]
    #
    output.append((points[current_x_ind].x, current_back_pointer))
    print_output(output,output_file) 


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_file',help='input_file_name',type=str,default='input.txt')
    parser.add_argument('--output_file',help='output written in output file',default='')

    args = parser.parse_args()
    main(args.input_file, args.output_file)
