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
                console.log(xhr, status, err);
            }).always(function(xhr, status){
                console.log(xhr, status);
        });
    }

    /* change order of image and offer presentation box depending on screen width - start*/
    function changeOrderOfLaoutElements() {

        const imageToChangePosition = $('#selected_for_school_img1');
        const selectedItem1 = $('.selected-item-1');
        const selectionRowToBeChanged = $('.selection-row').eq(1);

        /*conditions to fulfill*/
        const windowWidthCondition = window.innerWidth < 768;
        const classCondition = selectedItem1.eq(1).hasClass('selected_img');


        if (windowWidthCondition && classCondition) {
            selectedItem1.eq(1).remove();
            selectionRowToBeChanged.prepend(imageToChangePosition);
        } else if (!windowWidthCondition && !classCondition) {
            selectedItem1.eq(0).remove();
            selectionRowToBeChanged.append(imageToChangePosition);
        }
    }

    changeOrderOfLaoutElements();

    $(window).resize(function() {
        changeOrderOfLaoutElements();
    })

    /* change order of image and offer presentation box depending on screen width - stop */

    /* Show offer on click - start */

    function hideElement(nextRow, toggler) {
        nextRow.hide();
        toggler.removeClass('fa-eye-slash').addClass('fa-eye');
    }

    function prepareOffer(row, nextRow, thisToggler, prefix, url) {
        if (nextRow.hasClass('new-row')) {
            nextRow.show();
            thisToggler.removeClass('fa-eye').addClass('fa-eye-slash');
        } else {
            ajaxHandler(url, '', 'GET', showOffer, row, thisToggler, prefix);
        }
    }

    function showOffer(r, row, thisToggler, prefix) {
        let newRow;
        let newRowContent;
        let newRowContentText
        if (prefix === 'table-') {
            newRow = $("<tr>", {class: "new-row"});
            newRowContent = $("<td>", {colspan: "3"});
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


    function getOfferOnClick(mainElement, prefix) {
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
                    prepareOffer(thisRow, thisNextRow, thisToggler, prefix, url)
                } else {
                    prepareOffer(thisRow, thisNextRow, thisToggler, prefix, url)
                }
            }
        });
    }

    getOfferOnClick('table', 'table-');
    getOfferOnClick('.selected_wrapper', 'section-');

    /* Show offer on click - stop */


})