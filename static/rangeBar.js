function changeBound(controler, otherBound, otherController, isOtherBoundGreater) {
    const [from, to] = getParsed(controler, otherBound);
    if (isOtherBoundGreater){
        if (from > to){
            controler.value = to;
            otherController.value = to;
        } else {
            otherController.value = from;
        }
    } //Lower Boundry 
    else {
        if(from < to){
            controler.value = to;
            otherController.value = to;
        } else {
            otherController.value = from;
        }
    }
}


function getParsed(controler1, controler2){
    const from = parseInt(controler1.value, 10);
    const to = parseInt(controler2.value, 10);
    return [from, to];
}

window.onload = function () {
    const yearLowerSlider = document.getElementById('yearSliderLower');
    const yearUpperSlider = document.getElementById('yearSliderUpper');
    const yearLowerBox = document.getElementById('yearBoxLower');
    const yearUpperBox = document.getElementById('yearBoxUpper');


    const popLowerSlider = document.getElementById('popularitySliderLower');
    const popUpperSlider = document.getElementById('popularitySliderUpper');
    const popLowerBox = document.getElementById('popularityBoxLower');
    const popUpperBox = document.getElementById('popularityBoxUpper');

    yearLowerSlider.addEventListener("input", function ()
        {changeBound(yearLowerSlider, yearUpperSlider, yearLowerBox, true)});
    yearUpperSlider.addEventListener("input", function ()
        {changeBound(yearUpperSlider, yearLowerSlider, yearUpperBox, false)});
    yearLowerBox.addEventListener("input", function ()
        {changeBound(yearLowerBox, yearUpperBox, yearLowerSlider, true)});
    yearUpperBox.addEventListener("input", function ()
        {changeBound(yearUpperBox, yearLowerBox, yearUpperSlider, false)});

    popLowerSlider.addEventListener("input", function ()
        {changeBound(popLowerSlider, popUpperSlider, popLowerBox, true)});
    popUpperSlider.addEventListener("input", function ()
        {changeBound(popUpperSlider, popLowerSlider, popUpperBox, false)});
    popLowerBox.addEventListener("input", function ()
        {changeBound(popLowerBox, popUpperBox, popLowerSlider, true)});
    popUpperBox.addEventListener("input", function ()
        {changeBound(popUpperBox, popLowerBox, popUpperSlider, false)});
};
