$(document).ready(function() {

    /* change order of image and offer presentation box depending on screen width - start*/
    function changeOrderOfLaoutElements() {

        const imagesToChangePosition = $('.selected_img');
        const selectionRow = $('.selection-row');

        /*conditions to fulfill*/
        const windowWidthCondition = window.innerWidth < 768;

        if (windowWidthCondition) {
            selectionRow.each(function(index) {
                if (index % 2 !== 0) {
                    $(this).find(".selected_img").remove();
                    $(this).prepend(imagesToChangePosition[index]);
                }
            })

        } else  {
            selectionRow.each(function(index) {
                if (index % 2 !== 0 && $(this).children().eq(0).hasClass('selected_img')) {
                    $(this).children().eq(0).remove();
                    $(this).append(imagesToChangePosition[index]);
                }
            })
        }
    };

    changeOrderOfLaoutElements();

    $(window).resize(changeOrderOfLaoutElements);

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
            const hoverHeight = $('nav.navbar').outerHeight() + $(target).height();
            $(target).css({'top': $('nav.navbar').outerHeight() + 'px' })

            if ( ( ( mousePositionX < startTargetX || mousePositionX > endTargetX ) && mousePositionY < hoverHeight ) || mousePositionY > hoverHeight ) {
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

    const setTitlePadding = () => {
        const navHeight = $('nav.navbar').outerHeight();
        const titleHeight = $('.offer_title h1').innerHeight();
        const btnHeight = $('.offer_title .btn').innerHeight();
        const imgHeight = $('.header_img').height();
        let paddingValue = Math.floor((window.innerHeight - (navHeight + imgHeight + titleHeight + btnHeight)) / 2);
        paddingValue > 0 ? paddingValue = paddingValue : paddingValue = 0;
        $('.offer_title').css({'padding-top': paddingValue + 'px', 'padding-bottom': paddingValue + 'px',})
    };
    setTitlePadding();
    $(window).resize(setTitlePadding);
});