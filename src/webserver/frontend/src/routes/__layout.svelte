<script context="module">
    const publicPages = ['/', '/login', '/install'];

    export async function load({page, session}) {
        const {path} = page;

        if (publicPages.includes(path)) {
            return {};
        }

        if (!session.jwt) {
            return {
                status: 301,
                redirect: '/'
            };
        }

        return {};
    }
</script>
<script>
    import {session} from '$app/stores';
    import "../global.scss";
</script>

{#if $session.user}
    <nav class="navbar" role="navigation" aria-label="main navigation">
        <div class="navbar-brand">
            <a class="navbar-item" href="/">
                <img alt="OpenSOAR logo" src="/opensoar_logo.png"/>
            </a>
        </div>

        <div id="navbarPrimary" class="navbar-menu">
            <div class="navbar-start">
                <a class="navbar-item" href="/incidents">
                    Incidents
                </a>
                {#if $session.user.is_superuser}
                    <a class="navbar-item" href="/argo" rel="external" target="_blank">
                        Argo
                        <i class="fas fa-external-link-alt ml-1"></i>
                    </a>
                    <a class="navbar-item" href="/settings">
                        Settings
                    </a>
                {/if}
            </div>

            <div class="navbar-end">
                <div class="navbar-item">
                    <div class="buttons">
                        <a href="/profile">
                            <i class="fas fa-user"></i>
                        </a>
                    </div>
                </div>
                <div class="navbar-item">
                    <div class="buttons">
                        <a href="/logout" class="button">
                            Log out
                        </a>
                    </div>
                </div>
            </div>
        </div>
    </nav>
{/if}

<section class="is-fullheight">
    <div class="hero-body">
        <div class="container">
            <slot></slot>
        </div>
    </div>
</section>
