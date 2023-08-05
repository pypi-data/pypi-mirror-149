var checkTemplate = function(event){
    var $btn = $(event.target).closest("button");
    var check_url = $btn.attr("data-url");

     $.ajax({
        url: check_url,
        type : "GET",
        success: function(data){
            alert(data);
        },
        error: function(data){
            console.log(data);
        }
     });
};


var indexData = function(event){
    var $btn = $(event.target).closest("button");
    var index_url = $btn.attr("data-url");

     $.ajax({
        url: index_url,
        type : "GET",
        success: function(data){
            alert(data);
        },
        error: function(data){
            console.log(data);
        }
     });
};

$('.btn-check').on('click', checkTemplate);
$('.btn-index').on('click', indexData);
