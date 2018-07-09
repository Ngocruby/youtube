// Diese Datei ist BarChart aus D3-Bibliothek für Top-Genres
// Set margins
var margin = {
  top: 100,
  right: 20,
  bottom: 30,
  left: 40
};
//Breite und Höhe des Charts
var width = 960 - margin.left - margin.right;
var height = 500 - margin.top - margin.bottom;

var tip2 = d3.tip()
  .attr('class', 'd3-tip')
  .offset([-10, 0])
  .html(function (d) {
    return "<strong>Total:</strong> <span style='color:red'>" + d.total + "</span>";
  });

// Add our chart to the #bar div
var svg = d3.select("#bar").append("svg")
  .attr("width", width + margin.left + margin.right)
  .attr("height", height + margin.top + margin.bottom)
  .append("g")
  .attr("id", "chart")
  .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

svg.call(tip2);

var genresForLand;
d3.json("./json/youtube.json", function (error, youtube) { //get daten aus youtube.json
  genresForLand = youtube.genresForLand; //  das Objekt-genresForLand herausnehmen
  console.log(genresForLand);
  //alle key(Name des Landes) nehmen, Object.keys ist um die Object auf Array umzuwandeln
  var countryKeys = Object.keys(genresForLand); // stellen neue Array-countryKeys um den Name jedes Land herzunehmen
  console.log(countryKeys);

  // Dropdown Countries
  var myDiv = document.getElementById("myDiv"); //myDiv befindet sich in Datei chart.html

  //Auswahlliste erstellen und hinzufügen
  var selectList = document.createElement("select"); // für Select-HTML
  selectList.setAttribute("id", "mySelect"); //  stellen die ID für Select-HTML
  myDiv.appendChild(selectList); // hinzufügen "selectList" zu Element "myDiv"

  //Optionen für Auswahlliste erstellen und addieren 
  for (var i = 0; i < countryKeys.length; i++) {   
    var option = document.createElement("option"); // erstellen Obtion-HTML
    option.setAttribute("value", countryKeys[i]); // hinzufügen  "Value"
    option.text = countryKeys[i]; // erstellen "Text"
    selectList.appendChild(option); // hinzufügen "option" zu "selectList"
  }

  var country = countryKeys[0]; // take the 1st value on coutryKey (in this case: Afghanistan)
  console.log(genresForLand);
  console.log(country);
  var data = genresForLand[country]; //  Data für jedes Land herausnehmen

  drawMap(data); // Funktion "drawMap" läuft
});

$(document).on('change', '#mySelect', function (event) { // detect changes von ID:mySelect
  var value = event.target.value; // take countries' names
  var data = genresForLand[value]; // genres für Länder
  drawMap(data);
});


function drawMap(data) { // define drawing Map in a function
  $("#chart").html('');

  // x-Achse
  var x = d3.scaleBand()
    .rangeRound([0, width], 0.1)
    .padding(0.1); // Abstand zwischen Spalten
  //y-Achse
  var y = d3.scaleLinear()
    .range([height, 0]);


  //Use our X scale to set a bottom axis
  var xAxis = d3.axisBottom(x)
  // Same for our left axis
  var yAxis = d3.axisLeft(y)

  data.forEach(function (d) {
    d.total = +d.total;
  });

  x.domain(data.map(function (d) {
    return d.genre;
  }));

  y.domain([0, d3.max(data, function (d) {
    return d.total;
  })]);
  // Add the x-axis.
  svg.append("g")
    .attr("transform", "translate(0," + height + ")")
    .call(xAxis)
    .attr("id", "bars")
    .attr("class", "x axis");
  // creat the y-axis.
  svg.append("g")
    .attr("class", "y axis")
    .call(yAxis)
    .append("text")
    .attr("transform", "rotate(-90)")
    .attr("y", 6)
    .attr("dy", ".71em")
    .style("text-anchor", "end")
    .text("Total");

  svg.selectAll(".bar")
    .data(data)
    .enter().append("rect")
    .attr("class", "bar")
    .attr("x", function (d) {
      return x(d.genre);
    })
    .attr("width", x.bandwidth())
    .attr("y", function (d) {
      return y(d.total);
    })
    .attr("height", function (d) {
      return height - y(d.total);
    })
    .on('mouseover', tip2.show)
    .on('mouseout', tip2.hide);
}