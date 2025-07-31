export function getEtablissementFormData(data) {
    return {
        user: {
            email: data.email,
            password: data.password,
            confirm_password: data.confirmPassword,
            first_name: data.nom.split(' ')[0] || '',
            last_name: data.nom.split(' ').slice(1).join(' ') || '',
            telephone: data.telephone,
            user_type: 'etablissement'
        },
        nom: data.nom,
        type_etablissement: data.typeEtablissement,
        adresse: data.adresse
    };
}

export function getProfesseurFormData(data) {
    return {
        user: {
            email: data.email,
            password: data.password,
            confirm_password: data.confirmPassword,
            first_name: data.nom.split(' ')[0] || '',
            last_name: data.nom.split(' ').slice(1).join(' ') || '',
            telephone: data.telephone,
            user_type: 'professeur'
        },
        matiere: data.matiere,
        etablissement: data.etablissement
    };
}

export function getEleveFormData(data) {
    return {
        user: {
            email: data.email,
            password: data.password,
            confirm_password: data.confirmPassword,
            first_name: data.nom.split(' ')[0] || '',
            last_name: data.nom.split(' ').slice(1).join(' ') || '',
            telephone: data.telephone,
            user_type: 'eleve'
        },
        classe: data.classe,
        etablissement: data.etablissement
    };
}

export function getParentFormData(data) {
    return {
        user: {
            email: data.email,
            password: data.password,
            confirm_password: data.confirmPassword,
            first_name: data.nom.split(' ')[0] || '',
            last_name: data.nom.split(' ').slice(1).join(' ') || '',
            telephone: data.telephone,
            user_type: 'parent'
        },
        eleve: data.eleve
    };
}