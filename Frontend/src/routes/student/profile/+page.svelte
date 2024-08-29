<script>
    import NavProfile from '../../../lib/navStudent/navProfile.svelte'
    import { onMount } from 'svelte';
    import { getUserProfile, logout } from "../../../lib/auth";
    import { goto } from '$app/navigation';
    import { token, userProfile, infoFamiliale } from "../../../stores/auth";

    let user

    $: userProfile.subscribe(value => user = value);

    onMount(async () => {
        const response = await fetch(`http://127.0.0.1:8000/school/infoFamiliale/${user.id}/`);
        const data = await response.json();
        infoFamiliale.set(data);
    })
    
</script>

<div class="content">
    <NavProfile />
    <div class="content-body">
        {#if user}
            
            <h1>Année scolaire: 2023 - 2024</h1>
            <div class="info">
                <div class="profile">
                    <img src="/icons/profile.png" alt="">
                </div>
                <div class="infoDetail">
                    <ul>
                        <!-- {#if student}
                        <li><b>Nom</b> : <i>{student.name}</i></li>
                        <li><b>Prénom</b> : <i>{student.lastname}</i></li>
                        <li><b>Sexe</b> : <i>{student.sexe}</i></li>
                        <li><b>Classe</b> : <i>{student.class_degree}</i></li>
                        <li><b>Date de naissance</b> : <i>{student.birthday_date}</i></li>
                        <li><b>Adresse</b> : <i>{student.address}</i></li>
                        <li><b>Numéro mobile</b> : <i>{student.number}</i></li>
                        {:else}
                        <li>Loading...</li>
                        {/if} -->
                        <li><b>Nom </b> : <i>{user.student_name}</i></li>
                        <li><b>Prénom </b> : <i>{user.student_lastname}</i></li>
                        <li><b>Adresse</b> : <i>{user.address}</i></li>
                        <li><b>Numéro mobile</b> : <i>0{user.student_number}</i></li>
                        <li><b>Email</b> : <i>{user.email}</i></li>
                        <li><b>Sexe </b> : <i>{user.student_sexe}</i></li>
                        <li><b>Date de naissance </b> : <i>{user.student_birthday_date}</i></li>
                    </ul>
                </div>
                <div class="add">
                    <button>
                        <a href="/home">
                            <img src="/icons/modifier.png" alt="">
                        </a>
                    </button>
                </div>
            </div>
            
            <hr>
            <div class="body">
                <div class="infoDetail">
                    <h3>Info </h3>
                    <ul>
                        <li><b>Classe </b> : <i>{user.student_class}</i></li>
                        <li><b>Numéro d'inscription </b> : <i>{user.student_register_number}</i></li>
                        <li><b>Date d'inscription </b> : <i>{user.register_date}</i></li>
                        <li><b>Nom de l'établissement </b> : <i>{user.school_name}</i></li>
                    </ul><br>

                    <h3>Info Familiale</h3>
                    <ul class="infoFam">
                        <div class="">
                            {#each $infoFamiliale as info}
                            <li><b>Nom de la mère</b> : <i>{info.mother_name}</i></li>
                            <li><b>Prénom de la mère</b> : <i>{info.mother_lastname}</i></li>
                            <li><b>Profession de la mère</b> : <i>{info.mother_profession}</i></li>
                            <li><b>Numéro du mobile</b> : <i>0{info.mother_number}</i></li>
                            <li><b>Nom du père</b> : <i>{info.father_name}</i></li>
                            <li><b>Prénom du père</b> : <i>{info.father_lastname}</i></li>
                            <li><b>Profession du père</b> : <i>{info.father_profession}</i></li>
                            <li><b>Numéro du mobile</b> : <i>0{info.father_number}</i></li>
                            {/each}
                        </div>
                        <div class="add">
                            <button>
                                <a href="/home">
                                    <img src="/icons/modifier.png" alt="">
                                </a>
                            </button>
                        </div>
                    </ul><br>
                </div>
            </div>
        {:else}
        tsisy
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
    .add a{
        display: flex;
        align-items: center;
    }
    .add img{
        height: 50px;
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
        padding-top: 50px;
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
    .infoFam{
        display: flex;
    }


</style>