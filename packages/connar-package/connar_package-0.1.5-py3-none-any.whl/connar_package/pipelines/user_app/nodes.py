import pandas as pd
from moosir_feature.trades.alpha_manager import create_absolute_prediction_alphas


def predict(instances: pd.DataFrame, model):
    prediction_result = model.predict(instances)
    alphas = create_absolute_prediction_alphas(instances=instances,
                                               prediction_result=prediction_result)

    print(alphas)
    return alphas
