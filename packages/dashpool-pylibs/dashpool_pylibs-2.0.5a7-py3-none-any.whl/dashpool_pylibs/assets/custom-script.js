//make all svgs with a nice 16:9 ratio
function changePlotSize() {
    let width = window.innerWidth - 15;
    let heigh = window.innerHeight - 15;

    let minHeight = Math.max(50, heigh - 70);

    var svgs = document.getElementsByClassName("svg-container");

    Array.prototype.forEach.call(svgs, function (el) {
        let container = el.parentElement.parentElement;
        if (container.classList.contains("auto-size")) {
            el.style.height = Math.min(minHeight, Math.round(width * 0.56)) + "px";
        }
    });

}
window.onresize = changePlotSize;
window.document.getElementById("react-entry-point").addEventListener("DOMNodeInserted", function (e) {
    changePlotSize();

    //add card collapse

    document.querySelectorAll(".card-collaps-label").forEach(
        (l) => {
            var n = 0;
            let toggleElement = l;
            while (n < 3 && !toggleElement.classList.contains("card")) {
                n++;
                toggleElement = toggleElement.parentElement;
            }
            if (toggleElement.classList.contains("card")) {
                l.onclick = function () {
                    toggleElement.classList.toggle("card-collapsed");
                };
            }
        }
    );

    document.querySelectorAll(".configMenuButton").forEach(
        (l) => {
            let toggleElement = document.querySelector("#configMenu");
            l.onclick = function () {
                toggleElement.classList.toggle("configMenu-hide");
            };
        }

    );

    document.querySelectorAll(".paramMenuButton").forEach(
        (l) => {
            let toggleElement = document.querySelector("#paramMenu");
            l.onclick = function () {
                toggleElement.classList.toggle("paramMenu-hide");
            };
        }

    );

}, false);