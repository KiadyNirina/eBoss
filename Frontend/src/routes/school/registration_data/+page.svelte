<script>
    import { onMount } from "svelte";
    import NavData from "../../../lib/nav/navData.svelte";
    import Loading from "../../../lib/loading.svelte";
    import { ClassesStore, StudentsStore } from "../../../lib/studentsList";

    let menu = false
    let isLoading = true;
    let selected = false;
    const loading = setTimeout(() => {
        isLoading = false;
    }, 1000);

    onMount(() => {
        loading;
    })

</script>

<div class="content">
    <NavData />
    <div class="content-body">
        {#if isLoading}
            <div class="loading">
                <Loading />
            </div>
        
        {:else}

        <div class="body">
            <form action="" method="post">
                <input class="input" type="search" name="" id="" placeholder="Entrer le nom ou prénom ou classe ou motif">
            </form>
            <h3>Sauvegarde des données</h3>
            <hr>
            <div class="add">
                <button>
                    <a href="/school/registration_data/add">
                        <img src="/icons/ajouter.png" alt="">
                        <span>Ajouter les informations d'aujourd'hui</span>
                    </a>
                </button>
            </div>
            <p>Liste des données disponibles :</p>
            <table>
                <thead>
                    <th scope="col">id</th>
                    <th scope="col">Date</th>
                    <th scope="col">Nom</th>
                    <th scope="col">Prénom</th>
                    <th scope="col">Classe</th>
                    <th scope="col">Prof de</th>
                    <th scope="col">Motif</th>
                    <th scope="col">Somme</th>
                    <th scope="col">Reste</th>
                    <th scope="col">Type</th>
                    <th></th>
                </thead>
                <tbody>
                    <th scope="row">4</th>
                    <td>28-11-2024</td>
                    <td>Rambeloson</td>
                    <td>Kiady Nirina</td>
                    <td>L3</td>
                    <td></td>
                    <td>Ecolage 6ème mois</td>
                    <td>70.000 ar</td>
                    <td>0 ar</td>
                    <td>Entrée</td>
                    <td>Modif Supp</td>
                </tbody>
                <tbody>
                    <th scope="row">3</th>
                    <td>05-07-2024</td>
                    <td>Rasamoelison</td>
                    <td>Adolphe</td>
                    <td>L1, L2</td>
                    <td>Anglais, Français, Malagasy</td>
                    <td>Salaire 6ème mois</td>
                    <td>250.000 ar</td>
                    <td>50.000 ar</td>
                    <td>Sortie</td>
                    <td><div class="action">
                        <a href=""><img src="/icons/modifier.png" alt=""></a>
                        <a href=""><img src="/icons/supprimer.png" alt=""></a>
                    </div></td>
                </tbody>
                <tbody>
                    <th scope="row">2</th>
                    <td>12-07-2024</td>
                    <td>Rakotosolofo</td>
                    <td>Jean de Dieu</td>
                    <td>L1</td>
                    <td></td>
                    <td>Ecolage 3ème mois</td>
                    <td>70.000 ar</td>
                    <td>0 ar</td>
                    <td>Entrée</td>
                    <td>Modif Supp</td>
                </tbody>
                <tbody>
                    <th scope="row">1</th>
                    <td>05-07-2024</td>
                    <td>John</td>
                    <td>Doe</td>
                    <td>L1</td>
                    <td></td>
                    <td>Ecolage 6ème mois</td>
                    <td>70.000 ar</td>
                    <td>0 ar</td>
                    <td>Entrée</td>
                    <td><div class="action">
                        <a href=""><img src="/icons/modifier.png" alt=""></a>
                        <a href=""><img src="/icons/supprimer.png" alt=""></a>
                    </div></td>
                </tbody>
            </table>
        </div>
        
        {/if}
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
        margin-left: 5%;
        margin-right: 5%;
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
    table{
        width: 100%;
        text-align: center;
        border: 1px solid rgb(174, 174, 174);
        font-size: 18px;
    }
    th, td{
        margin-left: auto;
        margin-right: auto;
        border-left: 1px solid rgb(174, 174, 174);
        border-bottom: 1px solid rgb(174, 174, 174);
        padding: 10px;
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
    .action img{
        height: 30px;
        transition: 0.2s;
    }
    .action img:hover{
        background: rgba(128, 128, 128, 0.527);
        border-radius: 5px;
    }

</style>