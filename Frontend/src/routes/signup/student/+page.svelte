<script>
    import { classes, schoolName } from '../../../stores/auth';
    import { goto } from '$app/navigation';
    import { onMount } from "svelte";

    let student_name = '';
    let student_lastname = '';
    let student_sexe = '';
    let student_address = '';
    let student_number = '';
    let email = '';
    let student_birthday_date
    let school_type = '';
    let selected_level = [];
    let selected_classes = [];
    let password = '';
    let confirm_password = '';
    let groups = [];
    let user_permissions = [];

    let level_classes = {
        Ecole: ['12eme', '11eme', '10eme', '9eme', '8eme', '7eme'],
        College: ['6eme', '5eme', '4eme', '3eme'],
        Lycee: ['2nde', '1ere', 'Term'],
        Universite: ['L1', 'L2', 'L3', 'M1', 'M2']
    }

    let errorName = '';
    let errorAddress = '';
    let errorNumber = '';
    let errorEmail = '';
    let errorType = '';
    let errorLevel = '';
    let errorPassword = '';
    let errorConfirmPassword = '';

    let isDisabled = true;
    let isDisabled2 = true;
    let isDisabled3 = true;

    /*$: isDisabled = !(student_name, address, student_number, email) || errorName || errorAddress || errorNumber || errorEmail 
    $: isDisabled2 = !(school_type, selected_level) || errorType || errorLevel
    $: isDisabled3 = !(password, confirm_password) || errorPassword || errorConfirmPassword*/

    const validName = (name) => {
        const inputValue = name.target.value;
        const regex = /^[a-z A-Z]*$/;
        if(!regex.test(inputValue)) {
            errorName = 'Le nom ne doit pas contenir que de l\'alphabet';
        }else if(inputValue.length < 4){
            errorName = 'Le nom est trop court';
        }else{
            errorName = '';
        }
    }

    const validAddress = (address) => {
        const inputValue = address.target.value;
        const regex = /^[a-z A-Z0-9]*$/;
        if(!regex.test(inputValue)) {
            errorAddress = 'L\'adresse n\'est pas correcte';
        }else if(inputValue.length < 4){
            errorAddress = 'L\'adresse est trop court';
        }else{
            errorAddress = '';
        }
    }

    const validNumber = (school_number) => {
        const inputValue = school_number.target.value;
        const regex = /^[0-9]*$/;
        if(!regex.test(inputValue)) {
            errorNumber = 'Le numéro n\'est pas correcte';
        } else if (inputValue.length < 10) {
            errorNumber = 'Le numéro n\'est pas suffisant';
        } else if (inputValue.length > 10) {
            errorNumber = 'Le numéro est trop long';
        } else {
            errorNumber = '';
        }
    }

    const validEmail = (email) => {
        const inputValue = email.target.value;
        const regex = /^[0-9a-zA-Z@.]*$/;
        if(!regex.test(inputValue)) {
            errorEmail = 'L\'email n\'est pas correcte';
        } else if (inputValue.length < 1) {
            errorEmail = 'L\'email ne doit pas être vide';
        } else if (inputValue.length > 20) {
            errorEmail = 'L\'email est trop long';
        } else {
            errorEmail = '';
        }
    }

    const validType = (school_type) => {
        const inputValue = school_type.target.value;
        if(inputValue.length == 0){
            errorType = 'Veuillez selectionner le type de l\'établissement';
        } else {
            errorType = '';
        }
    }

    const validLevel = (selected_level) => {
        if(selected_classes === null) {
            errorLevel = 'Veuillez selectionnez le(s) niveau(x) scolaire(s)';
        } else {
            errorLevel = '';
        }
    }

    const validPassword = (password) => {
        const input = password.target.value
        if(input.length === 0) {
            errorPassword = 'Le mot de passe ne doit pas être vide';
        } else if(input.length < 6) {
            errorPassword = 'Le mot de passe est trop court';
        } else {
            errorPassword = '';
        }
    }

    const validConfirmPassword = (confirm_password) => {
        const inputValue = confirm_password.target.value
        if(inputValue !== password) {
            errorConfirmPassword = 'Les 2 mots de passes ne correspondent pas';
        } else {
            errorConfirmPassword = '';
        }
    }

    let info1 = true;
    let info2 = false;
    let info3 = false;

    const handleClick = () => {
        info1 = false;
        info2 = true;
        info3 = false;
    }

    const handleClickBack = () => {
        info1 = true;
        info2 = false;
        info3 = false;
    }

    const lastHandleClick = () => {
        info1 = false;
        info2 = false; 
        info3 = true;
    }

    function toggle_level(level) {
        if(selected_level.includes(level)) {
            selected_level = selected_level.filter(item => item !== level);
        } else {
            selected_level.push(level);
        }
        updateSelectedClasses();
    }

    function updateSelectedClasses() {
        selected_classes = [];
        selected_level.forEach(lev => {
            selected_classes = [...selected_classes, ...level_classes[lev]]
        })
    }

    async function fetchClasse(school_Name) {
        const response = await fetch(`http://localhost:8000/school/schoolClasse/${school_Name}`);
        const data = await response.json();
        classes.set(data);
    }

    onMount(async () => {
            const response = await fetch(`http://localhost:8000/school/schoolClasses/`);
            const data = await response.json();
            schoolName.set(data);
    })

    async function submitForm() {
        if( password !== confirm_password ) {
            error = 'Les mots de passes ne correspondent pas';
            return;
        }

        const response = await fetch('http://localhost:8000/school/schoolRegistration/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ 
                password: password,
                confirm_password: confirm_password,
                email: email,
                username: name,
                school_name: name,
                address: address,
                school_number: school_number,
                school_type: school_type,
                school_level: selected_level,
                school_classes: selected_classes,
                groups: groups,
                user_permissions: user_permissions,
             }),
        });

        const data = await response.json();
        alert('Inscription terminé avec succès!');
        goto('/login');

        if(response.ok) {
            console.log(data);
        }else{
            console.error(data);
        }
    }
