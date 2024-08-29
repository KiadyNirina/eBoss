<script>
    import { onMount } from "svelte";
    import { classes, students } from "../../../../../stores/auth";
    import { createEventDispatcher } from "svelte";
    import NaList from "../../../../../lib/nav/naList.svelte";
    import { userProfile } from "../../../../../stores/auth";

    let user

    $: userProfile.subscribe(value => user = value);

    let name = '';
    let lastname = '';
    let class_degree = '';
    let sexe = '';
    let birthday_date = '';
    let number = '';
    let emailStudent = '';
    let address = '';
    let register_date = '';
    let student_register_number = '';
    let student_picture = null;
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
    let registerNumberFieldError = '';
    let passwordFieldError = '';
    let confirm_passwordFieldError = ''


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

    const isValidRegisterNumber = (student_register_number) => {
        const inputValue = student_register_number.target.value;
        const regex = /^[0-9]*$/;
        if(!regex.test(inputValue)){
            registerNumberFieldError = 'Le numéro d\'inscription n\'est pas correcte';
        } else {
            registerNumberFieldError = '';
        }
    }

    const isValidPassword = (password) => {
        const inputValue = password.target.value;
        if(inputValue.length < 8) {
            passwordFieldError = 'Le mot de passe est trop court';
        } else {
            passwordFieldError = '';
        }
    }

    const isValidConfirmPassword = (confirm_password) => {
        const inputValue = confirm_password.target.value;
        if(inputValue != password) {
            confirm_passwordFieldError = 'Les 2 mots de passes ne sont pas identique';
        } else {
            confirm_passwordFieldError = '';
        }
    }

    let isDisabled = true;

    $: isDisabled = !(name && lastname && birthday_date && address && number && register_date && student_register_number && password && confirm_password) || nameFieldError || lastnameFieldError || birthdayFieldError || addressFieldError || numberFieldError || registerFieldError || registerNumberFieldError || passwordFieldError || confirm_passwordFieldError;

    /*onMount( async () => {
        const response = await fetch("http://localhost:8000/school/schoolClasses/");
        const data = await response.json();
        classes.set(data)
    } )*/

    async function handleSubmit() {

        const formData = new FormData();
            formData.append('password', password);
            formData.append('confirm_password', confirm_password);
            formData.append('email', emailStudent);
            formData.append('username', lastname);
            formData.append('school_name', user.school_name);
            formData.append('school_address', user.school_address);
            formData.append('school_number', user.school_number);
            formData.append('school_type', user.school_type);
            formData.append('school_level', JSON.stringify(user.school_level));
            formData.append('school_classes', JSON.stringify(user.school_classes));
            formData.append('student_name', name);
            formData.append('student_lastname', lastname);
            formData.append('student_sexe', sexe);
            formData.append('student_address', address);
            formData.append('student_class', class_degree);
            formData.append('student_number', number);
            formData.append('student_birthday_date', birthday_date);
            formData.append('register_date', register_date);
            formData.append('student_register_number', student_register_number);
            formData.append('student_picture', student_picture ? student_picture.files[0] : null);
            formData.append('role', 'student');
            //formData.append('groups', JSON.stringify([]));
            //formData.append('user_permissions', JSON.stringify([]));

        try{
            const endpoint = 'http://127.0.0.1:8000/school/schoolRegistration/';
            const response = await fetch(endpoint, {
                method: 'POST',
                body: formData,
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
            <h1>Ajouter un(e) élève </h1>

            {#if SuccessMessage}
                <div class="success">
                    <p>Elève ajouté(e) avec succès.</p>
                </div>
            {:else if ErrorMessage}
                <div class="error">
                    <p>Erreur lors de l'ajout de l'élève.</p>
                </div>
            {/if}

            <form on:submit|preventDefault={handleSubmit}>
                <label for="">Nom</label>
                <div class="input">
                    <input type="text" name="" placeholder="Nom de l'élève" bind:value={name} on:input={isValidName}>
                    {#if nameFieldError}
                        <span class="smallError">{nameFieldError}</span>
                    {/if}
                    
                    <input type="text" name="" placeholder="Prénom de l'élève" bind:value={lastname} on:input={isValidLastname}>
                    {#if lastnameFieldError}
                        <span class="smallError">{lastnameFieldError}</span>
                    {/if}

                    <select name="" id="" bind:value={class_degree} on:input={isValidClass}>
                            <option value="" disabled>Selectionnez votre classe</option>
                        {#if user}
                        {#each user.school_classes as classe}
                            <option value="{classe}">{ classe }</option> 
                        {/each}
                        {/if}
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
                </div>

                <div class="input-one">
                    <label for="">Séléctionnez votre sexe :</label>
                        <select name="" id="" bind:value={sexe}>
                            <option value="" disabled>Selectionnez le sexe de l'élève</option>
                            <option value="Male">Garçon</option>
                            <option value="Femelle">Fille</option>
                        </select>
                    {#if genderFieldError}
                        <span class="smallError">{genderFieldError}</span>
                    {/if}
                </div><br>

                <label for="">Numéro mobile et email</label>
                <div class="input">
                    <input type="text" placeholder="Numéro de mobile" on:input={isValidNumber} bind:value={number}><br>
                    {#if numberFieldError}
                        <span class="smallError">{numberFieldError}</span>
                    {/if}

                    <input type="text" name="" id="" placeholder="Email" bind:value={emailStudent}>
                </div>

                <label for="">Date, numéro d'inscription et Photo d'identité</label>
                <div class="input">
                    <input type="date" name="" bind:value={register_date} on:change={isValidRegister}>
                    {#if registerFieldError}
                        <span class="smallError">{registerFieldError}</span>
                    {/if}

                    <input type="text" name="" id="" placeholder="Entrer le numéro d'inscription de l'élève" bind:value={student_register_number} on:input={isValidRegisterNumber}>
                    {#if registerNumberFieldError}
                        <span class="smallError">{registerNumberFieldError}</span>
                    {/if}

                    <input type="file" name="" bind:this={student_picture} accept="image/*">
                </div>

                <label for="">Mot de passe</label>
                <div class="input">
                    <input type="password" name="" id="" placeholder="Mot de passe" bind:value={password} on:input={isValidPassword}>
                    {#if passwordFieldError}
                        <span class="smallError">{passwordFieldError}</span>
                    {/if}

                    <input type="password" name="" id="" placeholder="Confirmer mot de passe" bind:value={confirm_password} on:input={isValidConfirmPassword}>
                    {#if confirm_passwordFieldError}
                        <span class="smallError">{confirm_passwordFieldError}</span>
                    {/if}
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