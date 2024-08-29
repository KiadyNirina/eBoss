<script>
    import NavHome from "../../../lib/navStudent/navHome.svelte";
    import Loading from "../../../lib/loading.svelte";
    import { onMount } from "svelte";
    import App from '../../app.svelte';
    import { getUserStudent, logout } from "../../../lib/auth";
    import { goto } from '$app/navigation';
    import { token, userProfile, matiere, getStoreValue, students } from "../../../stores/auth";

    let user;

    userProfile.subscribe(value => user = value);

    async function fetchStudents(){
        const response = await fetch(`http://localhost:8000/school/studentAddedRecently/${user.school_name}/`);
        const data = await response.json();
        students.set(data)
    }

    onMount(async () => {
        const $token = getStoreValue(token);
        if($token) {
            const profile = await getUserStudent();
            if(profile){
                userProfile.set(profile);
            } else {
                goto('/login');
            }
        };
        fetchStudents();
    });

    //let isLoading = true;
    //let posts = [];

    /*onMount(() => {
        setTimeout(() => {
            isLoading = false;
        }, 2000);
    },
    async function () {
        const endpoint = `http://127.0.0.1:8000/post/`;
        const response = await fetch(endpoint);
        posts = await response.json();
    });*/

    // onMount(async () => {
    //     const endpoint = `http://127.0.0.1:8000/post/`;
    //     const response = await fetch(endpoint);
    //     posts = await response.json();
    // });



</script>

