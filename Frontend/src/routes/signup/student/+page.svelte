<script>
    import { api } from '$lib/api'; // Import du service API centralisé
    import { classes, schoolName } from '../../../stores/auth';
    import { goto } from '$app/navigation';
    import { onMount } from "svelte";

    // Données du formulaire
    let formData = {
        student_name: '',
        student_lastname: '',
        student_sexe: '',
        student_address: '',
        student_number: '',
        email: '',
        student_birthday_date: '',
        school_type: '',
        selected_level: [],
        selected_classes: [],
        password: '',
        confirm_password: '',
        groups: [],
        user_permissions: []
    };

    // Niveaux scolaires
    let level_classes = {
        Ecole: ['12eme', '11eme', '10eme', '9eme', '8eme', '7eme'],
        College: ['6eme', '5eme', '4eme', '3eme'],
        Lycee: ['2nde', '1ere', 'Term'],
        Universite: ['L1', 'L2', 'L3', 'M1', 'M2']
    };

    // États du formulaire
    let currentStep = 1;
    let errors = {};
    let isLoading = false;

    // Validation des champs
    const validateStep = (step) => {
        errors = {};
        let isValid = true;

        if (step === 1) {
            if (!formData.student_name.match(/^[a-z A-Z]*$/)) {
                errors.student_name = 'Le nom ne doit contenir que des lettres';
                isValid = false;
            }
            if (formData.student_name.length < 4) {
                errors.student_name = 'Le nom est trop court';
                isValid = false;
            }
            // Ajouter les autres validations pour le step 1...
        } else if (step === 2) {
            if (!formData.school_type) {
                errors.school_type = 'Veuillez sélectionner un type';
                isValid = false;
            }
            // Validations step 2...
        } else if (step === 3) {
            if (formData.password.length < 6) {
                errors.password = 'Le mot de passe doit faire au moins 6 caractères';
                isValid = false;
            }
            if (formData.password !== formData.confirm_password) {
                errors.confirm_password = 'Les mots de passe ne correspondent pas';
                isValid = false;
            }
        }

        return isValid;
    };

    // Navigation dans les étapes
    const nextStep = () => {
        if (validateStep(currentStep)) {
            currentStep++;
        }
    };

    const prevStep = () => {
        currentStep--;
    };

    // Gestion des niveaux scolaires
    function toggle_level(level) {
        if (formData.selected_level.includes(level)) {
            formData.selected_level = formData.selected_level.filter(item => item !== level);
        } else {
            formData.selected_level.push(level);
        }
        updateSelectedClasses();
    }

    function updateSelectedClasses() {
        formData.selected_classes = [];
        formData.selected_level.forEach(lev => {
            formData.selected_classes = [...formData.selected_classes, ...level_classes[lev]];
        });
    }

    // Soumission du formulaire
    async function submitForm() {
        if (!validateStep(3)) return;
        
        isLoading = true;
        
        try {
            // Utilisation du service API centralisé
            const response = await api.auth.signup({
                ...formData,
                role: 'STUDENT' // Définition du rôle étudiant
            });
            
            goto('/login');
        } catch (error) {
            console.error("erreur: ", error);
        } finally {
            isLoading = false;
        }
    }

    // Chargement initial
    onMount(async () => {
        try {
            const data = await api.schools.list();
            schoolName.set(data);
        } catch (error) {
            console.error("erreur: ", error);
        }
    });
</script>

<div class="body">
    <div class="container">
        <div class="form">
            <img src="/icons/logo.png" alt="">
            <h1>Créer un compte</h1>
            <p>Inscrivez-vous en tant qu'étudiant</p>
            
            <form on:submit|preventDefault={submitForm}>
                <!-- Étape 1: Informations personnelles -->
                {#if currentStep === 1}
                    <div class="two">
                        <div class="name">
                            <label for="">Nom :</label>
                            <input type="text" placeholder="Entrer votre nom" 
                                   bind:value={formData.student_name}>
                            {#if errors.student_name}
                                <span class="error">{errors.student_name}</span>
                            {/if}
                        </div>
                        
                        <div class="name">
                            <label for="">Prénom :</label>
                            <input type="text" placeholder="Entrer votre prénom" 
                                   bind:value={formData.student_lastname}>
                        </div>
                    </div>

                    <div class="one">
                        <label for="">Sexe :</label>
                        <select bind:value={formData.student_sexe}>
                            <option value="" disabled>Selectionnez votre sexe</option>
                            <option value="Male">Garçon</option>
                            <option value="Female">Fille</option>
                        </select>
                    </div>
                    
                    <div class="one">
                        <label for="">Date de naissance :</label>
                        <input type="date" bind:value={formData.student_birthday_date}>
                    </div>

                    <div class="two">
                        <div class="name">
                            <label for="">Téléphone :</label>
                            <input type="text" placeholder="Votre numéro" 
                                   bind:value={formData.student_number}>
                        </div> 

                        <div class="name">
                            <label for="">Email :</label>
                            <input type="email" placeholder="Votre email" 
                                   bind:value={formData.email}>
                            {#if errors.email}
                                <span class="error">{errors.email}</span>
                            {/if}
                        </div>
                    </div>

                    <div class="one">
                        <button type="button" on:click={nextStep}>Suivant</button>
                    </div>

                <!-- Étape 2: Informations scolaires -->
                {:else if currentStep === 2}
                    <div class="one">
                        <label for="">Établissement :</label>
                        <select>
                            <option value="" disabled>Selectionnez votre établissement</option>
                            {#each $schoolName as school}
                                <option value={school.id}>{school.school_name}</option>
                            {/each}
                        </select>
                    </div>

                    <div class="one">
                        <label>Niveaux :</label>
                        {#each Object.keys(level_classes) as level}
                            <label>
                                <input type="checkbox" 
                                       on:change={() => toggle_level(level)}
                                       checked={formData.selected_level.includes(level)}>
                                {level}
                            </label>
                        {/each}
                    </div>

                    <div class="two">
                        <button type="button" id="back" on:click={prevStep}>Retour</button>
                        <button type="button" on:click={nextStep}>Suivant</button>
                    </div>

                <!-- Étape 3: Mot de passe -->
                {:else}
                    <div class="one">
                        <label for="">Mot de passe :</label>
                        <input type="password" placeholder="Créez un mot de passe" 
                               bind:value={formData.password}>
                        {#if errors.password}
                            <span class="error">{errors.password}</span>
                        {/if}
                    </div>

                    <div class="one">
                        <label for="">Confirmation :</label>
                        <input type="password" placeholder="Confirmez le mot de passe" 
                               bind:value={formData.confirm_password}>
                        {#if errors.confirm_password}
                            <span class="error">{errors.confirm_password}</span>
                        {/if}
                    </div>

                    <div class="two">
                        <button type="button" id="back" on:click={prevStep}>Retour</button>
                        <button type="submit" disabled={isLoading}>
                            {isLoading ? 'En cours...' : 'S\'inscrire'}
                        </button>
                    </div>
                {/if}
            </form>

            <p>Avez-vous déjà un compte ? <a href="/login">Se connecter</a></p>
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