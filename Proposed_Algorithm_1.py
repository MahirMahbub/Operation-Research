# -*- coding: utf-8 -*-
"""
Created on Mon Jun 12 16:04:04 2017

@author: Mahir Mahbub Srizon
"""
import numpy as np
import math
from astropy.table import Table

class Proposed_Algorithm_1(object):

    def dam_method(self, two_d_list, supply, demand, row_len, colume_len):
        raw_2d_array = np.array(two_d_list.copy(), float)
        degenerate_flag = False
        result = [[0 for i in range(colume_len)]for i in range(row_len)]
        average = math.trunc(np.mean(raw_2d_array))
        raw_2d_array = raw_2d_array-average
        colume_name=["Destination "+str(i+1) for i in range(colume_len)]
        print(colume_name)
        for i in range((colume_len+row_len-1)):
            print("ITERATION "+str(i+1)+":\n")
            colume_dmi_list = np.nanmean(raw_2d_array, axis=1)
            print("Colume DMI:", colume_dmi_list)
            row_dmi_list = np.nanmean(raw_2d_array, axis=0)
            print("Row DMI:", row_dmi_list)
            maximum_row_indices = np.nanargmax(colume_dmi_list)
            maximum_colume_indices = np.nanargmax(row_dmi_list)
            print("Manipulated Main List:\n", raw_2d_array)
            print("Result List:\n", np.array(result))
            print("Supply:", supply)
            print("Demand:", demand)
            print()
            if row_dmi_list[maximum_colume_indices] < colume_dmi_list[
                    maximum_row_indices]:
                minimum_colume_indices = np.nanargmin(raw_2d_array[
                        maximum_row_indices])
                raw_2d_array[maximum_row_indices][
                        minimum_colume_indices] = min(
                        demand[minimum_colume_indices], supply[
                                maximum_row_indices])
                minvalue = min(demand[minimum_colume_indices], supply[
                        maximum_row_indices])
                if result[maximum_row_indices][
                        minimum_colume_indices] == 0 and not minvalue == 0:
                    result[maximum_row_indices][
                            minimum_colume_indices] = minvalue
                else:
                    print("Degenerated Solution")
                    degenerate_flag = True
                    break
                if minvalue == supply[maximum_row_indices]:
                    supply[maximum_row_indices] = 0
                    demand[minimum_colume_indices] -= minvalue
                    raw_2d_array[maximum_row_indices] = np.nan
                else:
                    demand[minimum_colume_indices] = 0
                    supply[maximum_row_indices] -= minvalue
                    raw_2d_array[:, minimum_colume_indices] = np.nan
            elif row_dmi_list[maximum_colume_indices] > colume_dmi_list[
                    maximum_row_indices]:
                minimum_row_indices = np.nanargmin(
                        raw_2d_array[:, maximum_colume_indices])
                raw_2d_array[minimum_row_indices][
                        maximum_colume_indices] = min(
                        supply[minimum_row_indices], demand[
                                maximum_colume_indices])
                minvalue = min(supply[minimum_row_indices], demand[
                        maximum_colume_indices])
                if result[minimum_row_indices][
                        maximum_colume_indices] == 0 and not minvalue == 0:
                    result[minimum_row_indices][
                            maximum_colume_indices] = minvalue
                else:
                    print("Degenerated Solution")
                    degenerate_flag = True
                    break
                if minvalue == demand[maximum_colume_indices]:
                    demand[maximum_colume_indices] = 0
                    supply[minimum_row_indices] -= minvalue
                    raw_2d_array[:, maximum_colume_indices] = np.nan
                else:
                    supply[minimum_row_indices] = 0
                    demand[maximum_colume_indices] -= minvalue
                    raw_2d_array[minimum_row_indices] = np.nan
            elif row_dmi_list[maximum_colume_indices] == colume_dmi_list[
                    maximum_row_indices]:
                minimum_colume_value = np.nanmin(raw_2d_array[
                        maximum_row_indices])
                minimum_row_value = np.nanmin(raw_2d_array[
                        :, maximum_colume_indices])
                if minimum_colume_value < minimum_row_value:
                    minimum_colume_indices = np.nanargmin(raw_2d_array[
                            maximum_row_indices])
                    raw_2d_array[maximum_row_indices][
                            minimum_colume_indices] = min(
                            demand[minimum_colume_indices], supply[
                                    maximum_row_indices])
                    minvalue = min(demand[minimum_colume_indices], supply[
                            maximum_row_indices])
                    if result[maximum_row_indices][
                            minimum_colume_indices] == 0 and not minvalue == 0:
                        result[maximum_row_indices][
                                minimum_colume_indices] = minvalue
                    else:
                        print("Degenerated Solution")
                        degenerate_flag = True
                        break
                    if minvalue == supply[maximum_row_indices]:
                        supply[maximum_row_indices] = 0
                        demand[minimum_colume_indices] -= minvalue
                        raw_2d_array[maximum_row_indices] = np.nan
                    else:
                        demand[minimum_colume_indices] = 0
                        supply[maximum_row_indices] -= minvalue
                        raw_2d_array[:, minimum_colume_indices] = np.nan
                elif minimum_colume_value >= minimum_row_value:
                    minimum_row_indices = np.nanargmin(raw_2d_array[
                            :, maximum_colume_indices])
                    raw_2d_array[minimum_row_indices][
                            maximum_colume_indices] = min(
                            supply[minimum_row_indices], demand[
                                    maximum_colume_indices])
                    minvalue = min(supply[minimum_row_indices], demand[
                            maximum_colume_indices])
                    if result[minimum_row_indices][
                            maximum_colume_indices] == 0 and not minvalue == 0:
                        result[minimum_row_indices][
                                maximum_colume_indices] = minvalue
                    else:
                        print("Degenerated Solution")
                        degenerate_flag = True
                        break
                    if minvalue == demand[maximum_colume_indices]:
                        demand[maximum_colume_indices] = 0
                        supply[minimum_row_indices] -= minvalue
                        raw_2d_array[:, maximum_colume_indices] = np.nan
                    else:
                        supply[minimum_row_indices] = 0
                        demand[maximum_colume_indices] -= minvalue
                        raw_2d_array[minimum_row_indices] = np.nan
            else:
                print("Degenerated Solution")
                degenerate_flag = True
                break
            print()
        if degenerate_flag is False:
            multiplied_array = np.multiply(result, two_d_list)
            print("\nFINAL RESULT LIST:\n")
            np.savetxt("dam_method_data.csv", np.array(result),delimiter=' , ')
            table=Table(np.array(result),names=colume_name)
            table.pprint(max_lines=-1, max_width=-1)
            print("\nOPTIMAL RESULT:", multiplied_array.sum())
            print()
            #print(table.info('stats'))
        else:
            print("Can not generate Output")
            print()

    def min_index_list(self, a, avglist):
        mask_array = np.ma.array(a, mask=np.isnan(a).tolist())
        np_minimum_indicies = np.where(mask_array == mask_array.min())
        print("the value", np_minimum_indicies)
        print()
        max_v = 0
        max_multivalue = 0
        for i in np_minimum_indicies[0]:
            if avglist[i] >= max_multivalue:
                max_v = i
                max_multivalue = avglist[i]
        return max_v

if __name__ == "__main__":
    cm = Proposed_Algorithm_1()
    cm.dam_method([[3,6,4],[3,3,1],[5,4,7],[1,6,2]],[5,8,7,14],[7,9,18],4,3)