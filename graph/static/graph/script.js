const ComboBox = document.getElementById("plottype");
const Element = document.getElementById("dynamic");
const FormElem = document.getElementById("main-form");
ComboBox.addEventListener("change", function () {
  let val = ComboBox.value;
  if (val == "trend") {
    Element.innerHTML = "";
    Element.innerHTML =
      Element.innerHTML +
      "<h5>Time Interval</h5>" +
      '<input type="date" id="start" name="start" min="2016-06-02" max="2019-06-19" value="2016-06-02"/>' +
      "<br />" +
      '<input type="date" id="end" name="end" min="2016-06-02" max="2019-06-19" value="2019-06-19"/>' +
      "<br />";
  } else if (val == "diurnal") {
    Element.innerHTML = "";
    Element.innerHTML =
      Element.innerHTML +
      "<h5>Select Date</h5>" +
      '<input type="date" id="diurnaldate" name="diurnaldate" min="2016-06-02" max="2019-06-19" value="2019-06-19"/>' +
      "<br/>";
    let radios = FormElem.elements["datafreq"];
    radios.forEach((radio) => (radio.disabled = true));
  } else if (val == "seasonal") {
    Element.innerHTML = "";
    Element.innerHTML =
      Element.innerHTML +
      "<h5>Select Year</h5>" +
      '<select name="seasonal_year" id="seasonal_year"><option value="2017">2017</option><option value="2018">2018</option></select>' +
      "<hr />" +
      "<h5>Seasons</h5>" +
      '<input type="radio" id="summer" name="season" value="summer" /><label for="summer">Summer [Dec,Jan,Feb]</label><br /><input type="radio" id="fall" name="season" value="fall" /><label for="fall">Fall [Mar,Apr,May]</label><br /><input type="radio" id="winter" name="season" value="winter" /><label for="monthly">Winter [Jun,Jul,Aug]</label><br /><input type="radio" id="spring" name="season" value="spring" /><label for="spring">Spring [Sep,Oct,Nov]</label';
    let radios = FormElem.elements["datafreq"];
    radios[2].disabled = true;
  }
});
