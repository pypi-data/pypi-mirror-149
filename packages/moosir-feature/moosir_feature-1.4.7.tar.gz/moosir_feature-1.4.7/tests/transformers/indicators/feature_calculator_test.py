import pytest

from moosir_feature.transformers.indicators.feature_calculator import *
from moosir_feature.transformers.indicators.tech_indicators import *


@pytest.fixture
def ohlc_prices():
    return pd.DataFrame(data=np.random.rand(10, 4), columns=["Open", "High", "Low", "Close"])


def test_create_operators():
    # arrange
    indicator_names = [RsiOperator.__name__,
                       BollingerBandOperator.__name__,
                       AtrOperator.__name__,
                       MaOperator.__name__,
                       MomentomOperator.__name__,
                       WmaOperator.__name__,
                       AdxOperator.__name__,
                       ]
    look_back_periods = [10, 20]
    prefix = "random"

    # act
    result = create_operators(look_back_periods=look_back_periods,
                              prefix=prefix,
                              tech_indicator_names=indicator_names)

    # assert
    assert len(result) == len(look_back_periods) * len(indicator_names)


def test_apply_historical_return(ohlc_prices):
    # arrange
    periods = [3, 4]
    magnifier_multiplier = 2
    expected_operators = [HistoricalReturnOperator.__name__]
    original_ohlc = ohlc_prices.copy()

    # act
    result = apply_historical_return(ohlc_price=ohlc_prices,
                                     periods=periods,
                                     magnifier_multiplier=magnifier_multiplier)

    # assert
    assert_operators_results(operator_names=expected_operators,
                             look_back_periods=periods,
                             original_ohlc=original_ohlc,
                             result=result,
                             expected_columns=["Ind-Returns"])


def test_apply_forward_max_return_and_price(ohlc_prices):
    # arrange
    periods = [3, 4]
    expected_operators = [ForwardMaxPriceAndReturn.__name__]
    original_ohlc = ohlc_prices.copy()
    expected_columns = ["Fwd-Price-Max-", "Fwd-Return-Max-"]

    # act
    result = apply_forward_max_return_and_price(ohlc_price=ohlc_prices,
                                                periods=periods)

    # assert
    assert len(result.columns) == 4 + 2 * len(expected_operators) * len(periods)

    for col in expected_columns:
        assert len(result.filter(like=col).columns) == len(periods)

    result_ohlc = result[["Open", "High", "Low", "Close"]]
    pd.testing.assert_frame_equal(result_ohlc, original_ohlc)


def test_apply_forward_min_return_and_price(ohlc_prices):
    # arrange
    periods = [3, 4]
    expected_operators = [ForwardMinPriceAndReturn.__name__]
    original_ohlc = ohlc_prices.copy()
    expected_columns = ["Fwd-Price-Min-", "Fwd-Return-Min-"]

    # act
    result = apply_forward_min_price_and_return(ohlc_price=ohlc_prices,
                                                periods=periods)

    # assert
    assert len(result.columns) == 4 + 2 * len(expected_operators) * len(periods)

    for col in expected_columns:
        assert len(result.filter(like=col).columns) == len(periods)

    result_ohlc = result[["Open", "High", "Low", "Close"]]
    pd.testing.assert_frame_equal(result_ohlc, original_ohlc)


def test_forward_highest_return(ohlc_prices):
    # arrange
    periods = [3, 4]
    original_ohlc = ohlc_prices.copy()
    expected_columns = ["Fwd-Price-Min-", "Fwd-Return-Min-",
                        "Fwd-Price-Max-", "Fwd-Return-Max-",
                        "Fwd-Return-Highest-"]

    # act
    result = apply_forward_min_price_and_return(ohlc_price=ohlc_prices,
                                                periods=periods)

    result = apply_forward_max_return_and_price(ohlc_price=result,
                                                periods=periods)

    result = apply_forward_highest_return(ohlc_price=result,
                                          periods=periods)

    # assert
    assert len(result.columns) == 4 + 4 * len(periods) + len(periods)

    for col in expected_columns:
        assert len(result.filter(like=col).columns) == len(periods)

    result_ohlc = result[["Open", "High", "Low", "Close"]]
    pd.testing.assert_frame_equal(result_ohlc, original_ohlc)


def test_apply_technical(ohlc_prices):
    # arrange
    indicators = [RsiOperator.__name__,
                  VilliamrOperator.__name__
                  ]
    original_ohlc = ohlc_prices.copy()
    look_back_periods = [3, 4]

    # act
    result, _ = apply_technical_indicators(ohlc_price=ohlc_prices,
                                           look_back_periods=look_back_periods,
                                           tech_indicator_names=indicators)

    # assert
    assert_operators_results(operator_names=indicators,
                             look_back_periods=look_back_periods,
                             original_ohlc=original_ohlc,
                             result=result,
                             expected_columns=["Rsi", "Willr"])


def test_apply_lags(ohlc_prices):
    # arrange
    periods = [3, 4]
    magnifier_multiplier = 2
    lag_periods = [2]
    return_period_for_lag = [3]

    # act
    _ = apply_historical_return(ohlc_price=ohlc_prices,
                                periods=periods,
                                magnifier_multiplier=magnifier_multiplier)

    # act

    lag_result = apply_lags(ohlc_price=ohlc_prices, lag_periods=lag_periods, ind_periods=return_period_for_lag)

    # assert
    result_cols = lag_result.columns
    #
    assert "Lag-Ind-Returns-3-T-0002" in result_cols
    assert "Lag-Ind-Returns-3-T-0003" not in result_cols


def assert_operators_results(operator_names, look_back_periods, original_ohlc, result, expected_columns):
    assert len(result.columns) == 4 + len(operator_names) * len(look_back_periods)

    for col in expected_columns:
        assert len(result.filter(like=col).columns) == len(look_back_periods)

    result_ohlc = result[["Open", "High", "Low", "Close"]]
    pd.testing.assert_frame_equal(result_ohlc, original_ohlc)
