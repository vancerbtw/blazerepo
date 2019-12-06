var wordInput = document.getElementById("search-box");
var form = document.getElementById("search-form");

async function retrieveSearch(search) {
    try {
        const response = await fetch('https://blazerepo.com/packages/search/' + search, {
            method: 'POST'
        });
        return response.json()
    } catch (error) {
        return {
            error: error
        }
    }
}

function search(input) {
    retrieveSearch(input).then((response) => {
        response.results.forEach(package => {
            console.log(package.name)
        });
    }).catch((err) => {
        throw err;
    })
}

form.addEventListener("submit", function(evt) {
    search(wordInput.value);
});