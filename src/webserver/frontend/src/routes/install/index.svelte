<script>
    import {browser} from '$app/env';
    import {goto} from "$app/navigation";
    import "../../global.scss";

    let badInstall = false;

    let password = "";
    let confirmPassword = "";
    let passwordMismatch;
    $: passwordMismatch = password !== confirmPassword;

    if (browser) {
        fetch('/install/status', {
            method: 'GET',
            credentials: 'include',
            headers: {
                "Content-Type": "application/json"
            }
        })
            .then(r => r.json())
            .then(d => {
                if (d.status) {
                    goto("/")
                }
            });
    }

    async function install(event) {
        if (passwordMismatch) {
            return
        }
        let jsonData = {};
        let data = new FormData(event.target);
        data.forEach((value, key) => jsonData[key] = value);
        delete jsonData.confirmPassword
        const response = await fetch(`/api/install`, {
            method: 'POST',
            credentials: 'include',
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(jsonData),
        }).then((r) => r.ok ? goto("/") : (badInstall = true));
    }
</script>

<div class="container has-text-centered">
    <img alt="OpenSOAR logo" src="/opensoar_logo.png" width="600"/>
</div>
<section class="is-fullheight">
    <h1 class="title has-text-centered">
        Initial Configuration
    </h1>
    <div class="container">
        <div class="columns is-centered">
            <div class="column is-5-tablet is-4-desktop is-3-widescreen">
                <form on:submit|preventDefault={install}>
                    {#if badInstall}
                        <p class="help is-danger block">Installation failed</p>
                    {/if}
                    <div class="field">
                        <label for="email" class="label">Admin User Email</label>
                        <div class="control">
                            <input type="email" placeholder="e.g. admin@example.com" id="email"
                                   class="input" name="email" required>
                        </div>
                    </div>
                    <div class="field">
                        <label for="password" class="label">Password</label>
                        <div class="control">
                            <input type="password" id="password" class="input" name="password" bind:value="{password}"
                                   required>
                        </div>
                    </div>
                    <div class="field">
                        <label for="confirmPassword" class="label">Confirm Password</label>
                        <div class="control">
                            <input type="password" id="confirmPassword" class="input" name="confirmPassword" bind:value="{confirmPassword}"
                                   required>
                        </div>
                        {#if passwordMismatch}
                            <p class="help is-danger block">Passwords do not match</p>
                        {/if}
                    </div>
                    <div class="field">
                        <label for="display_name" class="label">Display Name</label>
                        <div class="control">
                            <input type="text" id="display_name" class="input" name="display_name">
                        </div>
                    </div>
                    <div class="field">
                        <button type="submit" class="button is-success">
                            Install
                        </button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</section>