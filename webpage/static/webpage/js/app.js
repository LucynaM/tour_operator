$(document).ready(function() {

    /* change order of image and offer presentation box depending on screen width - start*/
    function changeOrderOfLaoutElements() {

        const imageToChangePosition = $('.img1');
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
    };

    changeOrderOfLaoutElements();

    $(window).resize(function() {
        changeOrderOfLaoutElements();
    });

    /* change order of image and offer presentation box depending on screen width - stop */

    /* calculate height of text box in offer selection - start */

    function setHeightOfText() {
        const selectedItems = $('.selected_data');
        selectedItems.each(function(index) {
            const itemHeight = $(this).height();
            const itemPadding = $(this).width() * 0.14;
            const itemHeaderHeight = $(this).find('h2').outerHeight(true);
            const itemBottomHeight = $(this).find('p').eq(1).outerHeight(true);
            const itemBody = $(this).find('p').eq(0);
            itemBody.outerHeight(itemHeight-itemPadding-itemHeaderHeight-itemBottomHeight);
        });
    };
    setHeightOfText();

    $(window).resize(function() {
        setHeightOfText();
    });

    /* calculate height of text box in offer selection - stop */


    /* nav toggle - start */

    let showHideNavElements = false;
    let startTargetX;
    let endTargetX;
    let target;


    const showNavElements = (e) => {
        target = e.target.dataset.target;
        $(`${target}`).slideDown();
        showHideNavElements = true;
        /* size of target */
        startTargetX = e.target.offsetLeft;
        endTargetX = startTargetX + e.target.offsetWidth;
    };



    const checkMousePosition = (e) => {

        if (showHideNavElements) {
            const mousePositionX = e.clientX;
            const mousePositionY = e.clientY;

            if ( ( ( mousePositionX < startTargetX || mousePositionX > endTargetX ) && mousePositionY < 323 ) || mousePositionY > 323 ) {
                    hideNavElements();
                    showHideNavElements = false;
            }
        }
    }


    const hideNavElements = () => {
        $(`${target}`).slideUp();
    };


    $('[data-toggle="to-display"]').mouseover(showNavElements);
    $(window).mousemove(checkMousePosition);


    /* nav toggle - stop */

});