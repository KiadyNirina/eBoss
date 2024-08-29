<script>
    import { onMount } from "svelte";
    import NavPresence from "../../../lib/nav/navPresence.svelte"
    import Loading from "../../../lib/loading.svelte";
    import { classes, userProfile, courses, schoolName } from "../../../stores/auth";

    /*let menu = false
    let isLoading = true;*/
    let selected = false;
    let user;

    $: userProfile.subscribe(value => user = value);

    /*const loading = setTimeout(() => {
        isLoading = false;
    }, 1000);

    onMount(() => {
        loading;
    })*/

    async function fetchCourse(school_name, classe_name) {
        const response = await fetch(`http://localhost:8000/school/courseAPI/${school_name}/${classe_name}/`);
        const data = await response.json();
        courses.set(data);
    }

    function handleClass(school_name, classe_name){
        selected = true;
        fetchCourse(school_name, classe_name);
    }

</script>

<div class="content">
    <NavPresence />
    <div class="content-body">
        <!-- {#if isLoading}
            <div class="loading">
                <Loading />
            </div>
        
        {:else} -->

        <div class="body">
            <h1>Année scolaire : 2023 - 2024</h1>
            <form action="" method="post">
                <input class="input" type="search" name="" id="" placeholder="Entrer la date du jour">
            </form>
            <h3>Gestion des cours</h3>
            <div class="add">
                <button>
                    <a href="/school/presence/add/">
                        <img src="/icons/ajouter.png" alt="">
                        <span>Ajouter les informations d'aujourd'hui</span>
                    </a>
                </button>
            </div>
            <hr>
            <p>Liste des classes :</p>
            <ul>
                {#each user.school_classes as classes}
                    <li on:click={() => handleClass(user.school_name, classes)}><div class="classe">
                        {classes}
                    </div></li>
                {/each}
            </ul><hr>
            <p>Liste des enregistrements disponibles :</p>
            <ul>
                {#if selected}
                    {#if $courses.length > 0}
                        {#each $courses as course}
                            <li><a href="/school/presence/{course.id}">
                                <div class="classe">
                                    {course.classe} : {course.date}
                                </div>
                            </a></li>
                        {/each}
                    {:else}
                        <p>Rien à afficher</p>
                    {/if}
                {/if}
            </ul>
        </div>
        
        <!--{/if}-->
    </div>
</div>

<style>

    .input{
        width: 100%;
        padding: 10px;
        border-radius: 5px;
        border: none;
        background: rgba(255, 255, 255, 0.559);
    }

    a{
        text-decoration: none;
        color: white;
    }

    .add a{
        display: flex;
        align-items: center;
    }
    .add img{
        height: 30px;
        margin-right: 10px;
    }
    .add button{
        background: transparent;
        border: 1px solid white;
        border-radius: 5px;
        transition: 0.2s;
        padding: 10px;
        margin-bottom: 5px;
    }
    .add button:hover{
        background: rgba(128, 128, 128, 0.574);
    }

    .content{
        padding: 1%;
        color: white;
        padding-top: 60px;
        font-size: 20px;
    }
    .content-body{
        margin-left: 15%;
        margin-right: 15%;
        background: #005358;
        padding: 10px;
        border-radius: 5px;
        border: none;
    }
    .loading{
        display: flex;
        align-items: center;
        justify-content: center;
    }
    hr{
        border: 1px solid rgba(255, 255, 255, 0.229);
    }
    .body{
        padding: 1%;
    }
    .classe{
        padding: 10px;
    }
    .classe:hover{
        background: #00393c;
    }
    h1{
        font-size: 20px;
        text-align: center;
        padding: 5px;
        border: 1px solid rgba(255, 255, 255, 0.282);
    }

</style>