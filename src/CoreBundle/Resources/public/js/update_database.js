
$(document).ready(function(){
    
    $("#options").change(function(){
        
        var tableName = $("#options").val();
        if(tableName == "Products")
            insertProduct();
        else if(tableName == "Categories")
                insertCategory();
             else insertKeypoint();
        $('.error').html("");
    });

    $("#input_picture").click(function(){
        $("#file").click();
    });

    $("#file").change(function(){

        $('#choose_file').attr('class','form-group has-success has-feedback');
        $('#glyph').attr('class','glyphicon glyphicon-ok form-control-feedback');
        $('#input_picture').val( this.files[0].name );
    });

    $("#productsSelector").change(function(){

        $('#category').val( $('option:selected',this).attr('category') );
    });
});

function insertProduct(){

    if( $("#categoriesSelector").children().length==1 ){

        $.ajax({
            type: "POST",
            url: "getCategories"
        }).done(function(respond){

            if(respond.length > 0){
                for(var i=0; i<respond.length; i++){
                    $("#categoriesSelector").append(new Option(respond[i].name, respond[i].id));
                }
            }
        });
    }

    $('#updateCategories').css('display','none');
    $('#updateProducts').css('display','block');
    $('#updateKeypoints').css('display','none');
}

function insertCategory(){

    $('#updateCategories').css('display','block');
    $('#updateProducts').css('display','none');
    $('#updateKeypoints').css('display','none');
}

function insertKeypoint(){

    if( $("#productsSelector").children().length==1 ){

        $.ajax({
            type: "POST",
            url: "getProducts"
        }).done(function(respond){

            if(respond.length > 0){
                for(var i=0; i<respond.length; i++){
                    $("#productsSelector").append('<option value="' + respond[i].id + '" category="' + respond[i].category + '">' + respond[i].name + '</option>');
                }
            }
        });
    }

    $('#updateCategories').css('display','none');
    $('#updateProducts').css('display','none');
    $('#updateKeypoints').css('display','block');
}
