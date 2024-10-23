<script>
    import { createEventDispatcher } from "svelte";
    import { login, getUserProfile, getUserStudent } from '../../../lib/auth';
    import { goto } from '$app/navigation'
    import { userProfile } from "../../../stores/auth";
    import { onMount } from "svelte";

    let email = '';
    let password = '';
    let errorMess = '';
    userProfile.subscribe(value => {
        if(value){
            goto('/student/home');
        }
    });

    async function handleSubmit() {
        const success = await login(email, password);
        if(success) {
            const profile = await getUserStudent();

            if(profile){
                userProfile.set(profile);
                userRole.set(profile.role)
                goto('/student/home')
            } else {
                errorMess = 'Connexion non autorisé';
            }
            
        } else {
            errorMess = 'Compte introuvable';
        }
    }
</script>

<div class="body">
        <div class="container">
            <div class="login-section">
                <img src="/icons/logo.png" alt="">
                <h1>Connexion</h1>
                <p>Vous vous connectez en tant qu' <b>étudiant</b></p>
                {#if errorMess}
                    <span>{errorMess}</span>
                {/if}

                <form on:submit|preventDefault={handleSubmit} class="login-form">
                    <input type="email" placeholder="E-mail" bind:value={email} required>
                    <input type="password" placeholder="Password" bind:value={password} required>
                    <div class="button">
                        <a id="cancel" href="/login"><button>Retour</button></a>
                        <button type="submit">Se connecter</button>
                    </div>
                    <div class="options">
                        <label>
                            <input type="checkbox"> Afficher le mot de passe
                        </label>
                        <a href="#">Mot de passe oublié?</a>
                    </div>
                </form><br><br>
                
                <p>Vous n'avez pas encore un compte? <a href="/signup/student">S'inscrire</a></p>
            </div>
            <div class="promo-section">
                <h2>Platform pour les établissements scolaires</h2>
            </div>
        </div>
    <footer>
        <p>© copyright 2024</p>
    </footer>
</div>

<style>

.body{
    padding: 2% 10%;
    font-family: 'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif;
}

a{
    color: #007bff;
    text-decoration: none;
}

span{
    color: rgb(255, 74, 74); 
}

.container {
    display: flex;
    box-shadow: 0 0 20px rgba(0, 0, 0, 0.605);
    border-radius: 8px;
    overflow: hidden;
    max-width: 1000px;
    width: 100%;
    margin: auto;
}

.promo-section {
    padding: 40px;
    flex: 1;
}

.login-section {
    background-color: #005358;
    flex: 1;
    padding: 50px;
    text-align: center;
}

.login-section h1 {
    margin: 0;
    font-size: 1.7em;
    color: white;
}

.login-section p {
    margin: 10px 0;
    color: white;
}

.login-section img{
    height: 70px;
}

.login-form {
    display: flex;
    flex-direction: column;
}

.login-form input[type="email"], .login-form input[type="password"] {
    padding: 10px;
    margin-bottom: 20px;
    border: 1px solid rgba(255, 255, 255, 0.175);
    background: transparent;
    border-radius: 5px;
    font-size: 1em;
    color: white;
}

.button{
    display: flex;
}
.button button{
    background-color: #007bff;
    color: #fff;
    padding: 10px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-size: 1em;
    width: 99%;
}

#cancel{
    width: 99%;
}

#cancel button{
    background-color: transparent;
    color: #007bff;
    border: 2px solid #007bff;
}

#cancel button:hover{
    color: #0054af;
    border: 2px solid #0054af;
}

.button button:hover{
    background-color: #0054af;
}

.options {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 10px;
}

.options label {
    color: white;
    font-size: 12px;
}

.options a {
    font-size: 12px;
}

.promo-section{
    background: url('/img/student.jpeg');
    background-repeat: no-repeat;
    background-size: cover;
}

.promo-section h2 {
    margin: 0;
    font-size: 1.5em;
    color: #333;
}

.promo-section a {
    display: block;
    margin: 20px 0;
    font-size: 12px;
}

footer {
    margin-top: 20px;
    width: 100%;
    text-align: center;
    font-size: 0.8em;
    color: #666;
}

.language-selector {
    margin-top: 10px;
}

</style>