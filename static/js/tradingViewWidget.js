// The TradingView Widget embeds trading charts from TradingView.com
var ticker = document.getElementById('ticker').textContent;

new TradingView.MediumWidget(
    {
        "symbols": [
        [
            ticker
        ]
        ],
        "chartOnly": false,
        "width": 1000,
        "height": 500,
        "locale": "en",
        "colorTheme": "dark",
        "isTransparent": false,
        "autosize": false,
        "showVolume": false,
        "hideDateRanges": false,
        "scalePosition": "right",
        "scaleMode": "Normal",
        "fontFamily": "-apple-system, BlinkMacSystemFont, Trebuchet MS, Roboto, Ubuntu, sans-serif",
        "noTimeScale": false,
        "valuesTracking": "1",
        "chartType": "line",
        "fontColor": "#787b86",
        "gridLineColor": "rgba(42, 46, 57, 0.06)",
        "container_id": "tradingview_0a9d5"
    });