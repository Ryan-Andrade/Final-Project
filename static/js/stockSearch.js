const search = document.getElementById('search');
const matchList = document.getElementById('match-list');

// Search stocks.json and filter it
const searchStocks = async searchText => {
    const res = await fetch('../static/data/stockTickerInfo2.json');
    const stocks = await res.json();

    console.log(stocks);

    // Get matches to current text input
    let matches = stocks.filter(stock => {
        const regex = new RegExp(`^${searchText}`, 'gi');
        return stock.ticker.match(regex) || stock.name.match(regex)
    });

    if(searchText.length == 0) {
        matches = [];
        matchList.innerHTML = '';
    }

    outputHtml(matches);
};

// Show results in HTML
const outputHtml = matches => {
    if(matches.length > 0) {
        const html = matches.map(
            match => `
            <div class="card card-body mb-1" onclick= "autofill('${match.ticker}');">
                <h4>Ticker: ${match.ticker}</h4>
                <p>Company Name: ${match.name}</p>
            </div>
        `
        )
        .join('');

        matchList.innerHTML = html;
    }
};

// Gets called when the user clicks on the search results,
// Inserts the ticker into the search bar,
// Calls myFunction() to update the data.
// Clears output.
function autofill(clicked_ticker) {
    document.getElementById('search').value = clicked_ticker;
    myFunction();
    matchList.innerHTML = '';
}


search.addEventListener('input', () => searchStocks(search.value));