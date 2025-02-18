import numpy as np
from glob import glob
from scipy.stats import pearsonr
import natsort
import argparse

""" This code calculates the person correlation between the predicted pwms and the ground truth"""


def user_input():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--predictions_add', help='predictions_path_address', type=str, required=True)
    parser.add_argument('-gt_path', '--gt_path_res_num', help='ground truth number of residuals 4 or 7', type=str, required=True)
    args = parser.parse_args()
    arguments = vars(args)

    return arguments
def main(args):

    paths = glob(args['predictions_add'] + '/*')  # pwm predictions path
    paths = natsort.natsorted(paths)
    pred_list = []
    for i in range(paths.__len__()):
        pred_list.append(np.load(paths[i]))
    pred_mat = np.asarray(pred_list)
    # path = 'ground_truth/'

    gt_mat = np.load(args['gt_path_res_num'])  # ground truth pwm

    # first position
    A_1 = gt_mat[:, 0]
    A_1_pred = pred_mat[:, 0]
    C_1 = gt_mat[:, 1]
    C_1_pred = pred_mat[:, 1]
    G_1 = gt_mat[:, 2]
    G_1_pred = pred_mat[:, 2]
    T_1 = gt_mat[:, 3]
    T_1_pred = pred_mat[:, 3]

    # second position
    A_2 = gt_mat[:, 4]
    A_2_pred = pred_mat[:, 4]
    C_2 = gt_mat[:, 5]
    C_2_pred = pred_mat[:, 5]
    G_2 = gt_mat[:, 6]
    G_2_pred = pred_mat[:, 6]
    T_2 = gt_mat[:, 7]
    T_2_pred = pred_mat[:, 7]

    # third position
    A_3 = gt_mat[:, 8]
    A_3_pred = pred_mat[:, 8]
    C_3 = gt_mat[:, 9]
    C_3_pred = pred_mat[:, 9]
    G_3 = gt_mat[:, 10]
    G_3_pred = pred_mat[:, 10]
    T_3 = gt_mat[:, 11]
    T_3_pred = pred_mat[:, 11]

    pred_list = [A_1_pred, A_2_pred, A_3_pred, C_1_pred, C_2_pred, C_3_pred, G_1_pred, G_2_pred, G_3_pred,
                 T_1_pred, T_2_pred, T_3_pred]

    ground_truth_ls = [A_1, A_2, A_3, C_1, C_2, C_3, G_1, G_2, G_3, T_1, T_2, T_3]

    con_pred_gt = np.concatenate((pred_mat, gt_mat), axis=1)  # concatenate predictions and ground truth

    def person_cor_func(arr, strat_index):

        return pearsonr(arr[strat_index: strat_index + 4], arr[strat_index + 12: strat_index + 16])[0]

    pos_1_perason_arr = np.apply_along_axis(person_cor_func, 1, con_pred_gt, strat_index=0)
    pos_2_perason_arr = np.apply_along_axis(person_cor_func, 1, con_pred_gt, strat_index=4)
    pos_3_perason_arr = np.apply_along_axis(person_cor_func, 1, con_pred_gt, strat_index=8)
    pos_pearson_l = [pos_1_perason_arr, pos_2_perason_arr, pos_3_perason_arr]

    pearson_ls = []
    p_value_ls = []

    # pearson correlation and p value calculation of each column in the pwm
    for i in range(pred_list.__len__()):
        pearson_ls.append(pearsonr(pred_list[i], ground_truth_ls[i])[0])
        p_value_ls.append(pearsonr(pred_list[i], ground_truth_ls[i])[1])
    print('pearson correlation and p value calculation of each column in the pwm')
    print(pearson_ls)
    print(p_value_ls)
    print('\n')

    # mean and std pearson correlation of each position
    for i in range(pos_pearson_l.__len__()):
        print('mean pearson correlation of position %d is %.4f' % (i+1, np.nanmean(pos_pearson_l[i])))
        print('std pearson correlation of position %d is %.4f' % (i+1, np.nanstd(pos_pearson_l[i])))
        print('\n')



if __name__ == "__main__":
    args = user_input()
    main(args)
    print('\n' + '\n')


