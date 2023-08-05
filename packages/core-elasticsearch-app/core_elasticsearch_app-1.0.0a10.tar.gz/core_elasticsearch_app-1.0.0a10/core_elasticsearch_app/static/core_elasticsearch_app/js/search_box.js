var defer_autocomplete = function(){
    $( ".es_search_box_input" ).autocomplete({
      source: function( request, response ) {
        $.ajax( {
          url: "/elasticsearch/rest/document/suggest?keywords="+request.term.split(/[ ,]+/).join(','),
          success: function( data ) {
            response($.map(data.slice(0, 5), function (item) {
                    return {
                        label: highlight(item, "title"),
                        value: item["_source"]["title"],
                        description: highlight(item, "description"),
                        id: item["_source"]["data_id"],
                    };
                }));
          }
        } );
      },
      minLength: 2,
      select: function( event, ui ) {
        console.log( "Selected: " + ui.item.value + " aka " + ui.item.id );
        window.location="/data?id=" + ui.item.id;
      },
       create: function() {
        $(this).data('ui-autocomplete')._renderItem= function( ul, item ) {
            return $( "<li>" )
            .append( "<div class='es_item'><div class='es_item_title'>" + item.label + "</div><div class='es_item_description'>" + item.description + "</div></div>" )
            .appendTo( ul );
          };
       }
    } );

    $( function() {
        $( ".es_search_icon" ).on( "click", function() {
            $( ".es_search_box_input" ).removeClass("hidden");
      } );
      });
};


// Waiting JQuery
onjQueryReady(defer_autocomplete);

var highlight = function(item, field){
    if (item["highlight"][field]){
        return item["highlight"][field];
    }
    if (item["_source"][field]){
        return item["_source"][field].substring(0, 100);
    }
    return ""
}


