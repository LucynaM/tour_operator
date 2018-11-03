$(document).ready(function(){

    /* Counter of characters - start*/

    function textCounter() {
        $('.counter').on('keyup', function() {
            const label = $('label[for="'+ $(this).attr('id') +'"]');
            const lengthOfThisText = $(this).val().length;
            const endOfText = label.text().indexOf('*') + 1;
            let labelText = label.text().slice(0, endOfText);
            labelText += (' Characters left: ' + (200-lengthOfThisText));
            label.text(labelText)
        })
    }

    textCounter();

    /* Counter of characters - stop*/


    /* Datepicker - start */

    function setDate() {
        const datePicker = $('.datepicker');
        datePicker.datepicker({ dateFormat: 'dd/mm/yy' });
    }

    setDate();

    /* Datepicker - stop */

    /* Redirect after creating pdf - start */

    function redirectOnSuccess() {
        $('#link-with-redirect').on('click', function() {
            setTimeout(function(){
                url = $(this).data('redirect');
                window.location.replace(url);
            }, 5000);
        });
    };
    redirectOnSuccess();

    /* Redirect after creating pdf - stop */

});