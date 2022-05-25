<script>
    import {browser} from "$app/env";

    let currentPage = 0;
    let skip = 0;
    let limit = 10;
    let selection = [];
    $: params = {
        skip: skip,
        limit: limit
    }
    let incident_data = {"incidents": [], "total": 0};

    async function getIncidents(params) {
        if (browser) {
            let urlParams = new URLSearchParams(params).toString();
            const data = await fetch(`/incidents/data?${urlParams}`, {
                method: 'GET',
                credentials: 'include',
                headers: {
                    'Content-Type': 'application/json'
                }
            })
            incident_data = await data.json();
        }
    }

    async function changePage(event) {
        incident_data = {"incidents": [], "total": 0};
        let newPage;
        switch (event.target.innerHTML) {
            case "Previous":
                newPage = currentPage - 1;
                break;
            case "Next":
                newPage = currentPage + 1;
                break;
            default:
                newPage = parseInt(event.target.innerHTML) - 1;
        }
        currentPage = newPage;
        skip = newPage * limit;
        document.getElementById('allSelector').checked = false;
    }

    async function changeLimit(event) {
        limit = parseInt(event.target.innerHTML);
        if (currentPage > (total / limit >> 0)) {
            await changePage({'target': {'innerHTML': "1"}})
        }
    }

    async function toggleSelectAll(event) {
        let checkboxes = document.getElementsByName('row');
        for (let i = 0, n = checkboxes.length; i < n; i++) {
            // checkboxes[i].checked = event.target.checked;
            let checkValue = parseInt(checkboxes[i].value)
            if (event.target.checked) {
                if (!selection.includes(checkValue)) {
                    selection.push(checkValue);
                }
            } else {
                selection = selection.filter(id => id !== checkValue);
            }
        }
        selection.sort((a, b) => (a - b));
        selection = selection;
    }

    $: getIncidents(params);
    $: incidents = incident_data.incidents;
    $: total = incident_data.total;
    $: pages = [...Array((total / limit >> 0) + 1).keys()];
    $: maxPage = (total / limit >> 0);
</script>

<div class="field">
    <div class="control">
        <input class="input" type="text" placeholder="Search">
    </div>
</div>
<div class="columns is-centered">
    <div class="column">
        <div class="is-pulled-right columns" style="padding: 1.25em;">
            <button class="button is-small" on:click={changeLimit}>10</button>
            <button class="button is-small" on:click={changeLimit}>25</button>
            <button class="button is-small" on:click={changeLimit}>50</button>
            <button class="button is-small" on:click={changeLimit}>100</button>
        </div>
        <table class="table box">
            <thead>
            <tr>
                <th><input type="checkbox" id="allSelector" on:click={toggleSelectAll}></th>
                <th>ID</th>
                <th>Owner</th>
                <th>Data</th>
            </tr>
            </thead>
            <tbody>
            {#if (incidents)}
                {#each incidents as incident}
                    <tr class='{selection.includes(incident.id) ? "is-selected" : ""}'>
                        <td><input type="checkbox" name="row" value="{incident.id}"
                                   bind:group={selection}></td>
                        <td>{incident.id}</td>
                        <td>{incident.owner.display_name ? incident.owner.display_name : incident.owner.email}</td>
                        <td>{incident.data}</td>
                    </tr>
                {/each}
            {/if}
            </tbody>
        </table>
        <nav class="pagination" role="navigation" aria-label="pagination">
            {#if (currentPage === 0)}
                <button class="button pagination-previous"
                        disabled>Previous
                </button>
            {:else}
                <button class="button pagination-previous"
                        on:click={changePage}>Previous
                </button>
            {/if}
            {#if (currentPage === maxPage)}
                <button class="button pagination-next"
                        disabled>Next
                </button>
            {:else}
                <button class="button pagination-next"
                        on:click={changePage}>Next
                </button>
            {/if}
            <ul class="pagination-list">
                {#each pages as page}
                    {#if (page === currentPage)}
                        <li>
                            <button class="button pagination-link is-current"
                                    aria-label="Page {page+1}" aria-current="page"
                                    on:click={changePage}>{page + 1}</button>
                        </li>
                    {:else}
                        <li>
                            <button class="button pagination-link"
                                    aria-label="Goto page {page+1}"
                                    on:click={changePage}>{page + 1}</button>
                        </li>
                    {/if}
                {/each}
            </ul>
        </nav>
    </div>
</div>