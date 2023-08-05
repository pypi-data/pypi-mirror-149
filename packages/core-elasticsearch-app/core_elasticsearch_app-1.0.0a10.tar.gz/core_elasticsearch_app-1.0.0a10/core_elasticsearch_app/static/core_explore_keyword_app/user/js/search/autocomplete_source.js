var getAutocompleteSource = function (request, response){
    $.ajax({
        type: 'GET',
        url: suggestionsURL + "?keyword=" +request.term,
        dataType: 'json',
        success: function (data) {
            response($.map(data, function (item) {
                if (item) {
                    return {
                        label: item,
                        value: item
                    }
                }
            }));
        }
    });
}