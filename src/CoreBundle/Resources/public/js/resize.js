$(document).ready(function() {

    //Input: the file loaded by the user
    //The method writes the user photo 2 times: first in a hidden canvas using the full image size and second in a canvas also seen by the user where the picture is resized
	function readImage(file) {

		if (file.type.match(/image.*/)) {
            //Adds the canvas where the image seen by the user will be displayed
            $(".jcrop-holder").remove();
            $("#centerCanvas").prepend($("<canvas id='canvas'></canvas>"));

            //Style
			document.getElementById("new_Btn").className = "form-group has-success has-feedback";
			document.getElementById("glyph").className = "glyphicon glyphicon-ok form-control-feedback";
			if (document.getElementById("options").value != "mynull")
				document.getElementById("buttonUpload").disabled = false;

			var reader = new FileReader();
			var image = document.createElement("img");

			reader.readAsDataURL(file);  
			reader.onload = function(_file) {
				image.src = _file.target.result;
                //Writes the full sized image in its corresponding canvas and also writes the image in the canvas seen by the user
				image.onload = function() {
                    var w = image.width,
                        h = image.height;
                    var fullCanvas = document.getElementById("fullSizedCanvas");
                    var fullCtx = fullCanvas.getContext("2d");
                    fullCanvas.width = w;
                    fullCanvas.height = h;
                    fullCtx.drawImage(image, 0, 0, w, h);


					var canvas = document.getElementById("canvas");

                    var dimensions = newDimensions(w, h);
                    w = dimensions.width;
                    h = dimensions.height;

					canvas.width = w;
					canvas.height = h;
                    var widthString = "width: " + w + "px; height: " + h + "px";
                    document.getElementById("centerCanvas").setAttribute("style", widthString);

					var ctx = canvas.getContext("2d");
					ctx.drawImage(image, 0, 0, w, h);

					image.onerror= function() {
						alert('Invalid file type: '+ file.type);
					}

                    //Style
                    canvas.style.display = "initial";
                    document.getElementById("main").setAttribute("style", "margin-left: 10%");
                    document.getElementById("centerCanvas").setAttribute("style", "float: right");
                    document.getElementById("centerCanvas").setAttribute("style", "margin-right: 10%");

                    // Crop the image
                    $('#canvas').Jcrop({
                        onChange:   showCoords,
                        onSelect:   showCoords,
                        onRelease:  clearCoords,
                        setSelect:   [ canvas.width/2-canvas.width/4,
                                       canvas.height/2-canvas.height/4,
                                       canvas.width/2+canvas.width/4,
                                       canvas.height/2+canvas.height/4 ]
                    },function(){
                        jcrop_api = this;
                    });

                    //Change background color for the pictures with transparent background
                    $(".jcrop-holder").css("background-color", "transparent");
				}
			}
		}
		else {
            //Style
			document.getElementById("inputSuccess2").value = "The selected file must be a photo!";
			document.getElementById("inputSuccess2").style.color = 'red';
			document.getElementById("new_Btn").className = "form-group has-error has-feedback";
			document.getElementById("glyph").className = "glyphicon glyphicon-remove form-control-feedback";
			document.getElementById("buttonUpload").disabled = true;
		}

	}

    //Photo resize method, keeping the original aspect ratio
    var newDimensions = function(w, h) {
        var MAX_WIDTH = 500;
        var MAX_HEIGHT = 650;

        if (w > h) {
            if (w > MAX_WIDTH) {
                h *= MAX_WIDTH / w;
                w = MAX_WIDTH;
            }
        } else {
            if (w < h) {
                if (h > MAX_HEIGHT) {
                    w *= MAX_HEIGHT / h;
                    h = MAX_HEIGHT;
                }
            } else {
                if (w == h) {
                    w = MAX_WIDTH;
                    h = MAX_WIDTH;
                }
            }
        }
        return {
            width: w,
            height: h
        };
    }

    // Simple event handler, called from onChange and onSelect
    // event handlers, as per the Jcrop invocation above
    function showCoords(c)
    {
        $('#x1').val(c.x);
        $('#y1').val(c.y);
        $('#x2').val(c.x2);
        $('#y2').val(c.y2);
        $('#w').val(c.w);
        $('#h').val(c.h);
    };

    // Simple event handler, called from onChange and onSelect
    // event handlers, as per the Jcrop invocation above
    function clearCoords()
    {
        $('#cropHiddenForm input').val('');
    };

    //Method to print an error message if something crashes when the user tries to upload a photo
    function uploadFailed() {
        var error= document.getElementById("errorMessage");
        error.style.display = "initial";
        error.style.color = "red";
        error.innerHTML = "<br/><br/>Upload failed!";
    }

    //Event triggered whenever the photo uploaded by the user is changed
    //If the browser supports file uploads, the image is sent to a method to be processed (to be written in the corresponding canvases), otherwise it will just alert a message
	$("#choose").change(function(e) {
		if (this.disabled) 
			return alert('File upload not supported!');
		document.getElementById("inputSuccess2").style.color = 'green';
		var F = this.files;
		if (F && F[0])
			for (var i=0; i<F.length; i++) {
				document.getElementById("inputSuccess2").value = F[i].name;
				readImage( F[i] );
			}
	});

    //Event triggered when the "Upload File" button is pressed
    //It calculates where the user actually cropped in the full sized canvas (remember that the user sees a smaller image and he crops on that one), then resize the croped part to desired dimensions (defined in photo resize method)
    //In the end, it sends an ajax containing the image, the category selected by the user and also sets the POST needed by the python scripts
	$("#buttonUpload").click(function(e) {
        var newC = document.getElementById("croppedCanvas");
        var widthRaport = parseFloat(document.getElementById('fullSizedCanvas').width / document.getElementById('canvas').width);
        var heightRaport = parseFloat(document.getElementById('fullSizedCanvas').height / document.getElementById('canvas').height);
        var w = parseInt(document.getElementById('w').value * widthRaport),
            h = parseInt(document.getElementById('h').value * heightRaport);
        var dimensions = newDimensions(w, h);
        w = dimensions.width;
        h = dimensions.height;

        newC.width = w;
        newC.height = h;
        var newCtx=newC.getContext("2d");
        var canvas = document.getElementById("fullSizedCanvas");
        newCtx.drawImage(canvas,
                         document.getElementById('x1').value * widthRaport,
                         document.getElementById('y1').value * heightRaport,
                         document.getElementById('w').value * widthRaport,
                         document.getElementById('h').value * heightRaport,
                         0,
                         0,
                         w,
                         h);

        //Prepare the data whcih is going to be send in the ajax
		var dataURL= newC.toDataURL();
		var selected = document.getElementById("options").value;
        //Test if the data which is going to be send is not null
		if (dataURL != document.getElementById("canvas_blank").toDataURL()) {
            //The actual ajax
			$.ajax({
			    type: "POST",
                url: Routing.generate('ajax'),
			    data: {image: dataURL,
			  	       select: selected}
			}).done(function(respond) {
			    // you will get back a success string, the catergory id, the name of the newly file added to server and its location or "Failed!"
			    console.log(respond);
                //Style and also sets the POST needed by the python scripts
			    if (respond.match("Success!")) {
                    var splitted_respond = respond.split("###!");
                    document.getElementById("selected").value = splitted_respond[1];
                    document.getElementById("picture_name").value = splitted_respond[2];
                    document.getElementById("picture_location").value = splitted_respond[3];
                    document.getElementById("hidden_form").submit();
                }
			    else {
                    uploadFailed();
                }
			});
		}
		else {
            uploadFailed();
        }
        $("#shadow").css("height", $(document).height()).hide();
        $("#shadow").toggle();
        $(".loader").css("display", "initial");
        $(".loader").fadeIn("slow");
	});

    //Style
	$("#new_Btn").mouseover(function(e) {
		var a = document.getElementById("inputSuccess2");
		if (a.value == "Click HERE to upload file...")
			a.style.color = 'red';
	});

    //Style
	$("#new_Btn").mouseout(function(e) {
		var a = document.getElementById("inputSuccess2");
		if (a.value == "Click HERE to upload file...")
			a.style.color = 'black';
	});

    //In order to style an input of file type, we had to hide the actual field and create something else which looks nicer
    //This event binds the actual input field with the text field seen by the user so that when he presses on the text field, he actually presses on the input field
	$('#new_Btn').on("click" , function() {
        $('#choose').click();
    });

    //Style
    $("#inputSuccess2").css("cursor", "pointer");

    //Style
    $("#options").change(function(e) {
		if ((document.getElementById("options").value != "mynull") && 
			(document.getElementById("inputSuccess2").value != "Click HERE to upload file...") &&
			(document.getElementById("inputSuccess2").value != "The selected file must be a photo!"))
			document.getElementById("buttonUpload").disabled = false;
		else
			document.getElementById("buttonUpload").disabled = true;
	});

});