<div class="content">
    <NavHome />
    <div class="navlat">
        {#if $userProfile === null}
        <div class="">
            <div class="profil">
                <img src="/icons/profile.png" alt="">
                <div class="name">
                    <span>Chargement...</span><br>
                    <span class="see">Voir votre profile</span>
                </div>
            </div>
        </div>
        {:else}
        <div class="">
            <a class="profil" href="/school/profile">
                    <img src="/icons/profile.png" alt="">
                    <div class="name">
                        <span>{user.username}</span><br>
                        <span class="see">Voir votre profile</span>
                    </div>
            </a>
        </div>
        {/if}
        <App />
    </div>

    <div class="navlat2">
        {#if $userProfile === null}
        <div class="">
            <div class="profil">
                <img src="/icons/profile.png" alt="">
                <div class="name">
                    <span>Chargement...</span><br>
                    <span class="see">Voir votre profile</span>
                </div>
            </div>
        </div>
        {:else}
        <div class="list">
            <p>Etudiants ajoutés récemment :</p>
            {#each $students as student}
            <a class="profil" href="">
                <img src="/icons/profile.png" alt="">
                <div class="name">
                    <span>{student.student_name} {student.student_lastname}</span><br>
                    <span class="see">classe: {student.student_class}</span>
                </div>
            </a>
            {/each}
            <a class="seeMore" href="/school/home/seeAllStudents"><p>Voir tout</p></a>
        </div>

        <div class="list">
            <p>Enseignants ajoutés récemment :</p>
            <a class="profil" href="">
                <img src="/icons/profile.png" alt="">
                <div class="name">
                    <span>{user.username}</span><br>
                    <span class="see">classe: 5eme</span>
                </div>
            </a>
            <a class="profil" href="">
                <img src="/icons/profile.png" alt="">
                <div class="name">
                    <span>{user.username}</span><br>
                    <span class="see">classe: 3eme</span>
                </div>
            </a>
        </div>

        <div class="list">
            <p>Parents ajoutés récemment :</p>
            <a class="profil" href="">
                <img src="/icons/profile.png" alt="">
                <div class="name">
                    <span>{user.username}</span><br>
                    <span class="see">classe: 5eme</span>
                </div>
            </a>
            <a class="profil" href="">
                <img src="/icons/profile.png" alt="">
                <div class="name">
                    <span>{user.username}</span><br>
                    <span class="see">classe: 3eme</span>
                </div>
            </a>
        </div>
        {/if}
    </div>
    
    <div class="content-body">
        {#if $userProfile === null}
            <div class="content-post">
                <div class="loading">
                    <Loading />
                </div>
            </div>
        {:else}

                <div class="content-post">
                    <div id="calendar">
                        <a href="/school/school calendar">Calendrier Scolaire &Gt;</a>
                    </div><br>

                    <div class="container">
                        <a href="/school/message" class="container1">
                                <div class="">
                                    <img src="/icons/message.png" alt="">
                                    <p>Messages</p>
                                </div>
                                <div class="number">
                                    <p>10</p>
                                </div>
                        </a>

                        <a href="/school/home/announcement/" class="container1">
                            <div class="">
                                <img src="/icons/annonce.png" alt="">
                                <p>Annonces</p>
                            </div>
                            <div class="number">
                                <p>2</p>
                            </div>
                        </a>

                        <a href="/school/list" class="container1">
                            <div class="">
                                <img src="/icons/liste.png" alt="">
                                <p>Listes des membres</p>
                            </div>
                            <div class="number1">
                                <p>+2</p>
                            </div>
                        </a>

                        <a href="/school/presence" class="container1">
                            <div class="">
                                <img src="/icons/classe.png" alt="">
                                <p>Gestion des cours</p>
                            </div>
                            <div class="number">
                                <p>5</p>
                            </div>
                        </a>
                    </div><br>

                    <div class="container">
                        <a href="/school/home/schedule" class="container1">
                            <div class="">
                                <img src="/icons/emploi du temps.png" alt="">
                                <p>Emploi du temps</p>
                            </div>
                            <div class="number">
                                <p>7</p>
                            </div>
                        </a>

                        <a href="/school/home/schedule" class="container1">
                            <div class="">
                                <img src="/icons/emploi du temps.png" alt="">
                                <p>Demande d'absence</p>
                            </div>
                            <div class="number">
                                <p>7</p>
                            </div>
                        </a>
                    </div>
                    
                </div>

            <!-- {#each posts as post}
                
                <div class="content-post">
                    <div class="profil">
                        <img src="/icons/profile.png" alt="">
                        <p><strong>Admin</strong></p>
                        <div class="action">
                            <a href=""><img src="/icons/modifier.png" alt=""></a>
                            <a href=""><img src="/icons/supprimer.png" alt=""></a>
                        </div>
                    </div>
                    <span>Date : { post.created_at }</span>
                    <hr>
                    <p>{ post.content }</p>
                    <img src="{post.picture}" alt="">
                </div>
            {/each} -->

        {/if}
    </div>
</div>

<style>
    .navlat{
        position: fixed;
        top: 60px;
        width: 23%;
        height: auto;
        background: #005358;
        padding: 10px;
        border-radius: 9px;
    }
    .navlat2{
        position: fixed;
        top: 395px;
        width: 23%;
        height: 230px;
        background: #005358;
        padding: 10px;
        border-radius: 9px;
        overflow-y: scroll;
    }
    .navlat p, li{
        color: white;
    }
    .filter{
        padding: 10px;
        margin-bottom: 10px;
        text-decoration: none;
        color: white;
        display: flex;
        align-items: center;
    }
    .filter:hover{
        background: #00393c;
    }
    .filter img{
        height: 25px;
        margin-right: 20px;
    }
    .content{
        margin: 0;
    }
    .content-body{
        padding: 1%;
        color: white;
        padding-top: 50px;
    }
    .loading{
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .content-post{
        background: #005358;
        margin-top: 10px;
        margin-left: 25%;
        margin-right: auto;
        padding: 2%;
        border-radius: 7px;
    }
    .content-post span{
        font-size: 11px;
    }
    .content-post p{
        font-size: 20px;
        word-spacing: 5px;
        line-height: 25px;
    }
    hr{
        border: 1px solid rgb(151, 151, 151);
    }
    .profil{
        display: flex;
        align-items: center;
        text-decoration: none;
        color: white;
        padding: 10px;
        margin-bottom: 10px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.218);
    }

    .profil:hover{
        background: rgba(1, 45, 53, 0.481);
    }
    .profil img{
        height: 40px;
        margin-right: 10px;
        border: 1px solid white;
        border-radius: 100%;
    }
    .see{
        font-size: 12px;
        color: rgba(255, 255, 255, 0.694);
    }
    .list{
        padding: 10px;
        color: white;
    }
    .list p{
        margin: 5px;
    }
    .action{
        margin-left: auto;
    }
    .action img{
        transition: 0.2s;
    }
    .action img:hover{
        background: rgba(128, 128, 128, 0.527);
        border-radius: 5px;
    }
    #calendar a,p{
        transition: 0.2s;
    }
    #calendar a{
        color: white;
        text-decoration: none;
        font-size: 18px;
        text-transform: uppercase;
    }
    #calendar a:hover{
        text-decoration: underline;
        color: #00dce0;
    }

    .container{
        display: flex;
    }

    .container img{
        height: 65px;
    }

    .number{
        border: 5px solid #005358;
        border-radius: 100%;
        padding: 10px;
        margin-left: auto;
        margin-bottom: auto;
    }

    .number1{
        border: 5px solid #00d42e;
        border-radius: 100%;
        padding: 10px;
        margin-left: auto;
        margin-bottom: auto;
    }

    .number1 p{
        color: #00d42e;
    }

    .number p, .number1 p{
        margin: 0;
        font-family: 'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana, sans-serif;
        font-weight: bold;
    }

    .container1{
        display: flex;
        align-items: center;
        margin-left: auto;
        margin-right: auto;
        background: #004649;
        padding: 20px;
        width: 20%;
        border-radius: 5px;
        color: white;
        text-decoration: none;
    }

    .container1 p{
        font-family: 'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana, sans-serif;
        font-weight: bold;
        font-size: 15px;
    }

    .container1:hover{
        box-shadow: 3px 3px 8px rgb(28, 28, 28);
        border: 1px solid rgba(255, 255, 255, 0.34);
    }

    .seeMore{
        text-decoration: none;
        color: white;
    }
    .seeMore p{
        background: #00393c;
        padding: 5px;
        text-align: center;
        border-radius: 5px;
    }

    @media screen and (max-width: 1150px) {
        .navlat{
            position: relative;
            width: 97%;
            top: 40px;
            padding: 2%;
        }
        .navlat2{
            position: relative;
            width: 97%;
            top: 45px;
            padding: 2%;
            margin-bottom: 50px;
        }
        .content-body{
            padding: 0;
        }
        .content-post{
            margin-left: auto;
            margin-right: auto;
            padding: 10px;
        }
        .container img{
            height: 50px;
        }
        .container1{
            background: #004649;
            padding: 10px;
            width: auto;
            border-radius: 5px;
            color: white;
            text-decoration: none;
        }

    }
</style>