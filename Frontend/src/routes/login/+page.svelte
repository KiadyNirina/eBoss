<script>
    /*import { createEventDispatcher } from "svelte";
    import { login, getUserProfile } from '../../lib/auth';
    import { goto } from '$app/navigation'
    import { userProfile } from "../../stores/auth";

    let email = '';
    let password = '';
    let errorMess = '';*/

</script>

<div class="body">
        <div class="container">
            <div class="login-section">
                <img src="/icons/logo.png" alt="">
                <h1>Connexion</h1>
                <p>Bienvenue sur eBoss! 👋</p>

                <ul>Se connecter en tant que :
                    <hr>
                    <a href="/login/school"><li>Etablissement</li></a>
                    <a href="/login/student"><li>Etudiant</li></a>
                    <a href="/login/teacher"><li>Professeur</li></a>
                    <a href="/login/parent"><li>Parent</li></a>
                </ul>
                <a id="cancel" href="/"><button>Retour</button></a>
            </div>
            <div class="promo-section">
                <h2>Platform pour les établissements scolaires</h2>
                <a href="#">Ansehen & Features sichern</a>
                <div class="promo-image"></div>
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
    color: white;
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

.login-section a{
    text-decoration: none;
    color: white;
}

.login-section ul{
    padding: 10px 0;
    border: 1px solid rgba(255, 255, 255, 0.365);
    border-radius: 5px;
}

.login-section li{
    padding: 10px;
    list-style: none;
}

hr{
    border : 1px solid rgba(255, 255, 255, 0.365);
}

.login-section li:hover{
    background-color: #003b3e;
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

.login-form button {
    background-color: #007bff;
    color: #fff;
    padding: 10px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-size: 1em;
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
    background: url('/img/school.jfif');
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

#cancel button{
    width: 100%;
    padding: 10px;
    border: none;
    border-radius: 5px;
    background-color: #007bff;
    color: white;
}

#cancel button:hover{
    background-color: #0054af;
    cursor: pointer;
}

</style>