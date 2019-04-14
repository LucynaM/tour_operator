$(document).ready(function() {

    function ajaxHandler(url, data, type, callback, ...others) {
        $.ajax({
                url: url,
                data: data,
                type: type,
                dataType: 'json'
            }).done(function(result) {
                callback(result, ...others);
            }).fail(function(xhr, status, err){
//                console.log(xhr, status, err);
            }).always(function(xhr, status){
//                console.log(xhr, status);
        });
    };


    /* Show offer on click - start*/

    const rowIndexes = [];
    $('.selection-row').each(function(index) {
        rowIndexes[index] = $(this).offset().top;
    })

    function slideTo(row) {
        const rowIndex = $('.selection-row').index(row);
        if (window.innerWidth > 992) {
            $('html, body').animate({
                scrollTop: rowIndexes[rowIndex],
            }, 300);
        };
    }

    function hideElement(nextRow, toggler, callback, ...others) {
        nextRow.slideUp()
        toggler.removeClass('open').addClass('closed');
        toggler.children().eq(0).removeClass('fa-caret-up').addClass('fa-caret-down');
        typeof callback === 'function' && callback(...others);
    };

    function prepareOffer(row, nextRow, thisToggler, url) {
        if (nextRow.hasClass('new-row')) {
            slideTo(row);
            nextRow.slideDown();
            thisToggler.removeClass('closed').addClass('open');
            thisToggler.children().eq(0).removeClass('fa-caret-down').addClass('fa-caret-up');
        } else {
            ajaxHandler(url, '', 'GET', showOffer, row, thisToggler);
        }
    };

    function showOffer(r, row, thisToggler) {
        let newRow;
        let newRowContent;
        let newRowContentText;
        if (row.prop('tagName') === 'TR') {
            const cellNumber = "" + row.children().length;
            newRow = $("<tr>", {class: "new-row"});
            newRowContent = $("<td>", {colspan: cellNumber});
            newRowContentText = '<p><strong>' + r.short_descr + '</strong></p>' +  r.schedule;
        } else {
            newRow = $("<div>", {class: "new-row"});
            newRowContent = $("<p>");
            newRowContentText = r.schedule;
        }

        row.after(newRow);
        thisToggler.removeClass('closed').addClass('open');
        thisToggler.children().eq(0).removeClass('fa-caret-down').addClass('fa-caret-up');
        newRow.append(newRowContent);
        newRowContent.html(newRowContentText);
        slideTo(row);
        newRow.slideDown();

    };


    function getOfferOnClick(mainElement) {
        $(mainElement).on('click touch', '.offer-details', function(e) {
            e.preventDefault();

            const thisToggler = $(this);
            const thisRow = $(this).closest('.closestElement');
            const thisNextRow = thisRow.next();

            if (thisToggler.hasClass('open')){
                hideElement(thisNextRow, thisToggler);
            } else {

                const anySwitchedToggler = $(mainElement + ' .open');
                console.log(anySwitchedToggler);
                const anySwitchedRow = anySwitchedToggler.closest('.closestElement').next();
                const url = $(this).data('url');
                if (anySwitchedToggler.length > 0) {
                    console.log("działam w ifie");
                    hideElement(anySwitchedRow, anySwitchedToggler, prepareOffer, thisRow, thisNextRow, thisToggler, url);
                } else {
                    prepareOffer(thisRow, thisNextRow, thisToggler, url);
                }
            }

        });
    };

    getOfferOnClick('table');
    getOfferOnClick('.selected_wrapper');

    /* Show offer on click - stop */

    /* Show holiday - start */

    $('#holiday .holiday-details>a').on('click touch', function(e){
        e.preventDefault();
        const hashValue = $(this).attr('href');

        $(hashValue).data('loaded', !($(hashValue).data('loaded')));
        if ($(hashValue).data('loaded')) {
            $('html, body').animate({
                scrollTop: $(this).offset().top
            }, 800);
        };
        $(hashValue).slideToggle();
        ($(hashValue).data('loaded')) ? $(this).text("Ukryj") : $(this).text("Szczegóły");
    })

    /* Show holiday - stop */

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
                const draggableId = ui.draggable.data('id');
                const draggableText = ui.draggable.html();

                // prepare data needed for ajax function
                const data = {}
                const url = $(this).data('url');

                if ($(this).hasClass('select-container')) {
                    // remove list element that has been dropped
                    ui.draggable.remove();
                    // create p element in order to contain info about selection and retrieve id of the element that has been deselected
                    const aboutSelected = checkIfSelection($(this));
                    // fill p element with information retrieved from list element that has been dropped
                    aboutSelected[0].html(draggableText);
                    aboutSelected[0].data("id", draggableId);
                    aboutSelected[0].data("sort", $(this).data('sort'));
                    aboutSelected[0].addClass('select-drag ui-widget-content');

                    data['sort'] = $(this).data('sort');
                    data['new_id'] = draggableId;

                    if (aboutSelected.length == 2) {
                        data["old_id"] = aboutSelected[1];
                    }
                } else {
                    data['sort'] = ui.draggable.data('sort');
                    data['old_id'] = draggableId;
                    // remove list element that has been dropped
                    ui.draggable.remove();
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


    function createList(r) {
        /*  create updated list of offer after ajax */
        let recommendation = false;
        let result_length = r.length;
        if (r.slice(-1) == 'recommendation') {
            recommendation = true;
            result_length --;
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


            if (recommendation) {
                const category = renameCategory(r[i].category);
                newListElement.html(category + ': <strong>'+ r[i].title + '</strong> - ' + r[i].duration_in_days );
            } else {
                newListElement.html('<strong>'+ r[i].title + '</strong> - ' + r[i].duration_in_days)
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
            case 'for_school':
                category = 'oferta dla szkół';
                break;
            case 'for_work':
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

   /* Change status of participant of a tour - start */

    function seeIfOK(r) {
        console.log(r);
    };

    function changeStatus() {
        $('select[name="status"]').on('change', function() {
            const url = $(this).data('url');
            const status = $(this).val();
            data = {
                status: status,
            };
            ajaxHandler(url, data, 'GET', seeIfOK);
        });
    };

    changeStatus();

    /* Change status of participant of a tour - stop */


    /* autocomplete - start */

    function processDirections(r, element) {
        element.autocomplete({source: r.directions});
    }

    function searchAutocomplete() {
        const searchForm = $('[type="search"]');
        searchForm.on('keyup', function() {
            const url = searchForm.data('url');
            ajaxHandler(url, '', 'GET', processDirections, searchForm);
        });
    };


    searchAutocomplete();

    function processData (r, element) {
        element.autocomplete({
            minLength: 0,
            source: function(request, response) {
                if (element.attr('id') == 'id_last_name') {
                    response(r.names)
                } else if (element.attr('id') == 'id_phone') {
                    r.new_phones = [];
                    for (let i=0; i<r.phones.length; i++) {
                        r.new_phones[i] = "" + r.phones[i];
                    };
                    response(r.new_phones);
                } else if (element.attr('id') == 'id_date_of_birth') {
                    response(r.dates_of_birth);
                };
            },
        });
    };


    function getParticipantData(element) {
        const nameField = $('#id_last_name');
        nameField.on('blur', function() {
            const firstName = $('#id_first_name').val();
            const lastName = $('#id_last_name').val();
            const data = {
                firstName: firstName,
                lastName: lastName,
            };
            /* get phones of people with given first and last name*/
            element.on('focus', function() {
                url = $('#participant_form').data('url');
                ajaxHandler(url, data, 'GET', processData, element);
            });
        });
    };

    function participantDataAutocomplete() {
        const lastName = $('#id_last_name');
        lastName.on('keyup', function() {
            url = $('#participant_form').data('url');
            ajaxHandler(url, '', 'GET', processData, lastName);
        });
    };


    function participantPhoneAutocomplete() {
        const phoneField = $('#id_phone');
        getParticipantData(phoneField);
    };

    function participantBirthAutocomplete() {
        const birthField = $('#id_date_of_birth');
        getParticipantData(birthField);
    };


    participantDataAutocomplete();
    participantPhoneAutocomplete();

    /* autocomplete -stop */


    /* smooth scrolling - start */
    function smoothScrolling() {
        $(".navbar a, .offer_title a, .full-offer a, aside a").on('click', function(event) {

            // Make sure this.hash has a value before overriding default behavior
            if (this.hash !== "") {
                // Prevent default anchor click behavior
                event.preventDefault();

                // Store hash
                var hash = this.hash;

                // Using jQuery's animate() method to add smooth page scroll
                // The optional number (800) specifies the number of milliseconds it takes to scroll to the specified area
                $('html, body').animate({
                    scrollTop: $(hash).offset().top
                }, 800);
            } // End if
        });
    }
    smoothScrolling();
    /* smooth scrolling - stop */

    /*scrollReveal - start*/
    if (window.innerWidth > 768) {
        window.sr = ScrollReveal({ reset: true }).reveal('.scroll', { duration: 500 });
    }
    /*scrollReveal - stop*/

    /*fix viewport bugs for safri and IOS - start*/

    window.viewportUnitsBuggyfill.init();

    /* fix viewport bugs for safri and IOS - stop */

});