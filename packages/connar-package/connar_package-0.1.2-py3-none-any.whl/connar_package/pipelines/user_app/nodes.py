import pandas as pd
from moosir_feature.trades.alpha_manager import create_quantile_alphas


def predict(instances: pd.DataFrame, model, alpha_threashold: float):
    preds = model.predict(instances)

    prediction_result = pd.DataFrame(data={"preds": preds}, index=instances.index)

    alphas = create_quantile_alphas(instances=instances,
                                    prediction_result=prediction_result,
                                    quantile_threshold=alpha_threashold)

    return alphas
