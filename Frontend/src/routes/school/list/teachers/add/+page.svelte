<script>
    import { onMount } from "svelte";
    import { classes, students } from "../../../../../stores/auth";
    import { createEventDispatcher } from "svelte";
    import NaList from "../../../../../lib/nav/naList.svelte";
    import { userProfile, matiere } from "../../../../../stores/auth";

    let user

    $: userProfile.subscribe(value => user = value);

    let name = '';
    let lastname = '';
    let class_degree = [];
    let subjects = [];
    let sexe = '';
    let birthday_date = '';
    let number = '';
    let emailStudent = '';
    let address = '';
    let register_date = '';
    let files;
    let password = '';
    let confirm_password = '';
    const dispatch = createEventDispatcher();

    let SuccessMessage = false;
    let ErrorMessage = false;

    let ErrorField = false;
    let nameFieldError = '';
    let lastnameFieldError = '';
    let classFieldError = '';
    let genderFieldError = '';
    let birthdayFieldError = '';
    let addressFieldError = '';
    let numberFieldError = '';
    let registerFieldError = '';

    const isValidName = (name) => {
        const inputValue = name.target.value;
        const regex = /^[a-zA-Z ]*$/;
        if(!regex.test(inputValue)) {
            nameFieldError = 'Le nom ne doit contenir que des lettres';
        }else if(inputValue.length < 2){
            nameFieldError = 'Le nom est trop court';
        } else {
            nameFieldError = '';
        }
    }

    const isValidLastname = (lastname) => {
        const inputValue = lastname.target.value;
        const regex = /^[a-zA-Z ]*$/;
        if(!regex.test(inputValue)) {
            lastnameFieldError = 'Le prénom ne doit contenir que des lettres';
        }else if(inputValue.length < 2){
            lastnameFieldError = 'Le prénom est trop court';
        } else {
            lastnameFieldError = '';
        }
    }

    const isValidClass = (class_degree) => {
        const inputValue = class_degree.target.value;
        //const regex = /^[a-zA-Z]*$/;
        if(inputValue.length < 1){
            classFieldError = 'La classe ne doit pas être vide';
        } else {
            classFieldError = '';
        }
    }

    const isValidGender = (sexe) => {
        const inputValue = sexe.target.value;
        //const regex = /^[a-zA-Z]*$/;
        if(inputValue.length === 0){
            genderFieldError = 'Le sexe ne doit pas être vide';
        } else {
            genderFieldError = '';
        }
    }

    const isValidBirthdayDate = (birthday_date) => {
        const inputValue = birthday_date.target.value;
        const dateObj = new Date(inputValue);
        const max = new Date();
        if(isNaN(dateObj.getDate())){
            birthdayFieldError = 'La date de naissance n\'est pas correcte';
        } else if (dateObj > max){
            birthdayFieldError = 'La date de naissance est invalide';
        } else {
            birthdayFieldError = '';
        }
    }

    const isValidAddress = (address) => {
        const inputValue = address.target.value;
        const regex = /^[a-zA-Z 0-9]*$/;
        if(!regex.test(inputValue)){
            addressFieldError = 'L\'adresse n\'est pas correcte';
        } else if(inputValue.length < 5){
            addressFieldError = 'L\'adresse est trop courte';
        } else {
            addressFieldError = '';
        }
    }

    const isValidNumber = (number) => {
        const inputValue = number.target.value;
        const regex = /^[0-9]*$/;
        if(!regex.test(inputValue)){
            numberFieldError = 'Le numéro n\'est pas correcte';
        } else if(inputValue.length < 10){
            numberFieldError = 'Le numéro doit contenir au moins 10 caractères';
        } else {
            numberFieldError = '';
        }
    }

    const isValidRegister = (register_date) => {
        const inputValue = register_date.target.value;
        const dateObj = new Date(inputValue);
        if(isNaN(dateObj.getTime())){
            registerFieldError = 'La date d\'inscription n\'est pas correcte';
        } else {
            registerFieldError = '';
        }
    }

    function toggle_level(level) {
        if(class_degree.includes(level)) {
            class_degree = class_degree.filter(item => item !== level);
        } else {
            class_degree.push(level);
        }
    }

    function toggle_subject(level) {
        if(subjects.includes(level)) {
            subjects = subjects.filter(item => item !== level);
        } else {
            subjects.push(level);
        }
    }

    let isDisabled = true;

    $: isDisabled = !(name && lastname && birthday_date && address && number && register_date) || nameFieldError || lastnameFieldError || birthdayFieldError || addressFieldError || numberFieldError || registerFieldError;

    onMount( async () => {
        const response = await fetch(`http://localhost:8000/school/classMatiere/${user.id}/`);
        const data = await response.json();
        matiere.set(data)
    })

    async function handleSubmit() {

        const formData = {
            password : password,
            confirm_password : confirm_password,
            email : emailStudent,
            username : lastname,
            school_name : user.school_name,
            address : address,
            teacher_name : name,
            teacher_lastname : lastname,
            teacher_sexe : sexe,
            teacher_classes : class_degree,
            teacher_subjects : subjects,
            teacher_number : number,
            teacher_birthday : birthday_date,
            teacher_register_date : register_date,
            role: 'teacher',
            groups: [],
            user_permissions: [],
        }

        try{
            const endpoint = 'http://127.0.0.1:8000/school/schoolRegistration/';
            const response = await fetch(endpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData),
            });

            const data = await response.json();

            if(!response.ok) {
                console.error(data)
                ErrorMessage = true;
            } else {
                console.log(data)
                SuccessMessage = true;
            }

        } catch( error ) {
            console.error('Error: ', error);
            ErrorMessage = true;
        }
    }
