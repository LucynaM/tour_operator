$(document).ready(function(){

    function ajaxHandler(url, data, type, callback, ...others) {
        $.ajax({
                url: url,
                data: data,
                type: type,
                dataType: 'json'
            }).done(function(result) {
                callback(result, ...others);
            }).fail(function(xhr, status, err){
                console.log(xhr, status, err);
            }).always(function(xhr, status){
                console.log(xhr, status);
        });
    }

    /* Show offer on click - start */

    function hideElement(nextRow, toggler) {
        nextRow.hide();
        toggler.removeClass('fa-eye-slash').addClass('fa-eye');
    }

    function prepareOffer(row, nextRow, thisToggler, url) {
        if (nextRow.hasClass('new-row')) {
            nextRow.show();
            thisToggler.removeClass('fa-eye').addClass('fa-eye-slash');
        } else {
            ajaxHandler(url, '', 'GET', showOffer, row, thisToggler);
        }
    }

    function showOffer(r, row, thisToggler) {
        let newRow;
        let newRowContent;
        let newRowContentText
        if (row.prop('tagName') === 'TR') {
            newRow = $("<tr>", {class: "new-row"});
            newRowContent = $("<td>", {colspan: "4"});
            newRowContentText = r.short_descr + '<br>' +  r.schedule;
        } else {
            newRow = $("<div>", {class: "new-row"});
            newRowContent = $("<p>");
            newRowContentText = r.schedule;
        }
        row.after(newRow);
        thisToggler.removeClass('fa-eye').addClass('fa-eye-slash');
        newRow.append(newRowContent);
        newRowContent.html(newRowContentText);

    }


    function getOfferOnClick(mainElement) {
        $(mainElement).on('click', '.offer-details', function(e) {
            e.preventDefault();

            const thisToggler = $(this);
            const thisRow = $(this).closest('.closestElement');
            const thisNextRow = thisRow.next();

            if (thisToggler.hasClass('fa-eye-slash')){
                hideElement(thisNextRow, thisToggler);
            } else {
                const anySwitchedToggler = $(mainElement + ' .fa-eye-slash');
                const anySwitchedRow = anySwitchedToggler.closest('.closestElement').next();
                const url = $(this).data('url');
                if (anySwitchedToggler) {
                    hideElement(anySwitchedRow, anySwitchedToggler);
                    prepareOffer(thisRow, thisNextRow, thisToggler, url)
                } else {
                    prepareOffer(thisRow, thisNextRow, thisToggler, url)
                }
            }
        });
    }

    getOfferOnClick('table');

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
        // initilize draggable
        makeDraggable();
        // initilize droppable
        $(".select-drop").droppable({
            drop: function( event, ui ) {
                // retrieve id and content from list element that has been dropped
                const newSelectedId = ui.draggable.data('id');
                const newSelectedText = ui.draggable.html();
                // remove list element that has been dropped
                ui.draggable.remove();
                // create p element in order to contain info about selection and retrieve id of the element that has been deselected
                const aboutSelected = checkIfSelection($(this));
                // fill p element with information retrieved from list element that has been dropped
                aboutSelected[0].html(newSelectedText);
                aboutSelected[0].data("id", newSelectedId);

                // prepare data needed for ajax function
                const url = $(this).data('url');

                const data = {
                    sort: getSort($(this)),
                    new_id: newSelectedId,
                }
                if (aboutSelected.length == 2) {
                    data["old_id"] = aboutSelected[1];
                }

                ajaxHandler(url, data, 'GET', createList);
            }
        });
    };


    function checkIfSelection(item) {
        // check if droppable already contains a p element
        if (item.children().length) {
            // if so, return p element and id of former selection
            const aboutSelected = item.children('p');
            const oldElementId = aboutSelected.data('id');
            return [aboutSelected, oldElementId]
        } else {
            // if no, create p element and return it
            const aboutSelected = $('<p>');
            item.append(aboutSelected);
            return [aboutSelected]
        }
    }

    function getSort(item) {
        /* retrieve information about sort of droppable element */
        const startCut = parseInt(item.attr('class').indexOf('sort'), 10) + 4;
        return item.attr('class').slice(startCut, startCut+1);

    }

    function createList(r) {
        /*  create updated list of offer after ajax */
        let recommendation = false;
        let result_length = r.length;
        if (r.slice(-1) == 'recommendation') {
            recommendation = true;
            result_length --
            }

        const list = chooseList(r, recommendation);
        list.children().each(function(index, element) {
                element.remove();
            }
        )
        for(let i = 0; i < result_length; i++) {
            const newListElement = $('<li>');
            list.append(newListElement);
            newListElement.data('id', r[i].id)
                .addClass('select-drag ui-widget-content')
                .css('position', 'relative');

            const dayMarker = (r[i] == '1')? 'dzień' : 'dni';

            if (recommendation) {
                const category = renameCategory(r[i].category);
                newListElement.html(category + ': <strong>'+ r[i].title + '</strong> - ' + r[i].duration_in_days + ' ' + dayMarker);
            } else {
                newListElement.html('<strong>'+ r[i].title + '</strong> - ' + r[i].duration_in_days + ' ' + dayMarker)
            }
        }
        // initilize draggable after ajax
        makeDraggable();
    }

    function chooseList(r, flag) {
        return flag ? $('#recommend ul') : $('#'+r[0].category +' ul');
    }

    function renameCategory(category) {
        switch (category) {
            case 'school_trip':
                category = 'oferta dla szkół';
                break;
            case 'work_trip':
                category = 'oferta dla firm';
                break;
            case 'pilgrimage':
                category = 'pielgrzymka';
                break;
            default:
                console.log("Nie ma takiej kategorii");
        }
        return category;
    }

    selectOffer();

    /* Select offer - stop */


});