import scoreval


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
import os


# Set path parameters, this is only applicable in this example and you can set it as you wish
BASE_DIR = "E:\\workspace\\stock"
RUN_DATE = '20220304' # str(datetime.now())[:10].replace('-','')

# Load test data
DATA_DIR = os.path.join(BASE_DIR,'data', RUN_DATE) # path to save processed data files

# Load model file
MODEL_DIR = os.path.join(BASE_DIR,'python/tf/models') # path where the model spec is located
models = []
models.append(
   tf.keras.models.load_model(os.path.join(MODEL_DIR,'./LG-L60D64L32FC16BN-v1.h5')),
)
models.append(
   tf.keras.models.load_model(os.path.join(MODEL_DIR,'./LG-L60D64L32FC16BN-v2.h5')),
)
models.append(
   tf.keras.models.load_model(os.path.join(MODEL_DIR,'./LG-L60D64L32FC16BN-v3.h5')),
)


with open(os.path.join(DATA_DIR, 'oot_lg.npz'), 'rb') as fp:
    oot_data = np.load(fp)
    oot_X_arr, oot_S_arr, oot_P_arr, oot_I_arr, oot_Y_arr, oot_R_arr = oot_data['x'], oot_data['s'], oot_data['p'],oot_data['i'],oot_data['y'],oot_data['r']

# Make my data set as a pandas DataFrame, this is required by ScoreEval
df_y = pd.DataFrame(np.concatenate([oot_Y_arr, oot_R_arr],axis=1))
df_y.columns=['label', 'symbol', 'date']
df_y['label'] = df_y['label'].astype(np.float16).astype(np.int16)
df_y.head()


se_oot = scoreval.ScoreEval(models)


# Run score, make sure the models have the same inputs. SE will call model.predict for each model. 
# That is not a good idea to take models with different inputs. Please always compare apple to apple. 
# Make sure X and Y have the same rows so that the score can be produced properly. 
rows=100
se_oot.run_score([oot_X_arr[:rows],oot_S_arr[:rows],oot_P_arr[:rows],oot_I_arr[:rows],], df_y.head(rows))

# Calculate precision/recall metrics by OP/Cutoff
se_oot.score_cut()

# Plot PR chart: it is better if the curve is reaching to the right upper corner. 
se_oot.plot_pr()

# WOE/IV chart: it is better if the bars' height is large at low and high bins, which is called 'indicative power'. 
# IV, in the chart title, is a weighed average of all bins, and it is better if larger.
se_oot.iv()

# The bar is how many 1-samples in that day. The lines is score quantiles in that day. 
# eg. q99 means the score value where 99% samples are less than it. 
se_oot.daily_qtls(figsize=(20,10))

print('done')