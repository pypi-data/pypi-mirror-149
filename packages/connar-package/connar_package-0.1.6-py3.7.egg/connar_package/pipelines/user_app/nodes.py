import pandas as pd
from moosir_feature.trades.alpha_manager import create_absolute_prediction_alphas


def predict(instances: pd.DataFrame, model):
    prediction_result = model.predict(instances)

    # todo: move this to the feature package
    if len(prediction_result) == 0:
        alphas = pd.DataFrame(columns=['Prediction', 'Signal'])
        alphas.index.name = "Timestamp"
        return alphas

    alphas = create_absolute_prediction_alphas(instances=instances,
                                               prediction_result=prediction_result)

    return alphas
