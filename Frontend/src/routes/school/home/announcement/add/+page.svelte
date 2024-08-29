<script>
    import NavHome from "../../../../../lib/nav/navHome.svelte";
    import Loading from "../../../../../lib/loading.svelte";
    import { onMount } from "svelte";
    import App from '../../../../app.svelte';
    import { getUserProfile, logout } from "../../../../../lib/auth";
    import { goto } from '$app/navigation';
    import { token, userProfile, matiere, getStoreValue, students } from "../../../../../stores/auth";

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
            const profile = await getUserProfile();
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
                    <span>Vide</span><br>
                    <span class="see">Voir votre profile</span>
                </div>
            </div>
        </div>
        {:else}
        <div class="">
            <a class="profil" href="">
                    <img src="/img/pdp_Archange.jpg" alt="">
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
                    <span>Vide</span><br>
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

                    <form action="" method="post">
                        <div class="container">
                            <textarea name="" id="" placeholder="Entrer le contenu"></textarea>
                            <input type="file" name="" id="">
                        </div>
    
                        <div class="add">
                            <button>
                                    <img src="/icons/ajouter.png" alt="">
                                    <span>Ajouter</span>
                            </button>
                        </div>
                    </form>
                    
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
    .add img{
        height: 30px;
        margin-right: 10px;
    }
    .add button{
        display: flex;
        align-items: center;
        color: white;
        background: transparent;
        border: 1px solid white;
        border-radius: 5px;
        transition: 0.2s;
        padding: 10px;
        margin-bottom: 5px;
    }
    .add button:hover{
        background: rgba(128, 128, 128, 0.574);
        cursor: pointer;
    }
    .post{
        display: flex;
    }
    .post img{
        height: 40px;
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
        padding: 10px;
        border: 1px solid rgba(255, 255, 255, 0.253);
        border-radius: 5px;
        margin-bottom: 15px;
    }

    textarea{
        width: 100%;
        height: 60px;
        border-radius: 5px;
        background-color: #004044;
        border: none;
        color: white;
    }

    input[type='file']{
        border: 1px solid rgba(255, 255, 255, 0.146);
        width: 100%;
        padding-left: 5px;
        padding-top: 5px;
        padding-bottom: 5px;
        cursor: pointer;
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