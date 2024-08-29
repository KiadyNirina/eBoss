<script>
    import NavNote from "../../../lib/nav/navNote.svelte";
    import { onMount } from "svelte";
    import { getUserProfile } from "../../../lib/auth";
    import { getStoreValue, token, notes, userProfile } from "../../../stores/auth";

    let user;
    let data = {};

    $: userProfile.subscribe(value => user = value);

    async function fetchNote() {
        const endpoint = `http://127.0.0.1:8000/school/noteListAPIView/?school=${user.school_name}`;
        const response = await fetch(endpoint);
        const result = await response.json();
        notes.set(result);
        data = result;
    }

    onMount(async () => {
        const $token = getStoreValue(token);
        if($token) {
            const profile = await getUserProfile();
            if(profile){
                userProfile.set(profile);
            } else {
                goto('/login');
            }
        };
        fetchNote();
    });

</script>
<div class="content">
    <NavNote/>
    <div class="content-body">
        <div class="body">
            <form action="" method="post">
                <input class="input" type="search" name="" id="" placeholder="Entrer le nom de l'élève ou l'année scolaire ou classe ou semestre ou matière">
            </form>
            <h3>Gestion des notes</h3>
            <hr>
            <div class="add">
                <button>
                    <a href="/school/notes/add">
                        <img src="/icons/ajouter.png" alt="">
                        <span>Ajouter une note</span>
                    </a>
                </button>
            </div>

            <div class="filter">
                <p>Trier par :
                <span><a href="">Année Scolaire</a></span>
                <span><a href="">Semestre</a></span>
                <span><a href="">Classe</a></span>
                <span><a href="">Matière</a></span>
                <span><a href="">Numéro d'inscription</a></span>
                </p>
            </div>
            <hr>

            <p>Listes des notes disponibles :</p>
            <ul>
                {#if Object.keys(data).length > 0}
                    {#each Object.keys(data) as note}
                        {#each data[note] as record}
                        <li>
                            <a href="/school/notes/{record.id}">
                                <div class="">
                                    <span>N°{record.id} {record.student}</span><br>
                                    <span id="detail">Date d'ajout: 29-07-2024 / Année scolaire : {record.school_year} / {record.semester} / classe : {record.classe} / matière : {record.matiere}</span>
                                </div>
                            </a>
                            <div class="img">
                                <a href=""><img src="/icons/modifier.png" alt=""></a>
                                <a href=""><img src="/icons/supprimer.png" alt=""></a>
                            </div>
                        </li>  
                        {/each}
                    {/each}
                {/if}
                <hr>
            </ul>
        </div>
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
    .body{
        padding: 1%;
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
    hr{
        border: 1px solid rgba(255, 255, 255, 0.229);
    }
    #detail{
        font-size: 14px;
    }
    li{
        padding: 10px;
        display: flex;
        align-items: center;
    }
    li:hover{
        background: grey;
    }
    .img{
        margin-left: auto;
    }
    li .img img{
        height: 30px;
        padding: 5px;
        border-radius: 5px;
    }
    .img img:hover{
        background: rgb(70, 70, 70);
    }
    .filter p{
        display: flex;
    }
    .filter span{
        margin-left: auto;
        margin-right: auto;
    }
</style>