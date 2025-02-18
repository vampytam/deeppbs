
from utiles_input_and_label import *
import pandas as pd

"""This function creates C_RC input and label for Transfer learning model:
INPUT DATA: each amino acid is represented by a 1X20 one hot vector therefore
             zinc finger with 12 positions is represented by 1X240 vector and
             zinc finger with 7 positions is represented by 1X140 vector and
             zinc finger with 4 positions is represented by 1X80 vector
 LABEL: the model label is one a position weight matrix (pwm): 3X4 (3 possible positions and 4 DNA nucleotides),
        In our model the pwm is reshaped to  1X12 vector"""


c_rc_df = pd.read_excel('UPDATE/C_RC_data.xlsx')
c_rc_df = group_zf_by_protein_name(c_rc_df)
c_rc_df.rename(columns={"12_seq": "res_12"}, inplace=True)


c_rc_df['res_7'] = c_rc_df.res_12.map(lambda x: x[2] + x[4:9] + x[-1])
c_rc_df['res_4'] = c_rc_df.res_12.map(lambda x: x[5] + x[7:9] + x[-1])

"one hot encoding"
one_hot_c_rc_4res = oneHot_Amino_acid_vec(c_rc_df['res_4'])
one_hot_c_rc_7res = oneHot_Amino_acid_vec(c_rc_df['res_7'])
one_hot_c_rc_12res = oneHot_Amino_acid_vec(c_rc_df['res_12'])

"labels: the pwm is the same to all sequence residuals"
pwm = (c_rc_df.filter(items=['A1', 'C1', 'G1', 'T1', 'A2', 'C2', 'G2', 'T2', 'A3', 'C3', 'G3', 'T3'])).values
"Savings"
save_path = 'UPDATE'
np.save(save_path + 'ground_truth_c_rc', pwm)
np.save(save_path + 'onehot_encoding_c_rc_4res', one_hot_c_rc_4res)
np.save(save_path + 'onehot_encoding_c_rc_7res', one_hot_c_rc_7res)
np.save(save_path + 'onehot_encoding_c_rc_12res', one_hot_c_rc_12res)
c_rc_df.to_csv(save_path + 'c_rc_df.csv', sep=' ', index=False)
