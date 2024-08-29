<script>
    import { onMount } from "svelte";
    import NavMess from "../../../../lib/nav/navMess.svelte";
    import Loading from "../../../../lib/loading.svelte";
    import { userProfile, students, studentSearched } from "../../../../stores/auth";

    let name = '';
    let selected = false;
    let user;

    $: userProfile.subscribe(value => user = value);

    let menu = false

    async function fetchStudents(schoolName, schoolClass) {
        const response = await fetch(`http://localhost:8000/school/schoolStudents/${schoolName}/${schoolClass}`);
        const data = await response.json();
        students.set(data);
    }

    function handleClass(schoolName, schoolClass) {
        selected = true;
        fetchStudents(schoolName, schoolClass);
    }

    async function searchStudents(){
        if(name.length === 0 && name.trim() === '') {
            studentSearched.set('');
            return;
        }
        const endpoint = `http://localhost:8000/school/search_students/${user.school_name}/${name}/`;
        const response = await fetch(endpoint);
        const data = await response.json();
        studentSearched.set(data);
    }


    /*let isLoading = true;
    let selected = false;
    const loading = setTimeout(() => {
        isLoading = false;
    }, 5000);

    async function fetchClass(){
        const endpoint = 'http://127.0.0.1:8000/list/class/';
        const response = await fetch(endpoint);
        const data = await response.json();
        ClassesStore.set(data);
    }

    async function fetchStudents(classId) {
        const response = await fetch(`http://127.0.0.1:8000/list/class/${classId}`);
        const data = await response.json();
        StudentsStore.set(data);
    }

    onMount(() => {
        loading;
        fetchClass();
    })*/

    const handleclick = () => {
        if(menu == false){
            menu = true
        }else{
            menu = false
        }
    }

    /*function handleClickClass(classId) {
        selected = true;
        fetchStudents(classId);
    }*/

</script>

<div class="content">
    <NavMess />
    <div class="content-body">
        <input class="input" type="search" placeholder="Entrer le nom de l'étudiant ou l'enseignant ou le parent" bind:value={name}>
        <hr>
        <!-- {#if isLoading}
            <div class="loading">
                <Loading />
            </div>
        
        {:else}

        <div class="body">
            {#each $ClassesStore as classe}
                <ul>
                    <li on:click={() => { handleClickClass(classe.id) }}>{ classe.class_degree }</li>
                </ul>
            {/each}

            {#if selected}
                {#each $StudentsStore as student}
                    <a href="">
                        <div class="profile">
                            <img src="/icons/profile.png" alt="">
                            <div class="info">
                                <span><b>{ student.name } { student.lastname }</b></span><br>
                                <span id="fonction">Fonction: Etudiant</span>
                            </div>
                            <span on:click={handleclick} id="menu">...</span>
    
                            {#if menu}
                                <div class="detail">
                                    <a href="a">Voir le profile</a><br>
                                    <a href="n">Vider la discussion</a><br>
                                </div>    
                            {/if}
                    
                        </div>
                    </a><hr>
                {/each}
            {/if}
        </div>
        
        {/if} -->

        <div class="body">
            <h3>Listes des classes</h3>
            <hr>

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
                            <a href="/school/message/students/{student.id}">
                                <div class="profile">
                                    <img src="{student.student_picture}" alt="">
                                    <div class="info">
                                        <span><b>{student.student_name} {student.student_lastname}</b></span><br>
                                        <span id="fonction">Classe: {student.student_class}</span>
                                    </div>
                                </div>
                            </a>
                        {/each}
                    {:else}
                            <p>Pas d'élève pour le moment</p>
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
        padding: 10px;
        border-radius: 5px;
        border: none;
    }
    .loading{
        display: flex;
        align-items: center;
        justify-content: center;
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
    .body p{
        padding: 15px;
        margin: 0;
        width: auto;
    }
    .body p:hover{
        background: rgba(255, 255, 255, 0.275);
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
    #menu{
        margin-left: auto;
        padding: 1%;
    }
    li:hover{
        background: #003f42;
        cursor: pointer;
    }
    .detail{
        padding: 1%;
    }
    .detail a:hover{
        background: #005358;
        border: 1px solid white;
    }
    @media screen and (max-width: 800px) {
        .content-body {
            margin: 0;
        }
        .wrap-input-18{
            height: auto;
        }
        .profile img{
            height: 30px;
        }
        .info b{
            font-size: 12px;
        }
        #fonction{
            font-size: 11px;
        }
    }

</style>