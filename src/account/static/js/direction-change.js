let fields = document.getElementsByClassName("direction-change");
for (let i = 0; i < fields.length; i++) {
  fields[i].addEventListener("input", function () {
    fields[i].style.direction = "ltr";
    if (fields[i].value == "") {
      fields[i].style.direction = "rtl";
    }
  });
}
