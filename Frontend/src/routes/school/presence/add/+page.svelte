<script>
    import NavPresence from "../../../../lib/nav/navPresence.svelte";
    import { userProfile, matiere, teacher, students } from "../../../../stores/auth";
    import { onMount } from "svelte";

    let user

    $: userProfile.subscribe(value => user = value);

    let date = new Date();
    let classe_degree = '';
    let subject = '';
    let prof = '';
    let seanceTrue = "oui";
    let seanceFalse = "non";
    let seance = seanceFalse;
    let course_start = '00:00';
    let course_end = '00:00';
    let activities = '';
    let students_missing = [];
    let remarks = '';

    let SuccessMessage = false;
    let ErrorMessage = false;

    function toggle_student(level) {
        if(students_missing.includes(level)) {
            students_missing = students_missing.filter(item => item !== level);
        } else {
            students_missing.push(level);
        }
    }

    async function matiereList() {
        const response = await fetch(`http://localhost:8000/school/classMatiere/${user.school_name}/`);
        const data = await response.json();
        matiere.set(data);
    }

    async function studentList(studentClass) {
        const response = await fetch(`http://localhost:8000/school/schoolStudents/${user.school_name}/${studentClass}`);
        const data = await response.json();
        students.set(data);
    }

    onMount(async () => {
        const response = await fetch(`http://localhost:8000/school/listTeacher/${user.school_name}/`);
        const data = await response.json();
        teacher.set(data);
        matiereList();
    })

    async function handleSubmit() {

        const formData = {
            nameSchool: user.id,
            classe: classe_degree,
            matiere: subject,
            teacher: prof,
            course: seance,
            course_start: course_start,
            course_end: course_end,
            activities: activities,
            students_missing: students_missing,
            remarks: remarks,
        }

        try{
            const endpoint = 'http://localhost:8000/school/courseCreateAPI/';
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
                ErrorMessage = true;
            } else {
                console.log(data)
                SuccessMessage = true;
            }

        } catch( error ) {
            console.error('Error: ', error);
            ErrorMessage = true;
        }
    }

</script>

<div class="content">
    <NavPresence />
    <div class="content-body">
        <div class="">
            <h1>Enregistrer les informations d'aujourd'hui</h1>
            <h5>Date : {date.getDate()} / {date.getMonth()} / {date.getFullYear()}</h5>
            <hr>

            {#if SuccessMessage}
                <div class="success">
                    <p>Professeur ajouté(e) avec succès.</p>
                </div>
            {:else if ErrorMessage}
                <div class="error">
                    <p>Erreur lors de l'ajout de l'information.</p>
                </div>
            {/if}

            <form on:submit|preventDefault={handleSubmit}>
                <label for="">Classe , Nom du professeur et la matière</label>
                    <div class="input">
                        <select name="" id="" bind:value={classe_degree} on:click={() => studentList(classe_degree)}>
                            <option value="" disabled>Selectionnez la classe</option>
                            {#each user.school_classes as classe}
                                <option value={classe}>{classe}</option>
                            {/each}
                        </select>
                        <select name="" id="" bind:value={prof}>
                            <option value="" disabled>Selectionnez le nom du professeur</option>
                            {#each $teacher as teach}
                                <option value="{teach.teacher_name} {teach.teacher_lastname}">{teach.teacher_name} {teach.teacher_lastname}</option>
                            {/each}
                        </select>
                        <select name="" id="" bind:value={subject}>
                            <option value="" disabled>Selectionnez la matière</option>
                            {#each $matiere as mat}
                                <option value={mat.subject}>{mat.subject}</option>
                            {/each}
                        </select>
                    </div>
                <label for="">Cours : </label>
                <div class="input-one">
                    <select name="" id="" bind:value={seance}>
                        <option value="" disabled>Selectionnez l'etat du cours</option>
                        <option value="oui">Oui</option>
                        <option value="non">Non</option>
                    </select>
                </div>
                {#if seance === seanceTrue}
                    <label for="">Heure de début et de fin du cours : </label>
                    <div class="input">
                        <input type="time" name="" id="" bind:value={course_start}>
                        <input type="time" name="" id="" bind:value={course_end}>
                    </div>
                    <label for="">Les activités faites :</label>
                    <div class="input-one">
                        <textarea name="" id="" rows="10" placeholder="Entrer ici les listes des activités fait" bind:value={activities}></textarea>
                    </div>
                    <label for="">Cochez les listes des élèves absents : </label>
                    <div class="checkbox">
                        {#if $students.length > 0}
                            {#each $students as stud}
                                <div class="checkboxInput">
                                    <input type="checkbox" name="" id="" on:change={() => toggle_student((stud.student_name) (stud.student_lastname))}><span>N°{stud.id} : {stud.student_name} {stud.student_lastname}</span>
                                </div>    
                            {/each}    
                        {:else}
                            <p>Rien à afficher</p>
                        {/if}
                        
                        
                        <!-- <input type="checkbox" name="" id="">N°2 Rakoto
                        <input type="checkbox" name="" id="">N°3 Marc
                        <input type="checkbox" name="" id="">N°4 Jean
                        <input type="checkbox" name="" id="">N°1 Luc
                        <input type="checkbox" name="" id="">N°2 Rakoto
                        <input type="checkbox" name="" id="">N°3 Marc
                        <input type="checkbox" name="" id="">N°4 Jean -->
                    </div>
                    <label for="">Remarques : </label>
                    <div class="input-one">
                        <textarea name="" id="" rows="10" placeholder="Entrer ici les remarques ..." bind:value={remarks}></textarea>
                    </div>
                {/if}
                <p>Nb : Tous les champs sont obligatoire</p>
    
                <button type="submit">Enregistrer</button>
                <a href="/school/presence/"><button id="cancel">Annuler</button></a>
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
    p{
        font-size: 13px;
        text-align: center;
    }
    button:hover{
        cursor: pointer;
        background: #003b3f;
    }
    hr{
        width: 50%;
        margin-bottom: 50px;
    }
    .checkbox{
        display: block;
        padding: 10px;
        margin-bottom: 20px;
        border-radius: 5px;
        border: 1px solid rgba(255, 255, 255, 0.389);
    }
    .checkboxInput{
        display: flex;
        width: auto;
        align-items: center;
        justify-content: center;
        margin-left: 10px;
    }
    input[type="checkbox"]{
        height: 30px;
    }
    input[type="checkbox"]:hover{
        cursor: pointer;
    }
    span{
        font-size: 18px;
        margin-left: 10px;
    }
    #cancel{
        background: none;
        border: 2px solid #002729;
    }
    #cancel:hover{
        background: #003b3f;
    }
    .success{
        background: green;
        border-radius: 10px;
        padding: 5px;
    }
    .success p{
        color: white;
        font-weight: bold;
        font-family: 'Courier New', Courier, monospace;
    }
    .error{
        background: rgba(255, 31, 31, 0.826);
        border-radius: 10px;
        padding: 5px;
    }
    .error p{
        color: white;
        font-weight: bold;
        font-family: 'Courier New', Courier, monospace;
    }
</style>