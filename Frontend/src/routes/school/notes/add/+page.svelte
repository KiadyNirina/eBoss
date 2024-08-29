<script>
    import { onMount } from "svelte";
    import NavNote from "../../../../lib/nav/navNote.svelte";
    import { userProfile, matiere } from "../../../../stores/auth";

    let user;
    let student_name = "";
    let student_lastname = "";
    let classe = "";
    let school_year = "";
    let semester = "";
    let session_start = "";
    let session_end = "";
    let subject = "";
    let note = "";
    let coef = "";

    $: userProfile.subscribe(value => user = value);

    async function fetchSubject() {
        const response = await fetch(`http://localhost:8000/school/classMatiere/${user.school_name}`);
        const data = await response.json()
        matiere.set(data)
    }

    onMount(() => {
        fetchSubject();
    });

    async function handleSubmit() {

        const formData = {
            school: user.school_name,
            student: student_lastname,
            classe: classe,
            school_year: school_year,
            semester: semester,
            session_start: session_start,
            session_end: session_end,
            matiere: subject,
            note: note,
            coef: coef,
        }

        try{
            const endpoint = 'http://localhost:8000/school/noteCreateView/';
            const response = await fetch(endpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData),
            });

            const data = await response.json();

            if(!response.ok) {
                console.error(data)
                alert('Ajout avec erreur')
            } else {
                console.log(data)
                alert('Ajout avec succès')
            }

        } catch( error ) {
            console.error('Error: ', error);
            alert('Erreur lors de l\'ajout');
        }
    }

</script>

<div class="content">
    <NavNote/>
    <div class="content-body">
        <form on:submit={handleSubmit} action="">
            <div class="body">
                <h3>Ajout d'une note</h3>
                <hr>
    
                <b>Informations de la période</b>
                <div class="student-info">
                        <div class="one">
                            <label for="">Année scolaire :</label>
                            <input type="text" name="" id="" bind:value={school_year} placeholder="Ex: 2023 - 2024"> 
                        </div>
                    <div class="one">
                        <label for="">Semestre / Trimestre :</label>
                        <input type="text" placeholder="Ex : Semestre 1 / Trimestre 1" bind:value={semester}>
                    </div>
                    <div class="two">
                        <div class="name">
                            <label for="">Date de début de l'examen :</label>
                            <input type="date" name="" id="" bind:value={session_start}>
                        </div>
                        <div class="name">
                            <label for="">Date de fin :</label>
                            <input type="date" name="" id="" bind:value={session_end}>
                        </div>
                    </div>
                </div>
    
                <b>Informations de l'élève</b>
                <div class="student-info">
                    <div class="one">
                        <label for="">Classe :</label>
                        <select name="" id="" bind:value={classe}>
                            {#each user.school_classes as classe}
                                <option value={classe}>{classe}</option>
                            {/each}
                        </select>
                    </div>
                    <div class="two">
                        <div class="name">
                            <label for="">Nom de l'élève :</label>
                            <input type="text" name="" id="" placeholder="Entrer le nom de l'élève" bind:value={student_name}>
                        </div>
                        <div class="name">
                            <label for="">Prénom :</label>
                            <input type="text" name="" id="" placeholder="Entrer le prénom de l'élève" bind:value={student_lastname}>
                        </div>
                    </div>
                </div>
    
                <b>Tableau des notes</b>
                <div class="student-info">
                    <table>
                        <thead>
                            <th scope="col">Matières</th>
                            <th scope="col">Coefficient</th>
                            <th scope="col">Notes</th>
                        </thead>
                        <tbody>
                            <th scope="row"><select name="" id="" bind:value={subject}>
                                <option value="" disabled>Selectionnez la matière</option>
                                {#each $matiere as mat}
                                    <option value={mat.subject}>{mat.subject}</option>
                                {/each}
                            </select></th>
                            <th><input type="number" name="" id="" placeholder="Entrer le coef" bind:value={coef}></th>
                            <th><input type="number" name="" id="" placeholder="Entrer la note" bind:value={note}></th>
                        </tbody>
                    </table>
                </div>
    
                <div class="add">
                    <button type="submit">Ajouter</button>
                </div>
            </div>
        </form>
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
        padding-top: 60px;
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
    .two{
        display: flex;
    }
    .two input, select{
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
    .name{
        width: 50%;
        padding: 10px;
    }
    .student-info{
        border: 1px solid rgba(255, 255, 255, 0.479);
        padding: 15px;
        border-radius: 5px;
        margin-top: 10px;
        margin-bottom: 20px;
    }
    .add button{
        background-color: white;
        border: 1px solid #00383b;
        border-radius: 5px;
        transition: 0.2s;
        padding: 10px;
        margin-bottom: 5px;
        width: 100%;
        color: #00383b;
        font-weight: bolder;
    }
    .add button:hover{
        background: rgb(193, 193, 193);
        cursor: pointer;
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
</style>