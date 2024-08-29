<script>
    import NavMess from "../../../../../lib/nav/navMess.svelte";
</script>

<div class="content">
    <NavMess/>
    <div class="content-body">
        <div class="profile">
            <div class="info">
                <img src="/icons/profile.png" alt="">
                <div class="name">
                    <p>ANDRIANASOLO Helisoa Olivia</p>
                    <p id="classe">Parent de: RAMBELOSON Kiady Mandresy | Classe: 5eme</p>
                </div>
            </div>
            <div class="menu">
                <img src="/icons/menu.png" alt="">
            </div>
        </div>
        <div class="body">
            <div class="sender">
                <img src="/icons/profile.png" alt="">
                <div class="message">
                    <span>26/07/2024 12:30</span>
                    <p>Lorem ipsum, dolor sit amet consectetur adipisicing elit. Quia nisi unde impedit saepe. Incidunt, fuga obcaecati quia nihil dolorum expedita in error, perferendis laborum voluptates sit est, similique blanditiis recusandae aliquid? Expedita eius enim quia! Sed modi molestias sapiente tempora at ullam illo veritatis repellat tempore. Et earum nam culpa.</p>
                </div>
            </div>

            <div class="recipient">
                <img src="/icons/profile.png" alt="">
                <div class="message">
                    <span>26/07/2024 12:30</span>
                    <p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Debitis, expedita.</p>
                </div>
            </div>

            <div class="sender">
                <img src="/icons/profile.png" alt="">
                <div class="message">
                    <span>26/07/2024 12:30</span>
                    <p>Lorem ipsum dolor sit amet.</p>
                </div>
            </div>

            <div class="recipient">
                <img src="/icons/profile.png" alt="">
                <div class="message">
                    <span>26/07/2024 12:30</span>
                    <p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Reprehenderit eaque sit mollitia ipsum velit magnam adipisci minima delectus asperiores in?</p>
                </div>
            </div>
            <div class="recipient">
                <img src="/icons/profile.png" alt="">
                <div class="message">
                    <span>26/07/2024 12:30</span>
                    <p>Lorem, ipsum dolor.</p>
                </div>
            </div>
        </div>
        <div class="input">
            <form action="" method="post">
                <textarea name="" id="" placeholder="Entrer votre message"></textarea>
                <button><img src="/icons/message.png" alt=""></button>
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
        font-size: 12px;
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