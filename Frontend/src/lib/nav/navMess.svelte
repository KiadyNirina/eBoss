<div class="navbar">
    <div class="logo">
        <a href="/school/home"><img src="/icons/logo.png" alt=""></a>
    </div>
    <div class="nav">
        <a href="/school/home"><img src="/icons/home.png" alt=""></a>
        <a href="/school/message"><img src="/icons/active/message.png" alt=""></a>
        <a href="/school/list"><img src="/icons/liste.png" alt=""></a>
        <a href="/school/presence"><img src="/icons/classe.png" alt=""></a>
        <a href="/school/registration_data"><img src="/icons/bases_de_données.png" alt=""></a>
        <a href=""><img src="/icons/facture.png" alt=""></a>
        <a href="/school/notes"><img src="/icons/bulletin.png" alt=""></a>
    </div>
    <div class="menu">
        <a href="/school/profile"><img src="/icons/profile.png" alt=""></a>
        <a href="/logout"><img src="/icons/déconnexion.png" alt=""></a>
    </div>
</div>

<style>
    .navbar{
        background: #00848b;
        padding: 7px;
        border-radius: 9px;
        position: fixed;
        width: 100%;
        top: 0;
        left: 0;
        display: flex;
        align-items: center;
        z-index: 100;
    }
    .navbar img{
        height: 25px;
        transition: 0.2s;
    }
    .navbar img:hover{
        height: 30px;
        background: rgba(255, 255, 255, 0.249);
        border-radius: 5px;
    }
    .logo{
        width: 10%;
    }
    .logo img{
        height: 30px;
    }
    .nav{
        width: 80%;
    }
    .nav img{
        margin-left: 2%;
        margin-right: 2%;
    }
    .menu{
        display: flex;
        width: 10%;
        margin-left: auto;
        margin-right: auto;
    }
    .menu a{
        margin-left: auto;
        margin-right: auto;
    }
    @media screen and (max-width : 800px) {
        .logo img, .nav img, .menu img{
            height: 20px;
        }
        .nav img, .menu img{
            margin-left: 7px;
            margin-right: 7px;
        }
        .nav {
            display: flex;
            width: auto;
        }
    }
</style>