</script>

<div class="content">
    <NaList />
    <div class="content-body">
        <div class="">
            <h1>Ajouter un(e) professeur(e) </h1>

            {#if SuccessMessage}
                <div class="success">
                    <p>Professeur ajouté(e) avec succès.</p>
                </div>
            {:else if ErrorMessage}
                <div class="error">
                    <p>Erreur lors de l'ajout du professeur.</p>
                </div>
            {/if}

            <form on:submit|preventDefault={handleSubmit}>
                <label for="">Nom</label>
                <div class="input">
                    <input type="text" name="" placeholder="Nom du prof" bind:value={name} on:input={isValidName}>
                    {#if nameFieldError}
                        <span class="smallError">{nameFieldError}</span>
                    {/if}
                
                    
                    <input type="text" name="" placeholder="Prénom du prof" bind:value={lastname} on:input={isValidLastname}>
                    {#if lastnameFieldError}
                        <span class="smallError">{lastnameFieldError}</span>
                    {/if}

                    <select name="" id="" bind:value={sexe}>
                            <option value="" disabled>Selectionnez le sexe</option>
                            <option value="Homme">Homme</option>
                            <option value="Femme">Femme</option> 
                    </select>
                    {#if classFieldError}
                        <span class="smallError">{classFieldError}</span>
                    {/if}
                </div><br>

                <label for="">Date de naissance</label>
                <div class="input">
                    <input type="date" name="" id="birthday" bind:value={birthday_date} on:change={isValidBirthdayDate}>
                    {#if birthdayFieldError}
                        <span class="smallError">{birthdayFieldError}</span>
                    {/if}

                    <input type="text" name="" id="address" placeholder="Adresse" bind:value={address} on:input={isValidAddress}><br>
                    {#if addressFieldError}
                        <span class="smallError">{addressFieldError}</span>
                    {/if}
                </div><br>

                <label for="">Séléctionnez les classes qui seront tenues par Mr/Mme <b>{name} {lastname}</b> :</label>
                <div class="input">
                    <div class="check">
                        {#each user.school_classes as classes}
                            <label for="">{classes}
                                <input type="checkbox" on:change={() => toggle_level(classes)} name="" id="">
                            </label>
                        {/each}
                    </div>
                </div><br>

                <label for="">Séléctionnez les matières qui seront tenues par Mr/Mme <b>{name} {lastname}</b> :</label>
                <div class="input">
                    <div class="check">
                        {#each $matiere as mat}
                            <label for="">{mat.subject}
                                <input type="checkbox" on:change={() => toggle_subject(mat.subject)} name="" id="">
                            </label>
                        {/each}
                    </div>
                </div><br>

                <label for="">Numéro mobile et email</label>
                <div class="input">
                    <input type="text" placeholder="Numéro de mobile" on:input={isValidNumber} bind:value={number}><br>
                    {#if numberFieldError}
                        <span class="smallError">{numberFieldError}</span>
                    {/if}

                    <input type="text" name="" id="" placeholder="Email" bind:value={emailStudent}>
                </div>

                <label for="">Date d'inscription et Photo d'identité</label>
                <div class="input">
                    <input type="date" name="" bind:value={register_date} on:change={isValidRegister}>
                    {#if registerFieldError}
                        <span class="smallError">{registerFieldError}</span>
                    {/if}

                    <input type="file" bind:files name=""><br>
                </div>

                <label for="">Mot de passe</label>
                <div class="input">
                    <input type="password" name="" id="" placeholder="Mot de passe" bind:value={password}>
                    <input type="password" name="" id="" placeholder="Confirmer mot de passe" bind:value={confirm_password}>
                </div>

                <p>Nb : Tous les champs sont obligatoire</p>

                <button disabled = {isDisabled} type="submit">Ajouter</button>
                <a href="/school/list/students"><button id="cancel">Annuler</button></a>
            </form>
        </div>
    </div>
</div>

<style>
    :focus {
    outline: 0;
    box-shadow: 0 0 0 4px white;
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

    .content{
        padding: 1%;
        color: white;
        padding-top: 60px;
        font-size: 20px;
    }
    h1{
        font-size: 30px;
        text-align: center;
    }
    .content-body{
        margin-left: 15%;
        margin-right: 15%;
        background: #005358;
        padding: 10px;
        border-radius: 5px;
        border: none;
    }
    .input, .input-one{
        padding: 5px;
        display: flex;
    }
    .input{
        border-radius: 5px;
        border: 1px solid rgba(255, 255, 255, 0.389);
    }
    .input input, select,
    .input-one input, select{
        width: 100%;
        color: white;
        margin: 5px;
        padding: 10px;
        border-radius: 5px;
        border: none;
        background: #004041;
    }
    option{
        color: #002729;
        background: white;
    }
    label{
        font-size: 15px;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    button{
        margin-top: 10px;
        padding: 10px;
        border-radius: 5px;
        border: none;
        font-family: 'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana, sans-serif;
        background: #002729;
        color: white;
        width: 100%;
    }
    button:disabled{
        color: grey;
        background: #003b3f;
    }
    p{
        font-size: 13px;
        text-align: center;
    }
    button:hover{
        cursor: pointer;
        background: #003b3f;
    }
    #cancel{
        background: none;
        border: 2px solid #002729;
    }
    #cancel:hover{
        background: #003b3f;
    }
    .success{
        background: green;
        border-radius: 10px;
        padding: 5px;
    }
    .success p{
        color: white;
        font-weight: bold;
        font-family: 'Courier New', Courier, monospace;
    }
    .error{
        background: rgba(255, 31, 31, 0.826);
        border-radius: 10px;
        padding: 5px;
    }
    .error p{
        color: white;
        font-weight: bold;
        font-family: 'Courier New', Courier, monospace;
    }
    .smallError{
        color: rgb(250, 97, 97);
        font-size: 12px;
        font-weight: bolder;
        font-family: 'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif;
    }
    @media screen and (max-width: 800px) {
        .content-body{
            margin-left: auto;
            margin-right: auto;
            padding: 10px;
        }
        .input input, select,
        .input-one input, select{
            margin: 2px;
            padding: 8px;
        }
    }
</style>