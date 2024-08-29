<script>
    import NavPresence from "../../../../lib/nav/navPresence.svelte";
    import { courses } from "../../../../stores/auth";
    import { onMount } from "svelte";

    export let data;

    let course = null;

    onMount(async () => {
        course = $courses.find(course => course.id == data.id);
        if (course) {
            const endpoint = `http://localhost:8000/school/courseOneAPI/${course.id}/`;
            const response = await fetch(endpoint);
            const data = await response.json();
            courses.set(data);
        }
    });
</script>

<div class="content">
    <NavPresence />
    <div class="content-body">
        <div class="">
            <h1>Enregistrements</h1>
            <h5>Année scolaire : 2023 - 2024</h5>
            {#if course}
                <h5>Date: {course.date}</h5>
                <hr>
                <div class="saveContent">
                    <ul>
                        <li><b>Cours</b>: {course.course}</li>
                        <li><b>Matière</b>: {course.matiere}</li>
                        <li><b>Profésseur</b>: {course.teacher}</li>
                        <li><b>Heure</b>: {course.course_start} <b> à </b> {course.course_end} </li>
                        <li><b>Liste des activités</b>: {course.activities} </li>
                        <li><b>Listes des élèves absents</b>:
                            <ul>
                                {#each course.students_missing as student}
                                    <li>N°{student} : {student}</li>
                                {/each}
                            </ul>
                        </li>
                    </ul>
                </div>
            {/if}
        </div>
    </div>
</div>

<style>
    hr{
        width: 50%;
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
    h5{
        text-align: center;
        font-family: 'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif;
        font-size: 12px;
    }
    .content-body{
        margin-left: 15%;
        margin-right: 15%;
        background: #005358;
        padding: 10px;
        border-radius: 5px;
        border: none;
    }
    .saveContent{
        padding: 20px;
    }
    b{
        margin-left: 10px;
        margin-right: 10px;
        font-size: 18px;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    li{
        font-size: 17px;
        font-family: 'Times New Roman', Times, serif;
        line-height: 30px;
        margin-bottom: 10px;
    }
</style>