</script>

<div class="body">
    <div class="container">
        <div class="form">
            <img src="/icons/logo.png" alt="">
            <h1>Créer un compte</h1>
            <p>Inscrivez-vous en tant qu'étudiant</p>
            <form>
                {#if info1}
                    <div class="two">
                        <div class="name">
                            <label for="">Nom :</label>
                            <input type="text" name="" id="" placeholder="Entrer le votre nom" bind:value={student_name} on:input={validName}>
                            {#if errorName}
                                <span class="error">{errorName}</span>
                            {/if}
                        </div>
                        
                        <div class="name">
                            <label for="">Prénom :</label>
                            <input type="text" name="" id="" placeholder="Entrer votre prénom" bind:value={student_lastname} on:input={validAddress}>
                            {#if errorAddress}
                                <span class="error">{errorAddress}</span>
                            {/if}
                        </div>
                    </div>

                    <div class="one">
                        <label for="">Sexe :</label>
                        <select name="" id="" bind:value={student_sexe}>
                            <option value="" disabled>Selectionnez votre sexe</option>
                            <option value="Male">Garçon</option>
                            <option value="Female">Fille</option>
                        </select>
                    </div>
                    
                    <div class="one">
                        <label for="">Date de naissance :</label>
                        <input type="date" name="" id="" bind:value={student_birthday_date}>
                    </div>

                    <div class="two">
                        <div class="name">
                            <label for="">Numéro :</label>
                            <input type="text" name="" id="" placeholder="Entrer le numéro du mobile de l'établissement" bind:value={student_number} on:input={validNumber}>
                            {#if errorNumber}
                                <span class="error">{errorNumber}</span>
                            {/if}       
                        </div> 

                        <div class="name">
                            <label for="">Email :</label>
                            <input type="email" name="" id="" placeholder="Entrer l'adresse email de l'établissement" bind:value={email} on:input={validEmail}>
                            {#if errorEmail}
                                <span class="error">{errorEmail}</span>
                            {/if} 
                        </div>
                    </div>

                {:else if info2}
                    <div class="one">
                        <label for="">Nom de l'établissement :</label>
                        <select name="" id="">
                            <option value="" disabled>Selectionnez le nom de l'établissement</option>
                            {#if $schoolName.length > 0}
                                {#each $schoolName as schoolname}
                                    <option value={schoolname.school_name} on:click={fetchClasse(schoolname.school_name)}>{schoolname.school_name}</option>
                                {/each}
                            {/if}
                        </select>
                    </div>
                    <hr>
                    <div class="one">
                        <label for="">Classe :</label>
                        <select name="" id="">
                            <option value="" disabled>Selectionnez votre classe</option>
                            {#if $classes.length > 0}
                                {#each $classes as classe}
                                    <option value="">{classe.school_classes}</option>                                    
                                {/each}
                            {:else}
                                <option value="">5eme</option>
                            {/if}
                        </select>
                    </div><hr>
                    
                    <div class="two">
                        <div class="name">
                            <label for="">Date d'inscription :</label>
                            <input type="date" name="" id="">
                        </div>
                        <div class="name">
                            <label for="">Numéro d'inscription :</label>
                            <input type="number" name="" id="" placeholder="Entrer votre numéro d'inscription">
                        </div>
                    </div>

                {/if} 
                {#if info3}
                    <div class="one">
                            <label for="">Mot de passe :</label>
                            <input type="password" name="" id="" placeholder="Entrer le mot de passe de l'établissement" bind:value={password} on:input={validPassword}>
                            {#if errorPassword}
                                <span class="error">{errorPassword}</span>
                            {/if}
                    </div>
                    <div class="one">
                            <label for="">Confirmer mot de passe :</label>
                            <input type="password" name="" id="" placeholder="Entrer à nouveau le mot de passe de l'établissement" bind:value={confirm_password} on:input={validConfirmPassword}>
                            {#if errorConfirmPassword}
                                <span class="error">{errorConfirmPassword}</span>
                            {/if}
                    </div>
                    <div class="one" id="forCondition">
                        <label for="" id="condition">
                            <input type="checkbox" name="" id="">
                            En cochant cette case, vous acceptez notre condition d'utilisation
                        </label>
                    </div>
                {/if}

                {#if info1}
                    <div class="one">
                        <!-- <button on:click={handleClick} disabled={isDisabled}>Suivant</button> -->
                        <button on:click={handleClick}>Suivant</button>
                    </div>    
                {:else if info2}
                    <div class="two">
                        <button id="back" on:click={handleClickBack}>Retour</button>
                        <button on:click={lastHandleClick}>Suivant</button>
                    </div>                
                {:else}
                    <div class="two">
                        <button id="back" on:click={handleClick}>Retour</button>
                        <button type="submit" on:click={submitForm} disabled={isDisabled3}>S'inscrire</button>
                    </div>      
                {/if}

                <!-- <div class="one">
                    <button type="submit">Créer</button>
                </div> -->

            </form>
            <p>Avez-vous déjà un compte ? <a href="/login/school">Se connecter</a></p>
        </div>
    </div>
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
        box-shadow: 0 0 20px rgba(0, 0, 0, 0.605);
        border-radius: 8px;
        overflow: hidden;
        max-width: 500px;
        width: 100%;
        display: flex;
        margin-left: auto;
        margin-right: auto;
        padding: 20px;
        background-color: #005358;
    }

    h1{
        font-size: 1.7em;
        text-align: center;
    }

    .form {
        color: white;
        width: 100%;
    }

    .form img{
        display: flex;
        margin-right: auto;
        margin-left: auto;
        height: 70px;
    }

    form{
        border: 1px solid rgba(255, 255, 255, 0.176);
        border-radius: 5px;
        padding: 10px;
        /*padding-right: 20px;*/
    }

    .two{
        display: flex;
        margin-bottom: 10px;
    }

    .name {
        width: 50%;
    }

    .name input{
        width: 90%;
        padding: 10px;
        background: none;
        border: 1px solid rgba(255, 255, 255, 0.175);
        border-radius: 5px;
        margin-top: 5px;
        color: white;
    }

    label{
        font-size: 15px;
    }

    .one {
        width: 100%;
        margin-bottom: 10px;
    }

    .one input{
        width: 95%;
        padding: 10px;
        border-radius: 5px;
        border: 1px solid rgba(255, 255, 255, 0.175);
        background: none;
        margin-top: 5px;
        color: white;
    }

    .one button{
        width: 99.5%;
        padding: 10px;
        border-radius: 5px;
        border: none;
        background-color: #007bff;
        color: #fff;
        cursor: pointer;
    }

    button:disabled, button[type='submit']:disabled{
        color: grey;
        background-color: #005abb;
    }

    .one button:hover, .two button:hover{
        background-color: #005abb;
    }

    .one select {
        width: 100%;
        padding: 10px;
        border: none;
        border-radius: 5px;
        background-color: rgb(0, 64, 69);
        color: white;
        margin-top: 5px;
    }

    .one option{
        color: rgb(0, 64, 69);
        background: white;
    }

    .two button{
        width: 49%;
        padding: 10px;
        border-radius: 5px;
        border: none;
        background-color: #007bff;
        color: #fff;
        cursor: pointer;
        display: flex;
        justify-content: center;
        margin-left: auto;
        margin-right: auto;
    }

    hr{
        border: 1px solid rgba(255, 255, 255, 0.259);
    }

    #back{
        background-color: transparent;
        border: 1px #007bff solid;
        color: #007bff;
    }

    input[type='checkbox'] {
        width: auto;
        cursor: pointer;
    }

    .check{
        width: 100%;
        display: flex;
    }

    .check label{
        font-size: 15px;
        margin-right: auto;
        margin-left: auto;
    }

    .classe{
        border: 1px solid rgba(255, 255, 255, 0.482);
        border-radius: 5px;
        padding: 10px;
        margin-left: auto;
        margin-right: auto;
    }

    ul{
        font-size: 13px;
    }

    #forCondition {
        width: 100%;
        align-items: center;
        justify-content: center;
        display: flex;
    }

    #condition {
        font-size: 15px;
        border: 1px solid rgba(255, 255, 255, 0.315);
        padding: 20px;
        border-radius: 5px;
        text-align: center;
    }

    .error{
        color: rgb(255, 82, 82);
        font-size: 15px;
    }
</style>