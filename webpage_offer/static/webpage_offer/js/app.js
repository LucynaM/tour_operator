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

    /* Select offer - start */
    function selectOffer() {
        $(".select-drag").draggable({
            cursor: "move",
            revert: "invalid",
            }
        );

        $(".select-drop").droppable({
            drop: function( event, ui ) {
                const newSelectedId = ui.draggable.data('id');
                const newSelectedText = ui.draggable.text();
                ui.draggable.hide();
                const aboutSelected = prepareSelection($(this));
                aboutSelected[0].text(newSelectedText);
                aboutSelected[0].data("id", newSelectedId);

                // prepare ajax
                const url = $(this).data('url')
                const data = {
                    sort: $(this).attr('id').slice(-1),
                    new_id: newSelectedId,
                }
                if (aboutSelected.length == 2) {
                    data["old_id"] = aboutSelected[1]
                }
                console.log(data);
                ajaxHandler(url, data, 'GET', showSelection);
            }
        });
    };


    function prepareSelection(item) {
        if (item.children().length) {
            const aboutSelected = item.children('p');
            const oldElementId = aboutSelected.data('id')
            // revert previous selected element to its original position in list
            $('li[data-id="'+oldElementId+'"]').css({"left": "0px", "top": "0px"}).show()
            return [aboutSelected, oldElementId]
        } else {
            const aboutSelected = $('<p>', {class: "test-dropped"})
            item.append(aboutSelected);
            return [aboutSelected]
        }
    }

    function showSelection(r) {
        console.log(r)
    }

      selectOffer();
    /* Select offer - stop */


});