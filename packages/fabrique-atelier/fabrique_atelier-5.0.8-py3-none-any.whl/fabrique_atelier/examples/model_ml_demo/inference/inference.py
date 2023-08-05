## 0. define parameters

import numpy as np 
import json
import lightgbm as lgb

classes = ("about", "services", "contacts", "roaming", "tariffs",
           "simcards", "balance", "internet", "messaging", "support")

np.seterr(all='raise') #raise errors on division by zero for example

bst = lgb.Booster(model_file='./inference/model.txt')  # init model

def predict(samples):

    results = []

    for sample in samples:
        
        ## 1. extract features from json message

        # 1.1. parse message and get features
        mes = json.loads(sample)
        features = np.array([mes['traffic'][cls] for cls in classes]).flatten()

        ## 2. make prediction

        # 2.1 get prediction
        pred_vals = bst.predict([features, ])[0]

        # 2.2 normalize scores, get class
        try:
            scores = pred_vals/pred_vals.sum()
        except:
            scores = pred_vals
        reason = classes[scores.argmax()]

        # 2.3 make and serialize message
        scores_dict = {cls: round(scores[i], 2) for i, cls in enumerate(classes)}
        res = dict(ts=mes['ts'], uid=mes['uid'], number=mes['number'], classes=scores_dict, reason=reason)
        
        results.append(json.dumps(res))
        
    return results
