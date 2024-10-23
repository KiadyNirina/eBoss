<script>
    import NavNote from "../../../../lib/nav/navNote.svelte";
    import { notes } from "../../../../stores/auth";
    import { onMount } from "svelte";

    export let data;

    let note = null;

    onMount(async () => {
        note = $notes.find(note => note.id == data.id);
        if (note) {
            const endpoint = `http://127.0.0.1:8000/school/noteAPIView/${note.id}`;
            const response = await fetch(endpoint);
            const data = await response.json();
            notes.set(data);
        }
    });
</script>
<div class="content">
    <NavNote/>
    <div class="content-body">
        <div class="body">
            {#if note}
            <h3>Détail d'une note</h3>
            <hr>

            <b>Informations de la période</b>
            <div class="student-info">
                <ul>
                    <li>Année scolaire : <i>{note.school_year}</i></li>
                    <li>Semestre / Trimestre : <i>{note.semester}</i></li>
                    <li>Date de l'examen : <i>27/07/2024</i> à <i>30/07/2024</i></li>
                </ul>
            </div>

            <b>Informations de l'élève</b>
            <div class="student-info">
                <ul>
                    <li>Nom : <i>RAMBELOSON</i></li>
                    <li>Prenom : <i>Kiady Nirina</i></li>
                    <li>Classe : <i>L1</i></li>
                    <li>Numéro d'inscription : <i>1</i></li>
                </ul>
            </div>

            <b>Tableau des notes</b>
            <div class="student-info">
                <table>
                    <thead>
                        <th scope="col">Matière</th>
                        <th scope="col">Coefficient</th>
                        <th scope="col">Note</th>
                    </thead>
                    <tbody>
                        <th scope="row">MATHS</th>
                        <th>2</th>
                        <th>38</th>
                    </tbody>
                </table>
            </div>

            <div class="add">
                <button>Retour</button>
                <button id="modif">Modifier</button>
            </div>
            {:else}
            <p>Chargement...</p>
            {/if}
        </div>
    </div>
</div>

<style>
    /*a{
        text-decoration: none;
        color: white;
    }*/
    .content{
        padding: 1%;
        color: white;
        padding-top: 50px;
        font-size: 20px;
        font-family: 'Trebuchet MS', 'Lucida Sans Unicode', 'Lucida Grande', 'Lucida Sans', Arial, sans-serif;
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
    .body h3{
        text-align: center;
    }
    select{
        width: 100%;
        padding: 8px;
        background: #00383b;
        border: none;
        border-radius: 5px;
        color: white;
        text-align: center;
    }
    label{
        font-size: 15px;
    }
    option{
        color: black;
    }
    .student-info{
        border: 1px solid rgba(255, 255, 255, 0.479);
        padding: 15px;
        border-radius: 5px;
        margin-top: 10px;
        margin-bottom: 20px;
    }
    .add{
        display: flex;
    }
    .add button{
        background-color: transparent;
        border: 1px solid white;
        border-radius: 5px;
        transition: 0.2s;
        padding: 10px;
        margin-bottom: 5px;
        width: 100%;
        color: white;
        font-weight: bolder;
        margin-left: 2px;
        margin-right: 2px;
    }
    .add button:hover{
        background: rgb(193, 193, 193);
        cursor: pointer;
        color: rgb(0, 87, 90);
    }
    #modif{
        background: rgb(193, 193, 193);
        color: rgb(0, 87, 90);
    }
    #modif:hover{
        background-color: transparent;
        border: 1px solid white;
        color: white;
    }
    hr{
        border: 1px solid rgba(255, 255, 255, 0.229);
    }
    .one input{
        width: 99%;
        padding: 8px;
        background: #00383b;
        border: none;
        border-radius: 5px;
        color: white;
        text-align: center;
    }
    table{
        width: 100%;
    }
    table, th{
        border: 1px solid white;
    }
    th{
        padding: 10px;
    }
    table input{
        background: none;
        border: none;
        padding: 10px;
        color: white;
    }
    i{
        font-size: 15px;
    }
    li{
        font-size: 20px;
        line-height: 25px;
    }
</style>