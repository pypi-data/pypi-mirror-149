var contentsEl = document.getElementsByClassName("contents")[0];
var imgEl = contentsEl.getElementsByTagName("img");
var imgModalContainer = document.getElementById("modal-inner-content-image");

for (var i = 0; i < imgEl.length; i++) {
  imgEl[i].onclick = function(e) {
    var targ = e.target || e.srcElement || e;
    if (targ.nodeType == 3) targ = targ.parentNode;
    e = e || window.event;
    if (targ.alt != "inline-icon") {
      bodyEl.classList.toggle("show-modal-img");
      var imgSrc = targ.src;
      var imgAlt = targ.alt;
      var imgClassList = targ.classList;
      imgModalContainer.innerHTML = "<img src='" + imgSrc + "' class='" + imgClassList + "' alt='" + imgAlt + "'>";
    }
  };
}
