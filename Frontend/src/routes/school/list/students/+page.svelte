<script>
    import NaList from "../../../../lib/nav/naList.svelte";
    import { onMount } from "svelte";
    import { classes, students, userProfile, studentSearched, studentsCount, studentCount, userRole } from "../../../../stores/auth";
    import { draw } from "svelte/transition";

    let selected = false;
    let name = '';
    let user

    $: userProfile.subscribe(value => user = value);

    const BASE_URL = "http://127.0.0.1:8000"; 

    async function fetchStudents(schoolName, schoolClass) {
        const response = await fetch(`${BASE_URL}/school/schoolStudents/${schoolName}/${schoolClass}`);
        const data = await response.json();
        students.set(data);
    }

    const countStudents = async () => {
        const response = await fetch(`${BASE_URL}/school/countStudents/${user.school_name}/`);
        const data = await response.json();
        studentsCount.set(data.count);
    }

    function handleClass(schoolName, schoolClass) {
        selected = true;
        fetchStudents(schoolName, schoolClass);
    }

    onMount(() => {
        countStudents();
    })

    async function searchStudents(){
        if(name.length === 0 && name.trim() === '') {
            studentSearched.set('');
            return;
        }
        const endpoint = `${BASE_URL}/school/search_students/${user.school_name}/${name}/`;
        const response = await fetch(endpoint);
        const data = await response.json();
        studentSearched.set(data);
    }

</script>

<div class="content">
    <NaList />
    <div class="content-body">
        <h1>Année scolaire : 2023 - 2024</h1>
        <div class="add">
            <button>
                <a href="/school/list/students/add">
                    <img src="/icons/ajouter.png" alt="">
                    <span>Ajouter un(e) élève</span>
                </a>
            </button>
        </div>

        <input class="input" type="search" bind:value={name} on:input={searchStudents} placeholder="Entrer le nom de l'étudiant">
        <!-- <input class="input" type="search" placeholder="Entrer le nom de l'étudiant"> -->

        <div class="body">
            <span><u>Nombres total des élèves</u> : {$studentsCount}</span>
            <h3>Listes des classes</h3>
            <hr>

            {#if $studentSearched.length > 0}

                {#each $studentSearched as searched}
                    <a href="/school/list/students/{searched.id}">
                        <div class="profile">
                            <img src="/img/picture.png" alt="">
                            <div class="info">
                                <span><b>{searched.student_name} {searched.student_lastname}</b></span><br>
                                <span id="fonction">Classe: {searched.student_class}</span>
                            </div>

                            <div class="detail">
                                <a href="a"><img src="/icons/modifier.png" alt=""></a><br>
                                <a href="n"><img src="/icons/supprimer.png" alt=""></a><br>
                            </div>    
                
                        </div>
                    </a><hr>   
                {/each}

            {:else}

            
                {#each user.school_classes as classe}
                        <ul>
                            <li on:click={() => handleClass(user.school_name, classe)}>
                                <div class="classe">{ classe }</div>
                            </li>
                        </ul>
                {/each}
                
                <h3>Listes des élèves</h3>
                <hr>

                {#if selected}
                    {#if $students.length > 0}
                        {#each $students as student}
                            <a href="/school/list/students/{student.id}">
                                <div class="profile">
                                    {#if student.student_picture}
                                        <img src="{student.student_picture}" alt={student.student_name} />
                                    {/if}
                                    <div class="info">
                                        <span><b>{student.student_name} {student.student_lastname}</b></span><br>
                                        <span id="fonction">Classe: {student.student_class}</span>
                                    </div>

                                    <div class="detail">
                                        <a href="a"><img src="/icons/modifier.png" alt=""></a><br>
                                        <a href="n"><img src="/icons/supprimer.png" alt=""></a><br>
                                    </div>    
                        
                                </div>
                            </a><hr>   
                        {/each}
                    {:else}
                            <p>Pas d'élève pour le moment</p>
                    {/if}
                {/if}

            {/if}
            

        </div>
    </div>
</div>

<style>
    a{
        text-decoration: none;
        color: white;
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
    .input{
        width: 100%;
        padding: 10px;
        border-radius: 5px;
        border: none;
        background: rgba(255, 255, 255, 0.559);
    }
    hr{
        border: 1px solid rgba(255, 255, 255, 0.229);
    }
    .body{
        padding: 1%;
    }
    .profile{
        padding: 1%;
        display: flex;
        align-items: center;
    }
    .profile img{
        border: 1px solid white;
        height: 50px;
    }
    .profile:hover{
        background: #003f42;
    }
    .info{
        margin-left: 10px;
    }
    .info b{
        font-size: 14px;
    }
    #fonction{
        font-size: 15px;
    }
    .detail{
        display: flex;
        margin-left: auto;
    }
    .detail img{
        padding: 10px;
        height: 30px;
        border: none;
    }
    .detail img:hover{
        background: rgba(128, 128, 128, 0.226);
        border-radius: 5px;
    }

    .classe{
        padding: 10px;
    }
    .classe:hover{
        cursor: pointer;
        background: #00393c;
    }
    h1{
        font-size: 20px;
        text-align: center;
        padding: 5px;
        border: 1px solid rgba(255, 255, 255, 0.282);
    }
    @media screen and (max-width: 800px) {
        .content-body{
            margin-left: auto;
            margin-right: auto;
            padding: 10px;
        }
    }

</style>