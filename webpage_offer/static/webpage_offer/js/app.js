$(document).ready(function(){

    /* Show offer on click - start */
    function ajaxHandler(url, data, type, callback) {
        $.ajax({
                url: url,
                data: data,
                type: type,
                dataType: 'json'
            }).done(function(result) {
                callback(result)
            }).fail(function(xhr, status, err){
                console.log(xhr, status, err);
            }).always(function(xhr, status){
                console.log(xhr, status);
        });
    }

    function showOffer(r) {
        const row = $("#"+ r.id);
        const nextRow = row.next();
        if (nextRow.hasClass('new-row')) {
            nextRow.toggle();
        } else {
            const newRow = $("<tr>", {class: "new-row"});
            const newCell = $("<td>", {colspan: "4"});
            const textOfCell = r.short_descr + '<br>' +  r.schedule;
            row.after(newRow);
            newRow.append(newCell);
            newCell.html(textOfCell);
        }
    }


    function getOfferOnClick() {
        $('table').on('click', '.offer-details', function(e) {
            e.preventDefault();
            const url = $(this).data('url');
            ajaxHandler(url, '', 'GET', showOffer);
        });
    }

    getOfferOnClick()

    /* Show offer on click - stop */

});