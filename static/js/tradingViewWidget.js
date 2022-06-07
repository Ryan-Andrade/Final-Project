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
    "width": "100%",
    "height": 500,
    "locale": "en",
    "colorTheme": "dark",
    "isTransparent": false,
    "autosize": true,
    "showVolume": false,
    "hideDateRanges": false,
    "scalePosition": "right",
    "scaleMode": "Normal",
    "fontFamily": "-apple-system, BlinkMacSystemFont, Trebuchet MS, Roboto, Ubuntu, sans-serif",
    "noTimeScale": false,
    "valuesTracking": "1",
    "chartType": "line",
    "fontColor": "#787b86",
    "gridLineColor": "rgba(240, 243, 250, 0.06)",
    "container_id": "tradingview_298c4"
  }
    );