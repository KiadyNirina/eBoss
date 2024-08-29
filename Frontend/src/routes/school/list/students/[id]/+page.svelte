<script>
    import NaList from '../../../../../lib/nav/naList.svelte';
    import { userProfile, students, studentSearched, infoFamiliale, matiere, notes } from '../../../../../stores/auth';
    import { onMount } from 'svelte';

    export let data;
    /*let user;

    userProfile.subscribe(value => user = value);

    let maths = 12;
    let pc = 15;
    let mlg = 22;
    let svt = 11;
    let hg = 23;
    let frs = 9;
    let totalNote = maths + pc + mlg + svt + hg + frs;

    let coefMaths = 1;
    let coefPc = 1;
    let coefMlg = 2;
    let coefSvt = 1;
    let coefHg = 2;
    let coefFrs = 1;
    let totalCoef = coefMaths + coefPc + coefMlg + coefSvt + coefHg + coefFrs;

    let moyen = totalNote / totalCoef*/
    // let familialeData = [];
    let student = null;
    let notesGroupedByYearAndSemester = {};

    async function fetchInfoFamiliale(student_id) {
        const response = await fetch(`http://127.0.0.1:8000/school/infoFamiliale/${student_id}/`);
        const data = await response.json();
        infoFamiliale.set(data);
    }

    async function fetchNote(){
        const response = await fetch(`http://localhost:8000/school/noteListAPIView/?school=${student.school_name}&student=${student.student_lastname}`);
        notesGroupedByYearAndSemester = await response.json();
        //notes.set(data);
    }

    onMount(async () => {
        student = $students.find(student => student.id == data.id) || $studentSearched.find(student => student.id == data.id);
        if (student) {
            const endpoint = `http://127.0.0.1:8000/school/student/${student.id}/`;
            const response = await fetch(endpoint);
            const data = await response.json();
            students.set(data);
            fetchInfoFamiliale(student.id);
            fetchNote();
        }
    });
    
</script>

