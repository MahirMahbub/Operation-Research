# -*- coding: utf-8 -*-
"""
Created on Tue Jun 20 00:15:02 2017

@author: Mahir Mahbub Srizon
"""
import numpy as np
from functools import reduce
from math import gcd
from astropy.table import Table
import warnings

class Proposed_Algorithm_2(object):

    def propose_method2(self, two_d_list, supply, demand, row_len, colume_len):
        common_factor = reduce(
                lambda x, y: gcd(x, y), reduce(lambda x, y: x+y, two_d_list))
        raw_2d_array = np.array(two_d_list.copy(), float)/common_factor
        print("Initial Table:", raw_2d_array)
        main_list_copy = np.array(two_d_list.copy(), float)
        result = np.array([[0.0 for i in range(colume_len)]for i in range(
                row_len)], float)
        row_customised_list = np.array(two_d_list.copy(), float)/common_factor
        colume_customised_list = np.array(
                two_d_list.copy(), float)/common_factor
        for row in range(row_len):
            temp_max = np.nanmax(raw_2d_array[row])
            row_customised_list[row] = temp_max-row_customised_list[row]
        for colume in range(colume_len):
            temp_max = np.nanmax(raw_2d_array[:, colume])
            colume_customised_list[
                    :, colume] = temp_max - colume_customised_list[:, colume]
        customized_table = np.array(np.absolute(
                (row_customised_list + colume_customised_list)//2))
        colume_name = ["Destination "+str(i+1) for i in range(colume_len)]
        print("Initial Customized List", customized_table)
        print("\n")
        for i in range(row_len+colume_len-1):
            print("ITERATION "+str(i+1)+":\n")
            colume_pointer_list = np.array([0.0] * row_len)
            row_pointer_list = np.array([0.0] * colume_len)
            for row in range(row_len):
                sliced_list = customized_table[row].copy()
                colume_pointer_list[row] = self.difference_high_value(
                        sliced_list)
            for colume in range(colume_len):
                sliced_list = customized_table[:, colume].copy()
                row_pointer_list[colume] = self.difference_high_value(
                        sliced_list)
            print("Colume Pointers:", colume_pointer_list)
            print("ROw Pointers:", row_pointer_list)
            maximum_row_indices = np.nanargmax(colume_pointer_list)
            maximum_colume_indices = np.nanargmax(row_pointer_list)
            if row_pointer_list[
                    maximum_colume_indices] < colume_pointer_list[
                            maximum_row_indices]:
                minvalue = 0.0
                try:
                    minimum_colume_indices = np.nanargmin(
                            main_list_copy[maximum_row_indices])
                    minvalue = min(demand[minimum_colume_indices], supply[
                            maximum_row_indices])
                except:
                    pass
                result[maximum_row_indices][minimum_colume_indices] = minvalue
                if minvalue == supply[maximum_row_indices]:
                    supply[maximum_row_indices] = 0
                    demand[minimum_colume_indices] -= minvalue
                    main_list_copy[maximum_row_indices] = np.nan
                    customized_table[maximum_row_indices] = np.nan
                else:
                    demand[minimum_colume_indices] = 0
                    supply[maximum_row_indices] -= minvalue
                    main_list_copy[:, minimum_colume_indices] = np.nan
                    customized_table[:, minimum_colume_indices] = np.nan
                print("Manipulated Main Table:\n", main_list_copy)
                print("Manipulated Customized Table:\n", customized_table)
            elif row_pointer_list[
                    maximum_colume_indices] > colume_pointer_list[
                            maximum_row_indices]:
                minvalue = 0.0
                try:
                    minimum_row_indices = np.nanargmin(main_list_copy[:, [
                            maximum_colume_indices]])
                    minvalue = min(supply[minimum_row_indices], demand[
                            maximum_colume_indices])
                except:
                    pass
                result[minimum_row_indices][maximum_colume_indices] = minvalue
                if minvalue == demand[maximum_colume_indices]:
                        demand[maximum_colume_indices] = 0
                        supply[minimum_row_indices] -= minvalue
                        main_list_copy[:, maximum_colume_indices] = np.nan
                        customized_table[:, maximum_colume_indices] = np.nan
                else:
                        supply[minimum_row_indices] = 0
                        demand[maximum_colume_indices] -= minvalue
                        main_list_copy[minimum_row_indices] = np.nan
                        customized_table[minimum_row_indices] = np.nan
            elif row_pointer_list[
                    maximum_colume_indices] == colume_pointer_list[
                            maximum_row_indices]:
                minvalue = 0.0
                try:
                    minimum_row_value = np.nanmin(main_list_copy[:, [
                            maximum_colume_indices]])
                    minimum_colume_value = np.nanmin(
                            main_list_copy[maximum_row_indices])
                    if minimum_colume_value > minimum_row_value:
                        minimum_row_indices = np.nanargmin(
                                main_list_copy[:, [maximum_colume_indices]])
                        minvalue = min(
                                supply[minimum_row_indices], demand[
                                        maximum_colume_indices])
                        if minvalue == demand[maximum_colume_indices]:
                            demand[maximum_colume_indices] = 0
                            supply[minimum_row_indices] -= minvalue
                            main_list_copy[:, maximum_colume_indices] = np.nan
                            customized_table[
                                    :, maximum_colume_indices] = np.nan
                        else:
                            supply[minimum_row_indices] = 0
                            demand[maximum_colume_indices] -= minvalue
                            main_list_copy[minimum_row_indices] = np.nan
                            customized_table[minimum_row_indices] = np.nan
                        result[minimum_row_indices][
                                maximum_colume_indices] = minvalue
                    else:
                        minimum_colume_indices = np.nanargmin(
                                main_list_copy[maximum_row_indices])
                        minvalue = min(demand[minimum_colume_indices], supply[
                                maximum_row_indices])
                        if minvalue == supply[maximum_row_indices]:
                            supply[maximum_row_indices] = 0
                            demand[minimum_colume_indices] -= minvalue
                            main_list_copy[maximum_row_indices] = np.nan
                            customized_table[maximum_row_indices] = np.nan
                        else:
                            demand[minimum_colume_indices] = 0
                            supply[maximum_row_indices] -= minvalue
                            main_list_copy[:, minimum_colume_indices] = np.nan
                            customized_table[
                                    :, minimum_colume_indices] = np.nan
                        result[maximum_row_indices][
                                minimum_colume_indices] = minvalue
                except:
                    pass
                print("Manipulated Main Table:\n", main_list_copy)
                print("Manipulated Customized Table:\n", customized_table)
            print("Combined Result Table:\n", result)
            print("Demand List:", demand)
            print("Supply List:", supply)
            print("\n")
        multiplied_array = np.multiply(result.tolist(), two_d_list)
        print("FINAL RESULT LIST:\n")
        np.savetxt("propose_method_data.csv", np.array(result), delimiter = ' , ')
        table = Table(np.array(result), names=colume_name)
        table.pprint(max_lines=-1, max_width=-1)
        print("\nOPTIMAL RESULT:", multiplied_array.sum())

    def difference_high_value(self, list_slice):
        try:
            try:
                index1 = np.nanargmax(list_slice)
                max1 = list_slice[index1]
            except:
                return np.nan
            list_slice[index1] = np.nan
            try:
                index2 = np.nanargmax(list_slice)
                max2 = np.nanmax(list_slice[index2])
            except:
                return max1
            return abs(max1 - max2)
        except:
            return np.nan

if __name__ == "__main__":
    cm =Proposed_Algorithm_2()
    warnings.filterwarnings('ignore')
    cm.propose_method2([[9,12,9,6,9,10],[7,3,7,7,5,5],[6,5,9,11,3,11],[6,8,11,2,2,10]],[5,6,2,9],[4,4,6,2,4,2],4,6)