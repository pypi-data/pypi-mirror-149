import pandas as pd
import pytest
import numpy as np

from moosir_feature.trades.alpha_manager import create_quantile_alphas

def test_create_quantile_alphas():
    # arrange

    preds_df = pd.DataFrame(data={"pred_col": [0.1, 0.2, 0.3, 0.4, 0.5]})
    instances = pd.DataFrame(data=np.random.random([5, 1]))

    # assert
    result = create_quantile_alphas(instances=instances, prediction_result=preds_df, quantile_threshold=0.2)

    # act
    assert result["Signal"].iloc[0] == -1
    assert result["Signal"].iloc[1] == 0
    assert result["Signal"].iloc[2] == 0
    assert result["Signal"].iloc[3] == 0
    assert result["Signal"].iloc[4] == 1