<div class="content">
    <NaList />
    <div class="content-body">
        {#if student}
            
        <h1>Année scolaire: 2023 - 2024</h1>
        <div class="info">
            <div class="profile">
                <img src="{student.student_picture}" alt="">
            </div>
            <div class="infoDetail">
                <ul>
                        <li><b>Nom</b> : <i>{student.student_name}</i></li>
                        <li><b>Prénom</b> : <i>{student.student_lastname}</i></li>
                        <li><b>Sexe</b> : <i>{student.student_sexe}</i></li>
                        <li><b>Classe</b> : <i>{student.student_class}</i></li>
                        <li><b>Date de naissance</b> : <i>{student.student_birthday_date}</i></li>
                        <li><b>Adresse</b> : <i>{student.student_address}</i></li>
                        <li><b>Numéro mobile</b> : <i>0{student.student_number}</i></li>
                </ul>
            </div>
            <div class="add">
                <button>
                    <a href="/school/home">
                        <img src="/icons/modifier.png" alt="">
                    </a>
                </button>
            </div>
        </div>
        
        <hr>
        <div class="body">
            <div class="infoDetail">
                <ul>
                    <!-- <li><b>Date d'inscription : </b>{student ? student.register_date : 'tsisy lty a'}</li> -->
                    <li><b>Numéro d'inscription : </b><i>2</i></li>
                    <li><b>Numéro de matricule : </b><i>0315</i></li>
                    <li><b>Date d'inscription : </b><i>{student.register_date}</i></li>
                </ul>
            </div>
            <div class="infoDetail">
                <div class="title">
                    <h3>Info familiale</h3>
                    <div class="add">
                        <button>
                            <a href="/school/list/students/{student.id}/editInfoFam{student.id}/{student.id}/">
                                <img src="/icons/modifier.png" alt="">
                            </a>
                        </button>
                    </div>
                </div>
                <ul class="infoFam">
                    <!-- {#each familialeData as familiale}
                    <li><b>Nom et prénom du mère : </b>{familiale.mother_name} {familiale.mother_lastname}</li>
                    <li><b>Mobile : </b>{familiale.mother_number}</li>
                    <li><b>Nom et prénom du père : </b>{familiale.father_name} {familiale.father_lastname}</li>
                    <li><b>Mobile : </b>{familiale.father_number}</li>
                    {/each} -->
                    <div class="">
                        {#each $infoFamiliale as info}
                            <li><b>Nom et prénom du mère : </b><i>{info.mother_name} {info.mother_lastname}</i></li>
                            <li><b>Numéro mobile du mère : </b><i>0{info.mother_number}</i></li>
                            <li><b>Proféssion du mère : </b><i>{info.mother_profession}</i></li>
                            <li><b>Nom et prénom de père : </b><i>{info.father_name} {info.father_lastname}</i></li>
                            <li><b>Numéro mobile de père : </b><i>0{info.father_number}</i></li>
                            <li><b>Proféssion de père : </b><i>{info.father_profession}</i></li>
                        {/each}
                    </div>
                </ul>
            </div>
            <div class="infoDetail">
                <div class="title">
                    <h3>Frais de scolarité</h3>
                    <div class="add">
                        <button>
                            <a href="/school/list/students/{student.id}/editInfoFam{student.id}/{student.id}/">
                                <img src="/icons/modifier.png" alt="">
                            </a>
                        </button>
                    </div>
                </div>
                <table>
                    <thead>
                        <th scope="col"></th>
                        <th scope="col">Date</th>
                        <th scope="col">Somme</th>
                        <th scope="col">N° du reçu</th>
                    </thead>
                    <tbody>
                        <th scope="row">inscription + Frais généraux</th>
                        <th>30 - 07 - 2024</th>
                        <th>30 000 ar</th>
                        <th>321</th>
                    </tbody>
                    <tbody>
                        <th scope="row">Divers</th>
                        <th></th>
                        <th></th>
                        <th></th>
                    </tbody>
                    <tbody>
                        <th scope="row">Sept</th>
                        <th></th>
                        <th></th>
                        <th></th>
                    </tbody>
                    <tbody>
                        <th scope="row">Oct</th>
                        <th></th>
                        <th></th>
                        <th></th>
                    </tbody>
                    <tbody>
                        <th scope="row">Nov</th>
                        <th></th>
                        <th></th>
                        <th></th>
                    </tbody>
                    <tbody>
                        <th scope="row">Dec</th>
                        <th></th>
                        <th></th>
                        <th></th>
                    </tbody>
                    <tbody>
                        <th scope="row">Jan</th>
                        <th></th>
                        <th></th>
                        <th></th>
                    </tbody>
                </table>
            </div>

            <div class="infoDetail">
                <div class="title">
                    <h3>Abscences</h3>
                    <div class="add">
                        <button>
                            <a href="/school/list/students/{student.id}/editInfoFam{student.id}/{student.id}/">
                                <img src="/icons/modifier.png" alt="">
                            </a>
                        </button>
                    </div>
                </div>
                <ul>
                    <li>Année scolaire: 2023 - 2024</li>
                    <li>Semestre: 1</li>
                    <table>
                        <thead>
                            <th scope="col">Date d'absence</th>
                            <th scope="col">Motif</th>
                            <th scope="col">Heure</th>
                        </thead>
                        <tbody>
                            <th>22 - 05 - 2024</th>
                            <th></th>
                            <th>04</th>
                        </tbody>
                        <tbody>
                            <th>Total d'heures</th>
                            <th></th>
                            <th>04</th>
                        </tbody>
                    </table>
                </ul>
            </div>

            <div class="infoDetail">
                <div class="title">
                    <h3>Notes</h3>
                    <div class="add">
                        <button>
                            <a href="/school/list/students/{student.id}/editNote{student.id}/">
                                <img src="/icons/modifier.png" alt="">
                            </a>
                        </button>
                    </div>
                </div>
                
                {#each Object.entries(notesGroupedByYearAndSemester) as [key, notes]}

                <table>
                    <thead>
                        <th scope="col"></th>
                        <th scope="col">Année scolaire</th>
                        <th scope="col">Semestre</th>
                        <th scope="col">Session du</th>
                        <th scope="col">Note</th>
                        <th scope="col">Coef</th>
                    </thead>
                    {#each notes as not}
                        <tbody>
                            <th scope="row">{not.matiere}</th>
                            <th>{not.school_year}</th>
                            <th>{not.semester}</th>
                            <th>{not.session_start}</th>
                            <th>{not.note}</th>
                            <th>{not.coef}</th>
                        </tbody>
                    {/each}
                    <tbody>
                        <th scope="row">Total</th>
                        <th></th>
                        <th></th>
                        <th></th>
                        <th></th>
                        <th></th>
                    </tbody>
                </table>
                <ul>
                    <li>Nombres d'élèves: 25</li>
                    <li>Rang: <b>4eme</b> / 25</li>
                    <li>Moyenne:</li>
                </ul><br>

                <a class="pdf" href="/school/list/students/{student.id}/exportPDF{student.id}">Expotez PDF</a>
                <br><br>
                <hr>
                <br>

                {/each}
            </div>
        </div>

        {/if}
    </div>
</div>

<style>
    .info{
        display: flex;
        align-items: center;
    }
    .info img{
        height: 200px;
    }
    .profile{
        margin-left: auto;
        margin-right: auto;
    }
    .infoDetail{
        margin-left: auto;
        margin-right: auto;
    }
    .infoDetail h3{
        font-family: Verdana, Geneva, Tahoma, sans-serif;
    }
    .infoDetail ul{
        line-height: 30px;
    }
    .infoDetail b{
        font-size: 20px;
        font-family: 'Franklin Gothic Medium', 'Arial Narrow', Arial, sans-serif;
    }
    .infoDetail i{
        font-family: Verdana, Geneva, Tahoma, sans-serif;
        font-size: 15px;
    }
    .add{
        margin-left: auto;
    }
    a{
        text-decoration: none;
        color: white;
    }
    .infoFam{
        display: flex;
    }
    .add a{
        display: flex;
        align-items: center;
    }
    .add img{
        height: 30px;
    }
    .add button{
        background: transparent;
        border: transparent;
        transition: 0.5s;
        padding: 5px;
        margin-bottom: 5px;
    }
    .add button:hover{
        border: 1.5px solid white;
        border-radius: 5px;
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
    .profile img{
        border: 1px solid rgba(255, 255, 255, 0.475);
        border-radius: 5px;
    }
    .profile:hover{
        background: #003f42;
    }
    .info{
        margin-left: 10px;
    }

    h1{
        font-size: 20px;
        font-family: 'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif;
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.282);
        padding: 5px;
    }
    table{
        width: 100%;
    }
    th{
        border: 1px solid rgba(255, 255, 255, 0.433);
        padding: 5px;
    }
    .title{
        display: flex;
        align-items: center;
    }
    ul{
        margin: 0;
    }
    .pdf{
        padding: 10px;
        border: 1px solid white;
        border-radius: 5px;
    }

</style>