<script>
    import NaList from '../../../../../../../lib/nav/naList.svelte';
    import { students, studentSearched, infoFamiliale } from '../../../../../../../stores/auth';
    import { onMount } from 'svelte';

    let student = null;
    
    let mother_name = $infoFamiliale.mother_name;
    let mother_lastname = $infoFamiliale.mother_lastname;
    let mother_profession = $infoFamiliale.mother_profession;
    let mother_number = $infoFamiliale.mother_number;
    let father_name = $infoFamiliale.father_name;
    let father_lastname = $infoFamiliale.father_lastname;
    let father_profession = $infoFamiliale.father_profession;
    let father_number = $infoFamiliale.father_number;

    let isEditMode = false;
    export let data;

    student = $students.find(student => student.id == data.id)
    
    async function fetchInfoFamiliale(student_id) {
        const response = await fetch(`http://127.0.0.1:8000/school/infoFamiliale/${student_id}/`);
        const data = await response.json();
        infoFamiliale.set(data);
    }

    onMount( async () => {
        if(student){
            isEditMode = true;
            const endpoint = `http://127.0.0.1:8000/school/student/${id}/`;
            const response = await fetch(endpoint);
            const data = await response.json();
            students.set(data);
            fetchInfoFamiliale(student.id);
        }
    });

    async function handleSubmit(){
        if(student){
            const method = isEditMode ? 'PUT' : 'POST';
            const url = isEditMode ? `http://127.0.0.1:8000/school/updateInfoFamiliale/${student.id}/` : 'http://localhost:8000/school/createInfoFamiliale/';
            const response = await fetch(url, {
                method: method,
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    student: student.id,
                    mother_name: mother_name,
                    mother_lastname: mother_lastname,
                    mother_profession: mother_profession,
                    mother_number: mother_number,
                    father_name: father_name,
                    father_lastname: father_lastname,
                    father_profession: father_profession,
                    father_number: father_number,
                }),
            });
            const data = await response.json();
            if(response.ok) {
                alert(`${isEditMode ? 'Modification' : 'Ajout'} avec succes`);
                console.log(data)
            } else {
                alert(`${isEditMode ? 'Modification' : 'Ajout'} avec erreur`);
                console.error(data)
            }
        }
    }
    
</script>

<div class="content">
    <NaList />
    <div class="content-body">
            
        <h1>Année scolaire: 2023 - 2024</h1>
        
        <hr>

        {#if student}
            
        <div class="body">
            <div class="infoDetail">
                <ul>
                    <li><b>Nom de l'établissement : </b><i>{student.school_name}</i></li>
                    <li><b>Nom de l'élève : </b><i>{student.student_name} {student.student_lastname}</i></li>
                    <li><b>Classe : </b><i>{student.student_class}</i></li>
                </ul>
            </div>
            <div class="infoDetail">
                <h3>Info familiale</h3>
                <form on:submit|preventDefault={handleSubmit}>
                    <ul class="infoFam">
                        <div class="">
                            <li><b>Nom du mère : </b></li><input type="text" placeholder="Entrer le nom du mère" bind:value={mother_name}>
                            <li><b>Prénom du mère : </b></li><input type="text" placeholder="Entrer le prénom du mère" bind:value={mother_lastname}>
                            <li><b>Mobile : </b></li><input type="text" placeholder="Entrer le numéro de mobile du mère" bind:value={mother_number}>
                            <li><b>Profession : </b></li><input type="text" placeholder="Entrer le profession du mère" bind:value={mother_profession}>
                            <li><b>Nom du père : </b></li><input type="text" placeholder="Entrer le nom de père" bind:value={father_name}>
                            <li><b>Prénom du père : </b></li><input type="text" placeholder="Entrer le prénom de père" bind:value={father_lastname}>
                            <li><b>Mobile : </b></li><input type="text" placeholder="Entrer le numéro de mobile de père" bind:value={father_number}>
                            <li><b>Profession : </b></li><input type="text" placeholder="Entrer le profession de père" bind:value={father_profession}>
                        </div>
                    </ul>
                    
                    <div class="add">
                        <a href="/school/list/students/{student.id}/">Annuler</a>
                        <button type="submit">{isEditMode ? "Modifier" : "Ajouter"}</button>
                    </div>
                </form>
            </div>
            
        </div>
        {/if}
    </div>
</div>

<style>
    .infoDetail{
        margin-left: auto;
        margin-right: auto;
    }
    .infoDetail h3{
        font-family: Verdana, Geneva, Tahoma, sans-serif;
    }
    .infoDetail b{
        font-size: 15px;
        font-family: 'Franklin Gothic Medium', 'Arial Narrow', Arial, sans-serif;
    }
    .infoDetail i{
        font-family: Verdana, Geneva, Tahoma, sans-serif;
        font-size: 15px;
    }
    .add{
        display: flex;
        align-items: center;
    }
    .add a{
        text-decoration: none;
        color: white;
        text-align: center;
    }
    .add button, .add a{
        background: transparent;
        border: transparent;
        transition: 0.5s;
        padding: 10px;
        margin-bottom: 5px;
        color: white;
        font-size: 15px;
        width: 100%;
    }
    .add button:hover, .add a:hover{
        border: 1.5px solid white;
        border-radius: 5px;
        cursor: pointer;
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
    hr{
        border: 1px solid rgba(255, 255, 255, 0.229);
    }
    .body{
        padding: 1%;
    }

    h1{
        font-size: 20px;
        font-family: 'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif;
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.282);
        padding: 5px;
    }
    input{
        border: none;
        background: #003f41;
        height: 35px;
        width: 100%;
        padding-left: 10px;
        border-radius: 5px;
    }
    .infoFam{
        border: 1.5px solid white;
        border-radius: 5px;
        padding: 30px;
    }

</style>