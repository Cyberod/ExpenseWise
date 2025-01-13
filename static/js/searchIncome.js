const searchField = document.querySelector('#searchField')
const tableOutput = document.querySelector(".table-output")
const appTable = document.querySelector(".app-table")
const paginationContainer = document.querySelector(".pagination-container")
const tBody = document.querySelector(".table-body")


tableOutput.style.display = "none"

searchField.addEventListener('keyup', (e) => {
    const searchValue = e.target.value

    if (searchValue.trim().length > 0) {
        paginationContainer.style.display = "none";
        tBody.innerHTML = "";

        fetch("/Income/search-income", {
            body: JSON.stringify({ searchText: searchValue }),
            method: "POST",
        })

        .then((res) => res.json())
        .then((data) => {

            tableOutput.innerHTML = '';
            tBody.innerHTML = '';

            tableOutput.style.display = "block"
            appTable.style.display = "none"

            if (data.length === 0) {
                tableOutput.innerHTML = `    
                <div class="no-results text-center p-4">
                    <h4 class="text-muted">No results found</h4>
                </div>`
            }else {
                // Create table structure if results are found
                tableOutput.innerHTML = `
                <table class="table table-striped table-hover">
                    <thead>
                        <tr>
                            <th>Amount</th>
                            <th>Category</th>
                            <th>Description</th>
                            <th>Date</th>
                        </tr>
                    </thead>
                    <tbody class="table-body">
                    </tbody>
                </table>
                `;

                const newTBody = tableOutput.querySelector(".table-body");

                data.forEach(item => {
                    newTBody.innerHTML +=`               
                <tr>
                    <td>${item.source}</td>
                    <td>${item.amount}</td>
                    <td>${item.description}</td>
                    <td>${item.date}</td> 
                </tr>`
                    
                });


            }

        });
    }else{
        tableOutput.style.display = "none"
        appTable.style.display = "block"
        paginationContainer.style.display = "block"
    }
});