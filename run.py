import pandas as pd
import numpy as np
import fnmatch
import os
import matplotlib.pyplot as plt

def v1():

    # rootdir = raw_input("Where is the data?\nIn particular, what folder are the 001, 002, 003, ... folders located\nthink /Users/taylorandrews/Documents/projects/tms/data/")

    names = ['time', 'CH1', 'CH2', 'CH3', 'CH4']
    RL = {'L': 'CH1', 'R': 'CH2'}
    file_num = 2

    # rootdir = '/Users/taylorandrews/Documents/projects/tms/data/'
    # subdir = '*_filt_original.csv'
    # subdir = 'MEP_RL_1_filt_original.csv' # testing

    # matches = []
    # for root, dirnames, filenames in os.walk(rootdir):
    #     for filename in fnmatch.filter(filenames, subdir):
    #         matches.append(os.path.join(root, filename))

    matches =  ['/Users/taylorandrews/Documents/projects/coding-business/tms/new_data/MRS_010/iSP Trials/iSP_LL_LH_Filt.csv']

    for fname in matches:
        print(f"processing {fname} ({file_num} of {len(matches)})")
        df = pd.read_csv(fname, header=14, names=names, engine='python')
        subject = RL[fname[fname.find('iSP_')+4]]
        df['10tile'] = pd.qcut(df['time'], 10, labels=False)
        sub_df = pd.DataFrame()
        for i in range(10):
            df_seg = df[df['10tile']==i]
            df_seg['scaled'] = (df_seg[subject]-df_seg[subject].min())/(df_seg[subject].max()-df_seg[subject].min())
            sub_df = sub_df.append(df_seg)
        df = sub_df
        df['anomaly_pred'] = np.where(df['scaled'].abs().diff()>0.1, 1, 0).astype(int)

        for i in df[df['anomaly_pred']==1].index.values:
            # if sum(df['anomaly_pred'][i-5:i+5]) == 1:
            #     df.loc[i, 'anomaly_pred'] = 0
            if sum(df['anomaly_pred'][i-min(i, 8000):i]) > 0:
                df.loc[i, 'anomaly_pred'] = 0

        df.to_csv(fname[:-4] + '_auto_labeled.csv')

        file_num += 1

    ## to check accuracy
    # df_labels = pd.read_csv('data/{}/MEP_LL_1_filt.csv'.format(subject), header=14, names=names)
    # df['anomaly_actual'] = df_labels['CH1'].mask(df_labels['CH1'] < 1000, other=0).apply(lambda x: int(x/10000))

    df[df['anomaly_pred'] + df['anomaly_actual'] > 0]


if __name__ == '__main__':

    # filepath =  '/Users/taylorandrews/Documents/projects/coding-business/tms/new_data/MRS_010/iSP Trials/iSP_LL_LH_Filt.csv'
    fp_marked =  '../data/001/MEP_LL_1_filt.csv'
    fp_pure =  '../data/001/MEP_LL_1_filt_original.csv'
    names = ['time', 'CH1', 'CH2', 'CH3', 'CH4']
    df_marked = pd.read_csv(fp_marked, header=14, names=names, engine='python')
    df_pure = pd.read_csv(fp_pure, header=14, names=names, engine='python')




    import matplotlib.pyplot as plt
    plt.plot(df_marked['CH1'])
    plt.plot(df_pure['CH1'])
    plt.show()
