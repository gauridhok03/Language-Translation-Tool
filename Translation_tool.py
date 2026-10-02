from flask import Flask, request, jsonify, render_template_string
from deep_translator import GoogleTranslator


app = Flask(__name__)


HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Language Translator</title>


    <style>


*{
    margin:0;
    padding:0;
    box-sizing:border-box;
    font-family:"Poppins",sans-serif;
}


body{
    min-height:100vh;
    display:flex;
    justify-content:center;
    align-items:center;
    padding:30px;


    background:linear-gradient(135deg,#0f1d57,#173b92,#1e5cff);
}


.container{


    width:100%;
    max-width:1050px;


    background:rgba(255,255,255,.08);


    backdrop-filter:blur(18px);


    border:1px solid rgba(255,255,255,.15);


    border-radius:28px;


    padding:35px;


    box-shadow:0 20px 60px rgba(0,0,0,.35);
}


.header{
    text-align:center;
    margin-bottom:30px;
}


.header h1{


    color:#fff;


    font-size:42px;


    font-weight:700;


    letter-spacing:.5px;
}


.subtitle{


    color:#d7e4ff;


    margin-top:8px;


    font-size:15px;
}


.languages{


    display:grid;


    grid-template-columns:1fr auto 1fr;


    gap:18px;


    align-items:end;


    margin-bottom:25px;
}


.select-group{


    display:flex;


    flex-direction:column;


    gap:8px;
}


label{


    color:white;


    font-size:15px;


    font-weight:600;
}


select{


    width:100%;


    padding:14px 18px;


    border:none;


    outline:none;


    border-radius:16px;


    background:rgba(255,255,255,.18);


    color:white;


    font-size:15px;


    cursor:pointer;
}


select option{


    color:black;
}


.swap-button{


    width:60px;


    height:60px;


    border-radius:50%;


    border:none;


    cursor:pointer;


    font-size:22px;


    background:white;


    color:#2555ff;


    transition:.3s;
}


.swap-button:hover{


    transform:rotate(180deg) scale(1.08);
}


.textareas{


    display:grid;


    grid-template-columns:1fr 1fr;


    gap:25px;
}


textarea{


    width:100%;


    min-height:260px;


    resize:none;


    padding:20px;


    border:none;


    outline:none;


    border-radius:22px;


    background:rgba(255,255,255,.12);


    color:white;


    font-size:17px;


    line-height:1.6;
}


textarea::placeholder{


    color:#d6e0ff;
}


textarea[readonly]{


    background:rgba(255,255,255,.15);
}


.toolbar{


    display:flex;


    gap:15px;


    justify-content:center;


    margin-top:25px;


    flex-wrap:wrap;
}


.toolbar button{


    padding:14px 28px;


    border:none;


    border-radius:14px;


    cursor:pointer;


    font-size:16px;


    font-weight:600;


    transition:.3s;
}


.primary{


    background:white;


    color:#2555ff;


    box-shadow:0 8px 20px rgba(255,255,255,.2);
}


.primary:hover{


    background:#dbe7ff;


    transform:translateY(-2px);
}


.secondary{


    background:rgba(255,255,255,.15);


    color:white;
}


.secondary:hover{


    background:rgba(255,255,255,.28);


    transform:translateY(-2px);
}


.status{


    margin-top:18px;


    color:white;


    text-align:center;
}


.footer{


    margin-top:30px;


    color:#d7e4ff;


    text-align:center;
}


@media(max-width:850px){


.languages{


grid-template-columns:1fr;
}


.swap-button{


width:100%;
border-radius:16px;
}


.textareas{


grid-template-columns:1fr;
}


.header h1{


font-size:32px;
}


}


</style>
</head>


<body>


<div class="container">
    <div class="header">
        <div>
            <h1> AI Language Translator</h1>
            <p class="subtitle">Powered by AI • Translate instantly into multiple languages.</p>
        </div>
    </div>


    <div class="section">
        <div class="languages">
            <div class="select-group">
                <label for="source">Source Language</label>
                <select id="source">
                    <option value="en">English</option>
                    <option value="mr">Marathi</option>
                    <option value="hi">Hindi</option>
                    <option value="de">German</option>
                    <option value="fr">French</option>
                    <option value="es">Spanish</option>
                    <option value="ko">Korean</option>
                </select>
            </div>


            <button class="swap-button" type="button" onclick="swapLanguages()" aria-label="Swap languages">⇆</button>


            <div class="select-group">
                <label for="target">Target Language</label>
                <select id="target">
                    <option value="mr">Marathi</option>
                    <option value="hi">Hindi</option>
                    <option value="en">English</option>
                    <option value="de">German</option>
                    <option value="fr">French</option>
                    <option value="es">Spanish</option>
                    <option value="ko">Korean</option>
                </select>
            </div>
        </div>


        <div class="textareas">
            <textarea id="inputText" placeholder="Type or paste text here..." aria-label="Source text"></textarea>
            <textarea id="outputText" placeholder="Translation appears here..." readonly aria-label="Translated text"></textarea>
        </div>


        <div class="toolbar">
            <button class="primary" id="translateButton" type="button" onclick="translateText()">Translate</button>
            <button class="secondary" type="button" onclick="clearText()">Clear</button>
            <button class="secondary" type="button" onclick="copyText()">Copy</button>
            <button class="secondary" type="button" onclick="speakText()">🔊 Speak</button>
        </div>


        <div id="status" class="status"></div>
    </div>


</div>


<script>
    
async function translateText() {


    let text = document.getElementById("inputText").value;
    let source = document.getElementById("source").value;
    let target = document.getElementById("target").value;


    if(text.trim() === ""){
        alert("Enter text first");
        return;
    }


    const response = await fetch("/translate",{
        method:"POST",
        headers:{
            "Content-Type":"application/json"
        },
        body:JSON.stringify({
            text:text,
            source:source,
            target:target
        })
    });


    const data = await response.json();


    document.getElementById("outputText").value =
        data.translated;
}


function copyText(){


    let text =
        document.getElementById("outputText").value;


    navigator.clipboard.writeText(text);


    alert("Copied!");
}


function speakText(){


    let text =
        document.getElementById("outputText").value;


    let speech =
        new SpeechSynthesisUtterance(text);


    speech.lang =
        document.getElementById("target").value;


    speechSynthesis.speak(speech);
}


function clearText(){


    document.getElementById("inputText").value = "";
    document.getElementById("outputText").value = "";
}


function swapLanguages(){


    let source =
        document.getElementById("source");


    let target =
        document.getElementById("target");


    let temp = source.value;


    source.value = target.value;
    target.value = temp;
}



</script>


</body>
</html>
"""



@app.route("/translate", methods=["POST"])
def translate():                             #API ENDPOINT
    data = request.get_json()


    translated = GoogleTranslator(
        source=data["source"],
        target=data["target"]
    ).translate(data["text"])


    return jsonify({"translated": translated})



@app.route("/")
def index():
    return render_template_string(HTML)    



if __name__ == "__main__":
    app.run(debug=True)
