const search = document.getElementById('search');
const matchList = document.getElementById('match-list');

// Search stocks.json and filter it
const searchStocks = async searchText => {
    const res = await fetch('../static/data/stocks1.json');
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
            <div class="card card-body mb-1" id=${match.ticker} onclick= "autofill('${match.ticker}');">
                <h4>Ticker: ${match.ticker}</h4>
                <p>Company Name: ${match.name}</p>
            </div>
        `
        )
        .join('');

        matchList.innerHTML = html;
    }
};

//document.onclick = autofill

function autofill(clicked_id) {
    clicked_id.cancelBubble = true;
    console.log(clicked_id);
    document.getElementById('search').value = clicked_id;
    myFunction();
}


search.addEventListener('input', () => searchStocks(search.value));