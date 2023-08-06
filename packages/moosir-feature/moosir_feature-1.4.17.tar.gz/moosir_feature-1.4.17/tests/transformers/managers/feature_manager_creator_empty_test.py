import pytest

from moosir_feature.transformers.managers.feature_manager import *
from moosir_feature.transformers.indicators.feature_calculator import *
from moosir_feature.transformers.basic_features.feature_calculator import *


@pytest.fixture
def ohlc():
    df = pd.DataFrame(data=np.random.rand(100, 4),
                      columns=["Open", "High", "Low", "Close"],
                      index=pd.date_range(start="01/01/2000", periods=100, freq="10T"),
                      )
    df.index.name = "Timestamp"
    return df


def _print(features, targets, all):
    print(features)
    print(features.columns)
    print('-' * 50)
    print(targets)
    print(targets.columns)
    print('-' * 50)
    print(all)
    print(all.columns)


def _run_manager(ohlc, target_settings, feature_settings_list, lag_settings_list):
    mgr = FeatureCreatorManager(target_settings=target_settings,
                                feature_settings_list=feature_settings_list,
                                lag_settings_list=lag_settings_list
                                )

    # act
    features, clean_data = mgr.create_features(instances=ohlc)

    return features, clean_data


def test_feature_manager_calculate_when_every_emtpy(ohlc: pd.DataFrame):
    # arrange
    target_settings = TargetSettings()
    feature_settings_list = []
    lag_settings_list = []

    # act
    features, clean_data = _run_manager(ohlc=ohlc,
                                        target_settings=target_settings,
                                        feature_settings_list=feature_settings_list,
                                        lag_settings_list=lag_settings_list)

    _print(features, clean_data, clean_data)

    # assert features
    assert features.shape == ohlc.shape
