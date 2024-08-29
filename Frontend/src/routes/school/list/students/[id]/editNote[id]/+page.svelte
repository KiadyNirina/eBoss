<script>
    import NaList from '../../../../../../lib/nav/naList.svelte';
    import { students, studentSearched, infoFamiliale } from '../../../../../../stores/auth';
    import { onMount } from 'svelte';
    import html2pdf from 'html2pdf.js';

    let content;

    function generatePDF() {
        const options = {
        margin:       1,
        filename:     'page.pdf',
        image:        { type: 'jpeg', quality: 0.98 },
        html2canvas:  { scale: 2 },
        jsPDF:        { unit: 'in', format: 'letter', orientation: 'portrait' }
        };
        
        html2pdf().from(content).set(options).save();
    }
    
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

    onMount( async () => {
        if(data){
            student = $students.find(student => student.id == data.id)
            if(student){
                isEditMode = true;
                const endpoint = `http://127.0.0.1:8000/school/student/${id}/`;
                const response = await fetch(endpoint);
                const data = await response.json();
                    students.set(data);
            }
        }
    });

    /*async function handleSubmit(){
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
    }*/
    
</script>

<div class="content">
    <NaList />
    <div class="content-body">
            
        <h1>Année scolaire: 2023 - 2024</h1>
        
        <hr>

        <button on:click={generatePDF}>Expotez en PDF</button>

        {#if student}
            
        <div class="body" bind:this={content}>
            <div class="infoDetail">
                <ul>
                    <li><b>Nom de l'établissement : </b><i>{student.school_name}</i></li>
                    <li><b>Nom de l'élève : </b><i>{student.student_name} {student.student_lastname}</i></li>
                    <li><b>Classe : </b><i>{student.student_class}</i></li>
                </ul>
            </div>
            <div class="infoDetail">
                <h3>Note</h3>
                <form>
                    
                    <table>
                        <thead>
                            <th>Matière</th>
                            <th>Note</th>
                            <th>Coef</th>
                        </thead>
                        <tbody>
                            <th>MATHS</th>
                            <th>18</th>
                            <th>1</th>
                        </tbody>
                        <tbody>
                            <th>MLG</th>
                            <th>13</th>
                            <th>1</th>
                        </tbody>
                    </table>

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
    th{
        border: none;
        background: #003f41;
        width: 100%;
        padding: 10px;
        border-radius: 5px;
    }
    .infoFam{
        border: 1.5px solid white;
        border-radius: 5px;
        padding: 30px;
    }

</style>