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
    function makeDraggable() {
     $(".select-drag").draggable({
            cursor: "move",
            revert: "invalid",
            }
        );
    }

    function selectOffer() {
        makeDraggable()
        $(".select-drop").droppable({
            drop: function( event, ui ) {
                const newSelectedId = ui.draggable.data('id');
                const newSelectedText = ui.draggable.text();
                // remove list element
                ui.draggable.remove();
                // get p into selection placeholder
                const aboutSelected = prepareSelection($(this));
                // fill selection placeholder with content from list element
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
                ajaxHandler(url, data, 'GET', createList);
            }
        });
    };


    function prepareSelection(item) {
        if (item.children().length) {
            const aboutSelected = item.children('p');
            const oldElementId = aboutSelected.data('id')
            return [aboutSelected, oldElementId]
        } else {
            const aboutSelected = $('<p>', {class: "test-dropped"})
            item.append(aboutSelected);
            return [aboutSelected]
        }
    }

    function createList(r) {
        const list = $('ul');

        list.children().each(function(index, element) {
                element.remove();
            }
        )
        for(let i = 0; i < r.length; i++) {
            let newListElement = $('<li>');
            list.append(newListElement);
            newListElement.data('id', r[i].id).addClass('select-drag ui-widget-content ui-draggable ui-draggable-handle').css('position', 'relative');
            let dayMarker = (r[i] == '1')? 'dzień' : 'dni';
            newListElement.text(r[i].title + ' - ' + r[i].duration_in_days + ' ' + dayMarker)
        }
        // initilize droppable after ajax
        makeDraggable()

    }

      selectOffer();
    /* Select offer - stop */


});