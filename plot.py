
import argparse
import os
import pandas as pd
import numpy as np
import socket
import matplotlib.pyplot as plt


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', type=str, default='./results', help="Specify the path to load the results")
    parser.add_argument('-t','--timestamp', type=str, default=None, help="Specify the timestamp when the experiement started")
    args = parser.parse_args()
    
    if args.timestamp is None:
        log = args.path+'/'+np.sort(os.listdir(args.path))[-1]
    else:
        log = args.path+'/'+args.timestamp

    dfs = [pd.read_csv(log+'/'+fn) for fn in np.sort(os.listdir(log)) if fn[-4:]=='.csv']
    devices = [fn[:-4] for fn in np.sort(os.listdir(log))]

    fig, ax = plt.subplots(2,figsize=(12,10))
    fig.suptitle(socket.gethostname())
    for df,d in zip(dfs,devices):
         ax[0].plot(df.Time,df.Util,label=d) 
    ax[0].legend()
    ax[0].set_ylabel('Utilisation %')

    for df,d in zip(dfs,devices):
         ax[1].plot(df.Time,df.Mem,label=d) 
    ax[1].legend()
    ax[1].set_ylabel('Memory %')

    fig.tight_layout()
    fig.savefig(log+'/plot.pdf')
    print(f'plots saved in {log}')
