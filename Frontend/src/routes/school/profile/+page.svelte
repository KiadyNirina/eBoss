<script>
    import NavProfile from '../../../lib/nav/navProfile.svelte'
    import { onMount } from 'svelte';
    import { getUserProfile, logout } from "../../../lib/auth";
    import { goto } from '$app/navigation';
    import { token, userProfile, matiere, getStoreValue } from "../../../stores/auth";

    let user;

    userProfile.subscribe(value => user = value);

    onMount(async () => {
        const $token = getStoreValue(token);
        if($token) {

            const profile = await getUserProfile();
            
            if(profile){
                userProfile.set(profile);
                const response = await fetch(`http://localhost:8000/school/classMatiere/${user.school_name}/`);
                const data = await response.json();
                matiere.set(data);
            } else {
                goto('/login');
            }
        }
    })

</script>

<div class="content">
    <NavProfile />
    <div class="content-body">
        {#if user}
            
            <div class="info">
                <div class="profile">
                    <img src="/img/pdp_Archange.jpg" alt="">
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
                        <li><b>Nom de l'etablissment</b> : <i>{user.username}</i></li>
                        <li><b>Adresse</b> : <i>{user.address}</i></li>
                        <li><b>Numéro mobile</b> : <i>0{user.school_number}</i></li>
                        <li><b>Email</b> : <i>{user.email}</i></li>
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
                    <h3>Info de l'établissement</h3>
                    <ul>
                        <!-- {#each familialeData as familiale}
                        <li><b>Nom et prénom du mère : </b>{familiale.mother_name} {familiale.mother_lastname}</li>
                        <li><b>Mobile : </b>{familiale.mother_number}</li>
                        <li><b>Nom et prénom du père : </b>{familiale.father_name} {familiale.father_lastname}</li>
                        <li><b>Mobile : </b>{familiale.father_number}</li>
                        {/each} -->
                        <li><b>Type</b> : <i>{user.school_type}</i></li>
                        <li><b>Niveaux scolaires</b> : <i>{user.school_level}</i></li>
                        <li><b>Classes</b> : <i>{user.school_classes}</i></li>
                        <li><b>Matières</b> : <br>
                            <div class="matiere">
                                <i>
                                    {#each $matiere as mat}
                                        <ul>
                                            <li>{mat.subject} : ({mat.classe})</li>
                                        </ul>
                                    {/each}
                                </i>
                                <div class="add">
                                    <button>
                                        <a href="/school/profile/editSubject">
                                            <img src="/icons/modifier.png" alt="">
                                        </a>
                                    </button>
                                </div>
                            </div>
                        </li>
                    </ul>

                    <hr>

                    <div class="title">
                        <h3>Informations Académiques</h3>
                        <div class="add">
                            <button>
                                <a href="/school/profile/editSubject">
                                    <img src="/icons/modifier.png" alt="">
                                </a>
                            </button>
                        </div>
                    </div>
                    <ul>
                        <li><b>Année scolaire</b> : <i></i></li>
                        <li><b>Durée d'études</b> : <i>10 mois</i></li>
                        <li><b>Mois</b> : <i></i></li>
                        <li><b>Nombre de semestre</b> : <i></i></li>
                    </ul>

                    <hr>

                    <div class="title">
                        <h3>Informations Financières</h3>
                        <div class="add">
                            <button>
                                <a href="/school/profile/editSubject">
                                    <img src="/icons/modifier.png" alt="">
                                </a>
                            </button>
                        </div>
                    </div>
                    <ul>
                        <li><b>Inscription</b> : 
                            <div class="matiere">
                                <i>
                                    <ul>
                                        <li>40.000ar / mois : (6eme,5eme,4eme,3eme,2nde,1ere,Tle)</li>
                                    </ul>
                                </i>
                            </div> 
                        </li>
                        <li><b>Frais Généraux</b> : 
                            <div class="matiere">
                                <i>
                                    <ul>
                                        <li>35.000ar / mois : (6eme,5eme,4eme,3eme,2nde,1ere,Tle)</li>
                                    </ul>
                                </i>
                            </div> 
                        </li>
                        <li><b>Divers</b> : 
                            <div class="matiere">
                                <i>
                                    <ul>
                                        <li>50.000ar / mois : (6eme,5eme,4eme,3eme,2nde,1ere,Tle)</li>
                                    </ul>
                                </i>
                            </div> 
                        </li>
                        <li><b>Frais de scolarité</b> :
                            <div class="matiere">
                                <i>
                                    <ul>
                                        <li>300.000ar / mois : (6eme,5eme,4eme)</li>
                                        <li>70.000ar / mois : (3eme,2nde,1ere)</li>
                                        <li>80.000ar / mois : (Tle)</li>
                                    </ul>
                                </i>
                            </div> 
                        </li>
                    </ul>
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
        border: 2px solid rgba(255, 255, 255, 0.475);
        border-radius: 100%;
        padding: 5px;
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
    .matiere{
        display: flex;
    }
    .title{
        display: flex;
        align-items: center;
    }

</style>