<script>
    import NavMess from "../../../../../lib/nav/navMess.svelte";
    import { onMount, afterUpdate } from "svelte";
    import { students, userProfile } from "../../../../../stores/auth";

    export let data;

    let socket;
    let message = '';
    let messages = []; // Stockage des messages reçus
    let recipientId;  // ID de l'utilisateur cible
    let user;
    let student = null;

    // Abonnement au store userProfile
    $: userProfile.subscribe(value => {
        user = value;
    });

    student = $students.find(student => student.id == data.id);

    // Récupérer les informations de l'étudiant
    onMount(async () => {
        if (student) {
            const endpoint = `http://127.0.0.1:8000/school/student/${student.id}/`;
            const response = await fetch(endpoint);
            const studentData = await response.json();
            students.set(studentData); // Mettre à jour le store avec les nouvelles données
        }

        socket = new WebSocket(`ws://${window.location.host}/ws/chat/`);

        socket.onmessage = function(event) {
            const data = JSON.parse(event.data);
            console.log('Data:', data)
            // messages = [...messages, {
            //     sender: data.sender,
            //     message: data.message,
            //     timestamp: data.timestamp
            // }];
        };

        socket.onopen = function() {
            console.log('WebSocket connected');
        };

        socket.onclose = function() {
            console.log('WebSocket disconnected');
        };
    });

    function sendMessage() {
        if (message.trim()) {
            socket.send(JSON.stringify({
                'message': message,
                /*'sender_id': user.id,
                'recipient_id': student.id*/
            }));
            message = '';
        }
    }

</script>

<div class="content">
    <NavMess />
    <div class="content-body">
        <div class="profile">
            {#if student}
                <div class="info">
                    <img src="{student.student_picture}" alt="">
                    <div class="name">
                        <p>{student.student_name} {student.student_lastname}</p>
                        <p id="classe">classe : {student.student_class}</p>
                    </div>
                </div>
            {/if}
            <div class="menu">
                <img src="/icons/menu.png" alt="">
            </div>
        </div>

        <div class="body">
            {#each messages as mess}
                <div class="{mess.sender === user.username ? 'sender' : 'recipient'}">
                    <img src="/img/picture.png" alt="">
                    <div class="message">
                        <span>26/07/2024 12:30</span>
                        <p>sender: {mess.sender}, {mess.content}</p>
                    </div>
                </div>
            {/each}
        </div>
        
        <div class="input">
            <form action="" on:submit={sendMessage}>
                <textarea bind:value={message} placeholder="Entrer votre message"></textarea>
                <button type="submit"><img src="/icons/message.png" alt=""></button>
            </form>
        </div>
    </div>
</div>

<style>
    .content{
        padding: 1%;
        color: white;
        padding-top: 50px;
        font-size: 20px;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .content-body{
        margin-left: 15%;
        margin-right: 15%;
        background: #005358;
        padding: 10px;
        border-radius: 5px;
    }
    .body{
        padding: 80px 10px;
        padding-bottom: 50px;
    }
    .profile{
        top: 50px;
        display: flex;
        align-items: center;
        background-color: #003c3f;
        padding: 5px;
        position: fixed;
        width: 67.9%;
        left: 15.7%;
    }
    .info{
        display: flex;
        align-items: center;
    }
    .info img{
        height: 50px;
        border-radius: 100%;
    }
    .menu{
        display: flex;
        align-items: center;
        margin-left: auto;
    }
    .name{
        line-height: 10px;
        margin-left: 10px;
    }
    .name p{
        font-weight: bold;
    }
    #classe{
        font-size: 15px;
        font-weight: 400;
    }
    .sender{
        display: flex;
        align-items: center;
        width: 50%;
        margin-top: 5px;
    }
    .message{
        border: 1px solid rgba(255, 255, 255, 0.713);
        border-radius: 10px;
        padding: 10px;
        margin-left: 5px;
    }
    .message span{
        font-size: 11px;
    }
    .message p{
        font-size: 14px;
    }
    .sender img, .recipient img{
        height: 30px;
        border: 1px solid white;
        border-radius: 100%;
    }
    .recipient{
        display: flex;
        align-items: center;
        width: 50%;
        margin-left: auto;
        margin-top: 5px;
    }
    .recipient .message{
        border: none;
        color: #002c2e;
        background-color: rgba(255, 255, 255, 0.581);
    }
    .input{
        position: fixed;
        background-color: #003c3f;
        bottom: 0px;
        width: 67.9%;
        left: 15.7%;
        padding: 5px;
    }
    form{
        display: flex;
        align-items: center;
    }
    .input img{
        height: 40px;
    }
    .input button{
        margin: 5px;   
        background: none;
        padding: 0;
        border: none;
    }
    .input textarea{
        width: 100%;
        border-radius: 50px;
        padding: 5px;
        background: rgba(255, 255, 255, 0.581);
        color: #002c2e;
        border: none;
        margin: 5px; 
    }
    @media screen and (max-width: 800px) {
        .profile {
            left: 0;
            width: 100%;
            top: 35px;
        }
        .name{
            line-height: 5px;
        }
        .name p{
            font-size: 12px;
        }
        .menu img{
            height: 30px;
        }
        .content-body{
            margin-left: 0;
            margin-right: 0;
        }
        .body{
            padding: 35px 0;
        }
        .sender{
            width: 70%;
        }
        .message p{
            font-size: 11px;
        }
        .recipient{
            width: 70%;
        }
        .message span{
            font-size: 9px;
        }
    }
</style>