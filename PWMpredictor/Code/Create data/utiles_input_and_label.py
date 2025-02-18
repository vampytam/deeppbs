import numpy as np

def ht_one_hot_encode_amino_acids(files_list):
    """this function is responsible to produce the OneHot
    encoding for the AMINO ACIDS strings.
    The OneHOt matrix is used for the convolutional process"""
    return list(map(one_hot_encoding_amino_acids, files_list))


def one_hot_encoding_amino_acids(sequence):
    # define universe of possible input values
    amino_alphabet = 'ACDEFGHIKLMNPQRSTVWYX'
    # define a mapping of chars to integers
    char_to_int = dict((c, i) for i, c in enumerate(amino_alphabet))

    # integer encode iht_one_hot_encode_amino_acidsnput data
    integer_encoded = [char_to_int[char] for char in sequence]

    # one hot encode
    onehot_encoded = list()
    for value in integer_encoded:
        if value == 20:
            onehot_encoded.append(list(0.05 * np.ones(20)))
        else:
            letter = [0 for _ in range(len(amino_alphabet)-1)]
            letter[value] = 1
            onehot_encoded.append(letter)
    return np.asarray(onehot_encoded)


def dic_unique_amino_acids(amino_seq):
    val = np.arange(0, len(amino_seq) - 1)
    dic = dict((val, i) for i, val in enumerate(amino_seq))
    return dic



def oneHot_Amino_acid_vec(amino_seq):
    """this function is responsible to produce the OneHot vector
    encoding for the amino acids strings."""
    one_hot_matrix_amino_acids = ht_one_hot_encode_amino_acids(amino_seq)
    one_hot_amino_acids_vec = []

    # create a matrix: each row represents Amino acid
    for array in one_hot_matrix_amino_acids:
        one_hot_amino_acids_vec.append(array.flatten())
    return np.array(one_hot_amino_acids_vec)


def group_zf_by_protein_name(file_C_RC):
    """this function is responsible to group the zf according to their protein """
    protein = file_C_RC.UniProt_ID.unique()
    val = np.arange(0, len(protein) - 1)
    dic = dict((val, i) for i, val in enumerate(protein))
    file_C_RC['Source'] = file_C_RC['UniProt_ID']
    file_C_RC.rename(columns={"Source": "groups"}, inplace=True)
    return file_C_RC.replace({"groups": dic})