if (document.getElementById("thumbnail")) {
    document.getElementById("download").style.display = "";
};

var progressStIntr;

function progress() {
    var hostUrl= 'http://localhost:5000/progress';
    $.ajax({
        url: hostUrl,
        type:'POST',
        dataType: 'json',
        //data: JSON.stringify({'parameter1': 'param1', 'parameter2': 'param2' }),
        headers: {
            'Content-Type': 'application/json'
        },
        success: function(data) {
            $('.progress-bar').css('width', data['percent']+'%').attr('aria-valuenow', data['percent']);
            $('.progress-bar-label').text(data['percent']+'%');
            if(data['percent'] == 100){
                clearInterval(progressStIntr)
                alert("Convert Complete");
                document.getElementById("progress-bar-label").innerText = "Complete!";
                $(".progress-bar").removeClass('active');
                document.getElementById("progress-bar-label").innerText = "Complete!";
                document.getElementById("progress-bar-label").innerText = "Complete!";
            }
        },
        error: function(XMLHttpRequest, textStatus, errorThrown) {
            alert("error");
        },   
    });
}

function progressCheck(time){
    progressStIntr = setInterval('progress()', time);
}

$('#convert').on('click', function() {
    alert("Convert Start");
});

progressCheck(1000)

function progressCheck(time){
    progressStIntr = setInterval('progress()', time);
}