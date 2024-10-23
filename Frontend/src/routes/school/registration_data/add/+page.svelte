<script>
    import NavData from "../../../../lib/nav/navData.svelte";
    import { userProfile, classes, matiere } from "../../../../stores/auth";
    import { onMount } from "svelte";

    let user;
    let subject = "";
    let student = "";
    let selected_classes = "";
    let prof = "";
    let prof_classes = [];
    let type = "";
    let motif = "";
    let somme = "";
    let reste = "";

    function toggle_classes(level) {
        if(prof_classes.includes(level)) {
            prof_classes = prof_classes.filter(item => item !== level);
        } else {
            prof_classes.push(level);
        }
    }

    $: userProfile.subscribe(value => user = value);

    async function fetchSubject() {
        const endpoint = `http://127.0.0.1:8000/school/classMatiere/${user.school_name}/`;
        const response = await fetch(endpoint);
        const data = await response.json();
        matiere.set(data);
    }

    onMount(() => {
        async () => {
            const endpoint = `http://127.0.0.1:8000/school/schoolClasse/${user.school_name}`;
            const response = await fetch(endpoint);
            const data = await response.json();
            classes.set(data);
        }
        fetchSubject();
    })

    async function handleSubmit(){
        const response = await fetch('http://127.0.0.1:8000/school/createRegistrationData/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                school: user.school_name,
                type: type,
                student: student,
                classe: selected_classes,
                prof: prof,
                prof_de: subject,
                classes: prof_classes,
                motif: motif,
                somme: somme,
                reste: reste,
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

</script>

<div class="content">
    <NavData />
    <div class="content-body">
        <div class="">
            <h1>Ajouter une nouvelle donnée</h1>
            <h5>Date : Mardi 25 Juin 2024</h5>
            
            <select name="" id="" bind:value={type}>
                <option value="" disabled>Selectionnez le type de donnée</option>
                <option value="Ecolage">Ecolage</option>
                <option value="Salaire">Paiement salaire</option>
            </select>

            <hr>
            
            <form action="">
                <label for="">Nom, prénom {#if type == "Ecolage"}
                    et classe
                {/if} :</label>
                <div class="input">
                    <input type="text" name="" id="" placeholder="Nom">
                    <input type="text" name="" id="" placeholder="Prénom" bind:value={student}>
                    {#if type == "Ecolage"}
                    <select name="" id="" bind:value={selected_classes}>
                        <option disabled value="">Selectionnez la classe</option>
                        {#each $classes as classe}
                            {#each classe.school_classes as cl} 
                                <option value="{cl}">{cl}</option>
                            {/each} 
                        {/each}
                    </select>
                    {/if}
                </div>

                {#if type == "Salaire"}
                    <label for="">Profésseur de :</label>{subject}
                    <div class="input-checkbox">
                        {#each $matiere as mat}
                            <label for="">{mat.subject}</label>
                            <input type="checkbox" name="" id="" bind:value={subject}><br>
                        {/each}
                    </div>

                    <label for="">Classe :</label>
                    <div class="input-checkbox">
                        {#each $classes as classe}
                            <!-- {#each classe.school_classes as cl} -->
                                <label for="">{classe.school_classes}</label>
                                <input type="checkbox" name="" id="" on:change={() => toggle_classes(classe.school_classes)}><br>
                            <!-- {/each} -->
                        {/each}
                    </div>
                        
                        
                {/if}

                <div class="input-one">
                    <textarea name="" rows="2" id="" placeholder="Motif..." bind:value={motif}></textarea>
                </div>

                <label for="">Somme et reste à payer :</label>
                <div class="input">
                    <input type="number" name="" id="" placeholder="Somme" bind:value={somme}> <span>Ar</span>
                    <input type="number" name="" id="" placeholder="Reste à payer" bind:value={reste}> <span>Ar</span>
                </div>
                
                <p>Nb : Tous les champs sont obligatoire</p>
    
                <button on:click={handleSubmit}>Enregistrer</button>
                <a href="/school/registration_data"><button id="cancel">Annuler</button></a>
            </form>
        </div>
    </div>
</div>

<style>
    .content{
        padding: 1%;
        color: white;
        padding-top: 60px;
        font-size: 20px;
    }
    h1{
        font-size: 30px;
        text-align: center;
    }
    h5{
        text-align: center;
        font-family: 'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif;
        font-size: 12px;
    }
    .content-body{
        margin-left: 15%;
        margin-right: 15%;
        background: #005358;
        padding: 10px;
        border-radius: 5px;
        border: none;
    }
    .input, .input-one{
        padding: 5px;
        display: flex;
        margin-bottom: 20px;
    }
    .input{
        border-radius: 5px;
        border: 1px solid rgba(255, 255, 255, 0.389);
    }
    .input input, select, 
    .input-one input, select, textarea{
        width: 100%;
        color: white;
        margin: 5px;
        padding: 10px;
        border-radius: 5px;
        border: none;
        background: #004041;
    }
    .input-checkbox{
        border-radius: 5px;
        border: 1px solid rgba(255, 255, 255, 0.389);
        padding: 20px;
        margin-bottom: 10px;
    }
    option{
        color: #002729;
        background: white;
    }
    label{
        font-size: 15px;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    button{
        margin-top: 10px;
        padding: 10px;
        border-radius: 5px;
        border: none;
        font-family: 'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana, sans-serif;
        background: #002729;
        color: white;
        width: 100%;
    }
    #cancel{
        background: none;
        border: 2px solid #002729;
    }
    p{
        font-size: 13px;
        text-align: center;
    }
    button:hover{
        cursor: pointer;
        background: #003b3f;
    }
    #cancel:hover{
        background: #003b3f;
    }
    hr{
        width: 50%;
        margin-bottom: 50px;
    }
</style>