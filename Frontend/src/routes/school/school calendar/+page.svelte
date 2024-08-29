<script>
    import NavHome from "../../../lib/nav/navHome.svelte";

</script>

<div class="content">
    <NavHome />
    <div class="body">
        <div class="return">
            <a href="/home"><button>&Lt;</button></a>
        </div>
        <div class="content-body">
            <div class="content-post">
                <div class="button">
                    <a href=""><button><img src="/icons/modifier.png" alt=""></button></a>
                </div>
                <div class="">
                    <h1>Année scolaire : 2023 - 2024</h1>
                    <p><u>Date de rentrée scolaire</u> : </p>
                    <ul>
                        <li>2nde - Tle : </li>
                        <li>6ème - 3ème : </li>
                    </ul>
    
                    <p><u>Les périodes des DS</u> : </p>
                    <ul>
                        <li>1ère Trimestre : <ul>
                            <li>2nde - Tle : </li>
                            <li>6ème - 3ème : </li>
                        </ul></li><br>
                        <li>2ème Trimestre :<ul>
                            <li>2nde - Tle : </li>
                            <li>6ème - 3ème : </li>
                        </ul></li><br>
                        <li>3ème Trimestre : <ul>
                            <li>2nde - Tle : </li>
                            <li>6ème - 3ème : </li>
                        </ul></li>
                    </ul>
    
                    <p><u>Les périodes de vacances</u> (3 périodes réparties sur l'année) :</p>
                    <ul>
                        <li>1ère Trimestre : <ul>
                            <li>2nde - Tle : </li>
                            <li>6ème - 3ème : </li>
                        </ul></li><br>
                        <li>2ème Trimestre :<ul>
                            <li>2nde - Tle : </li>
                            <li>6ème - 3ème : </li>
                        </ul></li><br>
                        <li>3ème Trimestre : <ul>
                            <li>2nde - Tle : </li>
                            <li>6ème - 3ème : </li>
                        </ul></li>
                    </ul>
    
                    <p><u>Les jours fériés</u> : </p>
    
                    <p><u>Date de fin d'année scolaire</u> : </p>
                    <ul>
                        <li>2nde - Tle: </li>
                        <li>6ème - 3ème: </li>
                    </ul>
                </div>
            </div>
        </div>
    </div>
</div>

<style>
    .body{
        padding: 1%;
        padding-top: 50px;
    }
    .return button{
        position: fixed;
        background: #00848b;
        border: none;
        padding: 10px;
        border-radius: 5px;
        color: white;
        font-weight: bold;
        transition: 0.2s;
    }
    .return button:hover{
        cursor: pointer;
        padding: 12px;
    }
    .content-body{
        color: white;
    }
    .content-post{
        background: #005358;
        margin-top: 10px;
        margin-left: 15%;
        margin-right: 15%;
        padding: 2%;
        border-radius: 7px;
    }
    .content-post p{
        font-family: Verdana, Geneva, Tahoma, sans-serif;
    }
    .content-post p, li{
        font-size: 18px;
        word-spacing: 5px;
        line-height: 25px;
    }
    .button{
        position: absolute;
        display: flex;
        right: 5%;
        border: 1px solid rgba(255, 255, 255, 0.501);
        border-radius: 5px;
    }
    .button img{
        height: 40px;
    }
    .button button{
        background: none;
        border: transparent;
        transition: 0.2s;
    }
    .button button:hover{
        cursor: crosshair;
        background: rgba(128, 128, 128, 0.571);
        border-radius: 5px;
    }
    h1{
        font-size: 20px;
        text-align: center;
        padding: 5px;
        border: 1px solid rgba(255, 255, 255, 0.282);
        font-family: Verdana, Geneva, Tahoma, sans-serif;
    }
</style>