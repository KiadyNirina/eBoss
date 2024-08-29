<script>
    import NavProfile from '../../../../lib/nav/navProfile.svelte'
    import { onMount } from 'svelte';
    import { getUserProfile, logout } from "../../../../lib/auth";
    import { goto } from '$app/navigation';
    import { token, userProfile, matiere } from "../../../../stores/auth";

    let schoolLevel = '';
    let selected_level = [];
    let selected_classes = [];
    let subject = '';
    let user;

    let level_classes = {
        Ecole: ['12eme', '11eme', '10eme', '9eme', '8eme', '7eme'],
        College: ['6eme', '5eme', '4eme', '3eme'],
        Lycee: ['2nde', '1ere', 'Term'],
        Universite: ['L1', 'L2', 'L3', 'M1', 'M2']
    }

    function toggle_level(level) {
        if(selected_level.includes(level)) {
            selected_level = selected_level.filter(item => item !== level);
        } else {
            selected_level.push(level);
        }
        updateSelectedClasses();
    }

    function updateSelectedClasses() {
        selected_classes = [];
        selected_level.forEach(lev => {
            selected_classes = [...selected_classes, ...level_classes[lev]]
        })
    }

    $: userProfile.subscribe(value => user = value);

    async function handleSubmit(){
        const response = await fetch('http://localhost:8000/school/createClassMatiere/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                school: user.school_name,
                classe: selected_classes,
                subject: subject,
            }),
        });
        const data = await response.json();
        if(response.ok) {
            alert('Ajout avec succes');
            console.log(data)
        } else {
            alert('Ajout avec erreur');
            console.error(data)
        }
    }
    // onMount(async () => {
    //     if(user) {
    //         const profile = await getUserProfile();
    //         if(profile){
    //             userProfile.set(profile);
    //         }else{
    //             goto('/login');
    //         }
    //     } else {
    //         goto('/login');
    //     }
    // });
    // import { StudentsInClassStore, StudentSearched } from '../../../../lib/studentsList.js';
    // import { onMount } from 'svelte';

    // export let data;

    // let student = null;
    // let familialeData = [];

    // onMount(async () => {
    //     student = $StudentsInClassStore.find(student => student.id == data.id) || $StudentSearched.find(student => student.id == data.id);
    //     if (student) {
    //         const endpoint = `http://127.0.0.1:8000/list/class/studentInfoFamiliale/${student.id}/`;
    //         const response = await fetch(endpoint);
    //         familialeData = await response.json();
    //     }
    // });
    
</script>

<div class="content">
    <NavProfile />
    <div class="content-body">
        {#if user}
        
            <div class="body">
                <div class="infoDetail">
                    <h3>Ajout de matière</h3>
                    <ul>
                        {#each $matiere as mat}
                            <li>{mat.subject} : ({mat.classe})</li>
                        {/each}
                    </ul>
                    <form action="">
                        <ul>
                            <li><b>Etablissement</b> : <span>{user.school_name}</span>
                            </li>
                            <li>
                                <b>Niveau scolaire</b> : 
                                    {#each user.school_level as ulevel}
                                        {ulevel}
                                        <input type="checkbox" value="{ulevel}" name="" id="" on:change={() => toggle_level(ulevel)}>
                                    {/each}
                            </li>
                            <li><b>Classes</b> : {selected_classes}</li>
                            <li class="input">
                                <b>Matières</b> : 
                                <input type="text" placeholder="Entrer le nom de la matière" bind:value={subject}>
                            </li>
                        </ul>
                    </form>  
                    <div class="add">
                
                        <a href="/school/profile/">
                            Annuler
                        </a>    
                        <button on:click={handleSubmit}>Ajouter</button>
                    </div>  
                </div>
            </div>
        {:else}
        tsisy
        {/if}
    </div>
</div>

<style>
    .add{
        margin-left: auto;
        margin-right: auto;
    }
    a{
        text-decoration: none;
        color: white;
    }
    .add{
        display: flex;
        align-items: center;
        margin-top: 10px;
    }
    .add a{
        text-align: center;
        width: 100%;
        border: 1px solid white;
        border-radius: 5px;
        font-size: 15px;
        padding: 9px;
        margin-bottom: 5px;
    }
    .add a:hover{
        color: rgb(187, 187, 187);
        border: 1px solid rgb(187, 187, 187);
    }
    .add button{
        background: white;
        border: transparent;
        padding: 10px;
        margin-bottom: 5px;
        width: 100%;
        border: 1px solid white;
        border-radius: 5px;
        color: #003639;
    }
    .add button:hover{
        cursor: pointer;
        background: rgb(177, 177, 177);
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
        padding: 1%;
        border-radius: 5px;
        border: none;
    }
    .body{
        padding: 1%;
    }
    .input{
        display: flex;
        align-items: center;
    }
    input[type='text']{
        width: 100%;
        height: 30px;
        border: none;
        border-radius: 5px;
        background: #003639;
        margin: 5px;
        padding-left: 10px;
        color: white;
    }
    form{
        border: 1px solid rgb(162, 162, 162);
        border-radius: 5px;
    }
    .infoDetail h3{
        font-family: Verdana, Geneva, Tahoma, sans-serif;
    }

</style>